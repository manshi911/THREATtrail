"""
PhishGuard: Automated Email Threat Detection and Department-Wise Reporting System

This is the main entry point for the PhishGuard application.
"""

import os
import sys
import logging
import threading
import time
from pathlib import Path
from dotenv import load_dotenv

# Create necessary directories if they don't exist
os.makedirs('logs', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path("logs/phishguard.log")),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('phishguard')

# Make sure modules from src can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import PhishGuard modules
from src.email_integration.gmail_monitor import GmailMonitor
from src.threat_detection.threat_detector import ThreatDetector
from src.warning_system.alert_dialog import PhishingAlert
from src.data_logging.data_logger import DataLogger
from src.reporting.report_generator import ReportGenerator
from src.ocr_processing.ocr_processor import OCRProcessor

# Load environment variables from .env file
load_dotenv()

class PhishGuard:
    """Main PhishGuard application class."""
    
    def __init__(self):
        """Initialize the PhishGuard system."""
        logger.info("Initializing PhishGuard...")
        
        # Initialize components
        self.gmail_monitor = None
        self.threat_detector = ThreatDetector()
        self.warning_system = PhishingAlert()
        self.data_logger = DataLogger()
        self.report_generator = ReportGenerator(self.data_logger)
        self.ocr_processor = OCRProcessor()
        
        # Control variables
        self.monitor_thread = None
        self.report_thread = None
        self.running = False
        
    def start(self):
        """Start the PhishGuard monitoring and detection system."""
        logger.info("Starting PhishGuard system...")
        
        # Check environment variables
        if not os.getenv('EMAIL_APP_PASSWORD'):
            logger.error("App password not found in environment variables!")
            logger.error("Please set EMAIL_APP_PASSWORD in your .env file.")
            logger.error("You can generate an app password from https://myaccount.google.com/apppasswords")
            sys.exit(1)
        
        try:
            # Initialize and start Gmail monitoring in a separate thread
            self.gmail_monitor = GmailMonitor()
            self.running = True
            
            # Start email monitoring thread
            self.monitor_thread = threading.Thread(
                target=self._run_email_monitoring, 
                daemon=True
            )
            self.monitor_thread.start()
            
            # Start report generation thread
            self.report_thread = threading.Thread(
                target=self._run_report_generation,
                daemon=True
            )
            self.report_thread.start()
            
            logger.info("PhishGuard system started successfully.")
            
            # Keep the main thread running
            while self.running:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    self.stop()
                    break
        
        except Exception as e:
            logger.error(f"Error starting PhishGuard: {str(e)}")
            self.stop()
            sys.exit(1)
    
    def _run_email_monitoring(self):
        """Run the email monitoring service in a separate thread."""
        try:
            if self.gmail_monitor.connect():
                logger.info("Connected to Gmail IMAP server.")
                self.gmail_monitor.start_monitoring(self._process_emails)
            else:
                logger.error("Failed to connect to Gmail IMAP server.")
                self.stop()
        except Exception as e:
            logger.error(f"Error in email monitoring thread: {str(e)}")
            self.stop()
    
    def _run_report_generation(self):
        """Run the report generation service in a separate thread."""
        try:
            logger.info("Starting report generation service...")
            
            while self.running:
                current_time = time.localtime()
                
                # Generate daily reports at midnight
                if current_time.tm_hour == 0 and current_time.tm_min == 0:
                    logger.info("Generating daily reports...")
                    self.report_generator.generate_daily_reports(send_email=True)
                
                # Generate weekly reports on Sunday at midnight
                if current_time.tm_wday == 6 and current_time.tm_hour == 0 and current_time.tm_min == 0:
                    logger.info("Generating weekly summary report...")
                    self.report_generator.generate_weekly_summary()
                
                # Sleep for 1 minute before checking again
                time.sleep(60)
                
        except Exception as e:
            logger.error(f"Error in report generation thread: {str(e)}")
    
    def _process_emails(self, emails):
        """
        Process incoming emails for threat detection.
        
        Args:
            emails (list): List of email data dictionaries
        """
        logger.info(f"Processing {len(emails)} new emails...")
        
        for email_data in emails:
            subject = email_data.get('subject', 'No subject')
            sender = email_data.get('from', 'Unknown sender')
            logger.info(f"Analyzing email: {subject} from {sender}")
            
            # Analyze email using threat detector
            is_suspicious, risk_score, threat_type, indicators = self.threat_detector.analyze(email_data)
            
            # Process attachments with OCR if present
            attachments = email_data.get('attachments', [])
            ocr_indicators = []
            
            for attachment in attachments:
                is_attachment_suspicious, results = self.ocr_processor.process_attachment(attachment)
                
                if is_attachment_suspicious:
                    # Update the overall threat assessment
                    is_suspicious = True
                    risk_score = max(risk_score, 70)  # Suspicious attachments are high risk
                    
                    # Add OCR indicators to the list
                    ocr_indicators.extend(results.get('indicators', []))
                    
                    if threat_type == "suspicious_email":
                        threat_type = "image_based_phishing"
            
            # Combine all indicators
            all_indicators = indicators + ocr_indicators
            
            # If suspicious, trigger warning
            if is_suspicious:
                logger.warning(f"Phishing threat detected: {threat_type} (Risk: {risk_score:.1f}%)")
                
                # Show alert to user
                self.warning_system.show_alert(
                    email_data, 
                    risk_score, 
                    threat_type, 
                    all_indicators
                )
                
                # Log the threat to database
                self.data_logger.log_threat(
                    email_data,
                    risk_score,
                    threat_type,
                    all_indicators
                )
            else:
                logger.info(f"Email analyzed and found safe: {subject}")
            
            # Mark the email as read (optional, depending on your requirements)
            # self.gmail_monitor.mark_as_read(email_data['id'])
            
        logger.info(f"Finished processing {len(emails)} emails.")
    
    def stop(self):
        """Stop the PhishGuard system."""
        logger.info("Stopping PhishGuard system...")
        self.running = False
        
        if self.gmail_monitor:
            self.gmail_monitor.disconnect()
        
        # Close database connections
        if hasattr(self, 'data_logger'):
            self.data_logger.close()
        
        logger.info("PhishGuard system stopped.")


def main():
    """Main entry point for PhishGuard."""
    print("=" * 60)
    print("PhishGuard: Automated Email Threat Detection")
    print("=" * 60)
    print("Starting services... Press Ctrl+C to stop.")
    
    phishguard = PhishGuard()
    phishguard.start()


if __name__ == "__main__":
    main()

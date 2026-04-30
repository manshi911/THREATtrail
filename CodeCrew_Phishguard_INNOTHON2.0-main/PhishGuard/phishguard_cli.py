"""
PhishGuard: Main System Entry Point
"""

import argparse
import logging
import os
import sys
import time
import json
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/phishguard.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('phishguard')

def show_phishing_alert(email_data, risk_score, threat_type):
    """
    Display a warning dialog for detected phishing.
    
    Args:
        email_data (dict): Email information
        risk_score (float): Risk score (0-100)
        threat_type (str): Type of threat detected
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    subject = email_data.get('subject', 'No subject')
    sender = email_data.get('from', 'Unknown sender')
    
    # Create appropriate message based on risk level
    if risk_score > 80:
        level = "HIGH"
        message = f"⚠️ CRITICAL PHISHING ALERT ⚠️\n\n"
    elif risk_score > 60:
        level = "MEDIUM"
        message = f"⚠️ PHISHING WARNING ⚠️\n\n"
    else:
        level = "LOW"
        message = f"⚠️ SUSPICIOUS EMAIL ALERT ⚠️\n\n"
    
    message += (
        f"From: {sender}\n"
        f"Subject: {subject}\n\n"
        f"Risk Level: {level} ({risk_score:.1f}%)\n"
        f"Threat Type: {threat_type}\n\n"
        f"This email may be attempting to steal information or credentials.\n"
        f"It's recommended that you delete this email or report it as spam."
    )
    
    messagebox.showwarning("PhishGuard Warning", message)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="PhishGuard: Automated Email Threat Detection System")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("--simulate", action="store_true", help="Simulate phishing alert")
    parser.add_argument("--no-gui", action="store_true", help="Run without GUI warnings")
    return parser.parse_args()

def main():
    """Main entry point for PhishGuard."""
    print("\n" + "=" * 60)
    print(" PhishGuard Email Threat Detection System ".center(60, "="))
    print("=" * 60 + "\n")
    
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Parse arguments
    args = parse_arguments()
    
    if args.test:
        print("Running in test mode...")
        # Implement test mode logic
        
    if args.simulate:
        print("Simulating phishing alert...")
        # Create sample email data for simulation
        email_data = {
            'subject': 'Urgent: Your Account Will Be Suspended',
            'from': 'security@g00gle.com',
            'to': 'user@example.com',
            'body': {
                'plain': 'Your account will be suspended. Click here to verify your information: http://suspicious-link.com'
            }
        }
        
        # Show simulated alert if GUI is enabled
        if not args.no_gui:
            show_phishing_alert(email_data, 85.5, "domain_spoofing")
        else:
            print("Phishing detected (simulation):")
            print(f"Subject: {email_data['subject']}")
            print(f"From: {email_data['from']}")
            print(f"Risk score: 85.5")
            print(f"Threat type: domain_spoofing")
    
    # Normal operation
    if not args.test and not args.simulate:
        print("Starting PhishGuard in normal mode...")
        print("Press Ctrl+C to exit.")
        
        # Here we would import and initialize the full system components
        try:
            # Placeholder for actual system start
            print("\nSystem not fully implemented yet.")
            print("See the project repository for implementation details.")
            
            # To keep the program running until Ctrl+C
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nPhishGuard service stopped by user.")

if __name__ == "__main__":
    main()

"""
Warning System Module - Alert Dialog

This module provides the GUI alert system for PhishGuard,
displaying warning popups when phishing threats are detected.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import logging
import webbrowser
import os
from datetime import datetime

# Configure logging
logger = logging.getLogger('warning_system')

class PhishingAlert:
    """Display phishing alert dialogs to the user."""
    
    def __init__(self):
        """Initialize the PhishingAlert system."""
        self.active_alerts = 0
        self.max_alerts = 3  # Maximum number of simultaneous alerts
        self.alert_delay = 500  # Milliseconds between multiple alerts
    
    def show_alert(self, email_data, risk_score, threat_type, indicators=None):
        """
        Display an alert dialog for detected phishing.
        
        Args:
            email_data (dict): Email information
            risk_score (float): Risk score (0-100)
            threat_type (str): Type of threat detected
            indicators (list): List of detected indicators
        """
        # Check if we can show another alert
        if self.active_alerts >= self.max_alerts:
            logger.warning("Too many alerts active, skipping alert")
            return
        
        # Increment active alerts counter
        self.active_alerts += 1
        
        # Create alert in a separate thread to avoid blocking
        threading.Thread(
            target=self._create_alert_window,
            args=(email_data, risk_score, threat_type, indicators),
            daemon=True
        ).start()
    
    def _create_alert_window(self, email_data, risk_score, threat_type, indicators=None):
        """Create and display the alert window."""
        try:
            # Create root window
            root = tk.Tk()
            root.withdraw()  # Hide the root window initially
            
            # Configure the alert window
            self._show_alert_window(root, email_data, risk_score, threat_type, indicators)
            
            # When window closes, decrement counter
            root.protocol("WM_DELETE_WINDOW", lambda: self._on_close(root))
            
            # Show the window
            root.deiconify()
            root.lift()
            root.attributes('-topmost', True)
            root.focus_force()
            
            # Start the main loop
            root.mainloop()
            
        except Exception as e:
            logger.error(f"Error displaying alert: {str(e)}")
            self.active_alerts -= 1
    
    def _show_alert_window(self, root, email_data, risk_score, threat_type, indicators):
        """Configure and display the alert dialog window."""
        # Window settings
        root.title("PhishGuard Warning")
        root.geometry("600x500")
        root.configure(bg="#f0f0f0")
        
        # Try to set icon if available
        try:
            root.iconbitmap("icon.ico")
        except:
            pass
        
        # Extract email data
        subject = email_data.get('subject', 'No subject')
        sender = email_data.get('from', 'Unknown sender')
        recipient = email_data.get('to', 'Unknown recipient')
        date = email_data.get('date', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Determine risk level and colors
        if risk_score >= 80:
            risk_level = "HIGH"
            risk_color = "#ff3333"  # Red
            header_text = "CRITICAL PHISHING THREAT DETECTED"
        elif risk_score >= 60:
            risk_level = "MEDIUM"
            risk_color = "#ff9900"  # Orange
            header_text = "PHISHING WARNING"
        else:
            risk_level = "LOW"
            risk_color = "#ffcc00"  # Yellow
            header_text = "SUSPICIOUS EMAIL ALERT"
        
        # Create a header frame with warning icon
        header_frame = tk.Frame(root, bg=risk_color, height=70)
        header_frame.pack(fill=tk.X)
        
        # Warning icon (text-based for simplicity)
        tk.Label(
            header_frame, 
            text="⚠️", 
            font=("Arial", 24, "bold"),
            bg=risk_color,
            fg="white"
        ).pack(side=tk.LEFT, padx=20)
        
        # Header text
        tk.Label(
            header_frame,
            text=header_text,
            font=("Arial", 16, "bold"),
            bg=risk_color,
            fg="white"
        ).pack(side=tk.LEFT, padx=10)
        
        # Main content frame
        content_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Email details section
        details_frame = ttk.LabelFrame(content_frame, text="Email Details")
        details_frame.pack(fill=tk.X, pady=10)
        
        # Email fields
        fields = [
            ("From:", sender),
            ("Subject:", subject),
            ("To:", recipient),
            ("Date:", date)
        ]
        
        for i, (label, value) in enumerate(fields):
            ttk.Label(details_frame, text=label, width=10, anchor=tk.W).grid(
                row=i, column=0, sticky=tk.W, padx=5, pady=2
            )
            ttk.Label(details_frame, text=value, wraplength=450).grid(
                row=i, column=1, sticky=tk.W, padx=5, pady=2
            )
        
        # Threat details section
        threat_frame = ttk.LabelFrame(content_frame, text="Threat Information")
        threat_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(threat_frame, text="Risk Level:", width=15, anchor=tk.W).grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=2
        )
        ttk.Label(
            threat_frame, 
            text=f"{risk_level} ({risk_score:.1f}%)",
            foreground=risk_color
        ).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(threat_frame, text="Threat Type:", width=15, anchor=tk.W).grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2
        )
        ttk.Label(threat_frame, text=threat_type.replace('_', ' ').title()).grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=2
        )
        
        # Detected indicators
        if indicators:
            ttk.Label(threat_frame, text="Indicators:", width=15, anchor=tk.W).grid(
                row=2, column=0, sticky=tk.NW, padx=5, pady=2
            )
            
            indicators_text = "\n".join([
                "• " + indicator.replace('_', ' ').title()
                for indicator in indicators
            ])
            
            ttk.Label(threat_frame, text=indicators_text).grid(
                row=2, column=1, sticky=tk.W, padx=5, pady=2
            )
        
        # Recommendations section
        recommendations_frame = ttk.LabelFrame(content_frame, text="Recommendations")
        recommendations_frame.pack(fill=tk.X, pady=10)
        
        recommendations_text = (
            "• Do not click on any links in this email\n"
            "• Do not download or open any attachments\n"
            "• Do not reply with sensitive information\n"
            "• Report this email as phishing to IT security\n"
            "• Delete this email from your inbox"
        )
        
        ttk.Label(recommendations_frame, text=recommendations_text, justify=tk.LEFT).pack(
            anchor=tk.W, padx=5, pady=5
        )
        
        # Action buttons
        button_frame = tk.Frame(content_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="View Email Safely",
            command=lambda: self._view_email_safely(email_data)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Report as Phishing",
            command=lambda: self._report_phishing(email_data)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Close",
            command=lambda: self._on_close(root)
        ).pack(side=tk.RIGHT, padx=5)
    
    def _on_close(self, root):
        """Handle window close event."""
        self.active_alerts -= 1
        root.destroy()
    
    def _view_email_safely(self, email_data):
        """Display the email content in a safe viewer."""
        # In a real implementation, this would show the email in a sandboxed viewer
        logger.info(f"Viewing email safely: {email_data.get('subject', 'No subject')}")
        messagebox.showinfo(
            "Safe Viewer", 
            "In a full implementation, this would display the email content in a sandboxed viewer."
        )
    
    def _report_phishing(self, email_data):
        """Report the email as phishing to the security team."""
        # In a real implementation, this would send the email to a reporting system
        logger.info(f"Reporting phishing email: {email_data.get('subject', 'No subject')}")
        messagebox.showinfo(
            "Report Submitted", 
            "Thank you for reporting this phishing attempt. The security team has been notified."
        )


# For testing
if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.INFO)
    
    # Sample email data
    email_data = {
        'subject': 'Urgent: Your Account Security Verification Required',
        'from': 'security@g00gle.com',
        'to': 'user@example.com',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Show a test alert
    alert_system = PhishingAlert()
    alert_system.show_alert(
        email_data,
        risk_score=85.5,
        threat_type='domain_spoofing',
        indicators=[
            'suspicious_domain',
            'urgency_language',
            'suspicious_link',
            'brand_impersonation'
        ]
    )
    
    # Keep the main thread running
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("Test stopped by user")
"""
Email Integration Module - Gmail IMAP Connection

This module handles the connection to Gmail IMAP server and retrieves emails 
for analysis by the threat detection engine.
"""

import imaplib
import email
import email.header
import configparser
import os
import sys
import time
import logging
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path("logs/email_integration.log")),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('email_integration')

# Load environment variables from .env file
load_dotenv()

class GmailMonitor:
    def __init__(self, config_path='config.ini'):
        """Initialize Gmail monitor with configuration settings."""
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        
        # IMAP server configuration
        self.imap_server = self.config['GMAIL']['imap_server']
        self.imap_port = int(self.config['GMAIL']['imap_port'])
        self.email_address = self.config['AUTH']['email']
        
        # Get app password from environment variables
        self.app_password = os.getenv('EMAIL_APP_PASSWORD')
        if not self.app_password:
            logger.error("App password not found in environment variables!")
            raise ValueError("App password not set in environment variables. Please set EMAIL_APP_PASSWORD.")
        
        # Connection objects
        self.mail = None
        self.connected = False
          # Check interval
        self.check_interval = int(self.config['SETTINGS']['check_interval'])
        
    def connect(self):
        """Establish connection to Gmail IMAP server."""
        try:
            # Create IMAP4 class with SSL
            logger.info(f"Creating IMAP4_SSL connection to {self.imap_server}:{self.imap_port}")
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            
            # Login to the server
            logger.info(f"Attempting to login as {self.email_address}")
            self.mail.login(self.email_address, self.app_password)
            self.connected = True
            logger.info("Successfully logged into Gmail IMAP server")
            return True
            
        except imaplib.IMAP4.error as e:
            logger.error(f"IMAP authentication error: {str(e)}")
            logger.error("This might be due to incorrect app password or IMAP not being enabled in Gmail settings")
            self.connected = False
            return False
        except ConnectionRefusedError as e:
            logger.error(f"Connection refused: {str(e)}")
            logger.error("Check your network connection and firewall settings")
            self.connected = False
            return False  
        except Exception as e:
            logger.error(f"Failed to connect to Gmail IMAP server: {str(e)}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Close the connection to the IMAP server."""
        if self.mail and self.connected:
            self.mail.close()
            self.mail.logout()
            self.connected = False
            logger.info("Disconnected from Gmail IMAP server")
    
    def fetch_unread_emails(self, folder="INBOX", limit=10):
        """
        Retrieve unread emails from the specified folder.
        
        Args:
            folder (str): The mailbox folder to check (default: "INBOX")
            limit (int): Maximum number of emails to retrieve
            
        Returns:
            list: List of email message objects
        """
        if not self.connected:
            if not self.connect():
                logger.error("Cannot fetch emails: Not connected to server")
                return []
        
        try:
            # Select the mailbox folder
            status, messages = self.mail.select(folder)
            
            if status != 'OK':
                logger.error(f"Failed to select folder {folder}")
                return []
            
            # Search for unread emails
            status, data = self.mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                logger.error("Failed to search for unread emails")
                return []
            
            email_ids = data[0].split()
            logger.info(f"Found {len(email_ids)} unread email(s)")
            
            # Limit the number of emails to process
            if limit > 0 and len(email_ids) > limit:
                email_ids = email_ids[:limit]
            
            emails = []
            for e_id in email_ids:
                status, data = self.mail.fetch(e_id, '(RFC822)')
                
                if status != 'OK':
                    logger.error(f"Failed to fetch email with ID {e_id}")
                    continue
                
                raw_email = data[0][1]
                try:
                    email_message = email.message_from_bytes(raw_email)
                    emails.append({
                        'id': e_id.decode(),
                        'message': email_message,
                        'subject': self._decode_header(email_message['Subject']),
                        'from': self._decode_header(email_message['From']),
                        'to': self._decode_header(email_message['To']),
                        'date': self._decode_header(email_message['Date']),
                        'body': self._get_email_body(email_message),
                        'attachments': self._get_attachments(email_message)
                    })
                except Exception as e:
                    logger.error(f"Error parsing email with ID {e_id}: {str(e)}")
            
            return emails
            
        except Exception as e:
            logger.error(f"Error fetching emails: {str(e)}")
            return []
    
    def mark_as_read(self, email_id):
        """Mark an email as read."""
        if not self.connected:
            if not self.connect():
                return False
        
        try:
            self.mail.store(email_id, '+FLAGS', '\\Seen')
            return True
        except Exception as e:
            logger.error(f"Error marking email {email_id} as read: {str(e)}")
            return False
    
    def _decode_header(self, header):
        """Decode email header."""
        if header is None:
            return ""
            
        try:
            decoded_header = email.header.decode_header(header)
            header_parts = []
            for part, encoding in decoded_header:
                if isinstance(part, bytes):
                    if encoding:
                        header_parts.append(part.decode(encoding or 'utf-8', errors='replace'))
                    else:
                        header_parts.append(part.decode('utf-8', errors='replace'))
                else:
                    header_parts.append(str(part))
            return ' '.join(header_parts)
        except Exception as e:
            logger.error(f"Error decoding header: {str(e)}")
            return str(header)
    
    def _get_email_body(self, message):
        """Extract the email body in plain text and HTML formats."""
        body = {
            'plain': '',
            'html': ''
        }
        
        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))
                
                # Skip attachments
                if 'attachment' in content_disposition:
                    continue
                
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        decoded_payload = payload.decode(charset, errors='replace')
                        
                        if content_type == 'text/plain':
                            body['plain'] += decoded_payload
                        elif content_type == 'text/html':
                            body['html'] += decoded_payload
                except Exception as e:
                    logger.error(f"Error decoding email part: {str(e)}")
        else:
            # Not multipart - get the content directly
            try:
                payload = message.get_payload(decode=True)
                if payload:
                    charset = message.get_content_charset() or 'utf-8'
                    decoded_payload = payload.decode(charset, errors='replace')
                    
                    content_type = message.get_content_type()
                    if content_type == 'text/plain':
                        body['plain'] = decoded_payload
                    elif content_type == 'text/html':
                        body['html'] = decoded_payload
            except Exception as e:
                logger.error(f"Error decoding email content: {str(e)}")
        
        return body
    
    def _get_attachments(self, message):
        """Extract attachments from the email."""
        attachments = []
        
        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            
            filename = part.get_filename()
            if filename:
                content_type = part.get_content_type()
                try:
                    payload = part.get_payload(decode=True)
                    attachments.append({
                        'filename': filename,
                        'content_type': content_type,
                        'data': payload
                    })
                except Exception as e:
                    logger.error(f"Error extracting attachment {filename}: {str(e)}")
        
        return attachments
    
    def start_monitoring(self, callback_function=None):
        """
        Start continuous monitoring of the inbox.
        
        Args:
            callback_function: Function to call when new emails are detected.
                              Should accept a list of email objects as parameter.
        """
        logger.info("Starting email monitoring service...")
        
        if not callback_function:
            logger.warning("No callback function provided. Emails will be fetched but not processed.")
        
        try:
            while True:
                if not self.connected:
                    self.connect()
                
                if self.connected:
                    emails = self.fetch_unread_emails()
                    
                    if emails and callback_function:
                        callback_function(emails)
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("Email monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in monitoring loop: {str(e)}")
        finally:
            self.disconnect()


# Example usage
if __name__ == "__main__":
    def process_emails(emails):
        """Example callback function for email processing."""
        for email_data in emails:
            print(f"New email detected: {email_data['subject']} from {email_data['from']}")
            # This is where you would call the threat detection engine
    
    monitor = GmailMonitor()
    if monitor.connect():
        print("Connected to Gmail. Press Ctrl+C to stop monitoring.")
        monitor.start_monitoring(process_emails)
    else:
        print("Failed to connect to Gmail. Check your credentials and settings.")

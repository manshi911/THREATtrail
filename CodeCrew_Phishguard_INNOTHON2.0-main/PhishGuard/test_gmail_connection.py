#!/usr/bin/env python3
"""
Quick test script for Gmail IMAP connection.

This simplified script tests your Gmail connection setup.
"""

import os
import sys
import traceback
import configparser
import imaplib
from dotenv import load_dotenv

def main():
    """Test the Gmail IMAP connection."""
    print("\n=== PhishGuard Gmail IMAP Connection Test ===\n")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("❌ ERROR: .env file not found!")
        return False
        
    # Load environment variables
    print("Loading environment variables...")
    load_dotenv()
    
    # Check if app password is set
    app_password = os.getenv('EMAIL_APP_PASSWORD')
    if not app_password:
        print("❌ ERROR: EMAIL_APP_PASSWORD not found in .env file!")
        return False
    
    if app_password == "your_gmail_app_password_here":
        print("❌ ERROR: Default app password detected in .env file.")
        print("Please update EMAIL_APP_PASSWORD with your actual Gmail app password.")
        return False
        
    print("✓ App password found in environment variables.")
    
    # Check for config.ini
    if not os.path.exists('config.ini'):
        print("❌ ERROR: config.ini file not found!")
        return False

    # Read configuration
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Get email settings
    try:
        imap_server = config['GMAIL']['imap_server']
        imap_port = int(config['GMAIL']['imap_port'])
        email_address = config['AUTH']['email']
        
        print(f"Email configuration:")
        print(f"- IMAP Server: {imap_server}")
        print(f"- IMAP Port: {imap_port}")
        print(f"- Email Address: {email_address}")
        
        # Try to connect
        print("\nAttempting to connect to Gmail...")
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        
        # Login
        print(f"Logging in as {email_address}...")
        mail.login(email_address, app_password)
        print("✓ Login successful!")
        
        # Check inbox
        print("\nSelecting INBOX...")
        status, messages = mail.select("INBOX")
        
        if status != 'OK':
            print(f"❌ Failed to select INBOX: {status}")
            return False
            
        # Search for unread messages
        print("Searching for unread messages...")
        status, data = mail.search(None, 'UNSEEN')
        
        if status != 'OK':
            print(f"❌ Failed to search for unread emails: {status}")
            return False
            
        # Get email count
        email_ids = data[0].split()
        print(f"✓ Found {len(email_ids)} unread email(s)")
        
        # Close connection
        mail.close()
        mail.logout()
        print("\n✓ Test completed successfully! Gmail IMAP connection is working properly.")
        return True
        
    except KeyError as e:
        print(f"❌ Configuration error: Missing {e} in config.ini")
        return False
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP error: {str(e)}")
        print("\nThis could be due to:")
        print("1. Incorrect app password")
        print("2. IMAP not enabled in Gmail settings")
        print("3. Less secure app access restrictions")
        print("\nTo enable IMAP in Gmail:")
        print("1. Go to Gmail settings (gear icon)")
        print("2. Click 'See all settings'")
        print("3. Go to 'Forwarding and POP/IMAP' tab")
        print("4. Enable IMAP")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print("\n" + ("=" * 50))
    if not success:
        print("❌ Gmail IMAP connection test FAILED")
        sys.exit(1)
    else:
        print("✓ Gmail IMAP connection test SUCCEEDED")
        sys.exit(0)

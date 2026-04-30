#!/usr/bin/env python3
"""
Simple Gmail Test Script
"""

import os
import sys
import imaplib
import configparser
from dotenv import load_dotenv

def main():
    print("=== Simple Gmail Connection Test ===")
    
    # Load environment variables
    load_dotenv()
    
    # Get app password
    app_password = os.getenv("EMAIL_APP_PASSWORD")
    if not app_password:
        print("ERROR: No app password found in environment variables")
        sys.exit(1)
    
    # Read config
    config = configparser.ConfigParser()
    if not os.path.exists("config.ini"):
        print("ERROR: config.ini not found")
        sys.exit(1)
    
    config.read("config.ini")
    email = config["AUTH"]["email"]
    imap_server = config["GMAIL"]["imap_server"]
    imap_port = int(config["GMAIL"]["imap_port"])
    
    print(f"Connecting to {imap_server}:{imap_port} as {email}")
    
    try:
        # Connect to server
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        print("Connection established")
        
        # Login
        mail.login(email, app_password)
        print("Successfully logged in")
        
        # Select inbox
        mail.select("INBOX")
        print("Selected INBOX")
        
        # Logout
        mail.logout()
        print("Test completed successfully")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

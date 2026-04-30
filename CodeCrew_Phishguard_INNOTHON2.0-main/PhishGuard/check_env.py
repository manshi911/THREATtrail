#!/usr/bin/env python3
"""
Environment Variable and Config Test
"""

import os
import sys
import configparser
from dotenv import load_dotenv

def main():
    print("=== Environment and Config Test ===")
    
    # Check if .env exists
    if os.path.exists(".env"):
        print(".env file exists")
        
        # Try to load it
        load_dotenv()
        
        # Check app password
        app_password = os.getenv("EMAIL_APP_PASSWORD")
        if app_password:
            # Hide the actual password and show length
            masked_pw = '*' * len(app_password)
            print(f"App password found: {masked_pw} (length: {len(app_password)})")
        else:
            print("ERROR: EMAIL_APP_PASSWORD not found in environment")
    else:
        print("ERROR: .env file not found")
    
    # Check config.ini
    if os.path.exists("config.ini"):
        print("config.ini file exists")
        
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
            
            # Check required sections
            if "GMAIL" in config and "AUTH" in config:
                print("Required config sections found")
                
                # Print email settings
                print(f"Email address: {config['AUTH']['email']}")
                print(f"IMAP server: {config['GMAIL']['imap_server']}")
                print(f"IMAP port: {config['GMAIL']['imap_port']}")
            else:
                print("ERROR: Missing required sections in config.ini")
        except Exception as e:
            print(f"ERROR reading config.ini: {str(e)}")
    else:
        print("ERROR: config.ini file not found")

if __name__ == "__main__":
    main()

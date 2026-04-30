"""
PhishGuard Gmail Connection Test CLI

A simple command-line tool to test and configure Gmail IMAP connection.
"""

import os
import sys
import imaplib
import configparser
import re
import getpass
import json
from pathlib import Path

def print_header(text, width=60, fill_char="="):
    """Print a formatted header."""
    print(f"\n{fill_char * width}")
    print(f" {text} ".center(width, fill_char))
    print(f"{fill_char * width}\n")

def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")

def print_info(message):
    """Print an info message."""
    print(f"ℹ️ {message}")

def load_config():
    """Load configuration from config.ini and .env files."""
    config = {
        'email': None,
        'app_password': None,
        'imap_server': 'imap.gmail.com',
        'imap_port': 993
    }
    
    # Load email from config.ini
    if os.path.exists('config.ini'):
        try:
            parser = configparser.ConfigParser()
            parser.read('config.ini')
            
            if 'AUTH' in parser and 'email' in parser['AUTH']:
                config['email'] = parser['AUTH']['email']
            
            if 'GMAIL' in parser:
                if 'imap_server' in parser['GMAIL']:
                    config['imap_server'] = parser['GMAIL']['imap_server']
                
                if 'imap_port' in parser['GMAIL']:
                    config['imap_port'] = int(parser['GMAIL']['imap_port'])
            
            print_success(f"Loaded configuration from config.ini")
        except Exception as e:
            print_error(f"Failed to load config.ini: {str(e)}")
    else:
        print_info("config.ini file not found")
    
    # Load app password from .env
    if os.path.exists('.env'):
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('EMAIL_APP_PASSWORD='):
                        password = line.split('=', 1)[1].strip()
                        if password and password != 'your_gmail_app_password_here':
                            config['app_password'] = password
                            print_success("Loaded app password from .env file")
                        break
        except Exception as e:
            print_error(f"Failed to load .env file: {str(e)}")
    else:
        print_info(".env file not found")
    
    return config

def save_config(email, app_password):
    """Save configuration to config.ini and .env files."""
    # Save email to config.ini
    try:
        if os.path.exists('config.ini'):
            # Update existing file
            parser = configparser.ConfigParser()
            parser.read('config.ini')
            
            if 'AUTH' not in parser:
                parser['AUTH'] = {}
            
            parser['AUTH']['email'] = email
            
            with open('config.ini', 'w') as f:
                parser.write(f)
            
            print_success("Updated email in config.ini")
        else:
            # Create new config file
            parser = configparser.ConfigParser()
            parser['GMAIL'] = {
                'imap_server': 'imap.gmail.com',
                'imap_port': '993',
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': '587',
                'use_ssl': 'True'
            }
            parser['AUTH'] = {
                'email': email
            }
            parser['SETTINGS'] = {
                'check_interval': '60',
                'log_level': 'INFO',
                'department_mapping': 'data/department_mapping.json'
            }
            parser['REPORTING'] = {
                'daily_report_time': '17:00',
                'report_format': 'excel,pdf',
                'report_recipients': 'admin@company.com'
            }
            
            with open('config.ini', 'w') as f:
                parser.write(f)
            
            print_success("Created new config.ini file with email")
    except Exception as e:
        print_error(f"Failed to save email to config.ini: {str(e)}")
    
    # Save app password to .env
    try:
        if os.path.exists('.env'):
            # Read existing content
            with open('.env', 'r') as f:
                content = f.read()
            
            # Update or add the app password
            if 'EMAIL_APP_PASSWORD=' in content:
                content = re.sub(
                    r'EMAIL_APP_PASSWORD=.*',
                    f'EMAIL_APP_PASSWORD={app_password}',
                    content
                )
            else:
                if not content.endswith('\n'):
                    content += '\n'
                content += f'EMAIL_APP_PASSWORD={app_password}\n'
            
            # Write back
            with open('.env', 'w') as f:
                f.write(content)
            
            print_success("Updated app password in .env file")
        else:
            # Create new .env file
            with open('.env', 'w') as f:
                f.write(f'EMAIL_APP_PASSWORD={app_password}\n')
            
            print_success("Created new .env file with app password")
    except Exception as e:
        print_error(f"Failed to save app password to .env file: {str(e)}")

def test_connection(email, password, server='imap.gmail.com', port=993):
    """Test the Gmail IMAP connection."""
    print_header("Testing Gmail IMAP Connection", fill_char="-")
    print(f"Email: {email}")
    print(f"Server: {server}:{port}")
    print(f"App Password: {'*' * len(password)}")
    print("")
    
    try:
        # Connect to server
        print("Connecting to IMAP server...")
        mail = imaplib.IMAP4_SSL(server, port)
        print_success("Connection established")
        
        # Login
        print("\nLogging in...")
        mail.login(email, password)
        print_success("Login successful")
        
        # List available mailboxes
        print("\nListing mailboxes...")
        status, mailboxes = mail.list()
        if status == 'OK':
            print_success(f"Found {len(mailboxes)} mailboxes")
            # Show a few mailboxes
            for i, mb in enumerate(mailboxes[:3]):
                print(f"  - {mb.decode()}")
            if len(mailboxes) > 3:
                print(f"  - ...and {len(mailboxes)-3} more")
        
        # Select inbox
        print("\nSelecting INBOX...")
        status, data = mail.select("INBOX")
        if status == 'OK':
            print_success(f"INBOX selected. Message count: {data[0].decode()}")
            
            # Search for messages
            print("\nSearching for messages...")
            status, data = mail.search(None, "ALL")
            if status == 'OK':
                email_ids = data[0].split()
                print_success(f"Found {len(email_ids)} messages")
                
                # Get some recent emails
                if email_ids:
                    # Get the most recent email
                    latest_id = email_ids[-1]
                    print(f"\nRetrieving latest email (ID: {latest_id.decode()})...")
                    status, data = mail.fetch(latest_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
                    if status == 'OK':
                        print_success("Retrieved email headers")
                        header = data[0][1].decode()
                        print("\nHeaders of latest email:")
                        print(f"{header}")
        
        # Logout
        mail.close()
        mail.logout()
        print_success("\nSuccessfully logged out")
        
        print_header("CONNECTION TEST PASSED", fill_char="*")
        print("Your Gmail IMAP connection is working correctly!")
        print("You can now use PhishGuard to monitor your inbox.")
        
        return True
        
    except imaplib.IMAP4.error as e:
        print_error(f"\nIMAP ERROR: {str(e)}")
        print("\nPossible solutions:")
        print("1. Verify that your app password is correct")
        print("2. Make sure IMAP is enabled in your Gmail settings")
        print("   Visit: https://mail.google.com/mail/#settings/fwdandpop")
        print("3. Check if your Google Account has security restrictions")
        print("4. Try generating a new app password")
        print("   Visit: https://myaccount.google.com/apppasswords")
        
        print_header("CONNECTION TEST FAILED", fill_char="*")
        return False
        
    except Exception as e:
        print_error(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        print_header("CONNECTION TEST FAILED", fill_char="*")
        return False

def main():
    """Main function."""
    print_header("PhishGuard Gmail Connection Test")
    
    # Load existing configuration
    config = load_config()
    
    # Ask for email if not found
    if not config['email']:
        email = input("Enter your Gmail address: ")
    else:
        print(f"Current email: {config['email']}")
        change = input("Change email? (y/n) [n]: ").lower()
        if change == 'y':
            email = input("Enter your Gmail address: ")
        else:
            email = config['email']
    
    # Ask for app password
    if not config['app_password']:
        print("\nEnter your Gmail App Password")
        print("(This is a 16-character password with no spaces)")
        print("Generate one at: https://myaccount.google.com/apppasswords")
        app_password = getpass.getpass("App Password: ")
    else:
        print("\nApp password is already set")
        change = input("Change app password? (y/n) [n]: ").lower()
        if change == 'y':
            app_password = getpass.getpass("App Password: ")
        else:
            app_password = config['app_password']
    
    # Test the connection
    success = test_connection(email, app_password, config['imap_server'], config['imap_port'])
    
    # Save configuration if test was successful
    if success:
        print("\nWould you like to save these working credentials? (y/n) [y]: ", end="")
        save = input().lower()
        if save != 'n':
            save_config(email, app_password)
            print_success("Credentials saved successfully!")

if __name__ == "__main__":
    main()

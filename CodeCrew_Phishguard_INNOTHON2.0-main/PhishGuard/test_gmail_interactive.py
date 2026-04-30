#!/usr/bin/env python3
"""
Interactive Gmail IMAP Test Script

This script will help you test your Gmail IMAP connection
and save the working credentials to your config files.
"""

import os
import sys
import imaplib
import configparser
import re
from getpass import getpass

def test_connection(email, app_password):
    """Test connection to Gmail IMAP server."""
    print("\nTesting connection to Gmail IMAP server...")
    
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        print("✓ Connection established")
        
        # Login with credentials
        mail.login(email, app_password)
        print("✓ Login successful!")
        
        # Select the mailbox
        status, count = mail.select("INBOX")
        if status == "OK":
            print(f"✓ INBOX selected. Mail count: {count[0].decode()}")
            
            # Search for recent messages
            status, data = mail.search(None, "ALL")
            if status == "OK":
                email_ids = data[0].split()
                print(f"✓ Found {len(email_ids)} email(s) in total")
                
                # Get the latest email as a test
                if email_ids:
                    latest_id = email_ids[-1]
                    status, data = mail.fetch(latest_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM)])")
                    if status == "OK":
                        print(f"✓ Successfully retrieved latest email header")
                        header = data[0][1].decode()
                        print(f"\nLatest email header:")
                        print(f"{header}")
        
        # Close and logout
        mail.close()
        mail.logout()
        print("\n✅ CONNECTION TEST PASSED! Your Gmail IMAP connection is working.")
        return True
        
    except imaplib.IMAP4.error as e:
        print(f"\n❌ IMAP ERROR: {str(e)}")
        print("\nPossible solutions:")
        print("1. Verify your app password is correct (16 characters, no spaces)")
        print("2. Make sure IMAP is enabled in Gmail settings")
        print("3. Check if your Google Account has any security restrictions")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def save_credentials(email, app_password):
    """Save the working credentials to config files."""
    print("\nWould you like to save these working credentials? (y/n): ", end="")
    save = input().lower()
    
    if save != "y":
        print("Credentials not saved.")
        return
    
    # Update config.ini
    if os.path.exists("config.ini"):
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
            
            if "AUTH" in config:
                config["AUTH"]["email"] = email
                
                with open("config.ini", "w") as config_file:
                    config.write(config_file)
                
                print("✓ Email updated in config.ini")
            else:
                print("❌ AUTH section not found in config.ini")
        except Exception as e:
            print(f"❌ Error updating config.ini: {str(e)}")
    else:
        print("❌ config.ini not found")
    
    # Update .env file
    if os.path.exists(".env"):
        try:
            with open(".env", "r") as env_file:
                env_content = env_file.read()
            
            # Replace the EMAIL_APP_PASSWORD line
            if "EMAIL_APP_PASSWORD=" in env_content:
                env_content = re.sub(
                    r"EMAIL_APP_PASSWORD=.*",
                    f"EMAIL_APP_PASSWORD={app_password}",
                    env_content
                )
            else:
                env_content += f"\nEMAIL_APP_PASSWORD={app_password}"
            
            with open(".env", "w") as env_file:
                env_file.write(env_content)
            
            print("✓ App password updated in .env")
        except Exception as e:
            print(f"❌ Error updating .env: {str(e)}")
    else:
        try:
            with open(".env", "w") as env_file:
                env_file.write(f"EMAIL_APP_PASSWORD={app_password}\n")
            print("✓ Created .env file with app password")
        except Exception as e:
            print(f"❌ Error creating .env: {str(e)}")
    
    print("\nCredentials saved successfully! You can now run the PhishGuard system.")

def main():
    """Main function to interactively test Gmail connection."""
    print("\n" + "=" * 60)
    print(" INTERACTIVE GMAIL IMAP CONNECTION TEST ".center(60, "="))
    print("=" * 60)
    
    print("\nThis tool will help you test your Gmail IMAP connection")
    print("and save the working credentials to your config files.")
    
    # Get email address
    email = input("\nEnter your Gmail address: ")
    if not email or "@" not in email:
        print("Invalid email address")
        sys.exit(1)
    
    # Get app password
    print("\nEnter your Gmail App Password")
    print("(This is a 16-character password with no spaces)")
    print("Generate one at: https://myaccount.google.com/apppasswords")
    app_password = getpass("App Password: ")
    
    if not app_password:
        print("App password cannot be empty")
        sys.exit(1)
        
    if len(app_password) != 16:
        print(f"\nWARNING: App password is {len(app_password)} characters long.")
        print("Gmail app passwords are typically 16 characters without spaces.")
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != "y":
            sys.exit(1)
    
    # Test connection
    success = test_connection(email, app_password)
    
    if success:
        save_credentials(email, app_password)
        
        print("\n" + "=" * 60)
        print(" NEXT STEPS ".center(60, "="))
        print("=" * 60)
        print("\n1. Run the main PhishGuard application:")
        print("   python src/main.py")
        print("\n2. If you have issues, check your Gmail settings:")
        print("   - Make sure IMAP is enabled")
        print("   - Check for any security alerts in your Google Account")
        print("\n3. For additional help, consult the README.md file")
    else:
        print("\n" + "=" * 60)
        print(" CONNECTION TEST FAILED ".center(60, "="))
        print("=" * 60)
        print("\nPlease verify your credentials and Gmail settings.")
        print("Make sure 2-Step Verification is enabled and you've generated")
        print("an App Password specifically for this application.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Direct Gmail Connection Test

This script tests Gmail IMAP connection directly,
bypassing configuration files.
"""

import imaplib
import sys
import getpass  # For password input

def test_gmail_connection(email, app_password):
    """Test direct connection to Gmail IMAP."""
    print(f"Testing connection to Gmail IMAP for {email}")
    print("(App password masked)")
    
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        print("✓ Connection established")
        
        # Login
        mail.login(email, app_password)
        print("✓ Login successful")
        
        # Select inbox
        status, count = mail.select("INBOX")
        if status == "OK":
            print(f"✓ INBOX selected. Mail count: {count[0].decode()}")
            
            # Search for recent messages
            status, data = mail.search(None, "ALL")
            if status == "OK":
                email_ids = data[0].split()
                print(f"✓ Found {len(email_ids)} email(s) total")
        
        # Logout
        mail.logout()
        print("✓ Successfully logged out")
        print("\nGmail IMAP connection test PASSED!")
        return True
        
    except imaplib.IMAP4.error as e:
        print(f"\n❌ IMAP ERROR: {str(e)}")
        print("\nPossible solutions:")
        print("1. Verify your app password is correct")
        print("2. Make sure IMAP is enabled in Gmail settings")
        print("3. Check if your Google Account has any security restrictions")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to get credentials and test connection."""
    print("\n=== Direct Gmail Connection Test ===\n")
    
    # Ask for email
    email = input("Enter your Gmail address: ")
    if not email or "@" not in email:
        print("Invalid email address")
        sys.exit(1)
    
    # Ask for app password
    print("\nEnter your Gmail App Password")
    print("(This is a 16-character password with no spaces)")
    print("Generate one at: https://myaccount.google.com/apppasswords")
    app_password = input("App Password: ")
    
    if len(app_password) != 16:
        print("\nWARNING: App passwords are usually 16 characters long.")
        proceed = input("Proceed anyway? (y/n): ")
        if proceed.lower() != "y":
            sys.exit(1)
    
    print("\nTesting connection...")
    success = test_gmail_connection(email, app_password)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()

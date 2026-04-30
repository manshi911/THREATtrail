"""
Minimal Gmail IMAP Test

This script uses standard libraries to test a Gmail IMAP connection.
"""

import imaplib
import getpass
import sys

def main():
    print("\n===== MINIMAL GMAIL IMAP TEST =====\n")
    
    # Get credentials
    email = input("Enter your Gmail address: ")
    print("Enter your Gmail App Password (16 characters, no spaces)")
    app_password = getpass.getpass()
    
    print(f"\nTesting connection for: {email}")
    print(f"Password length: {len(app_password)} characters")
    
    try:
        # Connect to Gmail
        print("\n1. Creating connection to imap.gmail.com:993...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        print("   ✓ Connection established")
        
        # Login to account
        print("\n2. Attempting login...")
        mail.login(email, app_password)
        print("   ✓ Login successful!")
        
        # List mailboxes
        print("\n3. Listing mailboxes...")
        status, mailboxes = mail.list()
        if status == 'OK':
            print(f"   ✓ Found {len(mailboxes)} mailboxes")
            # Print first few mailboxes
            for i, mb in enumerate(mailboxes[:3]):
                print(f"     - {mb.decode()}")
            if len(mailboxes) > 3:
                print(f"     - ...and {len(mailboxes)-3} more")
        
        # Select inbox
        print("\n4. Selecting INBOX...")
        status, data = mail.select("INBOX")
        if status == 'OK':
            print(f"   ✓ INBOX selected. Message count: {data[0].decode()}")
            
            # Search for messages
            print("\n5. Searching for messages...")
            status, data = mail.search(None, "ALL")
            if status == 'OK':
                email_ids = data[0].split()
                print(f"   ✓ Found {len(email_ids)} messages")
                
                # Fetch latest message
                if email_ids:
                    latest_id = email_ids[-1]
                    print(f"\n6. Fetching header of message #{latest_id.decode()}...")
                    status, data = mail.fetch(latest_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
                    if status == 'OK':
                        print(f"   ✓ Successfully fetched header:")
                        print(f"\n{data[0][1].decode()}")
        
        # Close and logout
        mail.close()
        mail.logout()
        print("\n✅ SUCCESS! Your Gmail IMAP connection is working correctly.")
        
    except imaplib.IMAP4.error as e:
        print(f"\n❌ IMAP ERROR: {str(e)}")
        print("\nPossible solutions:")
        print("1. Check that your app password is correct")
        print("2. Make sure IMAP is enabled in Gmail settings")
        print("3. Check your Google Account security settings")
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)

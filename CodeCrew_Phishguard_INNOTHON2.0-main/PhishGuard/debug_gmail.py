#!/usr/bin/env python3
"""
Debug Gmail Connection

A simple script that tries to connect to Gmail IMAP
and prints detailed debug information along the way.
"""

import sys
import os
import imaplib
import email
import traceback
import platform
import socket

print("\n===== GMAIL DEBUG CONNECTION SCRIPT =====\n")

# Print system info
print("SYSTEM INFORMATION:")
print(f"Python version: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Current directory: {os.getcwd()}")
print("")

# Check if we can resolve Gmail's domain
print("NETWORK CHECK:")
try:
    gmail_ip = socket.gethostbyname("imap.gmail.com")
    print(f"✓ Successfully resolved imap.gmail.com to {gmail_ip}")
except socket.gaierror:
    print("❌ Failed to resolve imap.gmail.com - possible network issue")

# Email credentials
print("\nCONNECTION PARAMETERS:")
email_address = "dhruv200330@gmail.com"  # Replace with your actual email
app_password = input("Enter your Gmail App Password: ")

print(f"Email address: {email_address}")
print(f"App password length: {len(app_password)} characters")
print("IMAP server: imap.gmail.com")
print("IMAP port: 993")
print("")

# Enable debug for IMAP
imaplib.Debug = 4  # Enable IMAP debug output
print("IMAP debugging enabled at level 4")

# Try to connect
print("\nCONNECTION ATTEMPT:")
try:
    print("Creating SSL connection to imap.gmail.com:993...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    print("✓ Connection successful")
    
    print("\nAttempting to log in...")
    mail.login(email_address, app_password)
    print("✓ Login successful")
    
    print("\nSelecting INBOX...")
    status, count = mail.select("INBOX")
    if status == "OK":
        print(f"✓ INBOX selected. Message count: {count[0].decode()}")
    else:
        print(f"❌ Failed to select INBOX: {status}")
    
    print("\nSearching for emails...")
    status, data = mail.search(None, "ALL")
    if status == "OK":
        email_ids = data[0].split()
        print(f"✓ Found {len(email_ids)} emails in INBOX")
        
        if email_ids:
            print("\nFetching most recent email headers...")
            latest_id = email_ids[-1]
            status, data = mail.fetch(latest_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
            if status == "OK":
                print(f"✓ Successfully fetched headers for email ID {latest_id.decode()}")
                header = data[0][1].decode()
                print("\nMost recent email header:")
                print(f"{header}")
    else:
        print(f"❌ Failed to search emails: {status}")
    
    mail.close()
    mail.logout()
    print("\n✅ ALL TESTS PASSED - Your Gmail IMAP connection works!")
    print("You can now use PhishGuard with these credentials.")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nDetailed traceback:")
    traceback.print_exc()
    
    print("\nTROUBLESHOOTING STEPS:")
    print("1. Check if your App Password is correct (16 characters, no spaces)")
    print("2. Make sure IMAP is enabled in Gmail:")
    print("   - Go to Gmail > Settings > See all settings > Forwarding and POP/IMAP")
    print("   - Enable IMAP access")
    print("3. Check if your Google Account has security restrictions")
    print("   - Visit https://myaccount.google.com/security")
    print("4. Try generating a new App Password")
    print("   - Visit https://myaccount.google.com/apppasswords")

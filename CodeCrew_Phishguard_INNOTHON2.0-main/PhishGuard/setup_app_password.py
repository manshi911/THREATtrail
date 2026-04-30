#!/usr/bin/env python3
"""
App Password Generation Guide for PhishGuard

This script provides instructions for generating an App Password for Gmail,
which is required for PhishGuard to access your Gmail inbox via IMAP.
"""

import sys
import webbrowser
import os
from pathlib import Path
import time

def main():
    """Display instructions for generating an App Password for Gmail."""
    print("\n" + "=" * 75)
    print("APP PASSWORD GENERATION GUIDE FOR GMAIL".center(75))
    print("=" * 75 + "\n")
    
    print("PhishGuard requires a Gmail App Password to access your inbox.")
    print("Follow these steps to generate one:\n")
    
    print("Step 1: Make sure 2-Step Verification is enabled for your Google Account")
    print("       Without 2-Step Verification, you cannot generate App Passwords.\n")
    
    input("Press Enter to open Google 2-Step Verification settings in your browser... ")
    webbrowser.open("https://myaccount.google.com/security")
    time.sleep(2)
    
    print("\nIn the browser window that just opened:")
    print("1. Look for 'How you sign in to Google'")
    print("2. Make sure '2-Step Verification' is ON")
    print("3. If not, click on it and follow the steps to enable it")
    print("   (This might require your phone for verification)\n")
    
    input("After enabling 2-Step Verification, press Enter to continue... ")
    
    print("\nStep 2: Generate an App Password")
    input("Press Enter to open Google App Passwords page in your browser... ")
    webbrowser.open("https://myaccount.google.com/apppasswords")
    time.sleep(2)
    
    print("\nIn the browser window that just opened:")
    print("1. You might be asked to sign in again for security purposes")
    print("2. In the 'Select app' dropdown, choose 'Mail' or 'Other'")
    print("   (If you choose 'Other', enter 'PhishGuard' as the name)")
    print("3. In the 'Select device' dropdown, choose your device type or 'Other'")
    print("4. Click 'Generate'")
    print("5. Google will display a 16-character app password (with no spaces)")
    print("6. Copy this password\n")
    
    print("Step 3: Update your .env file with the App Password")
    print(f"1. Open the .env file in your PhishGuard directory")
    print("2. Find the line that says:")
    print("   EMAIL_APP_PASSWORD=your_gmail_app_password_here")
    print("3. Replace 'your_gmail_app_password_here' with your generated App Password")
    print("4. Save the file\n")
    
    print("Important Notes:")
    print("- App Passwords are 16 characters long, with NO SPACES")
    print("- Keep this password secure; it provides access to your Gmail account")
    print("- If you ever need to revoke this access, go back to the App Passwords")
    print("  page and remove the PhishGuard entry\n")
    
    print("-" * 75)
    print("After updating the .env file, you can run PhishGuard with:")
    print("python src/main.py")
    print("-" * 75 + "\n")
    
    input("Press Enter to exit this guide... ")

if __name__ == "__main__":
    main()

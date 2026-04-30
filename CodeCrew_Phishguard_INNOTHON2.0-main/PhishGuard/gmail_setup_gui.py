"""
PhishGuard Gmail Setup GUI

A simple GUI tool to help set up and test Gmail connection
for PhishGuard.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import imaplib
import os
import configparser
import re
import threading
import sys
import traceback
import webbrowser

class GmailSetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PhishGuard Gmail Setup")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Set app icon if available
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Variables
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # Load existing values
        self.load_existing_values()
        
        # Create UI
        self.create_ui()
    
    def load_existing_values(self):
        """Load existing values from config files."""
        # Load email from config.ini
        if os.path.exists("config.ini"):
            try:
                config = configparser.ConfigParser()
                config.read("config.ini")
                if "AUTH" in config and "email" in config["AUTH"]:
                    self.email_var.set(config["AUTH"]["email"])
            except:
                pass
        
        # Load app password from .env (just check if it exists)
        self.has_app_password = False
        if os.path.exists(".env"):
            try:
                with open(".env", "r") as f:
                    content = f.read()
                    if re.search(r'EMAIL_APP_PASSWORD=.+', content):
                        self.has_app_password = True
            except:
                pass
    
    def create_ui(self):
        """Create the user interface."""
        # Title
        title_frame = tk.Frame(self.root, pady=10)
        title_frame.pack(fill=tk.X)
        
        ttk.Label(title_frame, text="PhishGuard Gmail Setup", font=("Arial", 16, "bold")).pack()
        ttk.Label(title_frame, text="Configure and test your Gmail connection").pack()
        
        # Main content
        content = ttk.Notebook(self.root)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Setup tab
        setup_frame = ttk.Frame(content, padding=10)
        content.add(setup_frame, text="Setup")
        
        # Help tab
        help_frame = ttk.Frame(content, padding=10)
        content.add(help_frame, text="Help")
        
        # About tab
        about_frame = ttk.Frame(content, padding=10)
        content.add(about_frame, text="About")
        
        # Create setup tab content
        self.create_setup_tab(setup_frame)
        
        # Create help tab content
        self.create_help_tab(help_frame)
        
        # Create about tab content
        self.create_about_tab(about_frame)
        
        # Status bar
        status_frame = tk.Frame(self.root, pady=5)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        ttk.Label(status_frame, textvariable=self.status_var, anchor=tk.W).pack(side=tk.LEFT, padx=10)
    
    def create_setup_tab(self, parent):
        """Create the setup tab content."""
        # Email frame
        email_frame = ttk.LabelFrame(parent, text="Gmail Account", padding=10)
        email_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(email_frame, text="Gmail Address:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(email_frame, width=40, textvariable=self.email_var).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(email_frame, text="App Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(email_frame, width=40, textvariable=self.password_var, show="•")
        password_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        if self.has_app_password:
            # Show a masked placeholder
            self.password_var.set("****************")
        
        # Help button for app password
        ttk.Button(email_frame, text="Get App Password", command=self.open_app_password_page).grid(row=1, column=2, padx=5)
        
        # IMAP settings display
        imap_frame = ttk.LabelFrame(parent, text="IMAP Server Settings", padding=10)
        imap_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(imap_frame, text="Server:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(imap_frame, text="imap.gmail.com").grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(imap_frame, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(imap_frame, text="993 (SSL)").grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(parent, padding=10)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Test Connection", command=self.test_connection).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Configuration", command=self.save_configuration).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Enable IMAP in Gmail", command=self.open_gmail_imap_settings).pack(side=tk.LEFT, padx=5)
        
        # Log text area
        log_frame = ttk.LabelFrame(parent, text="Connection Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.log("Welcome to PhishGuard Gmail Setup")
        self.log("This utility helps you configure and test your Gmail connection")
        self.log("Click 'Test Connection' to verify your credentials")
    
    def create_help_tab(self, parent):
        """Create the help tab content."""
        # 2FA info
        twofa_frame = ttk.LabelFrame(parent, text="Step 1: Enable 2-Step Verification", padding=10)
        twofa_frame.pack(fill=tk.X, pady=5)
        
        twofa_text = """To use an App Password, you must first enable 2-Step Verification on your Google Account:

1. Go to your Google Account security settings
2. Find 'How you sign in to Google' section
3. Click on '2-Step Verification'
4. Follow the steps to enable it"""
        
        ttk.Label(twofa_frame, text=twofa_text, wraplength=550, justify=tk.LEFT).pack(fill=tk.X, pady=5)
        ttk.Button(twofa_frame, text="Open Google Security Settings", command=self.open_google_security).pack(anchor=tk.W, pady=5)
        
        # App Password info
        app_pw_frame = ttk.LabelFrame(parent, text="Step 2: Generate an App Password", padding=10)
        app_pw_frame.pack(fill=tk.X, pady=5)
        
        app_pw_text = """After enabling 2-Step Verification, you can generate an App Password:

1. Go to your Google Account > Security > App passwords
2. Select 'Mail' as the app
3. Select your device type (or choose 'Other' and enter 'PhishGuard')
4. Click 'Generate'
5. Copy the 16-character password (no spaces)
6. Paste it in the App Password field"""
        
        ttk.Label(app_pw_frame, text=app_pw_text, wraplength=550, justify=tk.LEFT).pack(fill=tk.X, pady=5)
        ttk.Button(app_pw_frame, text="Generate App Password", command=self.open_app_password_page).pack(anchor=tk.W, pady=5)
        
        # IMAP settings info
        imap_frame = ttk.LabelFrame(parent, text="Step 3: Enable IMAP in Gmail", padding=10)
        imap_frame.pack(fill=tk.X, pady=5)
        
        imap_text = """You need to enable IMAP access in your Gmail settings:

1. Go to Gmail
2. Click the gear icon (Settings)
3. Click 'See all settings'
4. Go to the 'Forwarding and POP/IMAP' tab
5. In the 'IMAP access' section, select 'Enable IMAP'
6. Click 'Save Changes'"""
        
        ttk.Label(imap_frame, text=imap_text, wraplength=550, justify=tk.LEFT).pack(fill=tk.X, pady=5)
        ttk.Button(imap_frame, text="Open Gmail Settings", command=self.open_gmail_imap_settings).pack(anchor=tk.W, pady=5)
        
        # Troubleshooting
        trouble_frame = ttk.LabelFrame(parent, text="Troubleshooting", padding=10)
        trouble_frame.pack(fill=tk.X, pady=5)
        
        trouble_text = """If you're having issues connecting to Gmail:

1. Make sure 2-Step Verification is enabled
2. Verify your App Password is correct (16 characters, no spaces)
3. Check that IMAP is enabled in Gmail
4. Check for any Google Account security alerts
5. Try generating a new App Password
6. Disable any VPN that might block connection"""
        
        ttk.Label(trouble_frame, text=trouble_text, wraplength=550, justify=tk.LEFT).pack(fill=tk.X, pady=5)
    
    def create_about_tab(self, parent):
        """Create the about tab content."""
        about_text = """PhishGuard: Automated Email Threat Detection and Reporting System

Version: 1.0.0
Hackathon Project

Features:
• Real-time email monitoring via IMAP
• AI-powered threat detection using NLP
• URL analysis with Gradient Boosting Classifier
• Image-based phishing detection through OCR
• Instant user alerts through GUI dialog boxes
• Detailed threat logging and reporting
• Department-wise threat analysis reports

This utility helps you set up the Gmail IMAP connection
required for PhishGuard to monitor your inbox."""
        
        ttk.Label(parent, text=about_text, wraplength=550, justify=tk.LEFT).pack(fill=tk.BOTH, expand=True, pady=10)
    
    def log(self, message):
        """Add a message to the log text area."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def open_google_security(self):
        """Open Google Account security settings."""
        webbrowser.open("https://myaccount.google.com/security")
    
    def open_app_password_page(self):
        """Open the App Password generation page."""
        webbrowser.open("https://myaccount.google.com/apppasswords")
    
    def open_gmail_imap_settings(self):
        """Open Gmail IMAP settings page."""
        webbrowser.open("https://mail.google.com/mail/#settings/fwdandpop")
    
    def test_connection(self):
        """Test the Gmail IMAP connection."""
        email = self.email_var.get()
        password = self.password_var.get()
        
        # Check inputs
        if not email:
            messagebox.showerror("Error", "Please enter your Gmail address")
            return
        
        if not password or password == "****************":
            messagebox.showerror("Error", "Please enter your App Password")
            return
        
        # Update status
        self.status_var.set("Testing connection...")
        self.log("\n--- Testing Gmail IMAP Connection ---")
        self.log(f"Email: {email}")
        self.log(f"App Password: {'*' * len(password)}")
        
        # Run the test in a separate thread to keep UI responsive
        threading.Thread(target=self._run_connection_test, args=(email, password), daemon=True).start()
    
    def _run_connection_test(self, email, password):
        """Run the actual connection test in a separate thread."""
        try:
            # Clear previous results
            self.log("Connecting to imap.gmail.com:993...")
            
            # Connect to Gmail
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            self.log("✓ Connection established")
            
            # Login
            self.log("Attempting to log in...")
            mail.login(email, password)
            self.log("✓ Login successful!")
            
            # Select inbox
            self.log("Selecting INBOX...")
            status, count = mail.select("INBOX")
            if status == 'OK':
                self.log(f"✓ INBOX selected. Message count: {count[0].decode()}")
                
                # Search for emails
                self.log("Searching for messages...")
                status, data = mail.search(None, "ALL")
                if status == 'OK':
                    email_ids = data[0].split()
                    self.log(f"✓ Found {len(email_ids)} messages")
                    
                    # Fetch latest email as a test
                    if email_ids:
                        latest_id = email_ids[-1]
                        self.log(f"Fetching headers of latest email...")
                        status, data = mail.fetch(latest_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
                        if status == 'OK':
                            self.log(f"✓ Successfully retrieved headers")
                            header = data[0][1].decode()
                            self.log(f"\n{header}")
            
            # Close and logout
            mail.close()
            mail.logout()
            
            # Update UI from main thread
            self.root.after(0, lambda: self._update_ui_after_test(True))
            
        except imaplib.IMAP4.error as e:
            error_msg = str(e)
            self.log(f"\n❌ IMAP ERROR: {error_msg}")
            
            # Show specific advice based on error
            if "Invalid credentials" in error_msg:
                self.log("Your App Password appears to be incorrect.")
                self.log("Please generate a new App Password from your Google Account.")
            elif "AUTHENTICATE failed" in error_msg:
                self.log("Authentication failed. Check your email and App Password.")
            else:
                self.log("Check that IMAP is enabled in your Gmail settings.")
                self.log("Make sure 2-Step Verification is enabled for your Google Account.")
            
            # Update UI from main thread
            self.root.after(0, lambda: self._update_ui_after_test(False))
            
        except Exception as e:
            self.log(f"\n❌ ERROR: {str(e)}")
            self.log("\nDetailed error:")
            self.log(traceback.format_exc())
            
            # Update UI from main thread
            self.root.after(0, lambda: self._update_ui_after_test(False))
    
    def _update_ui_after_test(self, success):
        """Update the UI after test completes."""
        if success:
            self.status_var.set("Connection test successful")
            self.log("\n✅ TEST PASSED! Your Gmail IMAP connection is working.")
            messagebox.showinfo("Success", "Gmail connection test successful! You can now save your configuration.")
        else:
            self.status_var.set("Connection test failed")
            self.log("\n❌ TEST FAILED. Please check the errors above.")
            messagebox.showerror("Error", "Gmail connection test failed. Check the log for details.")
    
    def save_configuration(self):
        """Save the Gmail connection configuration."""
        email = self.email_var.get()
        password = self.password_var.get()
        
        # Check inputs
        if not email:
            messagebox.showerror("Error", "Please enter your Gmail address")
            return
        
        if not password or password == "****************":
            messagebox.showerror("Error", "Please enter your App Password")
            return
        
        # Update status
        self.status_var.set("Saving configuration...")
        self.log("\n--- Saving Gmail Configuration ---")
        
        success = True
        
        # Save email to config.ini
        if os.path.exists("config.ini"):
            try:
                config = configparser.ConfigParser()
                config.read("config.ini")
                
                if "AUTH" in config:
                    config["AUTH"]["email"] = email
                    
                    with open("config.ini", "w") as config_file:
                        config.write(config_file)
                    
                    self.log("✓ Email updated in config.ini")
                else:
                    self.log("❌ AUTH section not found in config.ini")
                    success = False
            except Exception as e:
                self.log(f"❌ Error updating config.ini: {str(e)}")
                success = False
        else:
            self.log("❌ config.ini file not found")
            success = False
        
        # Save password to .env
        try:
            if os.path.exists(".env"):
                # Read existing content
                with open(".env", "r") as env_file:
                    env_content = env_file.read()
                
                # Replace or add EMAIL_APP_PASSWORD
                if "EMAIL_APP_PASSWORD=" in env_content:
                    env_content = re.sub(
                        r"EMAIL_APP_PASSWORD=.*",
                        f"EMAIL_APP_PASSWORD={password}",
                        env_content
                    )
                else:
                    env_content += f"\nEMAIL_APP_PASSWORD={password}"
                
                # Write back to file
                with open(".env", "w") as env_file:
                    env_file.write(env_content)
                
                self.log("✓ App password updated in .env file")
            else:
                # Create new .env file
                with open(".env", "w") as env_file:
                    env_file.write(f"EMAIL_APP_PASSWORD={password}\n")
                
                self.log("✓ Created new .env file with app password")
            
            # Update flag
            self.has_app_password = True
            
        except Exception as e:
            self.log(f"❌ Error updating .env file: {str(e)}")
            success = False
        
        # Update UI
        if success:
            self.status_var.set("Configuration saved successfully")
            self.log("\n✅ Configuration saved successfully!")
            messagebox.showinfo("Success", "Gmail configuration saved successfully!")
        else:
            self.status_var.set("Failed to save configuration")
            self.log("\n❌ Failed to save configuration. See errors above.")
            messagebox.showerror("Error", "Failed to save configuration. Check the log for details.")

def main():
    """Main entry point for the app."""
    root = tk.Tk()
    app = GmailSetupApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

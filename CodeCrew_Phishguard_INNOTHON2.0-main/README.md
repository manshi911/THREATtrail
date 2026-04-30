# PhishGuard: Automated Email Threat Detection and Department-Wise Reporting System

PhishGuard is a real-time, AI-powered email phishing detection system that automatically integrates with an organization's email inbox to detect potential phishing threats and immediately alert users. The system also provides department-wise threat reporting for organizational awareness.

## Features

- Real-time email monitoring via IMAP
- Multi-technique threat detection:
  - NLP-based text analysis
  - URL/domain reputation checking
  - Attachment analysis
  - Image-based phishing detection through OCR
- Instant user alerts through GUI dialog boxes
- Comprehensive threat logging in SQLite database
- Department-wise threat analysis and reporting
- Scheduled daily and weekly reports

## Project Structure

```
PhishGuard/
├── src/
│   ├── email_integration/   # Email monitoring and parsing
│   │   └── gmail_monitor.py # Gmail IMAP integration
│   ├── threat_detection/    # Threat analysis engine
│   │   └── threat_detector.py # Core threat detection logic
│   ├── ocr_processing/      # Image analysis and text extraction
│   │   └── ocr_processor.py # OCR-based phishing detection
│   ├── warning_system/      # User alert system
│   │   └── alert_dialog.py  # GUI alert dialogs
│   ├── data_logging/        # Threat logging and storage
│   │   └── data_logger.py   # Database operations
│   ├── reporting/           # Report generation
│   │   └── report_generator.py # Report creation and distribution
│   └── main.py              # Main application entry point
├── data/                    # Data storage
│   ├── phishguard.db        # SQLite database
│   └── departments.json     # Email-to-department mapping
├── logs/                    # Application logs
├── reports/                 # Generated reports
│   ├── html/                # HTML reports
│   ├── csv/                 # CSV reports
│   └── pdf/                 # PDF reports (future)
├── config.ini               # Application configuration
├── .env                     # Environment variables (credentials)
├── requirements.txt         # Python dependencies
└── README.md                # This documentation
```

## Setup

### Prerequisites

- Python 3.8 or higher
- Gmail account with IMAP access enabled
- Google App Password (requires 2-Step Verification)
- Tesseract OCR (optional, for image-based threat detection)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/Ritik-Malviya/CodeCrew_Phishguard_INNOTHON2.0
   cd phishguard
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. If using OCR functionality, install Tesseract OCR:
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt install tesseract-ocr`
   - macOS: `brew install tesseract`

4. Create a `.env` file with your Gmail App Password:
   ```
   EMAIL_APP_PASSWORD=your_app_password_here
   ```

5. Update `config.ini` with your email address and other settings.

### Generating a Google App Password

1. Enable 2-Step Verification on your Google Account at https://myaccount.google.com/security
2. Generate an App Password at https://myaccount.google.com/apppasswords
3. Select "Mail" as the app and your device type
4. Copy the generated 16-character password to your `.env` file

### Running the Setup Assistant

For easy setup and configuration:

```
python gmail_setup_gui.py
```

Or for command-line setup:

```
python test_gmail_interactive.py
```

## Usage

### Testing Gmail Connection

Run one of the test scripts to verify your connection to Gmail:

```
python test_gmail_connection.py
```

For interactive debugging:

```
python debug_gmail.py
```

### Running the Full Application

Start the main application:

```
python src/main.py
```

Or use the command-line interface for testing:

```
python phishguard_cli.py
```

## Department Mapping

The system automatically creates a default `data/departments.json` file with common departments. Edit this file to match your organization's email addresses and departments structure.

## Reporting

- Daily reports are automatically generated at midnight for each department
- Weekly summary reports are generated on Sundays at midnight
- Reports are stored in the `reports/` directory in both HTML and CSV formats

## Advanced Features

### OCR-Based Phishing Detection

PhishGuard can detect phishing attempts hidden in images by:
- Extracting text from images using OCR
- Analyzing the extracted text for suspicious content, keywords, and URLs
- Detecting login forms and other common phishing patterns in images

### URL Analysis

The system analyzes URLs in emails using:
- Domain reputation checking
- Typosquatting detection (similar to legitimate domains)
- IP address URL detection
- URL shortener identification
- Suspicious TLD (.xyz, .top, etc.) recognition

## Customization

- Adjust risk score thresholds in `threat_detector.py`
- Modify the suspicious keywords list for your industry
- Add custom indicators in the threat detection engine
- Configure department mapping for your organization

## Future Enhancements

- Integration with more email providers
- Machine learning model for improved accuracy
- Quarantine functionality for suspicious emails
- API for integration with other security tools

## License

[MIT License](LICENSE)

from PyQt5.QtWidgets import (QTableWidgetItem, QVBoxLayout, QHBoxLayout, QFrame, 
                           QLabel, QComboBox, QFormLayout, QPushButton, QWidget, 
                           QSizePolicy, QHeaderView, QTableWidget, QLineEdit, 
                           QCheckBox, QSlider)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from datetime import datetime
from color_scheme import COLORS
from ui_resources import get_icon

def populateThreatsList(self):
    """Populate the threats list with sample data."""
    # Sample data for the threats table
    threats = [
        {
            "datetime": "2025-05-10 10:30:45",
            "sender": "suspicious@example.com",
            "recipient": "finance@company.com",
            "subject": "Urgent: Your account has been compromised",
            "risk_level": "High",
            "risk_color": COLORS['danger'],
            "threat_type": "Phishing",
            "status": "Blocked"
        },
        {
            "datetime": "2025-05-10 09:45:22",
            "sender": "newsletter@unknown-domain.com",
            "recipient": "marketing@company.com",
            "subject": "Important Document Attached",
            "risk_level": "Medium",
            "risk_color": COLORS['warning'],
            "threat_type": "Suspicious Attachment",
            "status": "Quarantined"
        },
        {
            "datetime": "2025-05-09 16:20:15",
            "sender": "info@company-portal.net",
            "recipient": "hr@company.com",
            "subject": "Update your password now",
            "risk_level": "Low",
            "risk_color": COLORS['primary'],
            "threat_type": "Social Engineering",
            "status": "Warned"
        },
        {
            "datetime": "2025-05-09 14:05:51",
            "sender": "paypal-security@mail.tk",
            "recipient": "accounting@company.com",
            "subject": "Your payment was processed",
            "risk_level": "High",
            "risk_color": COLORS['danger'],
            "threat_type": "Phishing",
            "status": "Blocked"
        },
        {        "datetime": "2025-05-08 11:17:32",
            "sender": "hr-notification@domain.co",
            "recipient": "ceo@company.com",
            "subject": "Salary Adjustment Document",
            "risk_level": "Medium",
            "risk_color": COLORS['warning'],
            "threat_type": "Suspicious Link",
            "status": "Quarantined"
        },
        {
            "datetime": "2025-05-08 09:30:05",
            "sender": "drive-share@g00gle.co",
            "recipient": "support@company.com",
            "subject": "Shared: Project Documents",
            "risk_level": "High",
            "risk_color": COLORS['danger'],
            "threat_type": "Fake Domain",
            "status": "Blocked"
        },
        {
            "datetime": "2025-05-07 15:42:18",
            "sender": "account@amaz0n-security.com",
            "recipient": "purchasing@company.com",
            "subject": "Your order has been suspended",
            "risk_level": "High",
            "risk_color": COLORS['danger'],
            "threat_type": "Phishing",
            "status": "Blocked"
        }
    ]
    
    # Clear existing items
    self.threats_table.setRowCount(0)
    
    # Add sample data
    for i, threat in enumerate(threats):
        self.threats_table.insertRow(i)
          # Date/Time column
        date_obj = datetime.strptime(threat["datetime"], "%Y-%m-%d %H:%M:%S")
        date_str = date_obj.strftime("%Y-%m-%d")
        time_str = date_obj.strftime("%H:%M")
        date_item = QTableWidgetItem(f"{date_str}\n{time_str}")
        date_item.setTextAlignment(Qt.AlignCenter)
        self.threats_table.setItem(i, 0, date_item)
        
        # Sender column
        self.threats_table.setItem(i, 1, QTableWidgetItem(threat["sender"]))
        
        # Recipient column
        self.threats_table.setItem(i, 2, QTableWidgetItem(threat["recipient"]))
        
        # Subject column
        self.threats_table.setItem(i, 3, QTableWidgetItem(threat["subject"]))
        
        # Risk Level column
        risk_item = QTableWidgetItem(threat["risk_level"])
        risk_item.setForeground(QColor(threat["risk_color"]))
        risk_item.setTextAlignment(Qt.AlignCenter)
        self.threats_table.setItem(i, 4, risk_item)
        
        # Threat Type column
        threat_type_item = QTableWidgetItem(threat["threat_type"])
        threat_type_item.setTextAlignment(Qt.AlignCenter)
        self.threats_table.setItem(i, 5, threat_type_item)
        
        # Status column
        status_item = QTableWidgetItem(threat["status"])
        if threat["status"] == "Blocked":
            status_item.setForeground(QColor(COLORS['danger']))
        elif threat["status"] == "Quarantined":
            status_item.setForeground(QColor(COLORS['warning']))
        else:
            status_item.setForeground(QColor(COLORS['primary']))
        status_item.setTextAlignment(Qt.AlignCenter)
        self.threats_table.setItem(i, 6, status_item)
    
    def createReportsTab(self, parent_widget):
        """Create the reports tab."""
        reports_layout = QVBoxLayout(parent_widget)
        reports_layout.setContentsMargins(15, 15, 15, 15)
        reports_layout.setSpacing(15)
        
        # Header with gradient
        header_frame = QFrame()
        header_frame.setStyleSheet(
            "QFrame {background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5c9aff, stop:1 #8cb8ff); "
            "border-radius: 8px; color: white; padding: 15px;}"
        )
        header_frame.setMinimumHeight(120)
        header_layout = QVBoxLayout(header_frame)
        
        header_title = QLabel("Threat Reports")
        header_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header_title.setStyleSheet("color: white;")
        
        header_subtitle = QLabel(
            "Generate detailed reports on email threats, analyze trends, and export data for further analysis."
        )
        header_subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        header_subtitle.setWordWrap(True)
        
        header_layout.addWidget(header_title)
        header_layout.addWidget(header_subtitle)
        
        # Report generation section
        report_frame = QFrame()
        report_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        report_layout = QVBoxLayout(report_frame)
        
        # Title
        report_title = QLabel("Generate New Report")
        report_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        report_layout.addWidget(report_title)
        
        # Form layout for report options
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(10, 10, 10, 10)
        
        # Report type combo
        report_type_combo = QComboBox()
        report_type_combo.addItems([
            "Threat Summary Report", 
            "Department Risk Analysis", 
            "Threat Trends Over Time",
            "Risk Score Distribution",
            "Email Source Analysis"
        ])
        form_layout.addRow("Report Type:", report_type_combo)
        
        # Time period combo
        time_period_combo = QComboBox()
        time_period_combo.addItems([
            "Last 7 Days",
            "Last 30 Days",
            "Last Quarter",
            "Year to Date",
            "Custom Period"
        ])
        form_layout.addRow("Time Period:", time_period_combo)
        
        # Department filter
        dept_filter = QComboBox()
        dept_filter.addItems([
            "All Departments",
            "Finance",
            "Human Resources",
            "IT",
            "Marketing",
            "Sales",
            "Operations"
        ])
        form_layout.addRow("Department:", dept_filter)
        
        # Format combo
        format_combo = QComboBox()
        format_combo.addItems(["PDF", "HTML", "CSV", "Excel"])
        form_layout.addRow("Format:", format_combo)
        
        # Add form to layout
        report_layout.addLayout(form_layout)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        buttons_layout.addWidget(spacer)
        
        preview_button = QPushButton("Preview Report")
        preview_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addWidget(preview_button)
        
        generate_button = QPushButton("Generate Report")
        generate_button.setObjectName("generate_report_button")  # For QSS styling
        generate_button.setIcon(get_icon("report"))
        generate_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addWidget(generate_button)
        
        report_layout.addLayout(buttons_layout)
        
        # Previous reports section
        previous_frame = QFrame()
        previous_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        previous_layout = QVBoxLayout(previous_frame)
        
        # Title with count
        previous_title_layout = QHBoxLayout()
        previous_title = QLabel("Previous Reports")
        previous_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        previous_count = QLabel("12 reports available")
        
        previous_title_layout.addWidget(previous_title)
        previous_title_layout.addStretch()
        previous_title_layout.addWidget(previous_count)
        
        previous_layout.addLayout(previous_title_layout)
        
        # Previous reports table
        reports_table = QTableWidget()
        reports_table.setColumnCount(5)
        reports_table.setHorizontalHeaderLabels([
            "Date Generated", "Report Type", "Period", "Format", "Actions"
        ])
        
        # Configure table appearance
        reports_table.setAlternatingRowColors(True)
        reports_table.setEditTriggers(QTableWidget.NoEditTriggers)
        reports_table.setSelectionBehavior(QTableWidget.SelectRows)
        reports_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Report Type column stretch
        reports_table.verticalHeader().setVisible(False)  # Hide row numbers
        
        # Add some example data
        reports_table.setRowCount(5)
        
        # Example report 1
        reports_table.setItem(0, 0, QTableWidgetItem("2025-05-09"))
        reports_table.setItem(0, 1, QTableWidgetItem("Threat Summary Report"))
        reports_table.setItem(0, 2, QTableWidgetItem("Last 7 Days"))
        reports_table.setItem(0, 3, QTableWidgetItem("PDF"))
        
        # Example report 2
        reports_table.setItem(1, 0, QTableWidgetItem("2025-05-05"))
        reports_table.setItem(1, 1, QTableWidgetItem("Department Risk Analysis"))
        reports_table.setItem(1, 2, QTableWidgetItem("Last 30 Days"))
        reports_table.setItem(1, 3, QTableWidgetItem("HTML"))
        
        # Example report 3
        reports_table.setItem(2, 0, QTableWidgetItem("2025-04-28"))
        reports_table.setItem(2, 1, QTableWidgetItem("Threat Trends Over Time"))
        reports_table.setItem(2, 2, QTableWidgetItem("Last Quarter"))
        reports_table.setItem(2, 3, QTableWidgetItem("PDF"))
        
        # Example report 4
        reports_table.setItem(3, 0, QTableWidgetItem("2025-04-15"))
        reports_table.setItem(3, 1, QTableWidgetItem("Risk Score Distribution"))
        reports_table.setItem(3, 2, QTableWidgetItem("Year to Date"))
        reports_table.setItem(3, 3, QTableWidgetItem("Excel"))
        
        # Example report 5
        reports_table.setItem(4, 0, QTableWidgetItem("2025-04-01"))
        reports_table.setItem(4, 1, QTableWidgetItem("Email Source Analysis"))
        reports_table.setItem(4, 2, QTableWidgetItem("Last 30 Days"))
        reports_table.setItem(4, 3, QTableWidgetItem("CSV"))
        
        # Add action buttons to each row
        for i in range(5):
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            view_btn = QPushButton("View")
            view_btn.setFixedWidth(60)
            view_btn.setCursor(Qt.PointingHandCursor)
            
            download_btn = QPushButton("Download")
            download_btn.setFixedWidth(80)
            download_btn.setCursor(Qt.PointingHandCursor)
            
            action_layout.addWidget(view_btn)
            action_layout.addWidget(download_btn)
            
            reports_table.setCellWidget(i, 4, action_widget)
        
        previous_layout.addWidget(reports_table)
        
        # Add all sections to the main layout
        reports_layout.addWidget(header_frame)
        reports_layout.addWidget(report_frame)
        reports_layout.addWidget(previous_frame)
        
    def createSettingsTab(self, parent_widget):
        """Create the settings tab."""
        settings_layout = QVBoxLayout(parent_widget)
        settings_layout.setContentsMargins(15, 15, 15, 15)
        settings_layout.setSpacing(15)
        
        # Header section
        header_frame = QFrame()
        header_frame.setStyleSheet(
            "QFrame {background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6c757d, stop:1 #868e96); "
            "border-radius: 8px; color: white; padding: 15px;}"
        )
        header_frame.setMinimumHeight(100)
        header_layout = QVBoxLayout(header_frame)
        
        header_title = QLabel("Settings")
        header_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header_title.setStyleSheet("color: white;")
        
        header_subtitle = QLabel(
            "Configure PhishGuard settings, email monitoring options, and notification preferences."
        )
        header_subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        header_subtitle.setWordWrap(True)
        
        header_layout.addWidget(header_title)
        header_layout.addWidget(header_subtitle)
        
        # Email monitoring settings
        email_settings_frame = QFrame()
        email_settings_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        email_settings_layout = QVBoxLayout(email_settings_frame)
        
        email_title = QLabel("Email Monitoring Settings")
        email_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        email_settings_layout.addWidget(email_title)
        
        # Form layout for email settings
        email_form = QFormLayout()
        email_form.setSpacing(10)
        email_form.setContentsMargins(10, 10, 10, 10)
        
        # Email check interval
        check_interval = QComboBox()
        check_interval.addItems(["Every 1 minute", "Every 5 minutes", "Every 10 minutes", "Every 30 minutes", "Every hour"])
        check_interval.setCurrentIndex(1)  # Default to 5 minutes
        email_form.addRow("Check Interval:", check_interval)
        
        # Email account
        email_account = QLineEdit("username@example.com")
        email_form.addRow("Email Account:", email_account)
        
        # Email domains to monitor
        monitored_domains = QLineEdit("company.com, company-subdomain.com")
        email_form.addRow("Domains to Monitor:", monitored_domains)
        
        # Add form to layout
        email_settings_layout.addLayout(email_form)
        
        # Notification settings
        notification_settings_frame = QFrame()
        notification_settings_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        notification_settings_layout = QVBoxLayout(notification_settings_frame)
        
        notification_title = QLabel("Notification Settings")
        notification_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        notification_settings_layout.addWidget(notification_title)
        
        # Notification options
        notification_options = QVBoxLayout()
        
        desktop_notify = QCheckBox("Show desktop notifications for high-risk threats")
        desktop_notify.setChecked(True)
        
        email_notify = QCheckBox("Send email notifications to security team")
        email_notify.setChecked(True)
        
        sound_notify = QCheckBox("Play sound alert for critical threats")
        sound_notify.setChecked(True)
        
        # Risk threshold
        risk_threshold_layout = QHBoxLayout()
        risk_threshold_layout.addWidget(QLabel("Minimum Risk Threshold for Alerts:"))
        
        risk_slider = QSlider(Qt.Horizontal)
        risk_slider.setMinimum(0)
        risk_slider.setMaximum(100)
        risk_slider.setValue(50)
        risk_slider.setTickPosition(QSlider.TicksBelow)
        risk_slider.setTickInterval(10)
        
        risk_value = QLabel("50%")
        
        risk_threshold_layout.addWidget(risk_slider)
        risk_threshold_layout.addWidget(risk_value)
        
        # Add options to layout
        notification_options.addWidget(desktop_notify)
        notification_options.addWidget(email_notify)
        notification_options.addWidget(sound_notify)
        notification_options.addLayout(risk_threshold_layout)
        
        notification_settings_layout.addLayout(notification_options)
        
        # Advanced settings
        advanced_settings_frame = QFrame()
        advanced_settings_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
        advanced_settings_layout = QVBoxLayout(advanced_settings_frame)
        
        advanced_title = QLabel("Advanced Settings")
        advanced_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        advanced_settings_layout.addWidget(advanced_title)
        
        # Advanced options
        advanced_options = QFormLayout()
        advanced_options.setSpacing(10)
        
        data_retention = QComboBox()
        data_retention.addItems(["30 days", "60 days", "90 days", "180 days", "1 year", "Forever"])
        advanced_options.addRow("Data Retention Period:", data_retention)
        
        log_level = QComboBox()
        log_level.addItems(["Error", "Warning", "Info", "Debug"])
        log_level.setCurrentIndex(2)  # Default to Info
        advanced_options.addRow("Logging Level:", log_level)
        
        auto_update = QCheckBox("Check for updates automatically")
        auto_update.setChecked(True)
        
        advanced_options.addRow("", auto_update)
        
        advanced_settings_layout.addLayout(advanced_options)
        
        # Save button section
        buttons_layout = QHBoxLayout()
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        buttons_layout.addWidget(spacer)
        
        reset_button = QPushButton("Reset to Defaults")
        reset_button.setCursor(Qt.PointingHandCursor)
        
        save_button = QPushButton("Save Settings")
        save_button.setObjectName("settings_button")  # For QSS styling
        save_button.setIcon(get_icon("settings"))
        save_button.setCursor(Qt.PointingHandCursor)
        
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(save_button)
        
        # Add all sections to main layout
        settings_layout.addWidget(header_frame)
        settings_layout.addWidget(email_settings_frame)
        settings_layout.addWidget(notification_settings_frame)
        settings_layout.addWidget(advanced_settings_frame)
        settings_layout.addLayout(buttons_layout)
        
    def updateStatistics(self):
        """Update the statistics and dashboard information."""
        # In a real app, we would query the database or backend for this data
        # For now, we'll just use the example data we've already set up
        self.last_checked_label.setText(f"Last Check: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

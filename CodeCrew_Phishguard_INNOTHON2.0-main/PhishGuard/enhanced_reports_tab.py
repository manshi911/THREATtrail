from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QLabel, 
                          QFont, QFrame, QPushButton, QSizePolicy, QTableWidget, 
                          QTableWidgetItem, QHeaderView, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

# Assuming get_icon is defined elsewhere
def get_icon(name):
    # This would normally return an icon, but is a placeholder here
    return None

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
        report_frame.setStyleSheet(
            "QFrame { background-color: white; border-radius: 8px; padding: 20px; border: 2px solid #cccccc; }"
        )
        report_frame.setMinimumHeight(400)  # Ensure minimum height for content
        report_layout = QVBoxLayout(report_frame)
        report_layout.setSpacing(20)
        
        # Title
        report_title = QLabel("Generate New Report")
        report_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        report_title.setStyleSheet("color: #0066cc; margin-bottom: 10px;")
        report_layout.addWidget(report_title)
        
        # Description
        report_description = QLabel("Select report options below and click 'Preview Report' to see a sample or 'Generate Report' to create the full report.")
        report_description.setWordWrap(True)
        report_description.setStyleSheet("color: #666; margin-bottom: 15px;")
        report_layout.addWidget(report_description)
        
        # Form layout for report options
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # Report type combo with enhanced visibility
        report_type_label = QLabel("Report Type:")
        report_type_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        report_type_label.setStyleSheet("color: #0066cc;")
        
        self.report_type_combo = QComboBox()
        self.report_type_combo.addItems([
            "Threat Summary Report", 
            "Department Risk Analysis", 
            "Threat Trends Over Time",
            "Risk Score Distribution",
            "Email Source Analysis"
        ])
        self.report_type_combo.setMinimumWidth(250)
        self.report_type_combo.setMinimumHeight(35)
        self.report_type_combo.setStyleSheet(
            "QComboBox { background-color: white; color: black; border: 2px solid #5c9aff; "
            "border-radius: 4px; padding: 4px; font-size: 13px; }"
            "QComboBox::drop-down { border-color: #5c9aff; width: 30px; }"
            "QComboBox QAbstractItemView { background-color: white; selection-background-color: #5c9aff; }"
        )
        form_layout.addRow(report_type_label, self.report_type_combo)
        
        # Time period combo with enhanced visibility
        time_period_label = QLabel("Time Period:")
        time_period_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        time_period_label.setStyleSheet("color: #0066cc;")
        
        self.time_period_combo = QComboBox()
        self.time_period_combo.addItems([
            "Last 7 Days",
            "Last 30 Days",
            "Last Quarter",
            "Year to Date",
            "Custom Period"
        ])
        self.time_period_combo.setMinimumWidth(250)
        self.time_period_combo.setMinimumHeight(35)
        self.time_period_combo.setStyleSheet(
            "QComboBox { background-color: white; color: black; border: 2px solid #5c9aff; "
            "border-radius: 4px; padding: 4px; font-size: 13px; }"
            "QComboBox::drop-down { border-color: #5c9aff; width: 30px; }"
            "QComboBox QAbstractItemView { background-color: white; selection-background-color: #5c9aff; }"
        )
        form_layout.addRow(time_period_label, self.time_period_combo)
        
        # Department filter with enhanced visibility
        department_label = QLabel("Department:")
        department_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        department_label.setStyleSheet("color: #0066cc;")
        
        self.dept_filter = QComboBox()
        self.dept_filter.addItems([
            "All Departments",
            "Finance",
            "Human Resources",
            "IT",
            "Marketing",
            "Sales",
            "Operations"
        ])
        self.dept_filter.setMinimumWidth(250)
        self.dept_filter.setMinimumHeight(35)
        self.dept_filter.setStyleSheet(
            "QComboBox { background-color: white; color: black; border: 2px solid #5c9aff; "
            "border-radius: 4px; padding: 4px; font-size: 13px; }"
            "QComboBox::drop-down { border-color: #5c9aff; width: 30px; }"
            "QComboBox QAbstractItemView { background-color: white; selection-background-color: #5c9aff; }"
        )
        form_layout.addRow(department_label, self.dept_filter)
        
        # Format combo with enhanced visibility
        format_label = QLabel("Format:")
        format_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        format_label.setStyleSheet("color: #0066cc;")
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PDF", "HTML", "CSV", "Excel"])
        self.format_combo.setMinimumWidth(250)
        self.format_combo.setMinimumHeight(35)
        self.format_combo.setStyleSheet(
            "QComboBox { background-color: white; color: black; border: 2px solid #5c9aff; "
            "border-radius: 4px; padding: 4px; font-size: 13px; }"
            "QComboBox::drop-down { border-color: #5c9aff; width: 30px; }"
            "QComboBox QAbstractItemView { background-color: white; selection-background-color: #5c9aff; }"
        )
        form_layout.addRow(format_label, self.format_combo)
        
        # Add form to layout
        report_layout.addLayout(form_layout)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(0, 25, 0, 0)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        buttons_layout.addWidget(spacer)
        
        preview_button = QPushButton("Preview Report")
        preview_button.setCursor(Qt.PointingHandCursor)
        preview_button.setStyleSheet(
            "QPushButton { font-size: 13px; font-weight: bold; color: #333333; background-color: #f0f0f0; "
            "border: 1px solid #cccccc; border-radius: 4px; padding: 8px 15px; }"
            "QPushButton:hover { background-color: #e0e0e0; border-color: #5c9aff; }"
            "QPushButton:pressed { background-color: #d0d0d0; }"
        )
        preview_button.setMinimumWidth(140)
        preview_button.setMinimumHeight(40)
        preview_button.clicked.connect(self.previewReport)
        buttons_layout.addWidget(preview_button)
        
        generate_button = QPushButton("Generate Report")
        generate_button.setObjectName("generate_report_button")  # For QSS styling
        generate_button.setIcon(get_icon("report"))
        generate_button.setCursor(Qt.PointingHandCursor)
        generate_button.setStyleSheet(
            "QPushButton { font-size: 13px; font-weight: bold; color: white; background-color: #4361ee; "
            "border: 1px solid #3f37c9; border-radius: 4px; padding: 8px 15px; }"
            "QPushButton:hover { background-color: #3f37c9; }"
            "QPushButton:pressed { background-color: #3730b5; }"
        )
        generate_button.setMinimumWidth(170)
        generate_button.setMinimumHeight(40)
        generate_button.clicked.connect(self.generateReport)
        buttons_layout.addWidget(generate_button)
        
        report_layout.addLayout(buttons_layout)
        
        # Previous reports section
        previous_frame = QFrame()
        previous_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px; margin-top: 15px; border: 1px solid #cccccc;")
        previous_layout = QVBoxLayout(previous_frame)
        
        # Title with count
        previous_title_layout = QHBoxLayout()
        previous_title = QLabel("Previous Reports")
        previous_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        previous_title.setStyleSheet("color: #0066cc; margin-bottom: 5px;")
        previous_count = QLabel("12 reports available")
        previous_count.setStyleSheet("color: #666666; font-size: 12px;")
        
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
        reports_table.setStyleSheet(
            "QTableWidget { border: 1px solid #dddddd; gridline-color: #dddddd; background-color: #ffffff; }"
            "QTableWidget::item { padding: 5px; }"
            "QHeaderView::section { background-color: #5c9aff; color: white; padding: 6px; font-weight: bold; }"
            "QTableWidget::item:selected { background-color: #e0e0ff; color: #000000; }"
        )
        reports_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Report Type column stretch
        reports_table.verticalHeader().setVisible(False)  # Hide row numbers
        reports_table.setMinimumHeight(200)  # Ensure the table has enough height
        
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
            action_layout.setContentsMargins(4, 2, 4, 2)
            action_layout.setSpacing(8)
            
            view_btn = QPushButton("View")
            view_btn.setFixedWidth(60)
            view_btn.setCursor(Qt.PointingHandCursor)
            view_btn.setStyleSheet(
                "QPushButton { font-size: 11px; color: #ffffff; background-color: #5c9aff; "
                "border: none; border-radius: 3px; padding: 4px 0px; }"
                "QPushButton:hover { background-color: #4361ee; }"
                "QPushButton:pressed { background-color: #3f37c9; }"
            )
            
            download_btn = QPushButton("Download")
            download_btn.setFixedWidth(80)
            download_btn.setCursor(Qt.PointingHandCursor)
            download_btn.setStyleSheet(
                "QPushButton { font-size: 11px; color: #333333; background-color: #f0f0f0; "
                "border: 1px solid #dddddd; border-radius: 3px; padding: 4px 0px; }"
                "QPushButton:hover { background-color: #e0e0e0; border-color: #5c9aff; }"
                "QPushButton:pressed { background-color: #d0d0d0; }"
            )
            
            action_layout.addWidget(view_btn)
            action_layout.addWidget(download_btn)
            
            reports_table.setCellWidget(i, 4, action_widget)
        
        previous_layout.addWidget(reports_table)
        
        # Add all sections to the main layout
        reports_layout.addWidget(header_frame)
        reports_layout.addWidget(report_frame)
        reports_layout.addWidget(previous_frame)

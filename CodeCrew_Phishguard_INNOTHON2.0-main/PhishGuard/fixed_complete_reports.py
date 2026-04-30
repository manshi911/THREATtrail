# # Add missing PyQt5 imports for widgets and utilities used in this file
# from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QLabel, QFont, QFrame, QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem, QHeaderView, QWidget, QMessageBox, QDialog)
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QColor

# def createReportsTab(self, parent_widget):
#         """Create the reports tab."""
#         reports_layout = QVBoxLayout(parent_widget)
#         reports_layout.setContentsMargins(15, 15, 15, 15)
#         reports_layout.setSpacing(15)
        
#         # Header with gradient
#         header_frame = QFrame()
#         header_frame.setStyleSheet(
#             "QFrame {background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5c9aff, stop:1 #8cb8ff); "
#             "border-radius: 8px; color: white; padding: 15px;}"
#         )
#         header_frame.setMinimumHeight(120)
#         header_layout = QVBoxLayout(header_frame)
        
#         header_title = QLabel("Threat Reports")
#         header_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
#         header_title.setStyleSheet("color: white;")
        
#         header_subtitle = QLabel(
#             "Generate detailed reports on email threats, analyze trends, and export data for further analysis."
#         )
#         header_subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
#         header_subtitle.setWordWrap(True)
        
#         header_layout.addWidget(header_title)
#         header_layout.addWidget(header_subtitle)
        
#         # Report generation section
#         report_frame = QFrame()
#         report_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 20px;")
#         report_frame.setMinimumHeight(350)  # Ensure minimum height for content
#         report_layout = QVBoxLayout(report_frame)
        
#         # Title
#         report_title = QLabel("Generate New Report")
#         report_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
#         report_title.setStyleSheet("color: #0066cc; margin-bottom: 10px;")
#         report_layout.addWidget(report_title)
        
#         # Description
#         report_description = QLabel("Select report options below and click 'Preview Report' to see a sample or 'Generate Report' to create the full report.")
#         report_description.setWordWrap(True)
#         report_description.setStyleSheet("color: #666; margin-bottom: 15px;")
#         report_layout.addWidget(report_description)
        
#         # Form layout for report options
#         form_layout = QFormLayout()
#         form_layout.setSpacing(15)
#         form_layout.setContentsMargins(20, 20, 20, 20)
#         form_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
#         form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
#         # Report type combo
#         report_type_label = QLabel("Report Type:")
#         report_type_label.setFont(QFont("Arial", 10))
#         report_type_label.setStyleSheet("color: #000000; background-color: transparent;")
        
#         self.report_type_combo = QComboBox()
#         self.report_type_combo.addItems([
#             "Threat Summary Report", 
#             "Department Risk Analysis", 
#             "Threat Trends Over Time",
#             "Risk Score Distribution",
#             "Email Source Analysis"
#         ])
#         self.report_type_combo.setMinimumWidth(250)
#         self.report_type_combo.setStyleSheet(
#             "QComboBox { color: #000000; font-size: 12px; font-family: Arial; background-color: white; border: 1px solid #ccc; padding: 2px; }"
#             "QComboBox::drop-down { border: none; }"
#             "QComboBox QAbstractItemView { color: #000000; background-color: white; selection-background-color: #5c9aff; font-size: 12px; font-family: Arial; border: 1px solid #ccc; }"
#             "QComboBox QAbstractItemView::item { color: #000000; background-color: white; padding: 3px; }"
#             "QComboBox QAbstractItemView::item:selected { color: white; background-color: #5c9aff; }"
#         )
#         form_layout.addRow(report_type_label, self.report_type_combo)
        
#         # Time period combo
#         time_period_label = QLabel("Time Period:")
#         time_period_label.setFont(QFont("Segoe UI", 10))
#         time_period_label.setStyleSheet("color: #333;")
        
#         self.time_period_combo = QComboBox()
#         self.time_period_combo.addItems([
#             "Last 7 Days",
#             "Last 30 Days",
#             "Last Quarter",
#             "Year to Date",
#             "Custom Period"
#         ])
#         self.time_period_combo.setMinimumWidth(250)
#         self.time_period_combo.setStyleSheet("QComboBox { color: #222; font-size: 14px; font-family: 'Segoe UI', Arial, sans-serif; } QComboBox QAbstractItemView { color: #222; background: #fff; font-size: 14px; font-family: 'Segoe UI', Arial, sans-serif; }")
#         form_layout.addRow(time_period_label, self.time_period_combo)
        
#         # Department filter
#         department_label = QLabel("Department:")
#         department_label.setFont(QFont("Segoe UI", 10))
#         department_label.setStyleSheet("color: #333;")
        
#         self.dept_filter = QComboBox()
#         self.dept_filter.addItems([
#             "All Departments",
#             "Finance",
#             "Human Resources",
#             "IT",
#             "Marketing",
#             "Sales",
#             "Operations"
#         ])
#         self.dept_filter.setMinimumWidth(250)
#         self.dept_filter.setStyleSheet("QComboBox { color: #222; font-size: 14px; font-family: 'Segoe UI', Arial, sans-serif; } QComboBox QAbstractItemView { color: #222; background: #fff; font-size: 14px; font-family: 'Segoe UI', Arial, sans-serif; }")
#         form_layout.addRow(department_label, self.dept_filter)
        
#         # Format combo
#         format_label = QLabel("Format:")
#         format_label.setFont(QFont("Segoe UI", 10))
#         format_label.setStyleSheet("color: #333;")
        
#         self.format_combo = QComboBox()
#         self.format_combo.addItems(["PDF", "HTML", "CSV", "Excel"])
#         self.format_combo.setMinimumWidth(250)
#         self.format_combo.setStyleSheet("QComboBox { color: #222; font-size: 14px; font-family: 'Segoe UI', Arial, sans-serif; } QComboBox QAbstractItemView { color: #222; background: #fff; font-size: 14px; font-family: 'Segoe UI', Arial, sans-serif; }")
#         form_layout.addRow(format_label, self.format_combo)
        
#         # Add form to layout
#         report_layout.addLayout(form_layout)
        
#         # Buttons layout
#         buttons_layout = QHBoxLayout()
#         buttons_layout.setSpacing(15)
#         buttons_layout.setContentsMargins(0, 15, 0, 0)
        
#         spacer = QWidget()
#         spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
#         buttons_layout.addWidget(spacer)
        
#         preview_button = QPushButton("Preview Report")
#         preview_button.setCursor(Qt.PointingHandCursor)
#         preview_button.setStyleSheet("font-size: 12px; padding: 8px 15px;")
#         preview_button.setMinimumWidth(120)
#         preview_button.clicked.connect(self.previewReport)
#         buttons_layout.addWidget(preview_button)
        
#         generate_button = QPushButton("Generate Report")
#         generate_button.setObjectName("generate_report_button")  # For QSS styling
#         generate_button.setIcon(get_icon("report"))
#         generate_button.setCursor(Qt.PointingHandCursor)
#         generate_button.setStyleSheet("font-size: 12px; padding: 8px 15px;")
#         generate_button.setMinimumWidth(150)
#         generate_button.clicked.connect(self.generateReport)
#         buttons_layout.addWidget(generate_button)
        
#         report_layout.addLayout(buttons_layout)
        
#         # Previous reports section
#         previous_frame = QFrame()
#         previous_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
#         previous_layout = QVBoxLayout(previous_frame)
        
#         # Title with count
#         previous_title_layout = QHBoxLayout()
#         previous_title = QLabel("Previous Reports")
#         previous_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
#         previous_count = QLabel("12 reports available")
        
#         previous_title_layout.addWidget(previous_title)
#         previous_title_layout.addStretch()
#         previous_title_layout.addWidget(previous_count)
        
#         previous_layout.addLayout(previous_title_layout)
        
#         # Previous reports table
#         reports_table = QTableWidget()
#         reports_table.setColumnCount(5)
#         reports_table.setHorizontalHeaderLabels([
#             "Date Generated", "Report Type", "Period", "Format", "Actions"
#         ])
        
#         # Configure table appearance
#         reports_table.setAlternatingRowColors(True)
#         reports_table.setEditTriggers(QTableWidget.NoEditTriggers)
#         reports_table.setSelectionBehavior(QTableWidget.SelectRows)
#         reports_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Report Type column stretch
#         reports_table.verticalHeader().setVisible(False)  # Hide row numbers
        
#         # Add some example data
#         reports_table.setRowCount(5)
        
#         # Example report 1
#         reports_table.setItem(0, 0, QTableWidgetItem("2025-05-09"))
#         reports_table.setItem(0, 1, QTableWidgetItem("Threat Summary Report"))
#         reports_table.setItem(0, 2, QTableWidgetItem("Last 7 Days"))
#         reports_table.setItem(0, 3, QTableWidgetItem("PDF"))
        
#         # Example report 2
#         reports_table.setItem(1, 0, QTableWidgetItem("2025-05-05"))
#         reports_table.setItem(1, 1, QTableWidgetItem("Department Risk Analysis"))
#         reports_table.setItem(1, 2, QTableWidgetItem("Last 30 Days"))
#         reports_table.setItem(1, 3, QTableWidgetItem("HTML"))
        
#         # Example report 3
#         reports_table.setItem(2, 0, QTableWidgetItem("2025-04-28"))
#         reports_table.setItem(2, 1, QTableWidgetItem("Threat Trends Over Time"))
#         reports_table.setItem(2, 2, QTableWidgetItem("Last Quarter"))
#         reports_table.setItem(2, 3, QTableWidgetItem("PDF"))
        
#         # Example report 4
#         reports_table.setItem(3, 0, QTableWidgetItem("2025-04-15"))
#         reports_table.setItem(3, 1, QTableWidgetItem("Risk Score Distribution"))
#         reports_table.setItem(3, 2, QTableWidgetItem("Year to Date"))
#         reports_table.setItem(3, 3, QTableWidgetItem("Excel"))
        
#         # Example report 5
#         reports_table.setItem(4, 0, QTableWidgetItem("2025-04-01"))
#         reports_table.setItem(4, 1, QTableWidgetItem("Email Source Analysis"))
#         reports_table.setItem(4, 2, QTableWidgetItem("Last 30 Days"))
#         reports_table.setItem(4, 3, QTableWidgetItem("CSV"))
        
#         # Add action buttons to each row
#         for i in range(5):
#             action_widget = QWidget()
#             action_layout = QHBoxLayout(action_widget)
#             action_layout.setContentsMargins(0, 0, 0, 0)
            
#             view_btn = QPushButton("View")
#             view_btn.setFixedWidth(60)
#             view_btn.setCursor(Qt.PointingHandCursor)
            
#             download_btn = QPushButton("Download")
#             download_btn.setFixedWidth(80)
#             download_btn.setCursor(Qt.PointingHandCursor)
            
#             action_layout.addWidget(view_btn)
#             action_layout.addWidget(download_btn)
            
#             reports_table.setCellWidget(i, 4, action_widget)
        
#         previous_layout.addWidget(reports_table)
        
#         # Add all sections to the main layout
#         reports_layout.addWidget(header_frame)
#         reports_layout.addWidget(report_frame)
#         reports_layout.addWidget(previous_frame)

#     def generateReport(self):
#         """Generate a report with the selected options."""
#         try:
#             # Get values from form inputs
#             report_type = self.report_type_combo.currentText()
#             time_period = self.time_period_combo.currentText()
#             department = self.dept_filter.currentText()
#             format_type = self.format_combo.currentText()
            
#             # Show generating message
#             self.statusBar.showMessage(f"Generating {report_type}...")
            
#             # In a real implementation, this would use the ReportGenerator to create the actual report
#             # For now, we'll just show a success message
#             QMessageBox.information(
#                 self, 
#                 "Report Generated", 
#                 f"The {report_type} has been generated in {format_type} format.\n\n"
#                 f"Time Period: {time_period}\n"
#                 f"Department: {department}"
#             )
            
#             self.statusBar.showMessage(f"Report generated successfully", 5000)
            
#         except Exception as e:
#             logger.error(f"Error generating report: {str(e)}")
#             QMessageBox.warning(self, "Generation Error", f"Could not generate report: {str(e)}")
#             self.statusBar.showMessage("Error generating report", 5000)

#     def previewReport(self):
#         """Preview the report with the selected options."""
#         try:
#             # Get values from form inputs
#             report_type = self.report_type_combo.currentText()
#             time_period = self.time_period_combo.currentText()
#             department = self.dept_filter.currentText()
#             format_type = self.format_combo.currentText()
            
#             # Create a preview dialog
#             preview_dialog = QDialog(self)
#             preview_dialog.setWindowTitle(f"Preview: {report_type}")
#             preview_dialog.setMinimumSize(800, 600)
            
#             # Dialog layout
#             dialog_layout = QVBoxLayout(preview_dialog)
            
#             # Header with report info
#             info_frame = QFrame()
#             info_frame.setStyleSheet(
#                 "background-color: #f0f4ff; border-radius: 8px; padding: 15px;"
#             )
#             info_layout = QVBoxLayout(info_frame)
            
#             # Report title
#             title_label = QLabel(report_type)
#             title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
#             info_layout.addWidget(title_label)
            
#             # Report details
#             details_text = f"Time Period: {time_period} | Department: {department} | Format: {format_type}"
#             details_label = QLabel(details_text)
#             details_label.setFont(QFont("Segoe UI", 10))
#             info_layout.addWidget(details_label)
            
#             date_label = QLabel(f"Report Date: {datetime.now().strftime('%Y-%m-%d')}")
#             date_label.setFont(QFont("Segoe UI", 10))
#             info_layout.addWidget(date_label)
            
#             # Add info frame to dialog
#             dialog_layout.addWidget(info_frame)
            
#             # Create a preview of the report content based on type
#             content_frame = QFrame()
#             content_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px;")
#             content_layout = QVBoxLayout(content_frame)
            
#             if report_type == "Threat Summary Report":
#                 self.createThreatSummaryPreview(content_layout)
#             elif report_type == "Department Risk Analysis":
#                 self.createDepartmentRiskPreview(content_layout)
#             elif report_type == "Threat Trends Over Time":
#                 self.createTrendPreview(content_layout)
#             elif report_type == "Risk Score Distribution":
#                 self.createRiskDistributionPreview(content_layout)
#             elif report_type == "Email Source Analysis":
#                 self.createSourceAnalysisPreview(content_layout)
            
#             # Add content frame to dialog
#             dialog_layout.addWidget(content_frame)
            
#             # Button to close the preview
#             close_button = QPushButton("Close Preview")
#             close_button.clicked.connect(preview_dialog.accept)
#             dialog_layout.addWidget(close_button)
            
#             # Show the dialog
#             preview_dialog.exec_()
            
#         except Exception as e:
#             logger.error(f"Error previewing report: {str(e)}")
#             QMessageBox.warning(self, "Preview Error", f"Could not preview report: {str(e)}")

#     def createThreatSummaryPreview(self, parent_layout):
#         """Create a preview of a threat summary report."""
#         # Title
#         section_title = QLabel("Threat Summary")
#         section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
#         parent_layout.addWidget(section_title)
        
#         # Statistics section
#         stats_frame = QFrame()
#         stats_frame.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; padding: 10px;")
#         stats_layout = QHBoxLayout(stats_frame)
        
#         # Create stat boxes
#         self.createStatBox(stats_layout, "Total Threats", "27", COLORS['primary'])
#         self.createStatBox(stats_layout, "High Risk", "8", COLORS['danger'])
#         self.createStatBox(stats_layout, "Medium Risk", "12", COLORS['warning'])
#         self.createStatBox(stats_layout, "Low Risk", "7", COLORS['success'])
        
#         parent_layout.addWidget(stats_frame)
        
#         # Threats table
#         table_title = QLabel("Recent Threats")
#         table_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
#         parent_layout.addWidget(table_title)
        
#         threats_table = QTableWidget()
#         threats_table.setColumnCount(5)
#         threats_table.setHorizontalHeaderLabels(["Date", "Sender", "Subject", "Risk Score", "Threat Type"])
#         threats_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)  # Subject column stretch
        
#         # Add sample data
#         sample_data = [
#             ["2025-05-10", "suspicious@example.com", "Urgent: Your account has been compromised", "85%", "Phishing"],
#             ["2025-05-10", "newsletter@unknown-domain.com", "Important Document Attached", "65%", "Suspicious Attachment"],
#             ["2025-05-09", "info@company-portal.net", "Update your password now", "40%", "Social Engineering"],
#             ["2025-05-09", "paypal-security@mail.tk", "Your payment was processed", "90%", "Phishing"],
#             ["2025-05-08", "hr-notification@domain.co", "Salary Adjustment Document", "55%", "Suspicious Link"]
#         ]
        
#         threats_table.setRowCount(len(sample_data))
        
#         for i, row in enumerate(sample_data):
#             threats_table.setItem(i, 0, QTableWidgetItem(row[0]))
#             threats_table.setItem(i, 1, QTableWidgetItem(row[1]))
#             threats_table.setItem(i, 2, QTableWidgetItem(row[2]))
            
#             risk_score = QTableWidgetItem(row[3])
#             score_value = int(row[3].replace("%", ""))
#             if score_value >= 80:
#                 risk_score.setForeground(QColor(COLORS['danger']))
#             elif score_value >= 50:
#                 risk_score.setForeground(QColor(COLORS['warning']))
#             else:
#                 risk_score.setForeground(QColor(COLORS['success']))
#             threats_table.setItem(i, 3, risk_score)
            
#             threats_table.setItem(i, 4, QTableWidgetItem(row[4]))
        
#         threats_table.setEditTriggers(QTableWidget.NoEditTriggers)
#         threats_table.setAlternatingRowColors(True)
#         parent_layout.addWidget(threats_table)

#     def createDepartmentRiskPreview(self, parent_layout):
#         """Create a preview of a department risk analysis report."""
#         # Title
#         section_title = QLabel("Department Risk Analysis")
#         section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
#         parent_layout.addWidget(section_title)
        
#         # Department statistics table
#         dept_table = QTableWidget()
#         dept_table.setColumnCount(4)
#         dept_table.setHorizontalHeaderLabels(["Department", "Threat Count", "Avg Risk Score", "Most Common Threat"])
        
#         # Sample department data
#         dept_data = [
#             ["Finance", "12", "78%", "Phishing"],
#             ["Human Resources", "8", "62%", "Social Engineering"],
#             ["IT", "4", "45%", "Malware"],
#             ["Marketing", "7", "58%", "Suspicious Links"],
#             ["Sales", "6", "67%", "Phishing"],
#             ["Operations", "5", "52%", "Suspicious Attachments"]
#         ]
        
#         dept_table.setRowCount(len(dept_data))
        
#         for i, row in enumerate(dept_data):
#             dept_table.setItem(i, 0, QTableWidgetItem(row[0]))
#             dept_table.setItem(i, 1, QTableWidgetItem(row[1]))
            
#             risk_score = QTableWidgetItem(row[2])
#             score_value = int(row[2].replace("%", ""))
#             if score_value >= 70:
#                 risk_score.setForeground(QColor(COLORS['danger']))
#             elif score_value >= 50:
#                 risk_score.setForeground(QColor(COLORS['warning']))
#             else:
#                 risk_score.setForeground(QColor(COLORS['success']))
#             dept_table.setItem(i, 2, risk_score)
            
#             dept_table.setItem(i, 3, QTableWidgetItem(row[3]))
        
#         dept_table.setEditTriggers(QTableWidget.NoEditTriggers)
#         dept_table.setAlternatingRowColors(True)
#         dept_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
#         parent_layout.addWidget(dept_table)
        
#         # Add a note
#         note_label = QLabel("This report shows risk analysis for each department based on email threats detected in the selected time period.")
#         note_label.setWordWrap(True)
#         note_label.setStyleSheet("color: #6c757d; font-style: italic;")
#         parent_layout.addWidget(note_label)

#     def createTrendPreview(self, parent_layout):
#         """Create a preview of a threat trends over time report."""
#         # Title
#         section_title = QLabel("Threat Trends Over Time")
#         section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
#         parent_layout.addWidget(section_title)
        
#         description = QLabel("This report shows the trend of email threats over the selected time period.")
#         description.setWordWrap(True)
#         parent_layout.addWidget(description)
        
#         # Placeholder for chart (in a real implementation, this would be a matplotlib chart)
#         chart_placeholder = QLabel("[ Chart: Threat trend over time would be displayed here ]")
#         chart_placeholder.setAlignment(Qt.AlignCenter)
#         chart_placeholder.setStyleSheet("background-color: #f8f9fa; padding: 40px; font-style: italic; color: #6c757d;")
#         chart_placeholder.setMinimumHeight(200)
#         parent_layout.addWidget(chart_placeholder)
        
#         # Trend data table
#         trend_table = QTableWidget()
#         trend_table.setColumnCount(4)
#         trend_table.setHorizontalHeaderLabels(["Date", "Total Threats", "High Risk", "Medium Risk"])
        
#         # Sample trend data
#         trend_data = [
#             ["2025-05-10", "6", "2", "3"],
#             ["2025-05-09", "8", "3", "4"],
#             ["2025-05-08", "5", "1", "2"],
#             ["2025-05-07", "4", "1", "1"],
#             ["2025-05-06", "7", "2", "3"],
#             ["2025-05-05", "9", "3", "4"],
#             ["2025-05-04", "4", "1", "2"]
#         ]
        
#         trend_table.setRowCount(len(trend_data))
        
#         for i, row in enumerate(trend_data):
#             for j, cell in enumerate(row):
#                 trend_table.setItem(i, j, QTableWidgetItem(cell))
        
#         trend_table.setEditTriggers(QTableWidget.NoEditTriggers)
#         trend_table.setAlternatingRowColors(True)
        
#         parent_layout.addWidget(trend_table)

#     def createRiskDistributionPreview(self, parent_layout):
#         """Create a preview of a risk score distribution report."""
#         # Title
#         section_title = QLabel("Risk Score Distribution")
#         section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
#         parent_layout.addWidget(section_title)
        
#         description = QLabel("This report shows the distribution of risk scores across all detected threats.")
#         description.setWordWrap(True)
#         parent_layout.addWidget(description)
        
#         # Placeholder for chart
#         chart_placeholder = QLabel("[ Chart: Risk score distribution would be displayed here ]")
#         chart_placeholder.setAlignment(Qt.AlignCenter)
#         chart_placeholder.setStyleSheet("background-color: #f8f9fa; padding: 40px; font-style: italic; color: #6c757d;")
#         chart_placeholder.setMinimumHeight(200)
#         parent_layout.addWidget(chart_placeholder)
        
#         # Risk distribution table
#         risk_table = QTableWidget()
#         risk_table.setColumnCount(3)
#         risk_table.setHorizontalHeaderLabels(["Risk Level", "Count", "Percentage"])
        
#         # Sample risk data
#         risk_data = [
#             ["High Risk (80-100%)", "8", "30%"],
#             ["Medium Risk (50-79%)", "12", "44%"],
#             ["Low Risk (0-49%)", "7", "26%"]
#         ]
        
#         risk_table.setRowCount(len(risk_data))
        
#         for i, row in enumerate(risk_data):
#             risk_level = QTableWidgetItem(row[0])
#             if i == 0:
#                 risk_level.setForeground(QColor(COLORS['danger']))
#             elif i == 1:
#                 risk_level.setForeground(QColor(COLORS['warning']))
#             else:
#                 risk_level.setForeground(QColor(COLORS['success']))
            
#             risk_table.setItem(i, 0, risk_level)
#             risk_table.setItem(i, 1, QTableWidgetItem(row[1]))
#             risk_table.setItem(i, 2, QTableWidgetItem(row[2]))
        
#         risk_table.setEditTriggers(QTableWidget.NoEditTriggers)
#         risk_table.setAlternatingRowColors(True)
#         risk_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
#         parent_layout.addWidget(risk_table)

#     def createSourceAnalysisPreview(self, parent_layout):
#         """Create a preview of an email source analysis report."""
#         # Title
#         section_title = QLabel("Email Source Analysis")
#         section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
#         parent_layout.addWidget(section_title)
        
#         description = QLabel("This report analyzes the sources of suspicious emails, including domains and geographic regions.")
#         description.setWordWrap(True)
#         parent_layout.addWidget(description)
        
#         # Placeholder for chart
#         chart_placeholder = QLabel("[ Chart: Email source distribution would be displayed here ]")
#         chart_placeholder.setAlignment(Qt.AlignCenter)
#         chart_placeholder.setStyleSheet("background-color: #f8f9fa; padding: 40px; font-style: italic; color: #6c757d;")
#         chart_placeholder.setMinimumHeight(200)
#         parent_layout.addWidget(chart_placeholder)
        
#         # Source analysis table
#         source_table = QTableWidget()
#         source_table.setColumnCount(3)
#         source_table.setHorizontalHeaderLabels(["Domain/Source", "Threat Count", "Common Threat Type"])
        
#         # Sample source data
#         source_data = [
#             ["mail.suspicious-domain.com", "5", "Phishing"],
#             ["newsletter-service.co", "3", "Suspicious Links"],
#             ["secure-alerts.net", "4", "Social Engineering"],
#             ["account-verify.info", "3", "Phishing"],
#             ["docshare.xyz", "2", "Malware"],
#             ["Other Sources", "10", "Various"]
#         ]
        
#         source_table.setRowCount(len(source_data))
        
#         for i, row in enumerate(source_data):
#             for j, cell in enumerate(row):
#                 source_table.setItem(i, j, QTableWidgetItem(cell))
        
#         source_table.setEditTriggers(QTableWidget.NoEditTriggers)
#         source_table.setAlternatingRowColors(True)
#         source_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
#         parent_layout.addWidget(source_table)

#     def createStatBox(self, parent_layout, title, value, color):
#         """Create a statistic box for the report preview."""
#         stat_frame = QFrame()
#         stat_frame.setStyleSheet(f"background-color: white; border-radius: 8px; border: 1px solid {color};")
#         stat_layout = QVBoxLayout(stat_frame)
        
#         # Title
#         title_label = QLabel(title)
#         title_label.setAlignment(Qt.AlignCenter)
#         title_label.setStyleSheet("color: #6c757d;")
        
#         # Value
#         value_label = QLabel(value)
#         value_label.setAlignment(Qt.AlignCenter)
#         value_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
#         value_label.setStyleSheet(f"color: {color};")
        
#         stat_layout.addWidget(title_label)
#         stat_layout.addWidget(value_label)
        
#         parent_layout.addWidget(stat_frame)

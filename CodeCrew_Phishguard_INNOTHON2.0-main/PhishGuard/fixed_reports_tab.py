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
        report_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 20px;")
        report_frame.setMinimumHeight(350)  # Ensure minimum height for content
        report_layout = QVBoxLayout(report_frame)
        
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
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # Report type combo
        report_type_label = QLabel("Report Type:")
        report_type_label.setFont(QFont("Segoe UI", 10))
        report_type_label.setStyleSheet("color: #333;")
        
        self.report_type_combo = QComboBox()
        self.report_type_combo.addItems([
            "Threat Summary Report", 
            "Department Risk Analysis", 
            "Threat Trends Over Time",
            "Risk Score Distribution",
            "Email Source Analysis"
        ])
        self.report_type_combo.setMinimumWidth(250)
        form_layout.addRow(report_type_label, self.report_type_combo)
        
        # Time period combo
        time_period_label = QLabel("Time Period:")
        time_period_label.setFont(QFont("Segoe UI", 10))
        time_period_label.setStyleSheet("color: #333;")
        
        self.time_period_combo = QComboBox()
        self.time_period_combo.addItems([
            "Last 7 Days",
            "Last 30 Days",
            "Last Quarter",
            "Year to Date",
            "Custom Period"
        ])
        self.time_period_combo.setMinimumWidth(250)
        form_layout.addRow(time_period_label, self.time_period_combo)
        
        # Department filter
        department_label = QLabel("Department:")
        department_label.setFont(QFont("Segoe UI", 10))
        department_label.setStyleSheet("color: #333;")
        
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
        form_layout.addRow(department_label, self.dept_filter)
        
        # Format combo
        format_label = QLabel("Format:")
        format_label.setFont(QFont("Segoe UI", 10))
        format_label.setStyleSheet("color: #333;")
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PDF", "HTML", "CSV", "Excel"])
        self.format_combo.setMinimumWidth(250)
        form_layout.addRow(format_label, self.format_combo)
        
        # Add form to layout
        report_layout.addLayout(form_layout)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(0, 15, 0, 0)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        buttons_layout.addWidget(spacer)
        
        preview_button = QPushButton("Preview Report")
        preview_button.setCursor(Qt.PointingHandCursor)
        preview_button.setStyleSheet("font-size: 12px; padding: 8px 15px;")
        preview_button.setMinimumWidth(120)
        preview_button.clicked.connect(self.previewReport)
        buttons_layout.addWidget(preview_button)
        
        generate_button = QPushButton("Generate Report")
        generate_button.setObjectName("generate_report_button")  # For QSS styling
        generate_button.setIcon(get_icon("report"))
        generate_button.setCursor(Qt.PointingHandCursor)
        generate_button.setStyleSheet("font-size: 12px; padding: 8px 15px;")
        generate_button.setMinimumWidth(150)
        generate_button.clicked.connect(self.generateReport)
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

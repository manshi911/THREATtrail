    def createSourceAnalysisPreview(self, parent_layout):
        """Create a preview of an email source analysis report."""
        # Title
        section_title = QLabel("Email Source Analysis")
        section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        parent_layout.addWidget(section_title)
        
        description = QLabel("This report analyzes the sources of suspicious emails, including domains and geographic regions.")
        description.setWordWrap(True)
        parent_layout.addWidget(description)
        
        # Placeholder for chart
        chart_placeholder = QLabel("[ Chart: Email source distribution would be displayed here ]")
        chart_placeholder.setAlignment(Qt.AlignCenter)
        chart_placeholder.setStyleSheet("background-color: #f8f9fa; padding: 40px; font-style: italic; color: #6c757d;")
        chart_placeholder.setMinimumHeight(200)
        parent_layout.addWidget(chart_placeholder)
        
        # Source analysis table
        source_table = QTableWidget()
        source_table.setColumnCount(3)
        source_table.setHorizontalHeaderLabels(["Domain/Source", "Threat Count", "Common Threat Type"])
        
        # Sample source data
        source_data = [
            ["mail.suspicious-domain.com", "5", "Phishing"],
            ["newsletter-service.co", "3", "Suspicious Links"],
            ["secure-alerts.net", "4", "Social Engineering"],
            ["account-verify.info", "3", "Phishing"],
            ["docshare.xyz", "2", "Malware"],
            ["Other Sources", "10", "Various"]
        ]
        
        source_table.setRowCount(len(source_data))
        
        for i, row in enumerate(source_data):
            for j, cell in enumerate(row):
                source_table.setItem(i, j, QTableWidgetItem(cell))
        
        source_table.setEditTriggers(QTableWidget.NoEditTriggers)
        source_table.setAlternatingRowColors(True)
        source_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        parent_layout.addWidget(source_table)
    
    def createStatBox(self, parent_layout, title, value, color):
        """Create a statistic box for the report preview."""
        stat_frame = QFrame()
        stat_frame.setStyleSheet(f"background-color: white; border-radius: 8px; border: 1px solid {color};")
        stat_layout = QVBoxLayout(stat_frame)
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #6c757d;")
        
        # Value
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        
        stat_layout.addWidget(title_label)
        stat_layout.addWidget(value_label)
        
        parent_layout.addWidget(stat_frame)
    
    def generateReport(self):
        """Generate a report with the selected options."""
        try:
            # Get values from form inputs
            report_type = self.report_type_combo.currentText()
            time_period = self.time_period_combo.currentText()
            department = self.dept_filter.currentText()
            format_type = self.format_combo.currentText()
            
            # Show generating message
            self.statusBar.showMessage(f"Generating {report_type}...")
            
            # In a real implementation, this would use the ReportGenerator to create the actual report
            # For now, we'll just show a success message
            QMessageBox.information(
                self, 
                "Report Generated", 
                f"The {report_type} has been generated in {format_type} format.\n\n"
                f"Time Period: {time_period}\n"
                f"Department: {department}"
            )
            
            self.statusBar.showMessage(f"Report generated successfully", 5000)
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            QMessageBox.warning(self, "Generation Error", f"Could not generate report: {str(e)}")
            self.statusBar.showMessage("Error generating report", 5000)

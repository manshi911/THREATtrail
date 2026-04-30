    def createRiskDistributionPreview(self, parent_layout):
        """Create a preview of a risk score distribution report."""
        # Title
        section_title = QLabel("Risk Score Distribution")
        section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        parent_layout.addWidget(section_title)
        
        description = QLabel("This report shows the distribution of risk scores across all detected threats.")
        description.setWordWrap(True)
        parent_layout.addWidget(description)
        
        # Placeholder for chart
        chart_placeholder = QLabel("[ Chart: Risk score distribution would be displayed here ]")
        chart_placeholder.setAlignment(Qt.AlignCenter)
        chart_placeholder.setStyleSheet("background-color: #f8f9fa; padding: 40px; font-style: italic; color: #6c757d;")
        chart_placeholder.setMinimumHeight(200)
        parent_layout.addWidget(chart_placeholder)
        
        # Risk distribution table
        risk_table = QTableWidget()
        risk_table.setColumnCount(3)
        risk_table.setHorizontalHeaderLabels(["Risk Level", "Count", "Percentage"])
        
        # Sample risk data
        risk_data = [
            ["High Risk (80-100%)", "8", "30%"],
            ["Medium Risk (50-79%)", "12", "44%"],
            ["Low Risk (0-49%)", "7", "26%"]
        ]
        
        risk_table.setRowCount(len(risk_data))
        
        for i, row in enumerate(risk_data):
            risk_level = QTableWidgetItem(row[0])
            if i == 0:
                risk_level.setForeground(QColor(COLORS['danger']))
            elif i == 1:
                risk_level.setForeground(QColor(COLORS['warning']))
            else:
                risk_level.setForeground(QColor(COLORS['success']))
            
            risk_table.setItem(i, 0, risk_level)
            risk_table.setItem(i, 1, QTableWidgetItem(row[1]))
            risk_table.setItem(i, 2, QTableWidgetItem(row[2]))
        
        risk_table.setEditTriggers(QTableWidget.NoEditTriggers)
        risk_table.setAlternatingRowColors(True)
        risk_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        parent_layout.addWidget(risk_table)

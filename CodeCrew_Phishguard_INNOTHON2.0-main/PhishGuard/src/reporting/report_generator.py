"""
Report Generation Module

This module handles the generation of department-wise phishing threat reports.
Reports can be generated in various formats including HTML, PDF, and CSV.
"""

import os
import logging
import json
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# Configure logging
logger = logging.getLogger('reporting')

class ReportGenerator:
    """
    Report generation class for PhishGuard.
    
    This class handles the generation of department-wise phishing threat reports
    based on data logged in the database.
    """
    
    def __init__(self, data_logger, report_dir='reports'):
        """
        Initialize the report generator.
        
        Args:
            data_logger: DataLogger instance to retrieve threat data
            report_dir (str): Directory to store generated reports
        """
        self.data_logger = data_logger
        self.report_dir = report_dir
        
        # Ensure the report directory exists
        os.makedirs(report_dir, exist_ok=True)
        
        # Create subdirectories for different report types
        os.makedirs(os.path.join(report_dir, 'html'), exist_ok=True)
        os.makedirs(os.path.join(report_dir, 'csv'), exist_ok=True)
        os.makedirs(os.path.join(report_dir, 'pdf'), exist_ok=True)
        
        # Load email configuration for report distribution
        self.email_config = self._load_email_config()
        
        # Set up color scheme for reports
        self.colors = {
            'primary': '#0066cc',
            'secondary': '#5c9aff',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'light': '#f8f9fa',
            'dark': '#343a40',
        }
    
    def _load_email_config(self, config_path='config.ini'):
        """Load email configuration for report distribution."""
        # This would normally load from config.ini
        # For simplicity, we're returning a default configuration
        return {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': 'phishguard@example.com',
            'use_app_password': True
        }
    
    def generate_daily_reports(self, send_email=False):
        """
        Generate daily reports for all departments.
        
        Args:
            send_email (bool): Whether to send reports via email
            
        Returns:
            dict: Dictionary mapping department names to report file paths
        """
        logger.info("Generating daily department reports")
        
        # Get department stats for the last 24 hours
        stats = self.data_logger.get_department_stats(days=1)
        
        if not stats:
            logger.info("No threat data available for reports")
            return {}
        
        # Date for the report
        today = datetime.now()
        report_date = today.strftime("%Y-%m-%d")
        
        # Generate report for each department
        report_files = {}
        
        for department in stats.keys():
            # Get detailed threat data for this department
            threats = self.data_logger.get_threats(department=department, days=1)
            
            if not threats:
                logger.info(f"No threats found for {department} department, skipping report")
                continue
            
            # Generate the reports in different formats
            html_path = self._generate_html_report(department, threats, stats[department], report_date)
            csv_path = self._generate_csv_report(department, threats, report_date)
            
            # Store report paths
            report_files[department] = {
                'html': html_path,
                'csv': csv_path
            }
            
            logger.info(f"Generated daily report for {department} department")
            
            # Send email report if requested
            if send_email:
                self._send_email_report(department, html_path, csv_path, report_date)
        
        return report_files
    
    def _generate_html_report(self, department, threats, stats, report_date):
        """
        Generate an HTML report for a department.
        
        Args:
            department (str): Department name
            threats (list): List of threat dictionaries
            stats (dict): Department statistics
            report_date (str): Date of the report
            
        Returns:
            str: Path to the generated HTML report
        """
        # Create the file path
        file_name = f"{department.lower().replace(' ', '_')}_{report_date}.html"
        file_path = os.path.join(self.report_dir, 'html', file_name)
        
        # Generate threat type distribution chart
        chart_path = self._generate_threat_distribution_chart(threats, department, report_date)
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PhishGuard Daily Report - {department}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    background: white;
                    padding: 20px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: {self.colors['primary']};
                    color: white;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-radius: 5px;
                }}
                h1, h2, h3 {{
                    margin-top: 0;
                    color: {self.colors['dark']};
                }}
                .header h1 {{
                    color: white;
                    margin: 0;
                }}
                .summary {{
                    background-color: {self.colors['light']};
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .summary-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-top: 15px;
                }}
                .summary-item {{
                    background: white;
                    padding: 15px;
                    border-radius: 5px;
                    box-shadow: 0 0 5px rgba(0,0,0,0.05);
                    text-align: center;
                }}
                .summary-item h3 {{
                    font-size: 24px;
                    margin: 0;
                }}
                .summary-item p {{
                    margin: 5px 0 0;
                    color: #666;
                }}
                .chart {{
                    margin: 20px 0;
                    text-align: center;
                }}
                .chart img {{
                    max-width: 100%;
                    height: auto;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px 12px;
                    text-align: left;
                }}
                th {{
                    background-color: {self.colors['secondary']};
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                .risk-high {{
                    background-color: {self.colors['danger']};
                    color: white;
                    padding: 3px 8px;
                    border-radius: 3px;
                }}
                .risk-medium {{
                    background-color: {self.colors['warning']};
                    color: #333;
                    padding: 3px 8px;
                    border-radius: 3px;
                }}
                .risk-low {{
                    background-color: {self.colors['success']};
                    color: white;
                    padding: 3px 8px;
                    border-radius: 3px;
                }}
                .footer {{
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    text-align: center;
                    font-size: 0.9em;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>PhishGuard Daily Report - {department}</h1>
                    <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
                
                <div class="summary">
                    <h2>Summary</h2>
                    <div class="summary-grid">
                        <div class="summary-item">
                            <p>Total Threats</p>
                            <h3>{stats['threat_count']}</h3>
                        </div>
                        <div class="summary-item">
                            <p>Average Risk Score</p>
                            <h3>{stats['avg_risk_score']}%</h3>
                        </div>
                        <div class="summary-item">
                            <p>Highest Risk Score</p>
                            <h3>{stats['max_risk_score']}%</h3>
                        </div>
                        <div class="summary-item">
                            <p>Unique Senders</p>
                            <h3>{stats['unique_senders']}</h3>
                        </div>
                    </div>
                </div>
                
                <div class="chart">
                    <h2>Threat Distribution</h2>
                    <img src="{os.path.basename(chart_path)}" alt="Threat Distribution">
                </div>
                
                <h2>Detailed Threats</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Sender</th>
                            <th>Subject</th>
                            <th>Risk Score</th>
                            <th>Threat Type</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add rows for each threat
        for threat in threats:
            # Format the timestamp
            timestamp = datetime.fromisoformat(threat['timestamp']).strftime("%H:%M:%S")
            
            # Determine risk level class
            risk_score = threat['risk_score']
            if risk_score >= 80:
                risk_class = "risk-high"
            elif risk_score >= 60:
                risk_class = "risk-medium"
            else:
                risk_class = "risk-low"
            
            # Format the threat type
            threat_type = threat['threat_type'].replace('_', ' ').title()
            
            # Add the table row
            html_content += f"""
                        <tr>
                            <td>{timestamp}</td>
                            <td>{threat['sender']}</td>
                            <td>{threat['subject']}</td>
                            <td><span class="{risk_class}">{risk_score:.1f}%</span></td>
                            <td>{threat_type}</td>
                        </tr>
            """
        
        # Complete the HTML
        html_content += """
                    </tbody>
                </table>
                
                <div class="footer">
                    <p>This report was automatically generated by PhishGuard.</p>
                    <p>If you have questions about this report, please contact your IT department.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Write the HTML to the file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Generated HTML report: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {str(e)}")
            return None
    
    def _generate_csv_report(self, department, threats, report_date):
        """
        Generate a CSV report for a department.
        
        Args:
            department (str): Department name
            threats (list): List of threat dictionaries
            report_date (str): Date of the report
            
        Returns:
            str: Path to the generated CSV report
        """
        # Create the file path
        file_name = f"{department.lower().replace(' ', '_')}_{report_date}.csv"
        file_path = os.path.join(self.report_dir, 'csv', file_name)
        
        # Write the CSV file
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header row
                writer.writerow([
                    'ID', 'Timestamp', 'Sender', 'Recipient', 'Subject',
                    'Risk Score', 'Threat Type', 'Indicators'
                ])
                
                # Write data rows
                for threat in threats:
                    # Convert indicators list to string
                    indicators_str = ', '.join(threat['indicators'])
                    
                    writer.writerow([
                        threat['id'],
                        threat['timestamp'],
                        threat['sender'],
                        threat['recipient'],
                        threat['subject'],
                        f"{threat['risk_score']:.1f}",
                        threat['threat_type'],
                        indicators_str
                    ])
            
            logger.info(f"Generated CSV report: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error generating CSV report: {str(e)}")
            return None
    
    def _generate_threat_distribution_chart(self, threats, department, report_date):
        """
        Generate a chart showing the distribution of threat types.
        
        Args:
            threats (list): List of threat dictionaries
            department (str): Department name
            report_date (str): Date of the report
            
        Returns:
            str: Path to the generated chart image
        """
        # Create the directory for charts if it doesn't exist
        charts_dir = os.path.join(self.report_dir, 'html', 'charts')
        os.makedirs(charts_dir, exist_ok=True)
        
        # Create the file path
        file_name = f"chart_{department.lower().replace(' ', '_')}_{report_date}.png"
        file_path = os.path.join(charts_dir, file_name)
        
        try:
            # Count occurrences of each threat type
            threat_types = {}
            for threat in threats:
                threat_type = threat['threat_type'].replace('_', ' ').title()
                threat_types[threat_type] = threat_types.get(threat_type, 0) + 1
            
            # Sort by count
            sorted_types = sorted(threat_types.items(), key=lambda x: x[1], reverse=True)
            
            # Extract labels and values
            labels = [item[0] for item in sorted_types]
            values = [item[1] for item in sorted_types]
            
            # Create the chart
            plt.figure(figsize=(10, 6))
            
            # Define custom colormap
            colors = [self.colors['danger'], self.colors['warning'], self.colors['primary']]
            n_bins = len(labels)
            custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=n_bins)
            
            # Create the bar chart
            bars = plt.bar(labels, values, color=custom_cmap(np.linspace(0, 1, len(labels))))
            
            plt.title('Phishing Threat Types Distribution', fontsize=16)
            plt.xlabel('Threat Type', fontsize=12)
            plt.ylabel('Number of Threats', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=10)
            
            # Save the chart
            plt.savefig(file_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Generated threat distribution chart: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error generating threat distribution chart: {str(e)}")
            return None
    
    def _send_email_report(self, department, html_path, csv_path, report_date):
        """
        Send the generated reports via email.
        
        Args:
            department (str): Department name
            html_path (str): Path to the HTML report
            csv_path (str): Path to the CSV report
            report_date (str): Date of the report
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        # In a real implementation, this would send emails to department contacts
        logger.info(f"Email distribution functionality not fully implemented")
        logger.info(f"Would send report for {department} department via email")
        
        # This is a placeholder for the actual email sending functionality
        return True
    
    def generate_weekly_summary(self):
        """
        Generate a weekly summary report across all departments.
        
        Returns:
            str: Path to the generated report
        """
        logger.info("Generating weekly summary report")
        
        # Get data for the last 7 days
        stats = self.data_logger.get_department_stats(days=7)
        
        if not stats:
            logger.info("No threat data available for weekly summary")
            return None
        
        # Date range for the report
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        date_range = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        
        # TODO: Implement weekly summary report generation
        
        logger.info("Weekly summary report generation not fully implemented")
        return None


# Example usage
if __name__ == "__main__":
    # This module requires the DataLogger to be instantiated
    # It's only for demonstration, so we're not actually creating reports here
    print("Report Generator module loaded")
    print("Use this module with a DataLogger instance to generate reports")

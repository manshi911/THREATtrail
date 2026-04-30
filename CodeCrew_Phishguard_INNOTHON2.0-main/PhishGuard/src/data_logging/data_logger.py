"""
Data Logging Module

This module handles the logging of detected phishing threats to a SQLite database
and provides functionality for retrieving threat logs for reporting.
"""

import sqlite3
import os
import json
import logging
from datetime import datetime
import uuid

# Configure logging
logger = logging.getLogger('data_logging')

class DataLogger:
    """
    Data logging class for PhishGuard.
    
    This class handles logging of detected phishing threats to a SQLite database
    and provides functions for retrieving and analyzing logged threats.
    """
    
    def __init__(self, db_path='data/phishguard.db'):
        """
        Initialize the data logger with the specified database path.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        # Ensure the database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._initialize_db()
        
        # Load department mapping if available
        self.department_mapping = self._load_department_mapping()
    
    def _initialize_db(self):
        """Initialize the database schema if it doesn't exist."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Create tables if they don't exist
            
            # Threats table for storing detected threats
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS threats (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                email_id TEXT,
                sender TEXT,
                recipient TEXT,
                subject TEXT,
                risk_score REAL,
                threat_type TEXT,
                indicators TEXT,
                department TEXT,
                action_taken TEXT,
                reported BOOLEAN DEFAULT 0
            )
            ''')
            
            # Departments table for organizing threats by department
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE,
                email_pattern TEXT,
                contact_person TEXT,
                report_frequency TEXT DEFAULT 'daily'
            )
            ''')
            
            # Reports table for tracking generated reports
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                department_id TEXT,
                report_type TEXT,
                threat_count INTEGER,
                file_path TEXT,
                FOREIGN KEY (department_id) REFERENCES departments (id)
            )
            ''')
            
            self.conn.commit()
            logger.info("Database initialized successfully")
            
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {str(e)}")
            if self.conn:
                self.conn.close()
                self.conn = None
    
    def _load_department_mapping(self, filepath='data/departments.json'):
        """
        Load department mapping from JSON file.
        
        Args:
            filepath (str): Path to the departments JSON file
            
        Returns:
            dict: Department mapping data
        """
        mapping = {}
        
        if not os.path.exists(filepath):
            # Create default department mapping
            default_mapping = {
                "departments": [
                    {
                        "id": str(uuid.uuid4()),
                        "name": "IT Department",
                        "email_pattern": "it@|tech@|support@",
                        "contact_person": "IT Manager"
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "name": "Finance",
                        "email_pattern": "finance@|accounting@|payroll@",
                        "contact_person": "Finance Director"
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "name": "Human Resources",
                        "email_pattern": "hr@|recruitment@|people@",
                        "contact_person": "HR Manager"
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "name": "Executive",
                        "email_pattern": "ceo@|cfo@|cto@|president@|director@",
                        "contact_person": "Executive Assistant"
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "name": "Sales",
                        "email_pattern": "sales@|marketing@|crm@",
                        "contact_person": "Sales Manager"
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "name": "Other",
                        "email_pattern": ".*",  # Catch-all pattern
                        "contact_person": "IT Support"
                    }
                ]
            }
            
            # Save default mapping
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(default_mapping, f, indent=4)
            
            # Insert departments into database
            if self.conn:
                try:
                    for dept in default_mapping["departments"]:
                        self.cursor.execute(
                            "INSERT OR IGNORE INTO departments (id, name, email_pattern, contact_person) VALUES (?, ?, ?, ?)",
                            (dept["id"], dept["name"], dept["email_pattern"], dept["contact_person"])
                        )
                    self.conn.commit()
                except sqlite3.Error as e:
                    logger.error(f"Error inserting default departments: {str(e)}")
            
            mapping = default_mapping
        else:
            try:
                with open(filepath, 'r') as f:
                    mapping = json.load(f)
            except Exception as e:
                logger.error(f"Error loading department mapping: {str(e)}")
                # Return empty mapping in case of error
                mapping = {"departments": []}
        
        return mapping
    
    def log_threat(self, email_data, risk_score, threat_type, indicators, action_taken="alert_shown"):
        """
        Log a detected phishing threat to the database.
        
        Args:
            email_data (dict): Email information
            risk_score (float): Risk score (0-100)
            threat_type (str): Type of threat detected
            indicators (list): List of detected indicators
            action_taken (str): Action taken (default: "alert_shown")
            
        Returns:
            str: ID of the logged threat, or None if logging failed
        """
        if not self.conn:
            self._initialize_db()
            
        if not self.conn:
            logger.error("Cannot log threat: Database connection failed")
            return None
        
        try:
            # Generate a unique ID for the threat
            threat_id = str(uuid.uuid4())
            
            # Determine the department based on recipient email
            department = self._determine_department(email_data.get('to', ''))
            
            # Convert indicators list to JSON string
            indicators_json = json.dumps(indicators)
            
            # Insert threat into database
            self.cursor.execute(
                '''
                INSERT INTO threats 
                (id, timestamp, email_id, sender, recipient, subject, risk_score, 
                threat_type, indicators, department, action_taken)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    threat_id,
                    datetime.now().isoformat(),
                    email_data.get('id', ''),
                    email_data.get('from', ''),
                    email_data.get('to', ''),
                    email_data.get('subject', ''),
                    risk_score,
                    threat_type,
                    indicators_json,
                    department,
                    action_taken
                )
            )
            
            self.conn.commit()
            logger.info(f"Threat logged successfully: {threat_id}")
            
            return threat_id
            
        except sqlite3.Error as e:
            logger.error(f"Error logging threat: {str(e)}")
            return None
    
    def _determine_department(self, recipient_email):
        """
        Determine the department based on the recipient's email.
        
        Args:
            recipient_email (str): Recipient's email address
            
        Returns:
            str: Department name
        """
        if not recipient_email:
            return "Other"
        
        # Default department
        department = "Other"
        
        # Check against department patterns
        for dept in self.department_mapping.get("departments", []):
            pattern = dept.get("email_pattern", "")
            if pattern and any(p in recipient_email.lower() for p in pattern.split('|')):
                department = dept.get("name", "Other")
                break
        
        return department
    
    def get_threats(self, department=None, days=1, min_risk_score=0):
        """
        Retrieve logged threats from the database.
        
        Args:
            department (str): Filter threats by department (optional)
            days (int): Number of days to look back (default: 1)
            min_risk_score (float): Minimum risk score to include (default: 0)
            
        Returns:
            list: List of threat dictionaries
        """
        if not self.conn:
            self._initialize_db()
            
        if not self.conn:
            logger.error("Cannot get threats: Database connection failed")
            return []
        
        try:
            # Build the SQL query
            query = '''
            SELECT id, timestamp, sender, recipient, subject, risk_score, threat_type, indicators, department, action_taken
            FROM threats
            WHERE datetime(timestamp) >= datetime('now', ?)
            AND risk_score >= ?
            '''
            
            params = (f'-{days} days', min_risk_score)
            
            # Add department filter if specified
            if department:
                query += ' AND department = ?'
                params = params + (department,)
            
            # Execute the query
            self.cursor.execute(query, params)
            
            # Process the results
            threats = []
            for row in self.cursor.fetchall():
                # Parse the indicators JSON
                try:
                    indicators = json.loads(row[7])
                except:
                    indicators = []
                
                # Create threat dictionary
                threat = {
                    'id': row[0],
                    'timestamp': row[1],
                    'sender': row[2],
                    'recipient': row[3],
                    'subject': row[4],
                    'risk_score': row[5],
                    'threat_type': row[6],
                    'indicators': indicators,
                    'department': row[8],
                    'action_taken': row[9]
                }
                
                threats.append(threat)
            
            return threats
            
        except sqlite3.Error as e:
            logger.error(f"Error retrieving threats: {str(e)}")
            return []
    
    def get_department_stats(self, days=7):
        """
        Get threat statistics by department.
        
        Args:
            days (int): Number of days to include in statistics
            
        Returns:
            dict: Department statistics
        """
        if not self.conn:
            self._initialize_db()
            
        if not self.conn:
            logger.error("Cannot get department stats: Database connection failed")
            return {}
        
        try:
            # Query for department statistics
            self.cursor.execute(
                '''
                SELECT department, 
                       COUNT(*) as threat_count, 
                       AVG(risk_score) as avg_risk,
                       MAX(risk_score) as max_risk,
                       COUNT(DISTINCT sender) as unique_senders
                FROM threats
                WHERE datetime(timestamp) >= datetime('now', ?)
                GROUP BY department
                ORDER BY threat_count DESC
                ''',
                (f'-{days} days',)
            )
            
            # Process the results
            stats = {}
            for row in self.cursor.fetchall():
                stats[row[0]] = {
                    'threat_count': row[1],
                    'avg_risk_score': round(row[2], 2) if row[2] else 0,
                    'max_risk_score': row[3] if row[3] else 0,
                    'unique_senders': row[4]
                }
            
            return stats
            
        except sqlite3.Error as e:
            logger.error(f"Error retrieving department stats: {str(e)}")
            return {}
    
    def mark_threat_reported(self, threat_id):
        """
        Mark a threat as reported.
        
        Args:
            threat_id (str): ID of the threat to mark
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.conn:
            self._initialize_db()
            
        if not self.conn:
            logger.error("Cannot mark threat: Database connection failed")
            return False
        
        try:
            self.cursor.execute(
                "UPDATE threats SET reported = 1 WHERE id = ?",
                (threat_id,)
            )
            self.conn.commit()
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Error marking threat as reported: {str(e)}")
            return False
    
    def log_report_generation(self, department_id, report_type, threat_count, file_path):
        """
        Log a report generation event.
        
        Args:
            department_id (str): ID of the department
            report_type (str): Type of report (daily, weekly, etc.)
            threat_count (int): Number of threats included in the report
            file_path (str): Path to the generated report file
            
        Returns:
            str: ID of the logged report, or None if logging failed
        """
        if not self.conn:
            self._initialize_db()
            
        if not self.conn:
            logger.error("Cannot log report: Database connection failed")
            return None
        
        try:
            # Generate a unique ID for the report
            report_id = str(uuid.uuid4())
            
            # Insert report into database
            self.cursor.execute(
                '''
                INSERT INTO reports 
                (id, timestamp, department_id, report_type, threat_count, file_path)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (
                    report_id,
                    datetime.now().isoformat(),
                    department_id,
                    report_type,
                    threat_count,
                    file_path
                )
            )
            
            self.conn.commit()
            logger.info(f"Report logged successfully: {report_id}")
            
            return report_id
            
        except sqlite3.Error as e:
            logger.error(f"Error logging report: {str(e)}")
            return None
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("Database connection closed")


# Example usage
if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.INFO)
    
    # Create data logger instance
    data_logger = DataLogger()
    
    # Sample email data
    email_data = {
        'id': 'sample123',
        'subject': 'Urgent: Your Account Security Verification Required',
        'from': 'security@g00gle.com',
        'to': 'finance@example.com',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Log a sample threat
    threat_id = data_logger.log_threat(
        email_data,
        risk_score=85.5,
        threat_type='domain_spoofing',
        indicators=[
            'suspicious_domain',
            'urgency_language',
            'suspicious_link',
            'brand_impersonation'
        ]
    )
    
    print(f"Logged threat with ID: {threat_id}")
    
    # Get threats for the Finance department
    threats = data_logger.get_threats(department="Finance")
    print(f"Found {len(threats)} threats for Finance department")
    
    # Get department statistics
    stats = data_logger.get_department_stats()
    print("Department statistics:")
    for dept, dept_stats in stats.items():
        print(f"  {dept}: {dept_stats['threat_count']} threats, avg risk: {dept_stats['avg_risk_score']}")
    
    # Close the database connection
    data_logger.close()

"""
PhishGuard - Threat Detection Module

This module is responsible for analyzing emails and detecting potential phishing threats
using various techniques like NLP, URL analysis, and heuristic rules.
"""

import re
import logging
import json
import os
from urllib.parse import urlparse
import urllib.request
import socket
from datetime import datetime

# Configure logging
logger = logging.getLogger('threat_detection')

class ThreatDetector:
    """
    Core threat detection engine for PhishGuard.
    
    This class implements various methods to analyze email content and identify
    potential phishing threats based on multiple indicators.
    """
    
    def __init__(self, config_path='config.ini', known_domains_path='data/known_domains.json'):
        """
        Initialize the threat detector with configuration settings.
        
        Args:
            config_path (str): Path to the configuration file
            known_domains_path (str): Path to the known legitimate domains list
        """
        self.suspicious_keywords = [
            # Urgency
            'urgent', 'immediate', 'alert', 'attention', 'important',
            # Action required
            'verify your account', 'confirm your identity', 'update your information',
            'click here', 'click below', 'click the link',
            # Security threats
            'suspicious activity', 'unauthorized', 'security breach',
            'locked', 'suspended', 'disabled', 'limited',
            # Financial incentives
            'prize', 'won', 'winner', 'lottery', 'inheritance',
            # Accounts
            'password expired', 'account verification', 'unusual sign-in',
            # Legal threats
            'legal action', 'lawsuit', 'court', 'police',
            # Generic bait
            'exclusive offer', 'one-time opportunity'
        ]
        
        # Additional keywords for spam detection
        self.spam_keywords = [
            # Common spam terms
            'buy now', 'cheap', 'discount', 'free', 'limited time', 'offer', 'save',
            'deal', 'cash', 'earn money', 'make money', 'income', 'dollars', 
            # Health related
            'weight loss', 'diet', 'viagra', 'cialis', 'pharmacy', 'prescription',
            # Marketing spam
            'subscribe now', 'advertisement', 'marketing', 'bulk', 'opt-in',
            'best price', 'best rates', 'bonus', 'cash back',
            # Phrases
            'no obligation', 'no purchase necessary', 'satisfaction guaranteed',
            'this is not spam', 'direct email', 'click now',
            # Unsubscribe patterns
            'click to remove', 'opt out', 'unsubscribe'
        ]
        
        self.suspicious_domains = [
            'paypa1.com', 'amaz0n.com', 'g00gle.com', 'micros0ft.com',
            'faceb00k.com', 'apple-id.co', 'outlook-verify.com'
        ]
        
        # Load known legitimate domains if the file exists
        self.known_domains = []
        try:
            if os.path.exists(known_domains_path):
                with open(known_domains_path, 'r') as f:
                    domain_data = json.load(f)
                    self.known_domains = domain_data.get('domains', [])
            else:
                # Create default known domains file
                self._create_default_domains_list(known_domains_path)
        except Exception as e:
            logger.error(f"Error loading known domains: {str(e)}")
            # Create default known domains file
            self._create_default_domains_list(known_domains_path)
    
    def _create_default_domains_list(self, file_path):
        """Create a default known domains file with common legitimate domains."""
        default_domains = [
            "google.com", "gmail.com", "microsoft.com", "apple.com", "amazon.com",
            "facebook.com", "twitter.com", "linkedin.com", "instagram.com",
            "github.com", "gitlab.com", "dropbox.com", "yahoo.com", "outlook.com",
            "live.com", "hotmail.com", "paypal.com", "netflix.com", "spotify.com"
        ]
        
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump({'domains': default_domains}, f, indent=4)
            self.known_domains = default_domains
            logger.info(f"Created default known domains file at {file_path}")
        except Exception as e:
            logger.error(f"Error creating default domains file: {str(e)}")
    def analyze(self, email_data):
        """
        Analyze an email for phishing and spam indicators.
        
        Args:
            email_data (dict): Email information including headers and content
            
        Returns:
            tuple: (is_suspicious (bool), risk_score (float), threat_type (str), indicators (list))
        """
        indicators = []
        risk_score = 0
        
        # Extract email parts for analysis
        subject = email_data.get('subject', '')
        sender = email_data.get('from', '')
        body_plain = email_data.get('body', {}).get('plain', '')
        body_html = email_data.get('body', {}).get('html', '')
        attachments = email_data.get('attachments', [])
        recipients = email_data.get('to', '')
        cc = email_data.get('cc', '')
        headers = email_data.get('headers', {})
        
        # Combine the subject and body for text analysis
        full_text = f"{subject} {body_plain}".lower()
        
        # Check for suspicious text and language patterns
        text_score, text_indicators = self._analyze_text(full_text)
        indicators.extend(text_indicators)
        risk_score += text_score
        
        # Check for spam patterns
        spam_score, spam_indicators = self._analyze_spam(full_text, subject, sender, recipients, cc, headers)
        indicators.extend(spam_indicators)
        risk_score += spam_score
        
        # Check for suspicious URLs in the content
        url_score, url_indicators = self._analyze_urls(body_plain, body_html)
        indicators.extend(url_indicators)
        risk_score += url_score
        
        # Check sender's domain
        sender_score, sender_indicators = self._analyze_sender(sender)
        indicators.extend(sender_indicators)
        risk_score += sender_score
        
        # Check attachments
        attachment_score, attachment_indicators = self._analyze_attachments(attachments)
        indicators.extend(attachment_indicators)
        risk_score += attachment_score
          # Cap the risk score at 100
        risk_score = min(risk_score, 100)
        
        # Determine if the email is suspicious based on risk score threshold
        is_suspicious = risk_score >= 40  # Threshold can be adjusted
        
        # Determine the main threat type based on indicators
        threat_type = self._determine_threat_type(indicators)
        
        logger.info(f"Email analysis completed - Risk score: {risk_score:.1f}, Threat type: {threat_type}")
        
        return (is_suspicious, risk_score, threat_type, indicators)
    
    def _analyze_text(self, text):
        """
        Analyze the text content of the email for suspicious patterns.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            tuple: (score, indicators)
        """
        indicators = []
        score = 0
        
        # Check for suspicious keywords
        for keyword in self.suspicious_keywords:
            if keyword.lower() in text.lower():
                indicators.append(f"suspicious_keyword_{keyword.replace(' ', '_')}")
                score += 10
                logger.debug(f"Found suspicious keyword: {keyword}")
        
        # Check for urgency language
        urgency_patterns = [
            r"urgent", r"immediate", r"act now", r"expires", r"today only",
            r"24 hours", r"limited time", r"deadline", r"quickly"
        ]
        
        for pattern in urgency_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if "urgency_language" not in indicators:
                    indicators.append("urgency_language")
                    score += 15
                    logger.debug("Detected urgency language in email")
                break
        
        # Check for poor grammar and spelling
        # This is a simplified check - in a real system, use NLP models
        grammar_errors = [
            r"you(?:r|) (has|have) been", r"kindly do the needful", r"revert back",
            r"please\s+(?:to|)\s*contact", r"we are\s+(?:going to|)\s*proceeding"
        ]
        
        grammar_score = 0
        for pattern in grammar_errors:
            if re.search(pattern, text, re.IGNORECASE):
                grammar_score += 5
        
        if grammar_score > 0:
            indicators.append("poor_grammar")
            score += grammar_score
            logger.debug(f"Detected potential grammar issues")
        
        # Check for excessive use of special characters in URLs
        special_char_count = len(re.findall(r'[!@#$%^&*()_+\-=\[\]{};\'"\\|,<>\/?]', text))
        if special_char_count > 20:  # Threshold can be adjusted
            indicators.append("excessive_special_characters")
            score += 10
            logger.debug(f"Detected excessive special characters: {special_char_count}")
        
        return (score, indicators)
    
    def _analyze_spam(self, full_text, subject, sender, recipients, cc, headers):
        """
        Analyze the email for spam indicators.
        
        Args:
            full_text (str): Combined email subject and body text
            subject (str): Email subject
            sender (str): Email sender
            recipients (str): Email recipients
            cc (str): CC recipients
            headers (dict): Email headers
            
        Returns:
            tuple: (score, indicators)
        """
        indicators = []
        score = 0
        
        # Check for spam keywords in the text
        spam_keyword_count = 0
        for keyword in self.spam_keywords:
            if keyword.lower() in full_text:
                spam_keyword_count += 1
                if spam_keyword_count == 1:  # Only add this indicator once
                    indicators.append("spam_keywords_detected")
        
        # Add score based on the number of spam keywords found
        if spam_keyword_count > 0:
            base_score = min(spam_keyword_count * 5, 30)  # Cap at 30 points
            score += base_score
            logger.debug(f"Detected {spam_keyword_count} spam keywords")
        
        # Check for ALL CAPS in subject (common in spam)
        if subject.isupper() and len(subject) > 10:
            indicators.append("subject_all_caps")
            score += 15
            logger.debug("Subject is all uppercase")
        
        # Check for excessive punctuation in subject (!!!!, ???, etc.)
        if re.search(r'[!?]{3,}', subject):
            indicators.append("excessive_punctuation")
            score += 10
            logger.debug("Subject has excessive punctuation")
        
        # Check for BULK email indicators
        if 'bulk' in headers.get('Precedence', '').lower() or 'bulk' in full_text.lower():
            indicators.append("bulk_email")
            score += 20
            logger.debug("Email marked as bulk")
        
        # Check for many recipients or CC (potential mass mailing)
        recipient_count = len(recipients.split(',')) if recipients else 0
        cc_count = len(cc.split(',')) if cc else 0
        total_recipients = recipient_count + cc_count
        
        if total_recipients > 15:
            indicators.append("mass_mailing")
            score += 15
            logger.debug(f"Mass mailing detected with {total_recipients} recipients")
        
        # Check for spam-like HTML patterns (invisible text, background color tricks)
        if '<font color="#ffffff"' in full_text.lower() or '<div style="display:none"' in full_text.lower():
            indicators.append("hidden_text")
            score += 25
            logger.debug("Hidden text detected in HTML")
        
        # Check for spammy subject patterns
        subject_lower = subject.lower()
        spammy_subject_patterns = [
            r'^re: *re:', r'fw: *fw:', 
            r'\d+% off', r'save \d+%',
            r'free', r'buy now', r'limited time',
            r'dollars|€|\$\d+', r'discount'
        ]
        
        for pattern in spammy_subject_patterns:
            if re.search(pattern, subject_lower):
                if "spammy_subject" not in indicators:
                    indicators.append("spammy_subject")
                    score += 15
                    logger.debug(f"Spammy subject pattern detected: {pattern}")
                    break
        
        return (score, indicators)
    
    def _analyze_urls(self, plain_text, html_text):
        """
        Analyze URLs in the email for suspicious patterns.
        
        Args:
            plain_text (str): Plain text email body
            html_text (str): HTML email body
            
        Returns:
            tuple: (score, indicators)
        """
        indicators = []
        score = 0
        
        # Extract URLs from both plain text and HTML content
        # This is a simplified extractor - in a real system, use a more robust parser
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+|[^\s<>"]+\.[a-zA-Z]{2,}(?:/[^\s<>"]*)?'
        
        urls_plain = re.findall(url_pattern, plain_text)
        
        # Extract URLs from HTML content
        # Also capture href attributes to identify URL masking
        href_pattern = r'href=["\'](https?://[^\s<>"\']+|www\.[^\s<>"\']+)["\']'
        urls_html = re.findall(href_pattern, html_text)
        
        # Combine all URLs
        all_urls = list(set(urls_plain + urls_html))
        
        if len(all_urls) == 0:
            return (score, indicators)
        
        # Flag for malicious URL presence
        has_malicious_url = False
        
        for url in all_urls:
            # Clean up the URL
            if url.startswith("www."):
                url = "http://" + url
            
            try:
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.lower()
                
                # Remove www. prefix for domain comparison
                if domain.startswith("www."):
                    domain = domain[4:]
                
                # Check for IP address instead of domain name
                ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
                if re.match(ip_pattern, domain):
                    indicators.append("ip_address_url")
                    score += 25
                    has_malicious_url = True
                    logger.debug(f"Detected IP address URL: {domain}")
                    continue
                
                # Check for suspicious TLDs
                suspicious_tlds = ['.xyz', '.top', '.club', '.work', '.live']
                if any(domain.endswith(tld) for tld in suspicious_tlds):
                    indicators.append("suspicious_tld")
                    score += 10
                    logger.debug(f"Detected suspicious TLD in URL: {domain}")
                
                # Check against known legitimate domains
                is_known_domain = False
                for known_domain in self.known_domains:
                    if domain == known_domain or domain.endswith("." + known_domain):
                        is_known_domain = True
                        break
                
                if not is_known_domain:
                    # Check for typosquatting (similar to legitimate domains)
                    for known_domain in self.known_domains:
                        # Simple Levenshtein distance calculation
                        similarity = self._levenshtein_distance(domain, known_domain)
                        if similarity <= 3 and similarity > 0:  # Close but not exact match
                            indicators.append("domain_spoofing")
                            score += 30
                            has_malicious_url = True
                            logger.debug(f"Detected potential typosquatting: {domain} (similar to {known_domain})")
                            break
                
                # Check for suspicious domains
                for suspicious_domain in self.suspicious_domains:
                    if domain == suspicious_domain or domain.endswith("." + suspicious_domain):
                        indicators.append("known_malicious_domain")
                        score += 40
                        has_malicious_url = True
                        logger.debug(f"Detected known malicious domain: {domain}")
                        break
                
                # Check for URL redirection
                if "redirect" in url.lower() or "url=" in url.lower() or "link=" in url.lower():
                    indicators.append("url_redirection")
                    score += 15
                    logger.debug(f"Detected URL redirection: {url}")
                
                # Check for URL shorteners
                url_shorteners = ["bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd"]
                if any(shortener in domain for shortener in url_shorteners):
                    indicators.append("url_shortener")
                    score += 20
                    logger.debug(f"Detected URL shortener: {domain}")
                
            except Exception as e:
                logger.error(f"Error analyzing URL {url}: {str(e)}")
        
        # Add an overall indicator if any malicious URL was found
        if has_malicious_url and "suspicious_link" not in indicators:
            indicators.append("suspicious_link")
        
        return (score, indicators)
    
    def _analyze_sender(self, sender):
        """
        Analyze the sender's email address for suspicious patterns.
        
        Args:
            sender (str): The sender's email address
            
        Returns:
            tuple: (score, indicators)
        """
        indicators = []
        score = 0
        
        # Extract email address from the sender field
        email_pattern = r'[\w\.-]+@[\w\.-]+'
        matches = re.findall(email_pattern, sender)
        
        if not matches:
            # No valid email address found
            indicators.append("invalid_sender_format")
            score += 20
            logger.debug(f"Invalid sender format: {sender}")
            return (score, indicators)
        
        email_address = matches[0].lower()
        domain = email_address.split('@')[-1]
        
        # Check for suspicious sender domains
        for suspicious_domain in self.suspicious_domains:
            if domain == suspicious_domain or domain.endswith("." + suspicious_domain):
                indicators.append("suspicious_sender_domain")
                score += 30
                logger.debug(f"Detected suspicious sender domain: {domain}")
                break
        
        # Check for display name vs email address mismatch (potential spoofing)
        if '@' in sender:
            display_name = sender.split('<')[0].strip().lower() if '<' in sender else ""
            
            if display_name:
                # Look for brand names in display name but different domain
                common_brands = ["paypal", "amazon", "google", "microsoft", "apple", 
                                 "facebook", "netflix", "bank", "wellsfargo", "chase"]
                
                for brand in common_brands:
                    if brand in display_name and brand not in domain:
                        indicators.append("display_name_spoofing")
                        indicators.append("brand_impersonation")
                        score += 40
                        logger.debug(f"Detected display name spoofing: {display_name} with domain {domain}")
                        break
        
        return (score, indicators)
    
    def _analyze_attachments(self, attachments):
        """
        Analyze email attachments for suspicious patterns.
        
        Args:
            attachments (list): List of attachment dictionaries
            
        Returns:
            tuple: (score, indicators)
        """
        indicators = []
        score = 0
        
        if not attachments:
            return (score, indicators)
        
        # Suspicious attachment types
        suspicious_extensions = [
            '.exe', '.scr', '.bat', '.cmd', '.js', '.jar', '.vbs', 
            '.ps1', '.msi', '.hta', '.wsf', '.jse', '.pif'
        ]
        
        # Check each attachment
        for attachment in attachments:
            filename = attachment.get('filename', '').lower()
            content_type = attachment.get('content_type', '').lower()
            
            # Check file extension
            for ext in suspicious_extensions:
                if filename.endswith(ext):
                    indicators.append("malicious_attachment_type")
                    score += 50
                    logger.debug(f"Detected suspicious attachment: {filename}")
                    break
            
            # Check for double extensions (e.g., invoice.pdf.exe)
            if filename.count('.') > 1:
                file_parts = filename.split('.')
                if len(file_parts) > 2:
                    # Check if the last extension is executable
                    if f".{file_parts[-1]}" in suspicious_extensions:
                        indicators.append("double_extension_attachment")
                        score += 50
                        logger.debug(f"Detected double extension: {filename}")
            
            # Check content type vs extension mismatch
            if "application/pdf" in content_type and not filename.endswith('.pdf'):
                indicators.append("content_type_mismatch")
                score += 30
                logger.debug(f"Content type mismatch: {content_type} for file {filename}")
        
        return (score, indicators)
    
    def _determine_threat_type(self, indicators):
        """
        Determine the main threat type based on the detected indicators.
        
        Args:
            indicators (list): List of detected threat indicators
            
        Returns:
            str: The main threat type
        """        # Define indicator to threat type mapping
        indicator_mapping = {
            "suspicious_link": "phishing_attempt",
            "domain_spoofing": "domain_spoofing",
            "display_name_spoofing": "email_spoofing",
            "brand_impersonation": "brand_impersonation",
            "malicious_attachment_type": "malware_distribution",
            "double_extension_attachment": "malware_distribution",
            "urgency_language": "social_engineering",
            "suspicious_sender_domain": "phishing_attempt",
            "known_malicious_domain": "phishing_campaign",
            # Spam indicators
            "spam_keywords_detected": "spam_email",
            "subject_all_caps": "spam_email",
            "excessive_punctuation": "spam_email",
            "bulk_email": "spam_email",
            "mass_mailing": "spam_email",
            "hidden_text": "spam_email",
            "spammy_subject": "spam_email"
        }
        
        # Count occurrences of each threat type
        threat_counts = {}
        
        for indicator in indicators:
            for indicator_key, threat_type in indicator_mapping.items():
                if indicator_key in indicator or indicator in indicator_key:
                    threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
        
        # Default threat type
        if not threat_counts:
            return "suspicious_email"
        
        # Return the most common threat type
        return max(threat_counts.items(), key=lambda x: x[1])[0]
    
    def _levenshtein_distance(self, s1, s2):
        """
        Calculate the Levenshtein distance between two strings.
        Used for detecting typosquatting domains.
        
        Args:
            s1 (str): First string
            s2 (str): Second string
            
        Returns:
            int: The edit distance between the strings
        """
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]


# For testing
if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.DEBUG)
    
    # Create a threat detector instance
    detector = ThreatDetector()
    
    # Test with a sample phishing email
    phishing_email = {
        'subject': 'Urgent: Your Account Security Verification Required',
        'from': 'Security Team <security@g00gle.com>',
        'to': 'user@example.com',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'headers': {},
        'body': {
            'plain': '''
            Dear Valued Customer,
            
            We have detected unusual activity on your account.
            Please click the link below to verify your identity:
            
            https://g00gle.com/security/verify.php?id=1234567890
            
            If you do not verify within 24 hours, your account will be locked.
            
            Regards,
            Security Team
            ''',
            'html': '''
            <html>
            <body>
            <p>Dear Valued Customer,</p>
            <p>We have detected unusual activity on your account.</p>
            <p>Please <a href="https://g00gle.com/security/verify.php?id=1234567890">click here</a> to verify your identity.</p>
            <p>If you do not verify within 24 hours, your account will be locked.</p>
            <p>Regards,<br>Security Team</p>
            </body>
            </html>
            '''
        },
        'attachments': []
    }
    
    # Test with a sample spam email
    spam_email = {
        'subject': 'AMAZING DEAL!!! 90% OFF - BUY NOW!!!!',
        'from': 'Marketing <marketing@bulkmail.com>',
        'to': 'user1@example.com, user2@example.com, user3@example.com',
        'cc': 'user4@example.com, user5@example.com, user6@example.com',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'headers': {'Precedence': 'bulk'},
        'body': {
            'plain': '''
            LIMITED TIME OFFER!
            
            FREE VIAGRA SAMPLES
            MAKE MONEY FAST - WORK FROM HOME
            EARN $5000 WEEKLY!!!
            
            The best discount prices on all medications!
            Click here to get the best deal: https://cheap-meds.example.com
            
            This email is not spam.
            You are receiving this because you opted in to our mailing list.
            
            To unsubscribe click here: http://example.com/unsubscribe
            ''',
            'html': '''
            <html>
            <body>
            <h1>LIMITED TIME OFFER!</h1>
            <p><font color="#ffffff">Hidden text to bypass spam filters</font></p>
            <p><b>FREE VIAGRA SAMPLES</b></p>
            <p>MAKE MONEY FAST - WORK FROM HOME</p>
            <p>EARN $5000 WEEKLY!!!</p>
            <p>The best discount prices on all medications!</p>
            <p><a href="https://cheap-meds.example.com">Click here</a> to get the best deal!</p>
            <div style="display:none">Hidden content to trick spam filters</div>
            <p><small>This email is not spam.<br>
            You are receiving this because you opted in to our mailing list.</small></p>
            <p>To unsubscribe <a href="http://example.com/unsubscribe">click here</a></p>
            </body>
            </html>
            '''
        },
        'attachments': []
    }
    
    # Analyze the phishing email
    print("=== PHISHING EMAIL ANALYSIS ===")
    is_suspicious, risk_score, threat_type, indicators = detector.analyze(phishing_email)
    
    print(f"Is suspicious: {is_suspicious}")
    print(f"Risk score: {risk_score}")
    print(f"Threat type: {threat_type}")
    print("Indicators:")
    for indicator in indicators:
        print(f"  - {indicator}")
        
    # Analyze the spam email
    print("\n=== SPAM EMAIL ANALYSIS ===")
    is_suspicious, risk_score, threat_type, indicators = detector.analyze(spam_email)
    
    print(f"Is suspicious: {is_suspicious}")
    print(f"Risk score: {risk_score}")
    print(f"Threat type: {threat_type}")
    print("Indicators:")
    for indicator in indicators:
        print(f"  - {indicator}")

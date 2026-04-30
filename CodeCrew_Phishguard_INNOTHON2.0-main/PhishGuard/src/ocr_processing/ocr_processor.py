"""
OCR Module for Image-Based Phishing Detection

This module provides functionality to analyze images in emails for 
potential phishing content using Optical Character Recognition (OCR).
"""

import os
import io
import logging
import tempfile
from PIL import Image
import pytesseract
import numpy as np
import re
from urllib.parse import urlparse
import cv2

# Configure logging
logger = logging.getLogger('ocr_processor')

class OCRProcessor:
    """
    OCR processor for analyzing images in emails for potential phishing content.
    
    This class extracts text from images using OCR and analyzes it for
    suspicious content, URLs, and other indicators of phishing.
    """
    
    def __init__(self, tesseract_path=None):
        """
        Initialize the OCR processor.
        
        Args:
            tesseract_path (str): Path to Tesseract OCR executable (optional)
        """
        # Set Tesseract path if provided
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Keywords to look for in OCR'd text
        self.suspicious_keywords = [
            # Login related
            'login', 'sign in', 'username', 'password', 'credential',
            # Urgency
            'urgent', 'immediate', 'alert', 'attention', 'important',
            # Action required
            'verify your account', 'confirm your identity', 'update your information',
            'click here', 'click below', 'click the link',
            # Security threats
            'suspicious activity', 'unauthorized', 'security breach',
            'locked', 'suspended', 'disabled', 'limited',
            # Financial
            'payment', 'invoice', 'bank', 'credit card', 'billing',
            # Brands frequently targeted in phishing
            'paypal', 'apple', 'microsoft', 'google', 'facebook', 'amazon',
            'netflix', 'bank of america', 'chase', 'wells fargo'
        ]
        
        # Flag to track if OCR is available
        self.ocr_available = self._check_ocr_available()
    
    def _check_ocr_available(self):
        """
        Check if Tesseract OCR is available.
        
        Returns:
            bool: True if OCR is available, False otherwise
        """
        try:
            # Try to use Tesseract
            pytesseract.get_tesseract_version()
            logger.info("Tesseract OCR is available")
            return True
        except Exception as e:
            logger.warning(f"Tesseract OCR not available: {str(e)}")
            logger.warning("Image-based phishing detection will be limited")
            return False
    
    def process_image(self, image_data):
        """
        Process an image for potential phishing content.
        
        Args:
            image_data (bytes): Raw image data
            
        Returns:
            tuple: (is_suspicious (bool), extracted_text (str), indicators (list))
        """
        if not self.ocr_available:
            logger.warning("OCR not available for image processing")
            return False, "", ["ocr_unavailable"]
        
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(image_data))
            
            # Preprocess the image for better OCR results
            preprocessed_image = self._preprocess_image(image)
            
            # Extract text from image
            extracted_text = pytesseract.image_to_string(preprocessed_image)
            
            if not extracted_text:
                logger.info("No text extracted from image")
                return False, "", []
            
            # Analyze the extracted text
            is_suspicious, indicators = self._analyze_text(extracted_text)
            
            logger.info(f"Image analysis completed - Suspicious: {is_suspicious}")
            
            return is_suspicious, extracted_text, indicators
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return False, "", ["processing_error"]
    
    def _preprocess_image(self, image):
        """
        Preprocess the image to improve OCR accuracy.
        
        Args:
            image (PIL.Image): Image to preprocess
            
        Returns:
            PIL.Image: Preprocessed image
        """
        try:
            # Convert PIL image to numpy array for OpenCV processing
            img_np = np.array(image)
            
            # Check if image is grayscale or color
            if len(img_np.shape) == 2 or img_np.shape[2] == 1:
                # Already grayscale
                gray = img_np
            else:
                # Convert to grayscale
                gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            
            # Apply thresholding to handle different backgrounds
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            
            # Noise removal
            kernel = np.ones((1, 1), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
            
            # Convert back to PIL image for Tesseract
            preprocessed = Image.fromarray(opening)
            
            return preprocessed
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            # Return original image if processing fails
            return image
    
    def _analyze_text(self, text):
        """
        Analyze extracted text for suspicious content.
        
        Args:
            text (str): Text extracted from image
            
        Returns:
            tuple: (is_suspicious (bool), indicators (list))
        """
        indicators = []
        text_lower = text.lower()
        
        # Check for suspicious keywords
        for keyword in self.suspicious_keywords:
            if keyword.lower() in text_lower:
                indicators.append(f"ocr_keyword_{keyword.replace(' ', '_')}")
                logger.debug(f"Found suspicious keyword in image text: {keyword}")
        
        # Check for URLs in the text
        urls = self._extract_urls(text)
        for url in urls:
            indicators.append("ocr_contains_url")
            logger.debug(f"Found URL in image text: {url}")
            
            # Check for suspicious domains
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            # Look for IP addresses instead of domains
            ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
            if re.match(ip_pattern, domain):
                indicators.append("ocr_ip_address_url")
                logger.debug(f"Found IP address URL in image: {domain}")
            
            # Check for suspicious TLDs
            suspicious_tlds = ['.xyz', '.top', '.club', '.work', '.live']
            if any(domain.endswith(tld) for tld in suspicious_tlds):
                indicators.append("ocr_suspicious_tld")
                logger.debug(f"Found suspicious TLD in image URL: {domain}")
        
        # Check for form-like content
        if ('username' in text_lower and 'password' in text_lower) or \
           ('user' in text_lower and 'pass' in text_lower) or \
           ('log' in text_lower and 'pass' in text_lower):
            indicators.append("ocr_login_form")
            logger.debug("Found login form-like content in image")
        
        # Check for urgency language
        urgency_patterns = [
            r"urgent", r"immediate", r"act now", r"expires", r"today only",
            r"24 hours", r"limited time", r"deadline", r"quickly"
        ]
        
        for pattern in urgency_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                indicators.append("ocr_urgency_language")
                logger.debug("Detected urgency language in image text")
                break
        
        # Determine if the image is suspicious based on indicators
        is_suspicious = len(indicators) > 0
        
        return is_suspicious, indicators
    
    def _extract_urls(self, text):
        """
        Extract URLs from text.
        
        Args:
            text (str): Text to extract URLs from
            
        Returns:
            list: List of extracted URLs
        """
        # URL pattern matching
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+|[^\s<>"]+\.[a-zA-Z]{2,}(?:/[^\s<>"]*)?'
        
        urls = re.findall(url_pattern, text)
        
        # Clean and normalize URLs
        normalized_urls = []
        for url in urls:
            # Add http:// to URLs starting with www
            if url.startswith('www.'):
                url = 'http://' + url
            
            # Filter out strings that aren't likely to be URLs
            if '.' in url and len(url) > 5:
                normalized_urls.append(url)
        
        return normalized_urls
    
    def process_attachment(self, attachment):
        """
        Process an email attachment for OCR analysis.
        
        Args:
            attachment (dict): Attachment data
            
        Returns:
            tuple: (is_suspicious (bool), results (dict))
        """
        filename = attachment.get('filename', '')
        content_type = attachment.get('content_type', '')
        data = attachment.get('data', b'')
        
        # Skip non-image attachments
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        is_image = any(filename.lower().endswith(ext) for ext in image_extensions) or \
                   content_type.startswith('image/')
        
        if not is_image:
            logger.debug(f"Skipping non-image attachment: {filename}")
            return False, {'processed': False, 'reason': 'not_an_image'}
        
        # Process the image
        is_suspicious, extracted_text, indicators = self.process_image(data)
        
        results = {
            'processed': True,
            'filename': filename,
            'content_type': content_type,
            'is_suspicious': is_suspicious,
            'indicators': indicators,
            'extracted_text': extracted_text[:500] if len(extracted_text) > 500 else extracted_text
        }
        
        return is_suspicious, results


# Example usage
if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.DEBUG)
    
    # Create OCR processor
    ocr = OCRProcessor()
    
    # Check if OCR is available
    if ocr.ocr_available:
        print("OCR is available for testing")
        
        # Example: Create a test image with suspicious text
        try:
            from PIL import Image, ImageDraw, ImageFont
            import numpy as np
            
            # Create a blank image
            img = Image.new('RGB', (800, 600), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            
            # Try to use a font
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            # Add suspicious text to the image
            text = """
            URGENT: Your PayPal account has been limited
            
            We have detected suspicious activity on your account.
            Please verify your identity by clicking the link below:
            
            http://paypal-secure-login.xyz/verify.php
            
            Username: ___________________
            Password: ___________________
            
            If you do not verify within 24 hours, your account will be suspended.
            
            PayPal Security Team
            """
            
            d.text((50, 50), text, fill=(0, 0, 0), font=font)
            
            # Save to bytes
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            img_bytes = buf.getvalue()
            
            # Test OCR processing
            is_suspicious, extracted_text, indicators = ocr.process_image(img_bytes)
            
            print(f"Is suspicious: {is_suspicious}")
            print(f"Indicators: {indicators}")
            print(f"Extracted text: {extracted_text}")
            
        except ImportError:
            print("PIL or other dependencies not available for test image creation")
    else:
        print("OCR is not available. Please install Tesseract and configure the path.")

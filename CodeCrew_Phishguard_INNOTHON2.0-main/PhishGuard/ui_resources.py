"""
PhishGuard Icons and Resources

This module provides resources for the PhishGuard GUI.
"""

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, QByteArray

# Animation parameters
ANIMATIONS = {
    "header_fade": {
        "duration": 800,
        "start_value": 0.0,
        "end_value": 1.0,
        "curve": 6  # QEasingCurve.InOutQuad
    },
    "stat_number": {
        "duration": 1500,
        "curve": 23  # QEasingCurve.OutElastic
    },
    "notification": {
        "duration": 300,
        "start_value": 0.0,
        "end_value": 1.0,
        "curve": 1  # QEasingCurve.InQuad
    }
}

def get_icon(icon_name, size=None):
    """Get a QIcon from the icon name."""
    return QIcon()

def get_pixmap(icon_name, size=None):
    """Get a QPixmap from the icon name."""
    return QPixmap()

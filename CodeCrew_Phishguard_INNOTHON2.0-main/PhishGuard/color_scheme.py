# color_scheme.py - Color definitions for PhishGuard UI

# Main color scheme
COLORS = {
    'primary': '#007bff',    # Blue - used for main elements and buttons
    'secondary': '#6c757d',  # Gray - used for secondary elements
    'success': '#28a745',    # Green - used for success indicators
    'danger': '#dc3545',     # Red - used for high risk, errors, and alerts
    'warning': '#ffc107',    # Yellow - used for medium risk and warnings
    'info': '#17a2b8',       # Teal - used for information indicators
    'light': '#f8f9fa',      # Light gray - used for backgrounds
    'dark': '#343a40',       # Dark gray - used for text
    'white': '#ffffff',      # White - used for text on dark backgrounds
    'black': '#000000',      # Black - used for borders and emphasis
    
    # UI-specific colors
    'sidebar_bg': '#2c3e50',         # Dark blue for sidebar background
    'hover': '#3498db',              # Lighter blue for hover states
    'active': '#1a5276',             # Darker blue for active states
    'card_border': '#dfe6e9',        # Light gray for card borders
    'gradient_start': '#3498db',     # Blue gradient start
    'gradient_end': '#2980b9',       # Blue gradient end
    'chart_colors': [                # Colors for charts and graphs
        '#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
        '#1abc9c', '#d35400', '#2c3e50', '#27ae60', '#c0392b'
    ]
}

# Theme variables for QSS styling
THEME = {
    'font_family': 'Segoe UI, Arial, sans-serif',
    'border_radius': '4px',
    'shadow': '0px 2px 4px rgba(0, 0, 0, 0.1)',
    'spacing': '8px',
    'padding': '10px',
    'font_size_normal': '10pt',
    'font_size_large': '12pt',
    'font_size_small': '9pt',
    'font_size_header': '16pt',
}

# Color palette for different risk levels
RISK_COLORS = {
    'critical': '#c0392b',  # Dark red
    'high': '#e74c3c',      # Red
    'medium': '#f39c12',    # Orange
    'low': '#2ecc71',       # Green
    'info': '#3498db',      # Blue
}
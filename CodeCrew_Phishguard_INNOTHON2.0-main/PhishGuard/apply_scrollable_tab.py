"""
Apply scrollable Reports tab to PhishGuard GUI
"""

import re
import os
import sys

def main():
    # Make sure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Import the scrollable reports tab code
    sys.path.append(script_dir)
    from reports_tab_with_scrolling import get_scrollable_reports_tab
    
    # The new method code
    new_method = get_scrollable_reports_tab()
    
    # Read the original file
    with open('phishguard_gui.py', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # First, make a backup
    with open('phishguard_gui.py.before_scroll', 'w', encoding='utf-8') as file:
        file.write(content)
    
    # Define a pattern to match the createReportsTab method
    pattern = r'def createReportsTab\(self, parent_widget\):[\s\S]*?(?=\n    def \w+\(|\Z)'
    
    # Replace the method
    new_content = re.sub(pattern, new_method.strip(), content)
    
    # Write the modified content back to the file
    with open('phishguard_gui.py', 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    print("Successfully replaced createReportsTab method with scrollable version.")

if __name__ == "__main__":
    main()

import re

# File paths
main_file = r"c:\Users\ritik\OneDrive\Desktop\new\PhishGuard\phishguard_gui.py"
fix_file = r"c:\Users\ritik\OneDrive\Desktop\new\PhishGuard\final_reports_tab_fix.py"
backup_file = r"c:\Users\ritik\OneDrive\Desktop\new\PhishGuard\phishguard_gui.py.fix_backup"

# Load the fixed reports tab code
with open(fix_file, 'r') as f:
    fix_module = {}
    exec(f.read(), fix_module)
    fixed_code = fix_module['fixed_reports_tab_code']()

# Read the main file content
with open(main_file, 'r') as f:
    content = f.read()

# Create a backup of the original file
with open(backup_file, 'w') as f:
    f.write(content)

# Define a pattern to match the createReportsTab method
pattern = r"def createReportsTab\(self, parent_widget\):.*?(?=def \w+\(|$)"


# Use regex with DOTALL to match across multiple lines
replacement = fixed_code

# Replace the method in the content
modified_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write the modified content back to the file
with open(main_file, 'w') as f:
    f.write(modified_content)

print("Replacement completed successfully!")

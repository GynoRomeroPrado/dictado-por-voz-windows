
import re

with open('build.spec', 'r', encoding='utf-8') as f:
    content = f.read()

# Enable console
if "console=False" in content:
    content = content.replace("console=False", "console=True")
    print("Enabled console output")

# Ensure imports for collect_all are present if we were to use them, 
# but for now let's just rely on build.py changes for collection or 
# just see the error first.

with open('build.spec', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched build.spec")

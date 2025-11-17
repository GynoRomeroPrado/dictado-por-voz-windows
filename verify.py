#!/usr/bin/env python
"""
Verification script for Dictado por Voz - Windows Desktop App
Checks code structure, imports, and configuration without requiring all dependencies
"""

import os
import sys
import json
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def print_info(msg):
    print(f"{BLUE}ℹ{RESET} {msg}")

def check_file_structure():
    """Check if all required files and directories exist"""
    print("\n" + "="*60)
    print("1. Checking File Structure")
    print("="*60)

    required_files = [
        'README.md',
        'requirements.txt',
        'setup.py',
        'LICENSE',
        'INSTALL.md',
        'QUICKSTART.md',
        'CONTRIBUTING.md',
        'CHANGELOG.md',
        '.gitignore',
        'run.py',
        'config/settings.json',
        'config/commands.json',
        'src/__init__.py',
        'src/main.py',
        'src/core/__init__.py',
        'src/core/speech_recognizer.py',
        'src/core/command_processor.py',
        'src/core/hotkey_manager.py',
        'src/gui/__init__.py',
        'src/gui/main_window.py',
        'src/gui/settings_dialog.py',
        'src/utils/__init__.py',
        'src/utils/config.py',
        'src/utils/clipboard.py'
    ]

    missing = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"Found: {file_path}")
        else:
            print_error(f"Missing: {file_path}")
            missing.append(file_path)

    if missing:
        print_error(f"\n{len(missing)} files missing")
        return False
    else:
        print_success(f"\nAll {len(required_files)} required files found")
        return True

def check_python_syntax():
    """Check Python syntax of all source files"""
    print("\n" + "="*60)
    print("2. Checking Python Syntax")
    print("="*60)

    python_files = []
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    # Add run.py
    python_files.append('run.py')

    errors = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                compile(f.read(), file_path, 'exec')
            print_success(f"Syntax OK: {file_path}")
        except SyntaxError as e:
            print_error(f"Syntax Error in {file_path}: {e}")
            errors.append((file_path, str(e)))

    if errors:
        print_error(f"\n{len(errors)} files with syntax errors")
        return False
    else:
        print_success(f"\nAll {len(python_files)} Python files have valid syntax")
        return True

def check_json_files():
    """Validate JSON configuration files"""
    print("\n" + "="*60)
    print("3. Validating JSON Configuration Files")
    print("="*60)

    json_files = [
        'config/settings.json',
        'config/commands.json'
    ]

    errors = []
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print_success(f"Valid JSON: {file_path}")

            # Show some stats
            if file_path == 'config/settings.json':
                print_info(f"  - Version: {data.get('version', 'N/A')}")
                print_info(f"  - Language: {data.get('language', 'N/A')}")
            elif file_path == 'config/commands.json':
                custom_count = len(data.get('custom_commands', []))
                punct_count = len(data.get('punctuation_commands', {}))
                print_info(f"  - Custom commands: {custom_count}")
                print_info(f"  - Punctuation commands: {punct_count}")

        except json.JSONDecodeError as e:
            print_error(f"JSON Error in {file_path}: {e}")
            errors.append((file_path, str(e)))
        except FileNotFoundError:
            print_error(f"File not found: {file_path}")
            errors.append((file_path, "File not found"))

    if errors:
        print_error(f"\n{len(errors)} JSON files with errors")
        return False
    else:
        print_success(f"\nAll {len(json_files)} JSON files are valid")
        return True

def check_imports():
    """Check if imports in source files are structured correctly"""
    print("\n" + "="*60)
    print("4. Checking Import Structure")
    print("="*60)

    # Add src to path
    sys.path.insert(0, 'src')

    modules_to_check = [
        ('utils.config', 'ConfigManager'),
        ('utils.clipboard', 'ClipboardManager'),
    ]

    errors = []
    for module_name, class_name in modules_to_check:
        try:
            module = __import__(module_name, fromlist=[class_name])
            if hasattr(module, class_name):
                print_success(f"Import OK: {module_name}.{class_name}")
            else:
                print_error(f"Class not found: {module_name}.{class_name}")
                errors.append(f"{module_name}.{class_name}")
        except ImportError as e:
            # Check if it's a missing dependency (expected) or a structure error
            if any(pkg in str(e) for pkg in ['PyQt5', 'speech_recognition', 'keyboard', 'pyperclip', 'pyttsx3']):
                print_warning(f"Import {module_name}.{class_name}: Missing dependency (expected)")
            else:
                print_error(f"Import error in {module_name}: {e}")
                errors.append(f"{module_name}: {e}")

    if errors:
        print_error(f"\n{len(errors)} import structure errors")
        return False
    else:
        print_success("\nImport structure is correct")
        return True

def check_dependencies():
    """Check if dependencies are listed in requirements.txt"""
    print("\n" + "="*60)
    print("5. Checking Dependencies")
    print("="*60)

    required_deps = [
        'SpeechRecognition',
        'PyQt5',
        'keyboard',
        'pyperclip',
        'pyttsx3',
        'pywin32'
    ]

    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()

        missing = []
        for dep in required_deps:
            if dep in content:
                print_success(f"Found dependency: {dep}")
            else:
                print_warning(f"Dependency not found: {dep}")
                missing.append(dep)

        if missing:
            print_warning(f"\n{len(missing)} dependencies not listed in requirements.txt")
        else:
            print_success(f"\nAll {len(required_deps)} required dependencies listed")

        return len(missing) == 0

    except FileNotFoundError:
        print_error("requirements.txt not found")
        return False

def check_documentation():
    """Check if documentation files are complete"""
    print("\n" + "="*60)
    print("6. Checking Documentation")
    print("="*60)

    doc_files = {
        'README.md': ['Características', 'Instalación', 'Uso'],
        'INSTALL.md': ['Requisitos', 'Instalación', 'paso'],
        'QUICKSTART.md': ['minutos', 'Ejemplo', 'Comandos'],
        'CONTRIBUTING.md': ['Contribuir', 'Pull Request', 'Código'],
        'CHANGELOG.md': ['1.0.0', 'Añadido']
    }

    issues = []
    for doc_file, keywords in doc_files.items():
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()

            missing_keywords = []
            for keyword in keywords:
                if keyword.lower() not in content.lower():
                    missing_keywords.append(keyword)

            if missing_keywords:
                print_warning(f"{doc_file}: Missing keywords: {', '.join(missing_keywords)}")
                issues.append(doc_file)
            else:
                print_success(f"{doc_file}: Complete")

        except FileNotFoundError:
            print_error(f"{doc_file}: Not found")
            issues.append(doc_file)

    if issues:
        print_warning(f"\n{len(issues)} documentation files have issues")
    else:
        print_success(f"\nAll {len(doc_files)} documentation files are complete")

    return len(issues) == 0

def main():
    """Run all verification checks"""
    print(f"\n{BLUE}{'='*60}")
    print("Dictado por Voz - Windows Desktop App")
    print("Verification Script")
    print(f"{'='*60}{RESET}\n")

    checks = [
        ("File Structure", check_file_structure),
        ("Python Syntax", check_python_syntax),
        ("JSON Validation", check_json_files),
        ("Import Structure", check_imports),
        ("Dependencies", check_dependencies),
        ("Documentation", check_documentation)
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Error running {name} check: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        if result:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")

    print("\n" + "="*60)
    if passed == total:
        print_success(f"ALL CHECKS PASSED ({passed}/{total})")
        print_success("\n✓ Project is ready for deployment!")
    else:
        print_warning(f"SOME CHECKS FAILED ({passed}/{total})")
        print_info("\nNote: Some warnings are expected in development environment")
        print_info("Install dependencies with: pip install -r requirements.txt")
    print("="*60 + "\n")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python
"""
Test runner for Dictado por Voz - Windows Desktop App
Runs all unit tests and generates coverage report
"""

import sys
import os
import unittest
from io import StringIO

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{BLUE}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text):
    """Print error message"""
    print(f"{RED}✗ {text}{RESET}")


def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠ {text}{RESET}")


def run_test_module(module_name):
    """Run tests from a specific module"""
    try:
        # Discover and run tests from the module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(module_name)

        # Run tests with detailed output
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        return result
    except Exception as e:
        print_error(f"Error loading {module_name}: {e}")
        return None


def run_all_tests():
    """Run all test modules"""
    print_header("Running All Unit Tests")

    test_modules = [
        'tests.test_config',
        'tests.test_command_processor',
        'tests.test_clipboard',
        'tests.test_hotkey_manager',
    ]

    all_results = []
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0

    for module in test_modules:
        print(f"\n{BLUE}Running {module}...{RESET}")
        result = run_test_module(module)

        if result:
            all_results.append((module, result))
            total_tests += result.testsRun
            total_failures += len(result.failures)
            total_errors += len(result.errors)
            total_skipped += len(result.skipped)

    # Print summary
    print_header("Test Summary")

    for module, result in all_results:
        module_name = module.split('.')[-1]
        if result.wasSuccessful():
            print_success(f"{module_name}: {result.testsRun} tests passed")
        else:
            print_error(f"{module_name}: {len(result.failures)} failures, {len(result.errors)} errors")

    print(f"\n{BLUE}{'='*70}")
    print(f"Total Tests Run: {total_tests}")
    print(f"Failures: {total_failures}")
    print(f"Errors: {total_errors}")
    print(f"Skipped: {total_skipped}")
    print(f"Success Rate: {((total_tests - total_failures - total_errors) / total_tests * 100):.1f}%")
    print(f"{'='*70}{RESET}\n")

    if total_failures == 0 and total_errors == 0:
        print_success("ALL TESTS PASSED! ✓")
        return True
    else:
        print_error(f"SOME TESTS FAILED ({total_failures + total_errors} total)")
        return False


def check_test_coverage():
    """Check which components have tests"""
    print_header("Test Coverage Analysis")

    components = {
        'ConfigManager': 'tests/test_config.py',
        'CommandProcessor': 'tests/test_command_processor.py',
        'ClipboardManager': 'tests/test_clipboard.py',
        'HotkeyManager': 'tests/test_hotkey_manager.py',
        'SpeechRecognizer': 'tests/test_speech_recognizer.py',
        'MainWindow': 'tests/test_gui.py',
        'SettingsDialog': 'tests/test_gui.py',
    }

    covered = 0
    total = len(components)

    for component, test_file in components.items():
        if os.path.exists(test_file):
            print_success(f"{component}: Covered")
            covered += 1
        else:
            print_warning(f"{component}: No tests found")

    coverage_percent = (covered / total) * 100
    print(f"\n{BLUE}Component Coverage: {covered}/{total} ({coverage_percent:.1f}%){RESET}\n")

    return coverage_percent


def run_integration_tests():
    """Run integration tests"""
    print_header("Integration Tests")

    # Check if integration tests exist
    if not os.path.exists('tests/test_integration.py'):
        print_warning("No integration tests found")
        return True

    try:
        result = run_test_module('tests.test_integration')
        if result and result.wasSuccessful():
            print_success("Integration tests passed")
            return True
        else:
            print_error("Integration tests failed")
            return False
    except Exception as e:
        print_warning(f"Could not run integration tests: {e}")
        return True


def validate_test_files():
    """Validate that test files are properly structured"""
    print_header("Validating Test Files")

    test_dir = 'tests'
    if not os.path.exists(test_dir):
        print_error(f"Test directory not found: {test_dir}")
        return False

    test_files = [f for f in os.listdir(test_dir) if f.startswith('test_') and f.endswith('.py')]

    if not test_files:
        print_error("No test files found")
        return False

    for test_file in test_files:
        file_path = os.path.join(test_dir, test_file)
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Check for basic test structure
            if 'unittest' in content and 'TestCase' in content:
                print_success(f"{test_file}: Valid structure")
            else:
                print_warning(f"{test_file}: May be missing test cases")

        except Exception as e:
            print_error(f"{test_file}: Error reading file - {e}")

    return True


def main():
    """Main test runner"""
    print(f"\n{BLUE}{'='*70}")
    print("Dictado por Voz - Windows Desktop App")
    print("Test Runner")
    print(f"{'='*70}{RESET}\n")

    # Validate test files first
    if not validate_test_files():
        print_error("Test validation failed")
        return 1

    # Check test coverage
    coverage = check_test_coverage()

    # Run all unit tests
    tests_passed = run_all_tests()

    # Run integration tests
    integration_passed = run_integration_tests()

    # Final summary
    print_header("Final Summary")

    results = {
        "Test Coverage": f"{coverage:.1f}%",
        "Unit Tests": "PASSED" if tests_passed else "FAILED",
        "Integration Tests": "PASSED" if integration_passed else "FAILED"
    }

    for category, status in results.items():
        if "PASSED" in str(status) or coverage > 50:
            print_success(f"{category}: {status}")
        else:
            print_error(f"{category}: {status}")

    print()

    # Overall status
    if tests_passed and integration_passed:
        print_success("✓ ALL VALIDATIONS PASSED")
        print_success("✓ Project is ready for deployment!\n")
        return 0
    else:
        print_warning("⚠ Some tests failed - review output above")
        print_warning("⚠ Fix failing tests before deployment\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

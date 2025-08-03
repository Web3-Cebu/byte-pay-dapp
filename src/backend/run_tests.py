#!/usr/bin/env python3
"""
Test runner script for BytePay API

This script sets up the test environment and runs all tests with proper configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_test_environment():
    """Set up the test environment"""
    # Ensure we're in the correct directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Remove any existing test database
    test_db_files = ["test.db", "test.db-shm", "test.db-wal"]
    for db_file in test_db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
    
    print("✅ Test environment setup complete")

def run_tests(test_path=None, verbose=True):
    """Run tests with pytest"""
    cmd = ["python", "-m", "pytest"]
    
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    if verbose:
        cmd.append("-v")
    
    # Add other useful options
    cmd.extend([
        "--tb=short",
        "--disable-warnings",
        "--color=yes"
    ])
    
    print(f"🚀 Running tests: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode

def main():
    """Main function"""
    if len(sys.argv) > 1:
        test_path = sys.argv[1]
    else:
        test_path = None
    
    setup_test_environment()
    exit_code = run_tests(test_path)
    
    if exit_code == 0:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n❌ Tests failed with exit code {exit_code}")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
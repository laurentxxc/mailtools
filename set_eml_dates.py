#!/usr/bin/env python3

"""
Script to set .eml file modification dates based on the Date header in the email.
This script processes .eml files and sets their file system modification time
to match the date found in the email's Date header.
"""

import os
import sys
import re
import argparse
from datetime import datetime
from email import message_from_file
from email.utils import parsedate_to_datetime
import subprocess

def extract_date_from_eml(file_path):
    """
    Extract the date from an .eml file's Date header.
    
    Args:
        file_path (str): Path to the .eml file
        
    Returns:
        datetime: Parsed datetime object, or None if parsing fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Try to parse as proper email message
            msg = message_from_file(f)
            date_header = msg.get('Date')
            
            if date_header:
                try:
                    # Use email.utils to parse the date
                    return parsedate_to_datetime(date_header)
                except (ValueError, TypeError):
                    # If email.utils fails, try manual parsing
                    pass
            
        # Fallback: manual header parsing for malformed emails
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f):
                if line_num > 50:  # Only check first 50 lines
                    break
                    
                # Look for Date: header (case insensitive)
                if line.lower().startswith('date:'):
                    date_str = line[5:].strip()
                    return parse_date_manually(date_str)
                    
                # Stop at empty line (end of headers)
                if line.strip() == '':
                    break
                    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return None

def parse_date_manually(date_str):
    """
    Manually parse various date formats found in email headers.
    
    Args:
        date_str (str): Date string from email header
        
    Returns:
        datetime: Parsed datetime object, or None if parsing fails
    """
    # Common email date formats
    formats = [
        '%a, %d %b %Y %H:%M:%S %z',        # Tue, 5 Mar 2024 16:01:44 +0100
        '%a, %d %b %Y %H:%M:%S %Z',        # Tue, 5 Mar 2024 16:01:44 CET
        '%d %b %Y %H:%M:%S %z',            # 5 Mar 2024 16:01:44 +0100
        '%a, %d %b %Y %H:%M:%S',           # Tue, 5 Mar 2024 16:01:44 (no timezone)
        '%d %b %Y %H:%M:%S',               # 5 Mar 2024 16:01:44
        '%Y-%m-%d %H:%M:%S',               # 2024-03-05 16:01:44
        '%a %b %d %H:%M:%S %Y',            # Tue Mar 5 16:01:44 2024
        '%a %b %d %H:%M:%S %Z %Y',         # Tue Mar 5 16:01:44 CET 2024
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # Try removing timezone info and parsing again
    # Remove common timezone patterns
    date_clean = re.sub(r'\s*\([^)]+\)\s*$', '', date_str)  # Remove (timezone name)
    date_clean = re.sub(r'\s*[+-]\d{4}\s*$', '', date_clean)  # Remove +0100, -0500
    date_clean = re.sub(r'\s*(GMT|UTC|CET|EST|PST|MST|CST)\s*$', '', date_clean)  # Remove timezone names
    
    for fmt in ['%a, %d %b %Y %H:%M:%S', '%d %b %Y %H:%M:%S', '%a %b %d %H:%M:%S %Y']:
        try:
            return datetime.strptime(date_clean.strip(), fmt)
        except ValueError:
            continue
    
    return None

def set_file_date(file_path, dt):
    """
    Set the modification time of a file using touch command.
    
    Args:
        file_path (str): Path to the file
        dt (datetime): Datetime to set
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Format datetime for touch command: YYYYMMDDHHMM.SS
        timestamp = dt.strftime('%Y%m%d%H%M.%S')
        
        # Use touch command to set the file date
        result = subprocess.run(['touch', '-t', timestamp, file_path], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"Error setting date for {file_path}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error setting date for {file_path}: {e}")
        return False

def process_eml_file(file_path, dry_run=False, verbose=False):
    """
    Process a single .eml file to set its date.
    
    Args:
        file_path (str): Path to the .eml file
        dry_run (bool): If True, don't actually modify files
        verbose (bool): If True, print detailed information
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return False
    
    # Extract date from email
    dt = extract_date_from_eml(file_path)
    
    if dt is None:
        if verbose:
            print(f"❌ Could not extract date from: {os.path.basename(file_path)}")
        return False
    
    if dry_run:
        print(f"🔍 Would set {os.path.basename(file_path)} to: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    
    # Set the file date
    success = set_file_date(file_path, dt)
    
    if success:
        if verbose:
            print(f"✅ Set {os.path.basename(file_path)} to: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"❌ Failed to set date for: {os.path.basename(file_path)}")
    
    return success

def main():
    parser = argparse.ArgumentParser(description='Set .eml file dates based on email Date header')
    parser.add_argument('path', nargs='?', default='.', 
                       help='Path to .eml file or directory (default: current directory)')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Process directories recursively')
    parser.add_argument('-n', '--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--pattern', default='*.eml',
                       help='File pattern to match (default: *.eml)')
    
    args = parser.parse_args()
    
    path = os.path.abspath(args.path)
    
    if not os.path.exists(path):
        print(f"Error: Path does not exist: {path}")
        sys.exit(1)
    
    files_to_process = []
    
    if os.path.isfile(path):
        if path.lower().endswith('.eml'):
            files_to_process.append(path)
        else:
            print(f"Error: File is not a .eml file: {path}")
            sys.exit(1)
    else:
        # Directory processing
        import fnmatch
        
        if args.recursive:
            for root, dirs, files in os.walk(path):
                for filename in files:
                    if fnmatch.fnmatch(filename.lower(), args.pattern.lower()):
                        files_to_process.append(os.path.join(root, filename))
        else:
            for filename in os.listdir(path):
                if fnmatch.fnmatch(filename.lower(), args.pattern.lower()):
                    file_path = os.path.join(path, filename)
                    if os.path.isfile(file_path):
                        files_to_process.append(file_path)
    
    if not files_to_process:
        print(f"No .eml files found in: {path}")
        sys.exit(0)
    
    print(f"Found {len(files_to_process)} .eml file(s) to process")
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
    
    success_count = 0
    fail_count = 0
    
    for file_path in files_to_process:
        if process_eml_file(file_path, args.dry_run, args.verbose):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n📊 Summary:")
    print(f"✅ Successfully processed: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📄 Total files: {len(files_to_process)}")

if __name__ == '__main__':
    main()
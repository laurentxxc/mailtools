# EML File Date Setting Scripts

This directory contains scripts to set the modification date of .eml files based on the Date header found in the email message.

## Files

- `set_eml_dates.py` - Main Python script that processes .eml files
- `set_eml_dates.sh` - Shell wrapper script for easier usage
- `README_EML_DATES.md` - This documentation file

## Features

- **Robust Date Parsing**: Handles various email date formats including timezones
- **Dry Run Mode**: Preview changes before applying them
- **Recursive Processing**: Process entire directory trees
- **Error Handling**: Gracefully handles malformed emails and date parsing errors
- **Verbose Output**: Detailed logging of operations
- **Cross Platform**: Works on macOS, Linux, and other Unix-like systems

## Requirements

- Python 3.6 or later
- `touch` command (standard on Unix-like systems)
- Standard Python libraries (email, datetime, subprocess, argparse, etc.)

## Usage

### Quick Start

```bash
# Process all .eml files in current directory (dry run)
./set_eml_dates.sh -n

# Process all .eml files in current directory
./set_eml_dates.sh

# Process recursively with verbose output
./set_eml_dates.sh -rv /path/to/mail/archive

# Process a single file
./set_eml_dates.sh myemail.eml
```

### Using the Python Script Directly

```bash
# Process current directory with dry run
python3 set_eml_dates.py --dry-run

# Process recursively with verbose output
python3 set_eml_dates.py -rv /path/to/emails

# Get help
python3 set_eml_dates.py --help
```

### Options

- `-h, --help`: Show help message
- `-n, --dry-run`: Show what would be done without making changes
- `-r, --recursive`: Process directories recursively
- `-v, --verbose`: Verbose output showing each file processed
- `--pattern PATTERN`: File pattern to match (default: *.eml)

## Supported Date Formats

The script handles various email date formats including:

- `Tue, 5 Mar 2024 16:01:44 +0100` (RFC 2822 format)
- `Tue, 5 Mar 2024 16:01:44 CET` (Named timezone)
- `5 Mar 2024 16:01:44 +0100` (Without day name)
- `Tue Mar 5 16:01:44 2024` (Alternative format)
- `2024-03-05 16:01:44` (ISO format)
- And many more variations with/without timezones

## Examples

### Process Current Directory
```bash
# Dry run to see what would happen
./set_eml_dates.sh -n

# Actually process the files
./set_eml_dates.sh
```

### Process Entire Mail Archive Recursively
```bash
# Dry run first
./set_eml_dates.sh -nr /Users/username/Documents/MailArchive

# Process with verbose output
./set_eml_dates.sh -rv /Users/username/Documents/MailArchive
```

### Process Single Year Directory
```bash
cd /Users/username/Documents/MailArchive/Outlook/2024/Sent
./set_eml_dates.sh -v
```

### Process Mounted Archive
```bash
# If you have a mounted DMG archive
./set_eml_dates.sh -rv "/Volumes/Messages 2007-2017"
```

## How It Works

1. **Date Extraction**: The script reads each .eml file and looks for the "Date:" header
2. **Date Parsing**: Uses Python's email utilities and manual parsing for various date formats
3. **File Date Setting**: Uses the `touch` command to set the file's modification time
4. **Error Handling**: Skips files where dates cannot be parsed and reports errors

## Output Examples

### Dry Run Mode
```
Found 321 .eml file(s) to process
🔍 DRY RUN MODE - No files will be modified
🔍 Would set example.eml to: 2024-03-05 16:01:44
🔍 Would set another.eml to: 2024-02-15 10:30:22

📊 Summary:
✅ Successfully processed: 321
❌ Failed: 0
📄 Total files: 321
```

### Normal Mode with Verbose Output
```
Found 10 .eml file(s) to process
✅ Set message1.eml to: 2024-01-15 14:23:45
✅ Set message2.eml to: 2024-01-16 09:12:33
❌ Could not extract date from: malformed.eml

📊 Summary:
✅ Successfully processed: 9
❌ Failed: 1
📄 Total files: 10
```

## Troubleshooting

### Common Issues

1. **Permission Errors**: Make sure you have write permissions to the files
2. **Date Parsing Failures**: Some emails may have malformed or missing Date headers
3. **Timezone Issues**: The script handles most timezone formats, but some unusual ones might not parse

### What to Check

- Ensure Python 3.6+ is installed
- Check that the .eml files are readable
- Verify file permissions allow modification
- Use verbose mode (`-v`) to see detailed processing information

### File Backup

**Important**: Always test with `--dry-run` first! While this script only modifies file timestamps (not content), it's good practice to:

1. Run a dry run first to see what will be changed
2. Consider backing up important email archives
3. Test on a small subset before processing large archives

## Performance Notes

- Processing speed depends on file count and disk I/O
- Large recursive operations may take time
- The script processes files sequentially (not in parallel)
- Expected rate: ~100-1000 files per minute depending on system

## Security Considerations

- The script only reads .eml file headers (first ~50 lines)
- Only file modification times are changed, not file content
- No network access is performed
- Uses standard Python libraries and system commands

## License

This script is provided as-is for personal use in managing email archives.
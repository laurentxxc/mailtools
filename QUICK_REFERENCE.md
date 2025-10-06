# Quick Reference: EML Date Setting Scripts

## 🚀 Quick Start

```bash
# Go to the directory with your scripts
cd /Users/lvt/Documents/MailArchive/Outlook

# Test on current directory (safe - no changes)
./set_eml_dates.sh -n

# Process current directory
./set_eml_dates.sh

# Process all years recursively with progress info
./set_eml_dates.sh -rv .
```

## 📁 Common Usage Patterns

### Single Directory
```bash
cd /path/to/emails/2024/Sent
/Users/lvt/Documents/MailArchive/Outlook/set_eml_dates.sh -v
```

### Entire Archive
```bash
# From the main archive directory
cd /Users/lvt/Documents/MailArchive/Outlook
./set_eml_dates.sh -rv .
```

### Mounted Archive (DMG)
```bash
./set_eml_dates.sh -rv "/Volumes/Messages 2007-2017"
```

## ⚡ Script Locations

- **Main Python Script**: `/Users/lvt/Documents/MailArchive/Outlook/set_eml_dates.py`
- **Shell Wrapper**: `/Users/lvt/Documents/MailArchive/Outlook/set_eml_dates.sh`
- **Documentation**: `/Users/lvt/Documents/MailArchive/Outlook/README_EML_DATES.md`

## 🔧 Key Options

| Option | Description |
|--------|-------------|
| `-n` or `--dry-run` | Preview changes without making them |
| `-r` or `--recursive` | Process subdirectories |
| `-v` or `--verbose` | Show detailed progress |
| `-h` or `--help` | Show help message |

## 📊 What It Does

✅ **Reads** the `Date:` header from each .eml file  
✅ **Sets** the file's modification date to match the email date  
✅ **Handles** various date formats and timezones  
✅ **Preserves** file content (only changes timestamps)  

## 🛡️ Safety Features

- **Always test with `-n` (dry run) first**
- Shows exactly what will be changed before doing it
- Only modifies file timestamps, never file content
- Gracefully handles malformed emails

## 📈 Expected Performance

- ~100-1000 files per minute
- Depends on disk speed and file count
- Sequential processing (one file at a time)

## 🚨 Important Notes

1. **Always run with `-n` first** to see what will happen
2. Make sure you have write permissions to the files
3. Some very old or malformed emails might not have parseable dates
4. The script is safe - it only changes file timestamps, never content
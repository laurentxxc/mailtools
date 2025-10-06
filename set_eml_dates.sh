#!/bin/bash

# Shell script wrapper for setting .eml file dates
# This script provides easy access to the Python script with common options

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/set_eml_dates.py"

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] [PATH]"
    echo ""
    echo "Set .eml file modification dates based on email Date headers"
    echo ""
    echo "OPTIONS:"
    echo "  -h, --help       Show this help message"
    echo "  -n, --dry-run    Show what would be done without making changes"
    echo "  -r, --recursive  Process directories recursively"
    echo "  -v, --verbose    Verbose output"
    echo ""
    echo "PATH:"
    echo "  Directory or file to process (default: current directory)"
    echo ""
    echo "EXAMPLES:"
    echo "  $0                           # Process current directory"
    echo "  $0 -n                        # Dry run on current directory"
    echo "  $0 -rv /path/to/emails       # Process recursively with verbose output"
    echo "  $0 -n -r .                   # Dry run recursively on current directory"
    echo "  $0 file.eml                  # Process single file"
    echo ""
}

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python script not found at $PYTHON_SCRIPT"
    exit 1
fi

# Parse command line arguments
ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -n|--dry-run)
            ARGS+=("--dry-run")
            shift
            ;;
        -r|--recursive)
            ARGS+=("--recursive")
            shift
            ;;
        -v|--verbose)
            ARGS+=("--verbose")
            shift
            ;;
        -*)
            echo "Unknown option $1"
            usage
            exit 1
            ;;
        *)
            ARGS+=("$1")
            shift
            ;;
    esac
done

# Execute the Python script with the arguments
python3 "$PYTHON_SCRIPT" "${ARGS[@]}"
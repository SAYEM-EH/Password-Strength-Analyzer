#!/bin/bash
# S4YEM.7KuroX Execution Script

if [ ! -d "venv" ]; then
    echo -e "\e[31m[!] Virtual environment not found. Please run ./install.sh first.\e[0m"
    exit 1
fi

source venv/bin/activate
python3 s4yem7kurox.py "$@"
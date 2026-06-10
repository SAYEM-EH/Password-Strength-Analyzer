#!/bin/bash
# S4YEM.7KuroX Installation Script

echo -e "\e[36m======================================================\e[0m"
echo -e "\e[36m  S4YEM.7KuroX Password Security Suite Installer\e[0m"
echo -e "\e[36m======================================================\e[0m"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "\e[31m[!] Python 3 is not installed. Please install Python 3.12+.\e[0m"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "\e[32m[+] Detected Python $PYTHON_VERSION\e[0m"

# Create virtual environment
echo -e "\e[33m[*] Creating virtual environment...\e[0m"
python3 -m venv venv

# Activate and install dependencies
echo -e "\e[33m[*] Activating virtual environment and installing dependencies...\e[0m"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo -e "\e[33m[*] Creating project directories...\e[0m"
mkdir -p reports logs

# Set permissions
chmod +x run.sh
chmod +x s4yem7kurox.py

echo -e "\e[36m======================================================\e[0m"
echo -e "\e[32m[+] Installation complete!\e[0m"
echo -e "\e[32m[+] Run the tool using: ./run.sh\e[0m"
echo -e "\e[36m======================================================\e[0m"
# Password-Strength-Analyzer





```text
███████╗ █████╗ ██╗   ██╗███████╗███╗   ███╗
██╔════╝██╔══██╗╚██╗ ██╔╝██╔════╝████╗ ████║
███████╗███████║ ╚████╔╝ █████╗  ██╔████╔██║
╚════██║██╔══██║  ╚██╔╝  ██╔══╝  ██║╚██╔╝██║
███████║██║  ██║   ██║   ███████╗██║ ╚═╝ ██║
╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
               S4YEM.7KuroX
```
                


![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)

![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=for-the-badge)

![OS](https://img.shields.io/badge/OS-Linux%20%7C%20macOS%20%7C%20Termux-purple?style=for-the-badge)



---



## 📖 Overview

**S4YEM.7KuroX** is a production-ready, offline password security toolkit. Designed with a sleek cyberpunk terminal interface, it provides enterprise-grade password analysis, cryptographically secure generation, brute-force time estimation, and **100% masked logging** to ensure your privacy.



---



## ⚡ Core Features



| Feature | Description |


|  **Strength Analyzer** | Assigns a 0–100 score and categorizes strength (Very Weak to Very Strong). |

|  **Secure Generator** | Uses Python's `secrets` module for cryptographically safe password creation. |

|  **Entropy Calculator** | Measures true mathematical randomness in bits. |

|  **Crack Time Estimator** | Human-readable estimates for Online, Offline, and High-End GPU attacks. |

|  **Pattern Detection** | Flags common passwords, dictionary words, keyboard sequences, and repeats. |

|  **Reporting System** | Export comprehensive analysis to `.txt` or `.json` formats. |

|  **Secure Logging** | Audit logs with **strict masking**. Sensitive data is *never* stored in plaintext. |



---



## 📥 Installation



1. **Clone the Repository:**

   ```bash

   https://github.com/SAYEM-EH/Password-Strength-Analyzer.git

   cd SAYEM.P7

   ```



2. **Run the Automated Installer:**

   This script creates a virtual environment, installs dependencies (`rich`, `colorama`), and sets up required directories.

   ```bash

   chmod +x install.sh

   ./install.sh

   ```

   *(For Termux users: Ensure you have run `pkg install python git` first).*



---



## 📝 Usage Guide



### Method 1: Interactive Terminal Menu (Recommended)

Launch the guided cyberpunk dashboard:

```bash

./run.sh

# or

python3 sayemp7.py

```



### Method 2: Command-Line Interface (CLI)

Perfect for quick checks or scripting:

```bash

# Analyze a specific password directly

./run.sh --password "MyS3cur3P@ssw0rd!"



# Generate a single 20-character secure password

./run.sh --generate --length 20



# View the built-in help menu

./run.sh --help

```



---



## Interactive Menu Walkthrough



When running the interactive mode, you will see a structured menu:

- **[01] Password Strength Analyzer**: Deep-dive analysis with scoring.

- **[02] Password Generator**: Customize length, character types, and quantity.

- **[03] Password Entropy Calculator**: View strength in bits.

- **[04] Security Recommendations**: Get actionable tips to improve weak passwords.

- **[05] Brute Force Estimator**: See crack times under different attack scenarios.

- **[06] Common Password Detection**: Checks against a built-in breached database.

- **[07] Dictionary Word Detection**: Identifies predictable dictionary words.

- **[08] Sequential Pattern Detection**: Flags keyboard walks (e.g., `qwerty`, `12345`).

- **[09] Repeated Character Detection**: Flags excessive repetition (e.g., `aaa`).

- **[10] Export TXT Report**: Saves the latest analysis to the `reports/` folder.

- **[11] Export JSON Report**: Saves analysis as structured JSON.

- **[12] View Security Logs**: Displays the last 10 entries of the masked audit log.

- **[13] About Tool**: Version info and project details.

- **[14] Help / Guide**: Displays the in-terminal quick guide.

- **[00] Exit**: Securely terminates the application.



---



## Security & Privacy Guarantee



1. **Zero Plaintext Logging**: The tool utilizes a custom `SecureLogger`. Any password processed is immediately masked (e.g., `P********d`) before being written to `logs/security_audit.log`.

2. **Cryptographic Generation**: Passwords are generated using Python's `secrets` module, which is designed for cryptography and is significantly more secure than the standard `random` module.

3. **100% Local Execution**: All analysis is performed locally on your machine. **No data is ever sent to external servers or APIs.**



---



## 🔧 Troubleshooting



| Issue | Solution |

| :--- | :--- |

| `ModuleNotFoundError: No module named 'rich'` | The virtual environment is not active. Run `source venv/bin/activate` or re-run `./install.sh`. |

| `Permission denied` when running `./run.sh` | Grant execution permissions: `chmod +x run.sh install.sh`. |

| Logs are not generating | Ensure the `logs/` directory exists and has write permissions (`chmod 755 logs/`). |



---



## Project Structure

```text

SAYEM.P7/

├── sayemp7.py             # Main Python application

├── common_passwords.txt   # Dictionary for common password detection

├── requirements.txt       # Python dependencies

├── install.sh             # Automated setup script

├── run.sh                 # Execution wrapper script

├── USER_MANUAL.txt        # Plain text user guide

├── README.md              # This documentation file

├── reports/               # Directory for exported TXT/JSON reports

└── logs/                  # Directory for secure, masked audit logs

```



---



## 📜 License

Distributed under the **MIT License**. See the `LICENSE` file for more information.



---



> **Developed with 💜 by SAYEM.P7**  

> *Stay Secure. Stay Anonymous.*

```



---


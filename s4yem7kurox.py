#!/usr/bin/env python3
"""
SAYEM.P7 Password Security Suite
Production-ready, error-free, cyberpunk-themed security toolkit.
"""

import os
import sys
import re
import json
import math
import secrets
import string
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# =============================================================================
# DEPENDENCY CHECK (Prevents ugly tracebacks)
# =============================================================================
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.markdown import Markdown
    from rich import box
except ImportError:
    print("\n[ERROR] Required library 'rich' is missing!")
    print("[FIX] Please run: pip install rich colorama\n")
    sys.exit(1)

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================
APP_NAME = "SAYEM.P7"
VERSION = "2.0.0"
BASE_DIR = Path(__file__).parent.resolve()
COMMON_PWD_FILE = BASE_DIR / "common_passwords.txt"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

BANNER = """
███████╗ █████╗ ██╗   ██╗███████╗███╗   ███╗
██╔════╝██╔══██╗╚██╗ ██╔╝██╔════╝████╗ ████║
███████╗███████║ ╚████╔╝ █████╗  ██╔████╔██║
╚════██║██╔══██║  ╚██╔╝  ██╔══╝  ██║╚██╔╝██║
███████║██║  ██║   ██║   ███████╗██║ ╚═╝ ██║
╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
               [bold bright_magenta]S4YEM.7KuroX[/bold bright_magenta]
         [dim]Advanced Password Security Kurox Protocol v{version}[/dim]
""".format(version=VERSION)

# =============================================================================
# LOGGER (Secure & Masked)
# =============================================================================
class SecureLogger:
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        log_file = self.log_dir / "security_audit.log"
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(APP_NAME)

    def mask(self, pwd: str) -> str:
        if not pwd: return "N/A"
        if len(pwd) <= 2: return '*' * len(pwd)
        return f"{pwd[0]}{'*' * (len(pwd) - 2)}{pwd[-1]}"

    def log(self, action: str, pwd: str = "", details: str = ""):
        msg = f"ACTION: {action} | TARGET: {self.mask(pwd)}"
        if details: msg += f" | DETAILS: {details}"
        self.logger.info(msg)

    def error(self, msg: str):
        self.logger.error(f"ERROR: {msg}")

# =============================================================================
# SECURITY ANALYZER
# =============================================================================
class Analyzer:
    def __init__(self, logger: SecureLogger):
        self.logger = logger
        self.common_pwds = self._load_common()

    def _load_common(self) -> set:
        try:
            if COMMON_PWD_FILE.exists():
                with open(COMMON_PWD_FILE, 'r', encoding='utf-8') as f:
                    return set(line.strip().lower() for line in f if line.strip())
        except Exception as e:
            self.logger.error(f"Load common passwords failed: {e}")
        return {"password", "123456", "12345678", "qwerty", "admin", "welcome"}

    def entropy(self, pwd: str) -> float:
        pool = 0
        if re.search(r'[a-z]', pwd): pool += 26
        if re.search(r'[A-Z]', pwd): pool += 26
        if re.search(r'\d', pwd): pool += 10
        if re.search(r'[^a-zA-Z0-9]', pwd): pool += 32
        return len(pwd) * math.log2(pool) if pool > 0 else 0.0

    def crack_time(self, entropy: float) -> Dict[str, str]:
        combos = 2 ** entropy
        rates = {
            "Online (100/sec)": 100,
            "Offline (10K/sec)": 10_000,
            "GPU Cluster (100B/sec)": 100_000_000_000
        }
        results = {}
        for scenario, rate in rates.items():
            secs = combos / rate
            if secs < 1: results[scenario] = "Instantly"
            elif secs < 60: results[scenario] = f"{secs:.1f} seconds"
            elif secs < 3600: results[scenario] = f"{secs/60:.1f} minutes"
            elif secs < 86400: results[scenario] = f"{secs/3600:.1f} hours"
            elif secs < 31536000: results[scenario] = f"{secs/86400:.1f} days"
            elif secs < 3153600000: results[scenario] = f"{secs/31536000:.1f} years"
            else: results[scenario] = f"{secs/31536000:.1e} years"
        return results

    def check_patterns(self, pwd: str) -> Dict[str, Any]:
        is_common = pwd.lower() in self.common_pwds
        dict_words = [w for w in ["password", "admin", "user", "login", "welcome", "dragon", "master"] if w in pwd.lower()]
        seq_patterns = [p for p in ['123', '234', '345', 'abc', 'qwe', 'asd', 'zxc'] if p in pwd.lower()]
        repeats = [m.group(0) for m in re.finditer(r'(.)\1{2,}', pwd)]
        
        return {
            "is_common": is_common,
            "dict_words": dict_words,
            "seq_patterns": seq_patterns,
            "repeats": repeats
        }

    def analyze(self, pwd: str) -> Dict[str, Any]:
        ent = self.entropy(pwd)
        score = min(100.0, (ent / 128.0) * 100.0)
        patterns = self.check_patterns(pwd)
        
        deductions = []
        if len(pwd) < 8: score -= 15; deductions.append("Length < 8")
        if patterns["is_common"]: score -= 40; deductions.append("Common password")
        if patterns["dict_words"]: score -= 20; deductions.append("Dictionary words")
        if patterns["seq_patterns"]: score -= 15; deductions.append("Sequential patterns")
        if patterns["repeats"]: score -= 10; deductions.append("Repeated chars")
        
        score = max(0.0, score)
        category = "Very Weak" if score <= 20 else "Weak" if score <= 40 else "Medium" if score <= 60 else "Strong" if score <= 80 else "Very Strong"
        
        return {"score": round(score, 1), "category": category, "entropy": round(ent, 2), "length": len(pwd), "deductions": deductions, "patterns": patterns}

    def recommendations(self, pwd: str) -> List[str]:
        recs = []
        if len(pwd) < 12: recs.append("Increase length to 12-16+ characters.")
        if not re.search(r'[A-Z]', pwd): recs.append("Add uppercase letters.")
        if not re.search(r'\d', pwd): recs.append("Add numbers.")
        if not re.search(r'[^a-zA-Z0-9]', pwd): recs.append("Add special symbols (!@#$%).")
        patterns = self.check_patterns(pwd)
        if patterns["is_common"] or patterns["dict_words"]: recs.append("Avoid common words or phrases.")
        if patterns["seq_patterns"]: recs.append("Avoid keyboard sequences (e.g., qwerty, 123).")
        if patterns["repeats"]: recs.append("Avoid repeating characters (e.g., aaa).")
        return recs if recs else ["Excellent! This password meets all security best practices."]

# =============================================================================
# GENERATOR & REPORTER
# =============================================================================
class Generator:
    def __init__(self, logger: SecureLogger):
        self.logger = logger

    def generate(self, length: int, upper: bool, lower: bool, digits: bool, symbols: bool, count: int) -> List[str]:
        pool = ""
        if lower: pool += string.ascii_lowercase
        if upper: pool += string.ascii_uppercase
        if digits: pool += string.digits
        if symbols: pool += string.punctuation
        if not pool: raise ValueError("At least one character type must be selected.")
        
        pwds = [''.join(secrets.choice(pool) for _ in range(length)) for _ in range(count)]
        for p in pwds: self.logger.log("PASSWORD_GENERATED", p, f"Len:{length}")
        return pwds

class Reporter:
    def __init__(self, reports_dir: Path, logger: SecureLogger):
        self.reports_dir = reports_dir
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger
        self.history: List[Dict] = []

    def add_history(self, pwd: str, analysis: Dict):
        self.history.append({
            "time": datetime.now().isoformat(),
            "target": self.logger.mask(pwd),
            "score": analysis["score"],
            "category": analysis["category"]
        })
        self.logger.log("HISTORY_UPDATED", pwd, f"Score: {analysis['score']}")

    def export_txt(self, pwd: str, analysis: Dict, recs: List[str], times: Dict[str, str]) -> str:
        filepath = self.reports_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"SAYEM.P7 Security Report | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n")
            f.write(f"Target: {self.logger.mask(pwd)}\n")
            f.write(f"Score: {analysis['score']}/100 ({analysis['category']})\n")
            f.write(f"Entropy: {analysis['entropy']} bits | Length: {analysis['length']}\n\n")
            f.write("CRACK TIMES:\n" + "\n".join(f"  - {k}: {v}" for k, v in times.items()) + "\n\n")
            f.write("RECOMMENDATIONS:\n" + "\n".join(f"  {i}. {r}" for i, r in enumerate(recs, 1)) + "\n")
        self.logger.log("EXPORT_TXT", pwd, str(filepath))
        return str(filepath)

    def export_json(self, pwd: str, analysis: Dict, recs: List[str], times: Dict[str, str]) -> str:
        filepath = self.reports_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        data = {
            "tool": APP_NAME, "version": VERSION, "timestamp": datetime.now().isoformat(),
            "target_masked": self.logger.mask(pwd), "analysis": analysis,
            "crack_times": times, "recommendations": recs
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        self.logger.log("EXPORT_JSON", pwd, str(filepath))
        return str(filepath)

# =============================================================================
# MAIN APPLICATION
# =============================================================================
class SAYEMP7App:
    def __init__(self):
        self.console = Console()
        self.logger = SecureLogger(LOGS_DIR)
        self.analyzer = Analyzer(self.logger)
        self.generator = Generator(self.logger)
        self.reporter = Reporter(REPORTS_DIR, self.logger)
        self.current_pwd = ""
        self.current_analysis = {}

    def _get_color(self, score: float) -> str:
        if score <= 20: return "red"
        if score <= 40: return "yellow"
        if score <= 60: return "bright_yellow"
        if score <= 80: return "bright_blue"
        return "green"

    def _get_pwd(self, prompt: str = "Enter password") -> str:
        pwd = Prompt.ask(f"[bold magenta]{prompt}[/bold magenta]", password=True)
        if not pwd:
            self.console.print("[red]Error: Password cannot be empty.[/red]")
            return self._get_pwd(prompt)
        return pwd

    def run(self):
        self.console.print(Panel(BANNER, border_style="cyan", expand=False))
        
        while True:
            # Bulletproof Menu System using Rich Table (No markup errors)
            table = Table(show_header=False, box=box.DOUBLE, border_style="cyan", title="[bold bright_magenta] MAIN MENU [/bold bright_magenta]")
            table.add_column("Opt", justify="right", style="bold magenta", width=4)
            table.add_column("Feature", style="cyan")
            table.add_column("Opt", justify="right", style="bold magenta", width=4)
            table.add_column("Feature", style="cyan")
            
            menu_items = [
                ("01", "Password Strength Analyzer", "08", "Sequential Pattern Detection"),
                ("02", "Password Generator", "09", "Repeated Character Detection"),
                ("03", "Password Entropy Calculator", "10", "Export TXT Report"),
                ("04", "Security Recommendations", "11", "Export JSON Report"),
                ("05", "Brute Force Crack Estimator", "12", "View Security Logs"),
                ("06", "Common Password Detection", "13", "About Tool"),
                ("07", "Dictionary Word Detection", "14", "Help / Guide"),
                ("00", "[bold red]Exit Application[/bold red]", "", "")
            ]
            for row in menu_items:
                table.add_row(row[0], row[1], row[2], row[3])
            
            self.console.print(table)
            choice = Prompt.ask("\n[bold bright_magenta]Select an option (00-14)[/bold bright_magenta]", default="0")

            try:
                if choice == "1":
                    pwd = self._get_pwd()
                    self.current_pwd = pwd
                    with Progress(SpinnerColumn(), TextColumn("[bold blue]Analyzing...[/bold blue]"), transient=True) as progress:
                        progress.add_task("Analyzing", total=None)
                        self.current_analysis = self.analyzer.analyze(pwd)
                    
                    self.logger.log("ANALYZED", pwd, f"Score: {self.current_analysis['score']}")
                    self.reporter.add_history(pwd, self.current_analysis)
                    
                    res_table = Table(title="Analysis Results", border_style="magenta")
                    res_table.add_column("Metric", style="cyan"); res_table.add_column("Value", style="bright_blue")
                    res_table.add_row("Score", f"{self.current_analysis['score']}/100")
                    res_table.add_row("Category", f"[bold {self._get_color(self.current_analysis['score'])}]{self.current_analysis['category']}[/bold]")
                    res_table.add_row("Entropy", f"{self.current_analysis['entropy']} bits")
                    res_table.add_row("Length", str(self.current_analysis['length']))
                    self.console.print(res_table)

                elif choice == "2":
                    self.console.print("[bold cyan]--- Password Generator ---[/bold cyan]")
                    length = int(Prompt.ask("Length", default="16"))
                    upper = Confirm.ask("Uppercase (A-Z)?", default=True)
                    lower = Confirm.ask("Lowercase (a-z)?", default=True)
                    digits = Confirm.ask("Numbers (0-9)?", default=True)
                    symbols = Confirm.ask("Symbols (!@#$)?", default=True)
                    count = int(Prompt.ask("Quantity", default="1"))
                    
                    pwds = self.generator.generate(length, upper, lower, digits, symbols, count)
                    gen_table = Table(title="Generated Passwords", border_style="green")
                    gen_table.add_column("#", style="cyan"); gen_table.add_column("Password", style="bright_magenta")
                    for i, p in enumerate(pwds, 1): gen_table.add_row(str(i), p)
                    self.console.print(gen_table)

                elif choice == "3":
                    pwd = self._get_pwd()
                    ent = self.analyzer.entropy(pwd)
                    self.console.print(f"\n[bold cyan]Entropy:[/bold cyan] [bright_magenta]{ent:.2f} bits[/bright_magenta]")

                elif choice == "4":
                    pwd = self._get_pwd()
                    recs = self.analyzer.recommendations(pwd)
                    self.console.print("\n[bold cyan]--- Recommendations ---[/bold cyan]")
                    for i, r in enumerate(recs, 1): self.console.print(f"  [magenta]▶[/magenta] {r}")

                elif choice == "5":
                    pwd = self._get_pwd()
                    times = self.analyzer.crack_time(self.analyzer.entropy(pwd))
                    t_table = Table(title="Crack Time Estimates", border_style="bright_blue")
                    t_table.add_column("Attack Vector", style="cyan"); t_table.add_column("Time", style="magenta")
                    for k, v in times.items(): t_table.add_row(k, v)
                    self.console.print(t_table)

                elif choice == "6":
                    pwd = self._get_pwd()
                    is_common = self.analyzer.check_patterns(pwd)["is_common"]
                    self.console.print(f"Result: [{'red' if is_common else 'green'}]{'FOUND in common lists' if is_common else 'NOT FOUND'}[/]")

                elif choice == "7":
                    pwd = self._get_pwd()
                    words = self.analyzer.check_patterns(pwd)["dict_words"]
                    self.console.print(f"Result: [{'red' if words else 'green'}]{', '.join(words) if words else 'No dictionary words detected'}[/]")

                elif choice == "8":
                    pwd = self._get_pwd()
                    seqs = self.analyzer.check_patterns(pwd)["seq_patterns"]
                    self.console.print(f"Result: [{'red' if seqs else 'green'}]{', '.join(seqs) if seqs else 'No sequential patterns detected'}[/]")

                elif choice == "9":
                    pwd = self._get_pwd()
                    reps = self.analyzer.check_patterns(pwd)["repeats"]
                    self.console.print(f"Result: [{'red' if reps else 'green'}]{', '.join(reps) if reps else 'No repeated characters detected'}[/]")

                elif choice == "10":
                    if not self.current_pwd: self.current_pwd = self._get_pwd("Enter password to export"); self.current_analysis = self.analyzer.analyze(self.current_pwd)
                    path = self.reporter.export_txt(self.current_pwd, self.current_analysis, self.analyzer.recommendations(self.current_pwd), self.analyzer.crack_time(self.current_analysis["entropy"]))
                    self.console.print(f"\n[green]✓ Exported to:[/green] [bold cyan]{path}[/bold cyan]")

                elif choice == "11":
                    if not self.current_pwd: self.current_pwd = self._get_pwd("Enter password to export"); self.current_analysis = self.analyzer.analyze(self.current_pwd)
                    path = self.reporter.export_json(self.current_pwd, self.current_analysis, self.analyzer.recommendations(self.current_pwd), self.analyzer.crack_time(self.current_analysis["entropy"]))
                    self.console.print(f"\n[green]✓ Exported to:[/green] [bold cyan]{path}[/bold cyan]")

                elif choice == "12":
                    log_file = LOGS_DIR / "security_audit.log"
                    if not log_file.exists():
                        self.console.print("[yellow]No logs found yet.[/yellow]")
                    else:
                        self.console.print("\n[bold cyan]--- Recent Logs (Masked) ---[/bold cyan]")
                        with open(log_file, 'r', encoding='utf-8') as f:
                            for line in f.readlines()[-10:]: self.console.print(f"  [dim]{line.strip()}[/dim]")

                elif choice == "13":
                    self.console.print(Panel(f"[bold cyan]{APP_NAME}[/bold cyan] v{VERSION}\nA production-ready password security toolkit.\nSecure. Local. Masked Logging.", border_style="magenta", expand=False))

                elif choice == "14":
                    help_md = """
# [bold bright_magenta]SAYEM.P7 Help Guide[/bold bright_magenta]
- **Options 1-9**: Perform various security checks on a password.
- **Options 10-11**: Save your latest analysis to a file.
- **Option 12**: View the secure, masked audit log.
- **CLI Usage**: `python3 sayemp7.py --password "YourPass123!"` or `--generate --length 16`
                    """
                    self.console.print(Panel(Markdown(help_md), border_style="cyan", expand=False))

                elif choice == "0":
                    self.console.print("\n[bold green]Shutting down S4YEM.7KuroX securely. Goodbye.[/bold green]")
                    self.logger.log("APP_EXIT")
                    break
                else:
                    self.console.print("[red]Invalid option. Please select 00-14.[/red]")
            
            except KeyboardInterrupt:
                self.console.print("\n[bold yellow]Interrupted. Exiting safely.[/bold yellow]")
                self.logger.log("APP_EXIT_INTERRUPTED")
                break
            except Exception as e:
                self.logger.error(f"Unhandled exception: {e}")
                self.console.print(f"[red]An unexpected error occurred: {e}[/red]")

def ensure_setup():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    if not COMMON_PWD_FILE.exists():
        with open(COMMON_PWD_FILE, 'w', encoding='utf-8') as f:
            f.write("password\n123456\n12345678\nqwerty\nadmin\nwelcome\niloveyou\nsunshine\nprincess\nfootball\n")

if __name__ == "__main__":
    ensure_setup()
    parser = argparse.ArgumentParser(description="SAYEM.P7 Password Security Suite")
    parser.add_argument('-p', '--password', type=str, help='Password to analyze directly')
    parser.add_argument('-g', '--generate', action='store_true', help='Generate a secure password and exit')
    parser.add_argument('-l', '--length', type=int, default=16, help='Length for generated password')
    args = parser.parse_args()

    app = SAYEMP7App()
    if args.generate:
        try:
            pwds = app.generator.generate(args.length, True, True, True, True, 1)
            app.console.print(f"[bold green]Generated:[/bold green] [magenta]{pwds[0]}[/magenta]")
        except Exception as e:
            app.console.print(f"[red]Error: {e}[/red]")
    elif args.password:
        app.current_pwd = args.password
        app.current_analysis = app.analyzer.analyze(args.password)
        app.console.print(f"[bold cyan]Score:[/bold cyan] {app.current_analysis['score']}/100 ({app.current_analysis['category']})")
    else:
        app.run()

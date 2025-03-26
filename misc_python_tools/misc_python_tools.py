from datetime import datetime
import pkg_resources
import subprocess
import threading
import atexit
import time
import sys


class Logger:
    def __init__(self):
        self.text = ""
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
        self.log_interval = None
        self.show_log_time = False
        atexit.register(self.stop)
        self.start()

    def set_log_interval(self, log_interval):
        self.log_interval = log_interval
        self.stop()
        self.start()

    def flush(self):
        if self.text:
            sys.stdout.write(self.text)
            sys.stdout.flush()
            self.text = ""

    def write(self, text: str):
        if self.show_log_time:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text = f"[{current_time}] {text}"
        with self.lock:
            self.text += text + "\n"

    def _run(self):
        while self.running:
            time.sleep(self.log_interval)
            with self.lock:
                self.flush()

    def start(self):
        if self.log_interval is not None and not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.flush()


def clearLines(numLines):
    """
    Clears the last numLines lines

    print("\033[A", end="\r") # Go up one line

    print("\033[K", end="\r") # Clear current line
    """
    sys.stdout.write("\033[A\033[K" * numLines)
    sys.stdout.flush()


def color_text(r, g, b, text: str):
    # Using 38 for foreground color and 48 for background color
    color_code = f"\033[38;2;{r};{g};{b}m"
    color_reset_code = "\033[0m"

    return f"{color_code}{text}{color_reset_code}"


def log(text: str):
    logger.write(text)


def log_bad(text: str):
    text = color_text(255, 0, 0, text)
    log(text)


def log_sys(text: str):
    text = color_text(50, 255, 255, text)
    log(text)


def log_good(text: str):
    text = color_text(0, 255, 0, text)
    log(text)


def log_clear(numLines):
    """
    Clears the last numLines lines

    print("\033[A", end="\r") # Go up one line

    print("\033[K", end="\r") # Clear current line
    """
    logger.write("\033[A\033[K" * numLines)


def upgrade_all_packages():
    # Get the list of all installed packages
    print(f"Getting installed packages")
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]
    for item in installed_packages:
        print(f"  {item}")
    print(f"Found {len(installed_packages):,} packages")

    # Upgrade each package
    print(f"Upgrading packages")
    successful_upgrades = 0
    for package in installed_packages:
        try:
            subprocess.run(["pip", "install", "--upgrade", package], check=True)
        except subprocess.CalledProcessError as e:
            continue
        successful_upgrades += 1

    print(f"{successful_upgrades:,}/{len(installed_packages):,} packages upgraded")


logger = Logger()

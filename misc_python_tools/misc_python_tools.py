from datetime import datetime
import threading
import atexit
import time
import sys

config = {"log_time": False, "log_interval": None}


class Logger:
    def __init__(self):
        self.text = ""
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
        atexit.register(self.stop)
        self.start()

    def write(self, text: str):
        with self.lock:
            self.text += text + "\n"

    def _run(self):
        while self.running:
            time.sleep(config["log_interval"])
            with self.lock:
                if self.text:
                    sys.stdout.write(self.text)
                    sys.stdout.flush()
                    self.text = ""

    def start(self):
        if config["log_interval"] is not None and not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()


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
    if config["log_time"]:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = f"[{current_time}] {text}"
    logger.write(text + "\n")


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
    import subprocess

    # Get the list of installed packages using pip freeze
    print(f"Getting installed packages")
    installed_packages = subprocess.check_output(["pip", "freeze"])
    installed_packages = installed_packages.decode("utf-8").splitlines()

    # Extract only the package names (ignoring version numbers)
    package_names = [
        pkg.split("==")[0] for pkg in installed_packages if not pkg.startswith("-e ")
    ]

    # Upgrade all packages using pip
    print(f"Upgrading packages")
    try:
        subprocess.run(
            ["python", "-m", "pip", "install", "--upgrade"] + package_names, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")
        return

    print(f"{len(package_names):,} packages upgraded")


logger = Logger()

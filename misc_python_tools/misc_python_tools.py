from datetime import datetime
import sys

config = {"log_time": False}


def clearLines(numLines):
    """
    Clears the last numLines lines

    print("\033[A", end="\r") # Go up one line

    print("\033[K", end="\r") # Clear current line
    """
    for i in range(numLines):
        sys.stdout.write("\033[A\033[K")
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
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def log_bad(text: str):
    text = color_text(255, 0, 0, text)
    log(text)


def log_sys(text: str):
    text = color_text(50, 255, 255, text)
    log(text)


def log_good(text: str):
    text = color_text(0, 255, 0, text)
    log(text)

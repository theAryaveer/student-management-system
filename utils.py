# ─────────────────────────────────────────────
#  HELPER UTILITIES
# ─────────────────────────────────────────────

import os
import sys

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("\033[1;33m" + "=" * 70 + "\033[0m")
    print("\033[1;34m" + "        STUDENT MANAGEMENT SYSTEM".center(70) + "\033[0m")
    print("\033[1;33m" + "=" * 70 + "\033[0m")

def header(title):
    clear()
    banner()
    print("\033[1;33m" + "=" * 70 + "\033[0m")
    print("\033[1;34m" + f"  {title.upper()}".center(70) + "\033[0m")
    print("\033[1;33m" + "=" * 70 + "\033[0m")

def pause():
    input("\n  Press Enter to continue...")

def divider():
    print("  " + "-" * 66)

def grade_from_percent(pct):
    if pct >= 90: return "A+"
    if pct >= 80: return "A"
    if pct >= 70: return "B"
    if pct >= 60: return "C"
    if pct >= 50: return "D"
    return "F"

def safe_str(value, default="N/A"):
    """Convert a value to string, replacing None with a default."""
    if value is None:
        return default
    return str(value)

def masked_input(prompt="  Enter Password : "):
    """Read password input showing * for each character typed."""
    print(prompt, end="", flush=True)
    password = []

    if os.name == "nt":
        # Windows: use msvcrt for character-by-character input
        import msvcrt
        while True:
            ch = msvcrt.getch()
            if ch in (b'\r', b'\n'):       # Enter key
                print()
                break
            elif ch == b'\x08':            # Backspace
                if password:
                    password.pop()
                    # Erase the last * on screen
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            elif ch == b'\x03':            # Ctrl+C
                raise KeyboardInterrupt
            else:
                password.append(ch.decode('utf-8', errors='replace'))
                sys.stdout.write('*')
                sys.stdout.flush()
    else:
        # Unix/Mac: use termios
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ('\r', '\n'):      # Enter
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                    break
                elif ch == '\x7f' or ch == '\x08':  # Backspace
                    if password:
                        password.pop()
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                elif ch == '\x03':          # Ctrl+C
                    raise KeyboardInterrupt
                else:
                    password.append(ch)
                    sys.stdout.write('*')
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return "".join(password)

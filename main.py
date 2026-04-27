#!/usr/bin/env python3
# SnapSpammer - main.py (TURBO EDITION)
import os, sys, time, json, platform, webbrowser, urllib.request, threading, itertools
from pathlib import Path
from colorama import Fore, Back, Style, init
init(autoreset=True)
try:
    import pyautogui, keyboard
    pyautogui.FAILSAFE = False  # Disable failsafe for maximum speed
    pyautogui.PAUSE = 0  # Remove default pause between actions
except Exception:
    pyautogui = None
    keyboard = None

# ----------------------------------------------------------------------
# Default Settings - Smooth & Reliable
# ----------------------------------------------------------------------
DEFAULT_SETTINGS = {
    "loop_delay": 0.15,      # Normal speed
    "click_delay": 0.25,     # Normal clicks
    "position_delay": 0.3,
    "shortcut_count": 1,
    "positions": {},
    "positions_spam": {},
    "auto_open_readme": True,
    "readme_url": "https://github.com/OGSMrgbbn/SnapSpammer/blob/main/readme.md",
    "snapchat_login": "https://web.snapchat.com/",
    # Message spam settings
    "spam_message": "",
    "spam_count": 50,
    "spam_delay": 0.2,
    "turbo_mode": False,     # Normal mode by default
}

BASE_DIR = Path(__file__).parent.resolve()
SETTINGS_PATH = BASE_DIR / "settings.json"
SNAP_IMAGE = BASE_DIR / "snapscore_100k.png"

# RGB Color Palette
SNAP_Y = Fore.YELLOW
SNAP_ACC = Fore.LIGHTYELLOW_EX
SNAP_W = Fore.WHITE
SNAP_R = Fore.LIGHTRED_EX
SNAP_G = Fore.LIGHTGREEN_EX
SNAP_C = Fore.LIGHTCYAN_EX
SNAP_M = Fore.LIGHTMAGENTA_EX
SNAP_B = Fore.LIGHTBLUE_EX

# Rainbow colors for animations
RAINBOW = [Fore.RED, Fore.LIGHTYELLOW_EX, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
FIRE = [Fore.RED, Fore.LIGHTYELLOW_EX, Fore.YELLOW, Fore.WHITE]
CYBER = [Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.WHITE, Fore.LIGHTGREEN_EX]

# ----------------------------------------------------------------------
# Version handling
# ----------------------------------------------------------------------
VERSION_FILE = BASE_DIR / "version.txt"
VERSION = VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else "0.0.0"
VERSION_URL = "https://raw.githubusercontent.com/OGSMrgbbn/SnapSpammer/main/version.txt"
RELEASES_URL = "https://github.com/OGSMrgbbn/SnapSpammer/releases"

def _parse_version(value):
    """Parse semantic-ish versions like 1.0.3 into comparable tuples."""
    parts = []
    for part in str(value).strip().split('.'):
        try:
            parts.append(int(part))
        except ValueError:
            # Keep non-numeric suffixes from breaking checks.
            break
    return tuple(parts)

def check_version():
    """Force update only when local version is older than remote."""
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=5) as resp:
            remote = resp.read().decode('utf-8').strip()

        local_v = _parse_version(VERSION)
        remote_v = _parse_version(remote)

        if remote_v and local_v and local_v < remote_v:
            pretty_print("OUTDATED VERSION!", SNAP_W)
            pretty_print(f"Local : {VERSION}", SNAP_W)
            pretty_print(f"Latest: {remote}", SNAP_W)
            pretty_print("You MUST download the new version to continue.", SNAP_W)
            pretty_print("Opening the download page...", SNAP_ACC)
            webbrowser.open(RELEASES_URL)
            input("Press ENTER to exit...")
            sys.exit(0)
        else:
            pretty_print(f"Version up-to-date: {VERSION}", SNAP_ACC)
            return True
    except Exception as e:
        pretty_print(f"Could not check version (network error): {e}", SNAP_W)
        pretty_print("Continuing offline.", SNAP_W)
        return True

# ----------------------------------------------------------------------
# Utility Functions - ENHANCED
# ----------------------------------------------------------------------
def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def title(msg):
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(msg)
        except:
            pass
    else:
        sys.stdout.write(f"\33]0;{msg}\a")
        sys.stdout.flush()

def pretty_print(text, color=SNAP_Y, delay=0.001):
    """Ultra-fast animated text"""
    for ch in str(text):
        sys.stdout.write(color + ch + Style.RESET_ALL)
        sys.stdout.flush()
        if delay > 0:
            time.sleep(delay)
    print("")

def rainbow_print(text, delay=0.001):
    """RGB rainbow text effect"""
    for i, ch in enumerate(str(text)):
        color = RAINBOW[i % len(RAINBOW)]
        sys.stdout.write(color + ch + Style.RESET_ALL)
        sys.stdout.flush()
        if delay > 0:
            time.sleep(delay)
    print("")

def fire_print(text, delay=0.001):
    """Fire gradient text effect"""
    for i, ch in enumerate(str(text)):
        color = FIRE[i % len(FIRE)]
        sys.stdout.write(color + ch + Style.RESET_ALL)
        sys.stdout.flush()
        if delay > 0:
            time.sleep(delay)
    print("")

def cyber_print(text, delay=0.001):
    """Cyber/Matrix style text"""
    for i, ch in enumerate(str(text)):
        color = CYBER[i % len(CYBER)]
        sys.stdout.write(color + ch + Style.RESET_ALL)
        sys.stdout.flush()
        if delay > 0:
            time.sleep(delay)
    print("")

def instant_print(text, color=SNAP_Y):
    """Instant print without animation"""
    print(color + str(text) + Style.RESET_ALL)

def progress_bar(current, total, width=40, color=SNAP_G):
    """Animated progress bar"""
    percent = current / total
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    sys.stdout.write(f"\r{color}[{bar}] {percent*100:.1f}% ({current}/{total}){Style.RESET_ALL}")
    sys.stdout.flush()

def spinner_animation(duration=1.0, text="Loading"):
    """Spinning animation"""
    spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{SNAP_C}{spinners[i % len(spinners)]} {text}...{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()

def load_settings():
    if SETTINGS_PATH.exists():
        try:
            with open(SETTINGS_PATH, "r") as fh:
                loaded = json.load(fh)
            # Merge with DEFAULT_SETTINGS to ensure all keys exist
            settings = DEFAULT_SETTINGS.copy()
            settings.update(loaded)
            return settings
        except:
            pretty_print("Corrupted settings.json – using defaults.", SNAP_W)
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def save_settings(data):
    try:
        with open(SETTINGS_PATH, "w") as fh:
            json.dump(data, fh, indent=2)
        return True
    except:
        return False

# ----------------------------------------------------------------------
# EPIC ASCII Banner
# ----------------------------------------------------------------------
BANNER_LINES = [
    "░██████╗███╗░░██╗░█████╗░██████╗░░██████╗██████╗░░█████╗░███╗░░░███╗███╗░░░███╗███████╗██████╗░",
    "██╔════╝████╗░██║██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗████╗░████║████╗░████║██╔════╝██╔══██╗",
    "╚█████╗░██╔██╗██║███████║██████╔╝╚█████╗░██████╔╝███████║██╔████╔██║██╔████╔██║█████╗░░██████╔╝",
    "░╚═══██╗██║╚████║██╔══██║██╔═══╝░░╚═══██╗██╔═══╝░██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝░░██╔══██╗",
    "██████╔╝██║░╚███║██║░░██║██║░░░░░██████╔╝██║░░░░░██║░░██║██║░╚═╝░██║██║░╚═╝░██║███████╗██║░░██║",
    "╚═════╝░╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░░░░╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝"
]

TURBO_ART = """
    ⚡ T U R B O   M O D E   A C T I V E ⚡
"""

def print_banner():
    """Epic rainbow animated banner"""
    print("")
    for i, line in enumerate(BANNER_LINES):
        color = RAINBOW[i % len(RAINBOW)]
        print(color + line + Style.RESET_ALL)
        time.sleep(0.02)
    print("")
    fire_print("    ⚡ TURBO EDITION ⚡  |  by mrgbbn  |  ANONYMOUS MODE", delay=0.002)
    print(SNAP_C + "    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    print("")

def boot_sequence():
    """Epic boot sequence with animations"""
    clear()
    
    # Glitch intro
    glitch_text = ">>> INITIALIZING SNAPSPAMMER <<<"
    for _ in range(3):
        for color in [SNAP_R, SNAP_G, SNAP_B]:
            sys.stdout.write(f"\r{color}{glitch_text}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.05)
    print("")
    print("")
    
    # Loading bar animation
    steps = [
        ("Initializing TURBO engine", SNAP_R),
        ("Loading stealth protocols", SNAP_M),
        ("Calibrating click precision", SNAP_C),
        ("Optimizing spam algorithms", SNAP_G),
        ("Bypassing rate limits", SNAP_Y),
        ("SYSTEM READY", SNAP_G),
    ]
    
    for text, color in steps:
        sys.stdout.write(f"{color}⚡ {text}")
        sys.stdout.flush()
        for _ in range(3):
            time.sleep(0.1)
            sys.stdout.write(f"{color}.")
            sys.stdout.flush()
        print(f" {SNAP_G}✓{Style.RESET_ALL}")
        time.sleep(0.05)
    
    print("")
    rainbow_print("████████████████████████████████████████████████████", delay=0.001)
    fire_print("   🔥 SNAPSPAMMER TURBO - READY TO DESTROY 🔥", delay=0.002)
    rainbow_print("████████████████████████████████████████████████████", delay=0.001)
    time.sleep(0.5)
    clear()

# ----------------------------------------------------------------------
# SnapBot Class (Snap Sending) - TURBO EDITION
# ----------------------------------------------------------------------
class SnapBot:
    def __init__(self, settings):
        self.settings = settings
        self.sent_snaps = 0
        self.first_try = True
        self.start_time = None

    def get_positions(self):
        if pyautogui is None or keyboard is None:
            pretty_print("pyautogui/keyboard missing; cannot capture positions.", SNAP_W)
            return
        rainbow_print("═══ POSITION CAPTURE MODE ═══", delay=0.002)
        print("")
        cyber_print("Move mouse to Camera button, press Y", delay=0.001)
        while not keyboard.is_pressed("y"):
            time.sleep(0.02)
        self.settings['positions']['switch_to_camera'] = pyautogui.position()
        instant_print("✓ Camera position saved!", SNAP_G)
        time.sleep(0.3)
        
        cyber_print("Move to Send To, press Y", delay=0.001)
        while not keyboard.is_pressed("y"):
            time.sleep(0.02)
        self.settings['positions']['send_to'] = pyautogui.position()
        instant_print("✓ Send To position saved!", SNAP_G)
        time.sleep(0.3)
        
        cyber_print("Move to Shortcut, press Y", delay=0.001)
        while not keyboard.is_pressed("y"):
            time.sleep(0.02)
        self.settings['positions']['shortcut'] = pyautogui.position()
        instant_print("✓ Shortcut position saved!", SNAP_G)
        time.sleep(0.3)
        
        cyber_print("Move to Select All, press Y", delay=0.001)
        while not keyboard.is_pressed("y"):
            time.sleep(0.02)
        self.settings['positions']['select_all'] = pyautogui.position()
        instant_print("✓ Select All position saved!", SNAP_G)
        print("")
        fire_print("🔥 ALL POSITIONS LOCKED IN! 🔥", delay=0.002)

    def estimate_time(self, snaps_target):
        loop = float(self.settings.get('loop_delay', 0.05))
        clicks = 6
        click_delay = float(self.settings.get('click_delay', 0.08))
        per_snap = (clicks * click_delay) + loop
        return per_snap * snaps_target

    def send_snap(self, started_time, shortcut_user_count):
        pos = self.settings.get('positions', {})
        if pyautogui is None:
            instant_print("⚠ pyautogui not installed!", SNAP_R)
            return False
        required = ['switch_to_camera', 'send_to', 'shortcut', 'select_all']
        if not all(k in pos for k in required):
            instant_print("⚠ Positions missing. Configure first! (Option 4)", SNAP_R)
            return False
        
        delay = self.settings.get('click_delay', 0.25)
        
        # Smooth clicking sequence
        pyautogui.moveTo(pos['switch_to_camera'])
        if self.first_try:
            pyautogui.click()
            self.first_try = False
        time.sleep(delay)
        pyautogui.click()
        time.sleep(delay)
        pyautogui.moveTo(pos['send_to'])
        pyautogui.click()
        time.sleep(delay)
        pyautogui.moveTo(pos['shortcut'])
        pyautogui.click()
        time.sleep(delay)
        pyautogui.moveTo(pos['select_all'])
        pyautogui.click()
        time.sleep(delay)
        pyautogui.moveTo(pos['send_to'])
        pyautogui.click()
        
        self.sent_snaps += 1
        total_snaps = self.sent_snaps * shortcut_user_count
        elapsed = int(time.time() - started_time)
        rate = total_snaps / max(elapsed, 1)
        
        # Live stats with color coding
        color = SNAP_G if rate > 1 else SNAP_Y
        sys.stdout.write(f"\r{color}⚡ Batch #{self.sent_snaps} | {total_snaps} snaps | {elapsed}s | {rate:.1f} snaps/sec{Style.RESET_ALL}   ")
        sys.stdout.flush()
        return True

# ----------------------------------------------------------------------
# Message Spammer Class - TURBO EDITION
# ----------------------------------------------------------------------
class MessageSpammer:
    def __init__(self, settings):
        self.settings = settings
        self.sent_messages = 0

    def get_spam_positions(self):
        if pyautogui is None or keyboard is None:
            instant_print("⚠ pyautogui/keyboard missing!", SNAP_R)
            return
        rainbow_print("═══ SPAM POSITION CAPTURE ═══", delay=0.002)
        print("")
        cyber_print("Move mouse to target USER PROFILE, press Y", delay=0.001)
        while not keyboard.is_pressed("y"):
            time.sleep(0.02)
        self.settings['positions_spam']['user_profile'] = pyautogui.position()
        instant_print("✓ User profile position saved!", SNAP_G)
        time.sleep(0.3)
        
        cyber_print("Move to MESSAGE INPUT field, press Y", delay=0.001)
        while not keyboard.is_pressed("y"):
            time.sleep(0.02)
        self.settings['positions_spam']['input_field'] = pyautogui.position()
        instant_print("✓ Input field position saved!", SNAP_G)
        time.sleep(0.3)
        
        cyber_print("Move to SEND BUTTON, press Y", delay=0.001)
        while not keyboard.is_pressed("y"):
            time.sleep(0.02)
        self.settings['positions_spam']['send_button'] = pyautogui.position()
        instant_print("✓ Send button position saved!", SNAP_G)
        print("")
        fire_print("🔥 SPAM POSITIONS LOCKED! 🔥", delay=0.002)

    def spam_messages(self, started_time):
        pos = self.settings.get('positions_spam', {})
        required = ['user_profile', 'input_field', 'send_button']
        if not all(k in pos for k in required):
            instant_print("⚠ Spam positions missing. Configure first! (Option 5)", SNAP_R)
            return
        message = self.settings.get('spam_message', '').strip()
        if not message:
            instant_print("⚠ No message set. Configure in Settings! (Option 3)", SNAP_R)
            return
        count = self.settings.get('spam_count', 50)
        delay = self.settings.get('spam_delay', 0.2)
        click_delay = self.settings.get('click_delay', 0.25)

        print("")
        fire_print(f"🚀 SPAM STARTED - {count} MESSAGES 🚀", delay=0.002)
        print("")
        
        for i in range(1, count + 1):
            if keyboard and keyboard.is_pressed('f6'):
                print("")
                instant_print("⏹ Spam stopped by user.", SNAP_Y)
                break
            
            # Smooth spam sequence
            pyautogui.click(pos['input_field'])
            time.sleep(click_delay)
            pyautogui.write(message, interval=0.02)
            time.sleep(click_delay)
            pyautogui.click(pos['send_button'])
            
            self.sent_messages += 1
            elapsed = int(time.time() - started_time)
            rate = self.sent_messages / max(elapsed, 1)
            
            # Progress bar with live stats
            progress_bar(i, count, color=SNAP_M)
            sys.stdout.write(f" | {rate:.1f} msg/s")
            sys.stdout.flush()
            
            time.sleep(delay)
        
        print("")
        print("")
        fire_print(f"✅ SPAM COMPLETE! {self.sent_messages} messages sent!", delay=0.002)

# ----------------------------------------------------------------------
# Menu Functions - ENHANCED
# ----------------------------------------------------------------------
def open_help_pages(settings):
    try:
        webbrowser.open(settings.get('readme_url'))
        webbrowser.open(settings.get('snapchat_login'))
    except:
        pass

def ensure_snap_image():
    if not SNAP_IMAGE.exists():
        pass  # Silent - no need to show this

def settings_menu(settings):
    clear()
    print_banner()
    rainbow_print("═══════════════ SETTINGS ═══════════════", delay=0.001)
    print(SNAP_W + "(Press ENTER to keep current value)" + Style.RESET_ALL)
    print("")
    try:
        turbo = settings.get('turbo_mode', True)
        turbo_status = f"{SNAP_G}ON{Style.RESET_ALL}" if turbo else f"{SNAP_R}OFF{Style.RESET_ALL}"
        t = input(f"{SNAP_C}⚡ TURBO MODE [{turbo_status}] (y/n): {Style.RESET_ALL}").strip().lower()
        if t == 'y': settings['turbo_mode'] = True
        elif t == 'n': settings['turbo_mode'] = False
        
        print("")
        cyber_print("─── Snap Boost Settings ───", delay=0.001)
        ld = input(f"{SNAP_Y}Loop delay [{settings.get('loop_delay')}]: {Style.RESET_ALL}").strip()
        if ld: settings['loop_delay'] = float(ld)
        cd = input(f"{SNAP_Y}Click delay [{settings.get('click_delay')}]: {Style.RESET_ALL}").strip()
        if cd: settings['click_delay'] = float(cd)
        sc = input(f"{SNAP_Y}Shortcut size [{settings.get('shortcut_count')}]: {Style.RESET_ALL}").strip()
        if sc: settings['shortcut_count'] = int(sc)
        
        print("")
        fire_print("─── Message Spam Settings ───", delay=0.001)
        msg = input(f"{SNAP_M}Spam message [{settings.get('spam_message', '')}]: {Style.RESET_ALL}").strip()
        if msg: settings['spam_message'] = msg
        cnt = input(f"{SNAP_M}Messages to send [{settings.get('spam_count', 100)}]: {Style.RESET_ALL}").strip()
        if cnt: settings['spam_count'] = int(cnt)
        spd = input(f"{SNAP_M}Spam delay [{settings.get('spam_delay', 0.05)}]: {Style.RESET_ALL}").strip()
        if spd: settings['spam_delay'] = float(spd)
    except:
        instant_print("⚠ Invalid input - keeping previous values.", SNAP_R)
    save_settings(settings)
    print("")
    instant_print("✓ Settings saved!", SNAP_G)
    input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

def configure_positions(settings):
    clear()
    print_banner()
    bot = SnapBot(settings)
    bot.get_positions()
    save_settings(settings)
    print("")
    instant_print("✓ Snap positions saved!", SNAP_G)
    input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

def configure_spam_positions(settings):
    clear()
    print_banner()
    spammer = MessageSpammer(settings)
    spammer.get_spam_positions()
    save_settings(settings)
    print("")
    instant_print("✓ Spam positions saved!", SNAP_G)
    input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

def import_positions(settings):
    clear()
    print_banner()
    cyber_print("═══ IMPORT POSITIONS ═══", delay=0.001)
    path = input(f"{SNAP_Y}Enter path to settings.json (or blank to cancel): {Style.RESET_ALL}").strip()
    if not path:
        return
    p = Path(path)
    if not p.exists():
        instant_print("⚠ File not found!", SNAP_R)
        input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")
        return
    with open(p, 'r') as fh:
        data = json.load(fh)
    if 'positions' in data:
        settings['positions'] = data['positions']
    if 'positions_spam' in data:
        settings['positions_spam'] = data['positions_spam']
    save_settings(settings)
    instant_print("✓ Positions imported!", SNAP_G)
    input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

def help_menu(settings):
    clear()
    print_banner()
    rainbow_print("═══════════════ HELP ═══════════════", delay=0.001)
    print("")
    cyber_print("Opening README and Snapchat Web...", delay=0.001)
    open_help_pages(settings)
    input(f"{SNAP_W}Press ENTER to return...{Style.RESET_ALL}")

def estimate_menu(settings):
    clear()
    print_banner()
    rainbow_print("═══ TIME ESTIMATOR ═══", delay=0.001)
    try:
        n = int(input(f"{SNAP_Y}How many snaps? {Style.RESET_ALL}"))
    except:
        instant_print("⚠ Invalid number!", SNAP_R)
        input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")
        return
    bot = SnapBot(settings)
    secs = bot.estimate_time(n)
    mins = secs / 60
    print("")
    fire_print(f"⏱ Estimated time: {int(secs)} seconds ({mins:.1f} minutes)", delay=0.002)
    input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

def exit_screen():
    clear()
    print("")
    rainbow_print("████████████████████████████████████████████████████████", delay=0.002)
    print("")
    fire_print("     Thanks for using SNAPSPAMMER TURBO!", delay=0.003)
    cyber_print("     https://github.com/OGSMrgbbn/SnapSpammer", delay=0.003)
    print("")
    rainbow_print("████████████████████████████████████████████████████████", delay=0.002)
    print("")

# ----------------------------------------------------------------------
# Main Loop - TURBO EDITION
# ----------------------------------------------------------------------
def main():
    title('⚡ SnapSpammer TURBO')
    settings = load_settings()

    # ---- VERSION CHECK -------------------------------------------------
    check_version()
    # -------------------------------------------------------------------

    boot_sequence()
    ensure_snap_image()

    while True:
        clear()
        print_banner()
        
        # Status display
        turbo = settings.get('turbo_mode', True)
        turbo_status = f"{SNAP_G}⚡ TURBO ON{Style.RESET_ALL}" if turbo else f"{SNAP_R}TURBO OFF{Style.RESET_ALL}"
        print(f"  {turbo_status}  |  Loop: {settings.get('loop_delay')}s  |  Click: {settings.get('click_delay')}s")
        print("")
        
        # Menu options with colors
        print(f"  {SNAP_G}[1]{Style.RESET_ALL} {SNAP_Y}⚡ Start Snap Boost{Style.RESET_ALL}")
        print(f"  {SNAP_G}[2]{Style.RESET_ALL} {SNAP_M}💬 Start Message Spam{Style.RESET_ALL}")
        print(f"  {SNAP_C}[3]{Style.RESET_ALL} {SNAP_W}⚙️  Settings{Style.RESET_ALL}")
        print(f"  {SNAP_C}[4]{Style.RESET_ALL} {SNAP_W}📍 Configure Snap Positions{Style.RESET_ALL}")
        print(f"  {SNAP_C}[5]{Style.RESET_ALL} {SNAP_W}📍 Configure Spam Positions{Style.RESET_ALL}")
        print(f"  {SNAP_C}[6]{Style.RESET_ALL} {SNAP_W}📥 Import Positions{Style.RESET_ALL}")
        print(f"  {SNAP_C}[7]{Style.RESET_ALL} {SNAP_W}⏱️  Estimate Time{Style.RESET_ALL}")
        print(f"  {SNAP_C}[8]{Style.RESET_ALL} {SNAP_W}❓ Help{Style.RESET_ALL}")
        print(f"  {SNAP_R}[9]{Style.RESET_ALL} {SNAP_W}🚪 Exit{Style.RESET_ALL}")
        print("")
        c = input(f"{SNAP_Y}Select > {Style.RESET_ALL}").strip()

        if c == '1':
            clear()
            print_banner()
            bot = SnapBot(settings)
            print("")
            fire_print("🚀 SNAP BOOST ACTIVATED! 🚀", delay=0.002)
            cyber_print("Press F6 to stop", delay=0.001)
            print("")
            started = time.time()
            while True:
                try:
                    if keyboard and keyboard.is_pressed('f6'):
                        print("")
                        instant_print("⏹ Stopped!", SNAP_Y)
                        break
                except:
                    pass
                result = bot.send_snap(started, settings.get('shortcut_count', 1))
                if not result:
                    break
                time.sleep(settings.get('loop_delay', 0.15))
            print("")
            fire_print(f"✅ Session complete! {bot.sent_snaps} batches sent!", delay=0.002)
            save_settings(settings)
            input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

        elif c == '2':
            clear()
            print_banner()
            spammer = MessageSpammer(settings)
            fire_print("💬 MESSAGE SPAM MODE 💬", delay=0.002)
            cyber_print("Press F6 to stop", delay=0.001)
            started = time.time()
            spammer.spam_messages(started)
            save_settings(settings)
            input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

        elif c == '3':
            settings_menu(settings)

        elif c == '4':
            configure_positions(settings)

        elif c == '5':
            configure_spam_positions(settings)

        elif c == '6':
            import_positions(settings)

        elif c == '7':
            estimate_menu(settings)

        elif c == '8':
            help_menu(settings)

        elif c == '9':
            save_settings(settings)
            exit_screen()
            break
        else:
            continue

if __name__ == '__main__':
    main()

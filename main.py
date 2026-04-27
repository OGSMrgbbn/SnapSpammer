#!/usr/bin/env python3
# SnapSpammer - main.py (TURBO EDITION)
import os, sys, time, json, platform, webbrowser, urllib.request, threading, itertools, hashlib
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
    "ia_pairs": [],            # Klick+Tippen-Paare [[x,y,text], ...]
    "premium_key": "",         # Premium-Lizenzschlüssel
    # --- RandomTextSpammer (Premium) ---
    "rts_prefix":      "",      # Text vor dem Zufallsblock, z.B. 'hallo '
    "rts_suffix":      "",      # Text nach dem Zufallsblock, z.B. ' @mrgbbn.de'
    "rts_length":      12,      # Länge des Zufallsblocks
    "rts_charset":     "mixed", # 'letters' | 'digits' | 'mixed' | 'hex'
    "rts_count":       10,      # Wie oft absenden
    "rts_delay":       0.3,     # Pause zwischen Sendungen
    "rts_positions":   {},      # input_field + send_button
    "rts_blocks":      [],      # Baukasten-Blöcke
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
RELEASES_URL     = "https://github.com/OGSMrgbbn/SnapSpammer/releases"
PREMIUM_KEYS_URL = "https://raw.githubusercontent.com/OGSMrgbbn/SnapSpammer/main/premium_keys.txt"

# ----------------------------------------------------------------------
# Premium-Checker
# ----------------------------------------------------------------------
_premium_cache: bool | None = None

def _hash_key(raw: str) -> str:
    return hashlib.sha256(raw.strip().encode()).hexdigest()

def is_premium(settings) -> bool:
    """True wenn der gespeicherte Key direkt in der Remote-Liste steht."""
    global _premium_cache
    if _premium_cache is not None:
        return _premium_cache
    raw_key = settings.get("premium_key", "").strip()
    if not raw_key:
        _premium_cache = False
        return False
    try:
        with urllib.request.urlopen(PREMIUM_KEYS_URL, timeout=5) as resp:
            valid_keys = {
                line.strip() for line in resp.read().decode().splitlines()
                if line.strip() and not line.strip().startswith("#")
            }
        _premium_cache = raw_key in valid_keys
    except Exception:
        # Offline – akzeptiere gespeicherten Key ohne Netzwerk
        _premium_cache = bool(raw_key)
    return _premium_cache

def set_premium_key(settings):
    """Key eingeben + sofort prüfen, speichern und Cache zurücksetzen."""
    global _premium_cache
    _premium_cache = None
    print("")
    cyber_print("═══ PREMIUM-AKTIVIERUNG ═══", delay=0.001)
    print("")
    key = input(f"{SNAP_Y}  Premium-Key eingeben: {Style.RESET_ALL}").strip()
    settings["premium_key"] = key
    save_settings(settings)
    _premium_cache = None
    if is_premium(settings):
        fire_print("  ✅ PREMIUM AKTIVIERT!", delay=0.002)
    else:
        instant_print("  ❌ Ungültiger Key.", SNAP_R)

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
# Interaktionsassistent – v2 Feature
# Klick-/Tipp-Sequenzen, Nutzer behält volle Kontrolle
# ----------------------------------------------------------------------
class InteraktionsAssistent:
    """Klick→Tippen-Paarsystem.
    Jedes Paar = (Mausposition, Text).
    Abfolge: klick → tippe → klick → tippe → ...
    Nur Premium-Nutzer können > 1 Durchlauf machen."""

    def __init__(self, settings):
        self.settings = settings
        # Paare: [{"pos": [x,y], "text": "...", "label": "..."}]
        self.pairs = list(settings.get("ia_pairs", []))

    # ── Konfiguration ─────────────────────────────────────────────
    def configure(self):
        if pyautogui is None or keyboard is None:
            instant_print("⚠ pyautogui/keyboard nicht installiert!", SNAP_R)
            return
        clear()
        print_banner()
        rainbow_print("═══ INTERAKTIONSASSISTENT – KONFIGURATION ═══", delay=0.001)
        print("")
        instant_print("  Für jedes Paar: Mausposition festlegen + Text eingeben.", SNAP_C)
        instant_print("  Leer lassen beim Namen → automatischer Name.", SNAP_W)
        instant_print("  Anzahl Paare selbst bestimmen.", SNAP_W)
        print("")
        self.pairs = []
        while True:
            pnr = len(self.pairs) + 1
            print("")
            cyber_print(f"─── PAAR #{pnr} ────────────────────────────────────────────────", delay=0.001)
            # ―― Position ――
            label = input(f"{SNAP_C}  Name für dieses Paar (ENTER = Paar #{pnr}): {Style.RESET_ALL}").strip() or f"Paar #{pnr}"
            instant_print(f"  Bewege Maus zur Klick-Position für '{label}', drücke Y ...", SNAP_W)
            while not keyboard.is_pressed("y"):
                time.sleep(0.02)
            pos = list(pyautogui.position())
            time.sleep(0.3)
            instant_print(f"  ✓ Klick-Position: ({pos[0]}, {pos[1]})", SNAP_G)
            # ―― Text ――
            text = input(f"{SNAP_Y}  Text der getippt wird (ENTER = leer lassen): {Style.RESET_ALL}")
            self.pairs.append({"pos": pos, "text": text, "label": label})
            instant_print(f"  ✓ '{label}' gespeichert  →  klick({pos[0]},{pos[1]}) + tippe \"{text[:40]}\"", SNAP_G)
            # Weiteres Paar?
            more = input(f"{SNAP_M}  Noch ein Paar hinzufügen? (j/n) > {Style.RESET_ALL}").strip().lower()
            if more != "j":
                break
        self.settings["ia_pairs"] = self.pairs
        save_settings(self.settings)
        print("")
        fire_print(f"🔒 {len(self.pairs)} Paare gespeichert!", delay=0.002)

    # ── Vorschau ──────────────────────────────────────────────────
    def preview(self):
        if not self.pairs:
            instant_print("  ⚠ Keine Paare konfiguriert. Erst Option [10] nutzen!", SNAP_R)
            return False
        print("")
        cyber_print("─── AKTIONSPLAN (Klick → Tippen) ────────────────────────", delay=0.001)
        for i, p in enumerate(self.pairs, 1):
            pos  = p.get("pos", [0, 0])
            text = str(p.get("text", ""))[:50]
            print(f"  {SNAP_C}[{i:02d}]{Style.RESET_ALL} {SNAP_G}KLICK{Style.RESET_ALL} @ ({pos[0]},{pos[1]})  {SNAP_M}➔ TIPPE{Style.RESET_ALL} \"{text}\"  {SNAP_W}({p.get('label','')}){Style.RESET_ALL}")
        cyber_print("──────────────────────────────────────────────────────", delay=0.001)
        return True

    # ── Ausführen ─────────────────────────────────────────────────
    def run(self, repeat: int = 1):
        """Zeigt Plan → Bestätigung → Ausführen. F6 stoppt sofort."""
        if pyautogui is None:
            instant_print("⚠ pyautogui nicht installiert!", SNAP_R)
            return
        if not self.preview():
            input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")
            return
        premium = is_premium(self.settings)
        if repeat > 1 and not premium:
            instant_print("  ⚠ Mehrfache Wiederholungen sind nur für Premium-Nutzer! (Option [15])", SNAP_R)
            repeat = 1
        print("")
        print(f"  {SNAP_Y}Wiederholungen: {repeat}x{Style.RESET_ALL}   {SNAP_R}F6 = Abbruch jederzeit{Style.RESET_ALL}")
        print("")
        confirm = input(f"{SNAP_G}  Jetzt starten? (j/n) > {Style.RESET_ALL}").strip().lower()
        if confirm != "j":
            instant_print("  Abgebrochen.", SNAP_Y)
            return
        click_delay = float(self.settings.get("click_delay", 0.25))
        aborted = False
        for run_nr in range(1, repeat + 1):
            if aborted:
                break
            print("")
            fire_print(f"  ▶ Durchlauf {run_nr}/{repeat}", delay=0.001)
            for p in self.pairs:
                if keyboard and keyboard.is_pressed("f6"):
                    print("")
                    instant_print("  ⏹ Durch F6 gestoppt.", SNAP_Y)
                    aborted = True
                    break
                pos  = p.get("pos", [0, 0])
                text = p.get("text", "")
                # ―― Klick ――
                sys.stdout.write(f"\r{SNAP_C}  → KLICK  {p.get('label','')} @ ({pos[0]},{pos[1]}){Style.RESET_ALL}   ")
                sys.stdout.flush()
                pyautogui.moveTo(pos[0], pos[1])
                time.sleep(click_delay)
                pyautogui.click()
                time.sleep(0.08)
                # ―― Tippen ――
                if text:
                    sys.stdout.write(f"\r{SNAP_M}  → TIPPE  \"{text[:40]}\"{Style.RESET_ALL}   ")
                    sys.stdout.flush()
                    pyautogui.write(text, interval=0.03)
                time.sleep(0.05)
        print("")
        print("")
        if not aborted:
            fire_print(f"  ✅ {repeat} Durchlauf/Durchläufe abgeschlossen!", delay=0.002)
        instant_print("  Kontrolle zurück an den Nutzer.", SNAP_G)

# ----------------------------------------------------------------------
# RandomTextSpammer – Premium Feature
# Zufallstext (Länge + Zeichensatz wählbar) + fester Prefix/Suffix
# Klickt Input-Feld, tippt Text, klickt Senden – wiederholbar
# ----------------------------------------------------------------------
import random, string as _string

class RandomTextSpammer:
    """Baukasten-System: Text aus beliebig vielen Blöcken zusammenstellen.
    Jeder Block ist entweder 'random' (Länge + Zeichensatz wählbar)
    oder 'fest' (fixer Text). Alle Blöcke werden in settings.json gespeichert."""

    CHARSETS = {
        "letters": _string.ascii_letters,
        "digits":  _string.digits,
        "mixed":   _string.ascii_letters + _string.digits,
        "hex":     "0123456789abcdef",
        "lower":   _string.ascii_lowercase,
        "upper":   _string.ascii_uppercase,
    }

    def __init__(self, settings):
        self.settings = settings
        # blocks: [{"type": "random"|"fest", "value": ..., "length": ..., "charset": ...}, ...]
        self.blocks = list(settings.get("rts_blocks", []))

    # ── Text aus Blöcken generieren ────────────────────────────────────
    def _generate(self):
        parts = []
        for b in self.blocks:
            if b.get("type") == "fest":
                parts.append(str(b.get("value", "")))
            else:  # random
                charset = self.CHARSETS.get(b.get("charset", "mixed"), self.CHARSETS["mixed"])
                length  = max(1, int(b.get("length", 8)))
                parts.append("".join(random.choices(charset, k=length)))
        return "".join(parts)

    # ── Baukasten konfigurieren ────────────────────────────────────────
    def configure_builder(self):
        clear()
        print_banner()
        rainbow_print("═══ TEXT-BAUKASTEN – KONFIGURATION ═══", delay=0.001)
        print("")
        instant_print("  Baue deinen Text Block für Block zusammen.", SNAP_C)
        instant_print("  Jeder Block ist entweder ein ZUFALLSBLOCK oder ein FESTER TEXT.", SNAP_W)
        print("")

        self.blocks = []
        while True:
            bnr = len(self.blocks) + 1
            print("")
            cyber_print(f"─── BLOCK #{bnr} ─────────────────────────────────────────", delay=0.001)
            print(f"  {SNAP_G}[1]{Style.RESET_ALL} {SNAP_Y}Zufallsblock{Style.RESET_ALL}  – zufällige Zeichen, Länge + Zeichensatz wählbar")
            print(f"  {SNAP_G}[2]{Style.RESET_ALL} {SNAP_C}Fester Text {Style.RESET_ALL}  – genau dieser Text, immer gleich")
            print(f"  {SNAP_R}[3]{Style.RESET_ALL} Fertig – Baukasten abschließen")
            print("")
            cmd = input(f"{SNAP_Y}  Block-Typ > {Style.RESET_ALL}").strip()

            if cmd == "1":
                # Zufallsblock
                print("")
                instant_print("  Zeichensätze: letters | digits | mixed | hex | lower | upper", SNAP_W)
                charset = input(f"{SNAP_Y}  Zeichensatz [{SNAP_C}mixed{SNAP_Y}]: {Style.RESET_ALL}").strip() or "mixed"
                if charset not in self.CHARSETS:
                    instant_print(f"  ⚠ Unbekannt – 'mixed' wird verwendet.", SNAP_R)
                    charset = "mixed"
                try:
                    length = int(input(f"{SNAP_Y}  Länge (Zeichen) [{SNAP_C}8{SNAP_Y}]: {Style.RESET_ALL}").strip() or "8")
                except ValueError:
                    length = 8
                self.blocks.append({"type": "random", "charset": charset, "length": length})
                preview = "".join(random.choices(self.CHARSETS[charset], k=length))
                instant_print(f"  ✓ Zufallsblock #{bnr}: {length}× {charset}  –  Beispiel: '{preview}'", SNAP_G)

            elif cmd == "2":
                # Fester Text
                print("")
                value = input(f"{SNAP_Y}  Text eingeben: {Style.RESET_ALL}")
                self.blocks.append({"type": "fest", "value": value})
                instant_print(f"  ✓ Fester Block #{bnr}: '{value}'", SNAP_G)

            elif cmd == "3":
                if not self.blocks:
                    instant_print("  ⚠ Mindestens ein Block erforderlich!", SNAP_R)
                    continue
                break
            else:
                instant_print("  ⚠ Ungültige Eingabe.", SNAP_R)
                continue

        # Anzahl + Delay
        print("")
        cyber_print("─── SENDUNGS-EINSTELLUNGEN ──────────────────────────", delay=0.001)
        try:
            count = int(input(f"{SNAP_Y}  Anzahl Sendungen [{SNAP_C}{self.settings.get('rts_count', 10)}{SNAP_Y}]: {Style.RESET_ALL}").strip() or str(self.settings.get("rts_count", 10)))
        except ValueError:
            count = 10
        try:
            delay = float(input(f"{SNAP_Y}  Pause zwischen Sendungen (s) [{SNAP_C}{self.settings.get('rts_delay', 0.3)}{SNAP_Y}]: {Style.RESET_ALL}").strip() or str(self.settings.get("rts_delay", 0.3)))
        except ValueError:
            delay = 0.3

        self.settings["rts_blocks"] = self.blocks
        self.settings["rts_count"]  = count
        self.settings["rts_delay"]  = delay
        save_settings(self.settings)

        # Vorschau
        print("")
        fire_print(f"  🔒 Baukasten gespeichert! {len(self.blocks)} Blöcke, {count} Sendungen", delay=0.002)
        print("")
        instant_print("  Vorschau (3 Beispiele):", SNAP_C)
        for _ in range(3):
            instant_print(f"    → '{self._generate()}'", SNAP_M)

    # ── Baukasten anzeigen ─────────────────────────────────────────────
    def show_plan(self):
        if not self.blocks:
            instant_print("  ⚠ Kein Baukasten konfiguriert. Erst Option [12] nutzen!", SNAP_R)
            return False
        print("")
        cyber_print("─── BAUKASTEN-PLAN ──────────────────────────────────", delay=0.001)
        for i, b in enumerate(self.blocks, 1):
            if b.get("type") == "fest":
                print(f"  {SNAP_C}[{i:02d}]{Style.RESET_ALL} {SNAP_G}FEST   {Style.RESET_ALL}  → '{b.get('value','')}'")
            else:
                print(f"  {SNAP_C}[{i:02d}]{Style.RESET_ALL} {SNAP_M}RANDOM {Style.RESET_ALL}  → {b.get('length',8)}× {b.get('charset','mixed')}  (Beispiel: '{self._generate_block(b)}')")
        cyber_print("────────────────────────────────────────────────────", delay=0.001)
        print(f"  {SNAP_Y}Ergebnis-Beispiel: '{self._generate()}'{Style.RESET_ALL}")
        print(f"  {SNAP_Y}Ergebnis-Beispiel: '{self._generate()}'{Style.RESET_ALL}")
        print("")
        return True

    def _generate_block(self, b):
        charset = self.CHARSETS.get(b.get("charset", "mixed"), self.CHARSETS["mixed"])
        return "".join(random.choices(charset, k=max(1, int(b.get("length", 8)))))

    # ── Positionen erfassen ────────────────────────────────────────────
    def configure_positions(self):
        if pyautogui is None or keyboard is None:
            instant_print("⚠ pyautogui/keyboard nicht installiert!", SNAP_R)
            return
        rainbow_print("═══ RANDOM-TEXT – POSITIONEN ERFASSEN ═══", delay=0.001)
        print("")
        cyber_print("Bewege Maus zum TEXT-EINGABEFELD, drücke Y ...", delay=0.001)
        while not keyboard.is_pressed("y"):
            time.sleep(0.02)
        pos_input = list(pyautogui.position())
        instant_print(f"  ✓ Eingabefeld @ ({pos_input[0]}, {pos_input[1]})", SNAP_G)
        time.sleep(0.3)

        cyber_print("Bewege Maus zum SENDEN-BUTTON, drücke Y ...", delay=0.001)
        while not keyboard.is_pressed("y"):
            time.sleep(0.02)
        pos_send = list(pyautogui.position())
        instant_print(f"  ✓ Senden-Button @ ({pos_send[0]}, {pos_send[1]})", SNAP_G)
        time.sleep(0.3)

        self.settings["rts_positions"] = {
            "input_field": pos_input,
            "send_button": pos_send,
        }
        save_settings(self.settings)
        print("")
        fire_print("🔒 Positionen gespeichert!", delay=0.002)

    # ── Ausführen ──────────────────────────────────────────────────────
    def run(self):
        if pyautogui is None:
            instant_print("⚠ pyautogui nicht installiert!", SNAP_R)
            return
        pos = self.settings.get("rts_positions", {})
        if "input_field" not in pos or "send_button" not in pos:
            instant_print("⚠ Positionen fehlen! Erst Option [13] – Positionen erfassen.", SNAP_R)
            return
        if not self.show_plan():
            return

        count       = int(self.settings.get("rts_count", 10))
        delay       = float(self.settings.get("rts_delay", 0.3))
        click_delay = float(self.settings.get("click_delay", 0.25))
        inp         = pos["input_field"]
        send        = pos["send_button"]

        fire_print(f"  {count} Sendungen  |  F6 = Abbruch jederzeit", delay=0.001)
        print("")
        confirm = input(f"{SNAP_G}  Jetzt starten? (j/n) > {Style.RESET_ALL}").strip().lower()
        if confirm != "j":
            instant_print("  Abgebrochen.", SNAP_Y)
            return

        sent = 0
        for i in range(1, count + 1):
            if keyboard and keyboard.is_pressed("f6"):
                print("")
                instant_print("  ⏹ Durch F6 gestoppt.", SNAP_Y)
                break
            text = self._generate()
            pyautogui.click(inp[0], inp[1])
            time.sleep(click_delay)
            pyautogui.write(text, interval=0.02)
            time.sleep(click_delay)
            pyautogui.click(send[0], send[1])
            sent += 1
            sys.stdout.write(f"\r{SNAP_M}  [{i:04d}/{count}] → '{text[:70]}'{Style.RESET_ALL}   ")
            sys.stdout.flush()
            time.sleep(delay)

        print("")
        print("")
        fire_print(f"  ✅ {sent} Nachrichten gesendet!", delay=0.002)
        instant_print("  Kontrolle zurück an den Nutzer.", SNAP_G)

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
        prem_status   = f"{SNAP_Y}🔑 PREMIUM{Style.RESET_ALL}" if is_premium(settings) else f"{SNAP_W}FREE{Style.RESET_ALL}"
        print(f"  {turbo_status}  |  Loop: {settings.get('loop_delay')}s  |  Click: {settings.get('click_delay')}s  |  {prem_status}")
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
        print(f"  {SNAP_B}[10]{Style.RESET_ALL} {SNAP_C}🤖 Klick+Tippen-Assistent – Konfigurieren{Style.RESET_ALL}")
        print(f"  {SNAP_B}[11]{Style.RESET_ALL} {SNAP_C}▶  Klick+Tippen-Assistent – Starten{Style.RESET_ALL}")
        print(f"  {SNAP_M}[12]{Style.RESET_ALL} {SNAP_Y}🧩 Text-Baukasten – Konfigurieren{Style.RESET_ALL}")
        print(f"  {SNAP_M}[13]{Style.RESET_ALL} {SNAP_Y}📍 Random-Text Spammer – Positionen{Style.RESET_ALL}")
        print(f"  {SNAP_M}[14]{Style.RESET_ALL} {SNAP_Y}🚀 Random-Text Spammer – Starten{Style.RESET_ALL}")
        print(f"  {SNAP_Y}[15]{Style.RESET_ALL} {SNAP_Y}🔑 Premium-Key eingeben / prüfen{Style.RESET_ALL}")
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

        elif c == '10':
            clear()
            print_banner()
            ia = InteraktionsAssistent(settings)
            ia.configure()
            input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

        elif c == '11':
            clear()
            print_banner()
            rainbow_print("═══ KLICK+TIPPEN-ASSISTENT – STARTEN ═══", delay=0.001)
            ia = InteraktionsAssistent(settings)
            if not ia.pairs:
                instant_print("⚠ Keine Paare konfiguriert. Erst Option [10] nutzen!", SNAP_R)
                input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")
            else:
                if is_premium(settings):
                    try:
                        repeat = int(input(f"{SNAP_Y}  Wie oft wiederholen? (Standard: 1) > {Style.RESET_ALL}").strip() or "1")
                    except ValueError:
                        repeat = 1
                else:
                    instant_print("  🔑 Wiederholungen = Premium-Feature. 1x wird ausgeführt.", SNAP_Y)
                    repeat = 1
                ia.run(repeat)
                save_settings(settings)
                input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

        elif c == '15':
            clear()
            print_banner()
            set_premium_key(settings)
            input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

        elif c == '12':
            clear()
            print_banner()
            rts = RandomTextSpammer(settings)
            rts.configure_builder()
            input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

        elif c == '13':
            clear()
            print_banner()
            rts = RandomTextSpammer(settings)
            rts.configure_positions()
            input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

        elif c == '14':
            clear()
            print_banner()
            rainbow_print("═══ RANDOM-TEXT SPAMMER ═══", delay=0.001)
            rts = RandomTextSpammer(settings)
            rts.run()
            save_settings(settings)
            input(f"{SNAP_W}Press ENTER...{Style.RESET_ALL}")

        else:
            continue

if __name__ == '__main__':
    main()

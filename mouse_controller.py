#!/usr/bin/env python3
# mouse_controller.py - Separates Maus-Steuerungs-System
# Unabhängiges Modul für Mausbewegung und Klicks

import time
import sys

try:
    import pyautogui
    import keyboard
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0
    MOUSE_AVAILABLE = True
except ImportError:
    pyautogui = None
    keyboard = None
    MOUSE_AVAILABLE = False


class MouseController:
    """
    Unabhängiges Maus-Steuerungs-System
    Für Bewegung, Klicks und Position-Erfassung
    """
    
    def __init__(self, click_delay=0.25, move_duration=0):
        """
        Initialisiert den MouseController
        
        Args:
            click_delay: Verzögerung zwischen Klicks (Standard: 0.25s)
            move_duration: Dauer der Mausbewegung (0 = sofort)
        """
        self.click_delay = click_delay
        self.move_duration = move_duration
        self.positions = {}
        self.last_position = None
    
    @staticmethod
    def is_available():
        """Prüft ob Maus-Steuerung verfügbar ist"""
        return MOUSE_AVAILABLE
    
    # ─────────────────────────────────────────────────────────────
    # POSITION FUNKTIONEN
    # ─────────────────────────────────────────────────────────────
    
    def get_current_position(self):
        """Gibt aktuelle Mausposition zurück"""
        if not MOUSE_AVAILABLE:
            return None
        return pyautogui.position()
    
    def capture_position(self, name, hotkey='y', message=None):
        """
        Erfasst eine Position wenn Taste gedrückt wird
        
        Args:
            name: Name für die Position (z.B. 'button_1')
            hotkey: Taste zum Bestätigen (Standard: 'y')
            message: Optionale Nachricht zum Anzeigen
            
        Returns:
            tuple: (x, y) Position oder None bei Fehler
        """
        if not MOUSE_AVAILABLE:
            print("[!] Maus-Steuerung nicht verfügbar")
            return None
        
        if message:
            print(message)
        else:
            print(f"[>] Bewege Maus zu '{name}', drücke '{hotkey}' zum Speichern")
        
        while not keyboard.is_pressed(hotkey):
            time.sleep(0.02)
        
        pos = pyautogui.position()
        self.positions[name] = pos
        self.last_position = pos
        
        print(f"[✓] Position '{name}' gespeichert: {pos}")
        time.sleep(0.3)  # Kurze Pause nach Tastendruck
        
        return pos
    
    def capture_multiple_positions(self, names, hotkey='y'):
        """
        Erfasst mehrere Positionen nacheinander
        
        Args:
            names: Liste von Positionsnamen
            hotkey: Taste zum Bestätigen
            
        Returns:
            dict: Alle erfassten Positionen
        """
        print("═══ POSITIONS-ERFASSUNG ═══\n")
        
        for name in names:
            self.capture_position(name, hotkey)
        
        print(f"\n[✓] {len(names)} Positionen erfasst!")
        return self.positions.copy()
    
    def save_position(self, name, position):
        """Speichert eine Position manuell"""
        self.positions[name] = position
    
    def get_position(self, name):
        """Holt eine gespeicherte Position"""
        return self.positions.get(name)
    
    def has_position(self, name):
        """Prüft ob Position existiert"""
        return name in self.positions
    
    def has_all_positions(self, names):
        """Prüft ob alle angegebenen Positionen existieren"""
        return all(name in self.positions for name in names)
    
    def load_positions(self, positions_dict):
        """Lädt Positionen aus einem Dictionary"""
        self.positions.update(positions_dict)
    
    def get_all_positions(self):
        """Gibt alle gespeicherten Positionen zurück"""
        return self.positions.copy()
    
    def clear_positions(self):
        """Löscht alle gespeicherten Positionen"""
        self.positions.clear()
    
    # ─────────────────────────────────────────────────────────────
    # BEWEGUNGS FUNKTIONEN
    # ─────────────────────────────────────────────────────────────
    
    def move_to(self, x, y, duration=None):
        """
        Bewegt Maus zu absoluter Position
        
        Args:
            x: X-Koordinate
            y: Y-Koordinate
            duration: Bewegungsdauer (None = Standard)
        """
        if not MOUSE_AVAILABLE:
            return False
        
        dur = duration if duration is not None else self.move_duration
        pyautogui.moveTo(x, y, duration=dur)
        self.last_position = (x, y)
        return True
    
    def move_to_position(self, name, duration=None):
        """
        Bewegt Maus zu einer gespeicherten Position
        
        Args:
            name: Name der gespeicherten Position
            duration: Bewegungsdauer
        """
        pos = self.positions.get(name)
        if pos is None:
            print(f"[!] Position '{name}' nicht gefunden")
            return False
        return self.move_to(pos[0], pos[1], duration)
    
    def move_relative(self, dx, dy, duration=None):
        """
        Bewegt Maus relativ zur aktuellen Position
        
        Args:
            dx: Horizontale Verschiebung
            dy: Vertikale Verschiebung
            duration: Bewegungsdauer
        """
        if not MOUSE_AVAILABLE:
            return False
        
        dur = duration if duration is not None else self.move_duration
        pyautogui.moveRel(dx, dy, duration=dur)
        return True
    
    # ─────────────────────────────────────────────────────────────
    # KLICK FUNKTIONEN
    # ─────────────────────────────────────────────────────────────
    
    def click(self, x=None, y=None, clicks=1, button='left'):
        """
        Führt Mausklick aus
        
        Args:
            x: X-Koordinate (None = aktuelle Position)
            y: Y-Koordinate (None = aktuelle Position)
            clicks: Anzahl Klicks
            button: 'left', 'right', oder 'middle'
        """
        if not MOUSE_AVAILABLE:
            return False
        
        if x is not None and y is not None:
            pyautogui.click(x, y, clicks=clicks, button=button)
        else:
            pyautogui.click(clicks=clicks, button=button)
        return True
    
    def click_position(self, name, clicks=1, button='left'):
        """
        Klickt auf eine gespeicherte Position
        
        Args:
            name: Name der gespeicherten Position
            clicks: Anzahl Klicks
            button: Maustaste
        """
        pos = self.positions.get(name)
        if pos is None:
            print(f"[!] Position '{name}' nicht gefunden")
            return False
        return self.click(pos[0], pos[1], clicks, button)
    
    def double_click(self, x=None, y=None):
        """Doppelklick"""
        return self.click(x, y, clicks=2)
    
    def right_click(self, x=None, y=None):
        """Rechtsklick"""
        return self.click(x, y, button='right')
    
    def move_and_click(self, x, y, delay=None):
        """
        Bewegt zur Position und klickt mit Verzögerung
        
        Args:
            x: X-Koordinate
            y: Y-Koordinate
            delay: Verzögerung nach Bewegung (None = Standard)
        """
        if not MOUSE_AVAILABLE:
            return False
        
        self.move_to(x, y)
        d = delay if delay is not None else self.click_delay
        if d > 0:
            time.sleep(d)
        self.click()
        return True
    
    def move_and_click_position(self, name, delay=None):
        """
        Bewegt zu gespeicherter Position und klickt
        
        Args:
            name: Name der Position
            delay: Verzögerung nach Bewegung
        """
        pos = self.positions.get(name)
        if pos is None:
            print(f"[!] Position '{name}' nicht gefunden")
            return False
        return self.move_and_click(pos[0], pos[1], delay)
    
    # ─────────────────────────────────────────────────────────────
    # DRAG & DROP FUNKTIONEN
    # ─────────────────────────────────────────────────────────────
    
    def drag_to(self, x, y, duration=0.5, button='left'):
        """
        Zieht (Drag) zur angegebenen Position
        
        Args:
            x: Ziel X-Koordinate
            y: Ziel Y-Koordinate
            duration: Dauer des Ziehens
            button: Maustaste
        """
        if not MOUSE_AVAILABLE:
            return False
        
        pyautogui.dragTo(x, y, duration=duration, button=button)
        return True
    
    def drag_relative(self, dx, dy, duration=0.5, button='left'):
        """
        Zieht relativ zur aktuellen Position
        
        Args:
            dx: Horizontale Verschiebung
            dy: Vertikale Verschiebung
            duration: Dauer
            button: Maustaste
        """
        if not MOUSE_AVAILABLE:
            return False
        
        pyautogui.drag(dx, dy, duration=duration, button=button)
        return True
    
    # ─────────────────────────────────────────────────────────────
    # SCROLL FUNKTIONEN
    # ─────────────────────────────────────────────────────────────
    
    def scroll(self, amount, x=None, y=None):
        """
        Scrollt an aktueller oder angegebener Position
        
        Args:
            amount: Scroll-Betrag (positiv = hoch, negativ = runter)
            x: Optional X-Koordinate
            y: Optional Y-Koordinate
        """
        if not MOUSE_AVAILABLE:
            return False
        
        pyautogui.scroll(amount, x, y)
        return True
    
    def scroll_up(self, amount=3, x=None, y=None):
        """Scrollt nach oben"""
        return self.scroll(amount, x, y)
    
    def scroll_down(self, amount=3, x=None, y=None):
        """Scrollt nach unten"""
        return self.scroll(-amount, x, y)
    
    # ─────────────────────────────────────────────────────────────
    # SEQUENZ FUNKTIONEN
    # ─────────────────────────────────────────────────────────────
    
    def execute_sequence(self, actions, delay=None):
        """
        Führt eine Sequenz von Aktionen aus
        
        Args:
            actions: Liste von Aktionen: [('click', 'pos_name'), ('move', 'pos_name'), ...]
            delay: Verzögerung zwischen Aktionen
            
        Aktionstypen:
            ('click', 'position_name')
            ('move', 'position_name')
            ('wait', seconds)
            ('click_xy', x, y)
            ('move_xy', x, y)
        """
        d = delay if delay is not None else self.click_delay
        
        for action in actions:
            action_type = action[0]
            
            if action_type == 'click':
                self.move_and_click_position(action[1], d)
            elif action_type == 'move':
                self.move_to_position(action[1])
                if d > 0:
                    time.sleep(d)
            elif action_type == 'wait':
                time.sleep(action[1])
            elif action_type == 'click_xy':
                self.move_and_click(action[1], action[2], d)
            elif action_type == 'move_xy':
                self.move_to(action[1], action[2])
                if d > 0:
                    time.sleep(d)
    
    # ─────────────────────────────────────────────────────────────
    # HOTKEY / WARTEN FUNKTIONEN
    # ─────────────────────────────────────────────────────────────
    
    def wait_for_key(self, key='y'):
        """
        Wartet bis eine Taste gedrückt wird
        
        Args:
            key: Taste auf die gewartet wird
        """
        if not MOUSE_AVAILABLE:
            return False
        
        while not keyboard.is_pressed(key):
            time.sleep(0.02)
        return True
    
    def is_key_pressed(self, key):
        """Prüft ob Taste gedrückt ist"""
        if not MOUSE_AVAILABLE:
            return False
        return keyboard.is_pressed(key)
    
    # ─────────────────────────────────────────────────────────────
    # SETTINGS
    # ─────────────────────────────────────────────────────────────
    
    def set_click_delay(self, delay):
        """Setzt die Standard-Klickverzögerung"""
        self.click_delay = delay
    
    def set_move_duration(self, duration):
        """Setzt die Standard-Bewegungsdauer"""
        self.move_duration = duration
    
    def get_settings(self):
        """Gibt aktuelle Einstellungen zurück"""
        return {
            'click_delay': self.click_delay,
            'move_duration': self.move_duration
        }


# ─────────────────────────────────────────────────────────────────
# STANDALONE DEMO / TEST
# ─────────────────────────────────────────────────────────────────

def clear_screen():
    """Bildschirm löschen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu(mouse):
    """Zeigt das Hauptmenü"""
    print()
    print("═══════════════════════════════════════")
    print("  MOUSE CONTROLLER - DEMO")
    print("═══════════════════════════════════════")
    print()
    print(f"  Gespeicherte Positionen: {len(mouse.positions)}")
    if mouse.positions:
        for name, pos in mouse.positions.items():
            print(f"    - {name}: {pos}")
    print()
    print("  [1] Position erfassen")
    print("  [2] Aktuelle Position anzeigen (live)")
    print("  [3] Auf Position klicken")
    print("  [4] Sequenz-Test (3 Positionen)")
    print("  [5] Alle Positionen löschen")
    print("  [0] Beenden")
    print()

def demo():
    """Demo-Funktion zum Testen des MouseControllers"""
    clear_screen()
    
    if not MouseController.is_available():
        print("[!] Fehler: pyautogui/keyboard nicht installiert!")
        print("    Installiere mit: pip install pyautogui keyboard")
        input("Drücke ENTER zum Beenden...")
        return
    
    mouse = MouseController(click_delay=0.3)
    
    while True:
        clear_screen()
        show_menu(mouse)
        
        choice = input("Auswahl > ").strip()
        
        if choice == '1':
            print()
            name = input("Position-Name (oder ENTER für auto): ").strip()
            if not name:
                name = f"pos_{len(mouse.positions) + 1}"
            print(f"\nBewege Maus zur gewünschten Position...")
            print("Drücke 'Y' zum Speichern")
            pos = mouse.capture_position(name)
            print(f"\n[✓] '{name}' gespeichert: {pos}")
            input("\nDrücke ENTER für Menü...")
            
        elif choice == '2':
            print()
            print("Live-Position (Drücke 'Q' zum Stoppen):")
            print()
            try:
                while True:
                    pos = mouse.get_current_position()
                    print(f"\r  X: {pos[0]:4d}  |  Y: {pos[1]:4d}    ", end="", flush=True)
                    time.sleep(0.05)
                    if keyboard.is_pressed('q'):
                        break
            except:
                pass
            print()
            input("\nDrücke ENTER für Menü...")
            
        elif choice == '3':
            if not mouse.positions:
                print("\n[!] Keine Positionen gespeichert!")
                input("\nDrücke ENTER für Menü...")
                continue
            print()
            print("Verfügbare Positionen:")
            names = list(mouse.positions.keys())
            for i, name in enumerate(names, 1):
                print(f"  [{i}] {name}")
            print()
            try:
                idx = int(input("Nummer wählen: ").strip()) - 1
                if 0 <= idx < len(names):
                    delay = input("Verzögerung zwischen Klicks (Standard 0.5): ").strip()
                    delay = float(delay) if delay else 0.5
                    print(f"\nKlicke auf '{names[idx]}' in 3 Sekunden...")
                    print(">>> Drücke F6 zum Stoppen <<<")
                    time.sleep(3)
                    count = 0
                    while True:
                        if keyboard.is_pressed('f6'):
                            print(f"\n\n[✓] Gestoppt nach {count} Klicks!")
                            break
                        mouse.move_and_click_position(names[idx])
                        count += 1
                        print(f"\r  Klicks: {count}", end="", flush=True)
                        time.sleep(delay)
            except:
                print("[!] Ungültige Eingabe")
            input("\nDrücke ENTER für Menü...")
            
        elif choice == '4':
            print()
            print("Erfasse 3 Positionen für Sequenz-Test:")
            print()
            mouse.capture_position("punkt_1")
            mouse.capture_position("punkt_2")
            mouse.capture_position("punkt_3")
            
            delay = input("\nVerzögerung zwischen Klicks (Standard 0.5): ").strip()
            delay = float(delay) if delay else 0.5
            
            print("\n[>] Starte Klick-Sequenz in 3 Sekunden...")
            print(">>> Drücke F6 zum Stoppen <<<")
            time.sleep(3)
            
            sequence = [
                ('click', 'punkt_1'),
                ('wait', delay),
                ('click', 'punkt_2'),
                ('wait', delay),
                ('click', 'punkt_3'),
                ('wait', delay),
            ]
            
            count = 0
            while True:
                if keyboard.is_pressed('f6'):
                    print(f"\n\n[✓] Gestoppt nach {count} Durchläufen!")
                    break
                mouse.execute_sequence(sequence)
                count += 1
                print(f"\r  Durchläufe: {count}", end="", flush=True)
            
            input("\nDrücke ENTER für Menü...")
            
        elif choice == '5':
            mouse.clear_positions()
            print("\n[✓] Alle Positionen gelöscht!")
            input("\nDrücke ENTER für Menü...")
            
        elif choice == '0':
            break
    
    clear_screen()
    print("Demo beendet.")


if __name__ == '__main__':
    demo()

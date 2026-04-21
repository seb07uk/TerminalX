#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
psterm_editor — Zaawansowany edytor notatek w stylu MS-DOS EDIT
==============================================================
Umieść w ~/.terminalx_plugins/psterm_editor.py
"""

import json
import os
import sys
import datetime
from pathlib import Path

# --- Metadane ---
PLUGIN_META = {
    "name":         "psterm_editor",
    "version":      "2.0.0",
    "author":       "Sebastian Januchowski",
    "description":  "Edytor notatek z GUI w stylu Microsoft EDIT (DOS)",
    "tags":         ["editor", "dos", "office"],
    "requires_api": (2, 0),
}

# --- Importy z Twojego systemu (symulacja klas z psterm_office) ---
class A:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    BLK    = "\033[30m"
    WHT    = "\033[37m"
    LWHT   = "\033[97m"
    LYLW   = "\033[93m"
    LCYN   = "\033[96m"
    BLU    = "\033[34m"
    BG_BLU = "\033[44m"
    BG_CYN = "\033[46m"
    BG_WHT = "\033[47m"

class BOX:
    DOUBLE = {"TL": "╔", "TR": "╗", "BL": "╚", "BR": "╝", "H": "═", "V": "║", "LT": "╠", "RT": "╣", "TT": "╦", "BT": "╩"}
    SINGLE = {"TL": "┌", "TR": "┐", "BL": "└", "BR": "┘", "H": "─", "V": "│", "LT": "├", "RT": "┤"}

# --- Zarządzanie Danymi ---
DATA_DIR = Path.home() / ".terminalx_office"
NOTES_FILE = DATA_DIR / "notes.json"

def _load_notes():
    if NOTES_FILE.exists():
        try: return json.loads(NOTES_FILE.read_text(encoding="utf-8"))
        except: return []
    return []

def _save_notes(notes):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_FILE.write_text(json.dumps(notes, indent=2, ensure_ascii=False), encoding="utf-8")

# --- Silnik Renderowania GUI ---
def draw_edit_ui(filename="BEZNAZWY.TXT", content=None, status="F1=Pomoc"):
    w = min(os.get_terminal_size().columns - 2, 78)
    h = 15 # Wysokość obszaru roboczego
    
    # 1. Pasek Menu (Top)
    menu = f" Plik  Edycja  Szukaj  Opcje  Pomoc ".ljust(w + 2)
    print(f"{A.BG_WHT}{A.BLK}{menu}{A.RESET}")
    
    # 2. Nagłówek okna (Ramka)
    title = f" {filename} "
    print(f"{A.BLU}{BOX.DOUBLE['TL']}{BOX.DOUBLE['H']*2}{A.RESET}{A.BOLD}{A.LWHT}{title}{A.RESET}{A.BLU}{BOX.DOUBLE['H']*(w-len(title)-1)}{BOX.DOUBLE['TR']}{A.RESET}")
    
    # 3. Obszar Tekstu (Background Blue)
    if not content:
        content = [f"{A.WHT}▒" + " " * (w-2) for _ in range(h)]
    
    for i in range(h):
        line = content[i] if i < len(content) else ""
        # Usuwanie ANSI do obliczenia paddingu
        clean_line = line.replace(A.WHT, "").replace(A.RESET, "").replace(A.BOLD, "")
        pad = " " * (w - len(clean_line) - 1)
        print(f"{A.BLU}{BOX.DOUBLE['V']}{A.RESET}{A.BG_BLU}{A.WHT} {line}{pad}{A.RESET}{A.BLU}{BOX.DOUBLE['V']}{A.RESET}")
        
    # 4. Dół okna
    print(f"{A.BLU}{BOX.DOUBLE['BL']}{BOX.DOUBLE['H']*w}{BOX.DOUBLE['BR']}{A.RESET}")
    
    # 5. Pasek Statusu
    status_line = f" {status} ".ljust(w + 2)
    print(f"{A.BG_WHT}{A.BLK}{status_line}{A.RESET}")

# --- Komendy ---
def cmd_edit(args):
    """Główna komenda edytora."""
    notes = _load_notes()
    w = 78

    if not args:
        # Tryb Ekranu Głównego (Lista plików)
        os.system('cls' if os.name == 'nt' else 'clear')
        file_list = []
        for i, n in enumerate(notes[:10], 1):
            file_list.append(f"{i}. {n.get('title', 'Notatka')[:20]}")
        
        draw_edit_ui("KATALOG_NOTATEK.EXE", file_list, "ENTER=Edytuj  N=Nowa  DEL=Usuń  ESC=Wyjdź")
        return

    sub = args[0].lower()
    
    if sub == "new":
        os.system('cls' if os.name == 'nt' else 'clear')
        draw_edit_ui("NOWA_NOTATKA.TXT", ["", "  Wpisz treść poniżej...", ""], "Wpisz 'save' aby zapisać")
        title = input(f"\n{A.LYLW} Tytuł: {A.RESET}")
        print(f"{A.DIM} Treść (zakończ kropką '.' w nowej linii):{A.RESET}")
        lines = []
        while True:
            line = input(" > ")
            if line == ".": break
            lines.append(line)
        
        notes.append({
            "title": title,
            "body": "\n".join(lines),
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        })
        _save_notes(notes)
        print(f"{A.LCYN}✔ Zapisano w bazie psTERM.{A.RESET}")

    elif sub == "view":
        idx = int(args[1]) - 1 if len(args) > 1 else 0
        if 0 <= idx < len(notes):
            n = notes[idx]
            os.system('cls' if os.name == 'nt' else 'clear')
            content = n['body'].split("\n")[:12]
            draw_edit_ui(f"{n['title'].upper()[:15]}.TXT", content, "ESC=Powrót  E=Edytuj")
        else:
            print("Nie ma takiej notatki.")

# --- Rejestracja ---
def register(api):
    @api.command("edit", "Edytor MS-DOS Style", aliases=["edit.exe"])
    def _edit(args):
        cmd_edit(args)

def unregister(api):
    api.unregister_command("edit")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
psterm_office — Pakiet biurowy dla psTERM / TerminalX
======================================================
Narzędzia biurowe z grafiką w stylu DOS (CP437 / ASCII box-drawing).

Komendy:
  note      — notatnik (dodaj, listuj, edytuj, usuń, szukaj)
  cal       — kalendarz miesięczny z wydarzeniami
  todo      — lista zadań z priorytetami i statusem
  contacts  — książka adresowa
  office    — panel główny — przegląd wszystkich modułów

Umieszcz plik w ~/.terminalx_plugins/psterm_office.py
Plugin zostanie załadowany automatycznie przy starcie psTERM.
"""

from __future__ import annotations

import json
import os
import re
import sys
import datetime
from pathlib import Path

# ── Metadane pluginu ──────────────────────────────────────────────────────────

PLUGIN_META = {
    "name":         "psterm_office",
    "version":      "1.0.0",
    "author":       "Sebastian Januchowski / psTERM / polsoft.ITS",
    "description":  "Pakiet biurowy: notatnik, kalendarz, todo, kontakty — styl DOS",
    "tags":         ["biuro", "notatki", "kalendarz", "todo", "kontakty", "office"],
    "requires_api": (2, 0),
    "homepage":     "",
    "license":      "MIT",
}

# ── Ścieżki danych ────────────────────────────────────────────────────────────

def _data_dir() -> Path:
    """Katalog danych: obok skryptu TerminalX lub ~/.terminalx_office/"""
    # Próbujemy wykryć _BASE z głównego modułu
    try:
        import __main__ as _m
        base = getattr(_m, "_BASE", None)
        if base:
            d = Path(base) / ".terminalx_office"
            d.mkdir(parents=True, exist_ok=True)
            return d
    except Exception:
        pass
    d = Path.home() / ".terminalx_office"
    d.mkdir(parents=True, exist_ok=True)
    return d

DATA_DIR     = _data_dir()
NOTES_FILE   = DATA_DIR / "notes.json"
EVENTS_FILE  = DATA_DIR / "events.json"
TODO_FILE    = DATA_DIR / "todo.json"
CONTACTS_FILE= DATA_DIR / "contacts.json"

# ── Kolory ANSI ───────────────────────────────────────────────────────────────

class _A:
    """Minimalne kolory ANSI — nie zależą od motywu TerminalX."""
    _on = sys.stdout.isatty() and not os.environ.get("NO_COLOR")

    RESET  = "\033[0m"      if _on else ""
    BOLD   = "\033[1m"      if _on else ""
    DIM    = "\033[2m"      if _on else ""

    # kolory tekstu
    BLK    = "\033[30m"     if _on else ""
    RED    = "\033[31m"     if _on else ""
    GRN    = "\033[32m"     if _on else ""
    YLW    = "\033[33m"     if _on else ""
    BLU    = "\033[34m"     if _on else ""
    MAG    = "\033[35m"     if _on else ""
    CYN    = "\033[36m"     if _on else ""
    WHT    = "\033[37m"     if _on else ""

    # jasne warianty
    LRED   = "\033[91m"     if _on else ""
    LGRN   = "\033[92m"     if _on else ""
    LYLW   = "\033[93m"     if _on else ""
    LBLU   = "\033[94m"     if _on else ""
    LMAG   = "\033[95m"     if _on else ""
    LCYN   = "\033[96m"     if _on else ""
    LWHT   = "\033[97m"     if _on else ""

    # tła
    BG_BLU = "\033[44m"     if _on else ""
    BG_CYN = "\033[46m"     if _on else ""
    BG_GRN = "\033[42m"     if _on else ""
    BG_RED = "\033[41m"     if _on else ""

A = _A()

# ── Rysowanie ramek DOS (box-drawing CP437) ───────────────────────────────────

class _Box:
    """Zestawy znaków ramkowych — podwójna i pojedyncza linia (DOS/CP437)."""

    DOUBLE = {
        "TL": "╔", "TR": "╗", "BL": "╚", "BR": "╝",
        "H":  "═", "V":  "║",
        "TT": "╦", "BT": "╩", "LT": "╠", "RT": "╣", "CR": "╬",
    }
    SINGLE = {
        "TL": "┌", "TR": "┐", "BL": "└", "BR": "┘",
        "H":  "─", "V":  "│",
        "TT": "┬", "BT": "┴", "LT": "├", "RT": "┤", "CR": "┼",
    }
    THICK = {
        "TL": "▛", "TR": "▜", "BL": "▙", "BR": "▟",
        "H":  "▀", "V":  "▌",
        "TT": "▀", "BT": "▄", "LT": "▌", "RT": "▐", "CR": "+",
    }

BOX = _Box()

def _tw() -> int:
    """Szerokość terminala — bezpieczna."""
    try:
        return min(os.get_terminal_size().columns - 2, 78)
    except Exception:
        return 76

def _strip_ansi(s: str) -> str:
    return re.sub(r"\033\[[0-9;]*m", "", s)

def _vw(s: str) -> int:
    """Wizualna szerokość stringa (bez kodów ANSI)."""
    return len(_strip_ansi(s))

def box_top(title: str = "", w: int = 0, color: str = "", style: dict = None) -> str:
    c  = style or BOX.DOUBLE
    w  = w or _tw()
    co = color or A.CYN
    if title:
        t    = f" {title} "
        fill = max(2, w - 2 - len(t))
        bar  = c["H"] * 2 + t + c["H"] * fill
    else:
        bar = c["H"] * w
    return f"{co}{c['TL']}{bar}{c['TR']}{A.RESET}"

def box_row(text: str = "", w: int = 0, color: str = "", style: dict = None) -> str:
    c   = style or BOX.DOUBLE
    w   = w or _tw()
    co  = color or A.CYN
    vw  = _vw(text)
    pad = max(0, w - 2 - vw)
    return f"{co}{c['V']}{A.RESET} {text}{' ' * pad} {co}{c['V']}{A.RESET}"

def box_sep(w: int = 0, color: str = "", style: dict = None) -> str:
    c  = style or BOX.DOUBLE
    w  = w or _tw()
    co = color or A.CYN
    return f"{co}{c['LT']}{c['H'] * w}{c['RT']}{A.RESET}"

def box_bot(w: int = 0, color: str = "", style: dict = None) -> str:
    c  = style or BOX.DOUBLE
    w  = w or _tw()
    co = color or A.CYN
    return f"{co}{c['BL']}{c['H'] * w}{c['BR']}{A.RESET}"

def box_title(title: str, subtitle: str = "", w: int = 0,
              color: str = "", style: dict = None) -> None:
    """Drukuje pełną ramkę tytułową."""
    w = w or _tw()
    print(box_top(title, w=w, color=color, style=style))
    if subtitle:
        print(box_row(f"{A.DIM}{subtitle}{A.RESET}", w=w, color=color, style=style))
        print(box_sep(w=w, color=color, style=style))

def hr(w: int = 0, color: str = "", ch: str = "─") -> str:
    w = w or _tw()
    return f"{color or A.DIM}{ch * (w + 2)}{A.RESET}"

def badge(text: str, bg: str = "", fg: str = "") -> str:
    bg = bg or A.BG_BLU
    fg = fg or A.LWHT
    return f"{bg}{fg} {text} {A.RESET}"

# ── Helpers JSON ──────────────────────────────────────────────────────────────

def _load(path: Path, default=None):
    if default is None:
        default = []
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default

def _save(path: Path, data) -> bool:
    try:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    except Exception as e:
        print(f"{A.RED}[!] Błąd zapisu {path.name}: {e}{A.RESET}")
        return False

def _now_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def _today() -> str:
    return datetime.date.today().isoformat()

# ── INPUT helper ──────────────────────────────────────────────────────────────

def _ask(prompt: str, default: str = "") -> str:
    """Interaktywne pytanie z podpowiedzią."""
    hint = f" [{default}]" if default else ""
    try:
        val = input(f"  {A.LYLW}{prompt}{hint}{A.RESET}: ").strip()
        return val or default
    except (EOFError, KeyboardInterrupt):
        return default

def _confirm(prompt: str) -> bool:
    try:
        return input(f"  {A.YLW}{prompt} [T/n]{A.RESET}: ").strip().lower() not in ("n", "nie", "no")
    except (EOFError, KeyboardInterrupt):
        return False

# ═══════════════════════════════════════════════════════════════════════════════
#  MODUŁ 1 — NOTATNIK
# ═══════════════════════════════════════════════════════════════════════════════

def _notes_load() -> list:
    return _load(NOTES_FILE, [])

def _notes_save(data: list) -> bool:
    return _save(NOTES_FILE, data)

def cmd_note(args: list):
    """
    note                   — lista notatek
    note add [tytuł]       — nowa notatka
    note show <nr>         — pokaż notatkę
    note edit <nr>         — edytuj notatkę
    note del <nr>          — usuń notatkę
    note find <szukaj>     — szukaj w notatkach
    note export [plik]     — eksport do .txt
    """
    sub  = args[0].lower() if args else "list"
    rest = args[1:]
    w    = _tw()

    # ── list ──────────────────────────────────────────────────────────────────
    if sub in ("list", "ls", ""):
        notes = _notes_load()
        print()
        box_title("  NOTATNIK  ", f"Zapisane notatki: {len(notes)}  •  {NOTES_FILE}", w=w, color=A.CYN)
        if not notes:
            print(box_row(f"{A.DIM}  (brak notatek — użyj: note add){A.RESET}", w=w, color=A.CYN))
        else:
            for i, n in enumerate(notes, 1):
                preview = n.get("body", "")[:50].replace("\n", " ")
                title   = n.get("title", "(bez tytułu)")
                date    = n.get("date", "")
                num     = f"{A.LYLW}[{i:>2}]{A.RESET}"
                ti      = f"{A.BOLD}{A.LWHT}{title:<22}{A.RESET}"
                dt      = f"{A.DIM}{date}{A.RESET}"
                pr      = f" {A.DIM}…{preview}…{A.RESET}" if preview else ""
                print(box_row(f"{num} {ti} {dt}{pr}", w=w, color=A.CYN))
        print(box_bot(w=w, color=A.CYN))
        print(f"\n  {A.DIM}note add · note show <nr> · note edit <nr> · note del <nr> · note find <tekst>{A.RESET}\n")
        return

    # ── add ───────────────────────────────────────────────────────────────────
    if sub == "add":
        notes = _notes_load()
        print()
        box_title("  NOWA NOTATKA  ", w=w, color=A.GRN, style=BOX.SINGLE)
        title = " ".join(rest) if rest else _ask("Tytuł")
        if not title:
            print(f"  {A.RED}Anulowano — tytuł jest wymagany.{A.RESET}")
            return
        print(f"  {A.DIM}Treść (Enter = nowa linia, pusta linia = koniec):{A.RESET}")
        lines = []
        try:
            while True:
                ln = input("  > ")
                if ln == "" and lines and lines[-1] == "":
                    break
                lines.append(ln)
        except (EOFError, KeyboardInterrupt):
            pass
        body = "\n".join(lines).strip()
        note = {"id": len(notes) + 1, "title": title, "body": body, "date": _now_str()}
        notes.append(note)
        if _notes_save(notes):
            print(f"\n  {A.GRN}✔ Notatka [{len(notes)}] zapisana.{A.RESET}\n")
        return

    # ── show ──────────────────────────────────────────────────────────────────
    if sub in ("show", "view", "cat"):
        notes = _notes_load()
        idx   = int(rest[0]) - 1 if rest and rest[0].isdigit() else -1
        if idx < 0 or idx >= len(notes):
            print(f"  {A.RED}[!] Podaj numer notatki (1–{len(notes)}).{A.RESET}")
            return
        n = notes[idx]
        print()
        box_title(f"  {n.get('title','?')}  ", f"data: {n.get('date','')}  •  nr {idx+1}/{len(notes)}", w=w, color=A.CYN)
        for line in n.get("body", "(pusta)").split("\n"):
            print(box_row(f"  {line}", w=w, color=A.CYN))
        print(box_bot(w=w, color=A.CYN))
        print()
        return

    # ── edit ──────────────────────────────────────────────────────────────────
    if sub == "edit":
        notes = _notes_load()
        idx   = int(rest[0]) - 1 if rest and rest[0].isdigit() else -1
        if idx < 0 or idx >= len(notes):
            print(f"  {A.RED}[!] Podaj numer notatki.{A.RESET}")
            return
        n     = notes[idx]
        print()
        box_title(f"  EDYCJA: {n.get('title','?')}  ", w=w, color=A.YLW, style=BOX.SINGLE)
        new_title = _ask("Nowy tytuł", n.get("title", ""))
        print(f"  {A.DIM}Nowa treść (pusta linia = koniec):{A.RESET}")
        lines = []
        try:
            while True:
                ln = input("  > ")
                if ln == "" and lines and lines[-1] == "":
                    break
                lines.append(ln)
        except (EOFError, KeyboardInterrupt):
            pass
        new_body = "\n".join(lines).strip() or n.get("body", "")
        notes[idx]["title"]   = new_title
        notes[idx]["body"]    = new_body
        notes[idx]["edited"]  = _now_str()
        if _notes_save(notes):
            print(f"\n  {A.GRN}✔ Notatka [{idx+1}] zaktualizowana.{A.RESET}\n")
        return

    # ── del ───────────────────────────────────────────────────────────────────
    if sub in ("del", "rm", "delete", "remove"):
        notes = _notes_load()
        idx   = int(rest[0]) - 1 if rest and rest[0].isdigit() else -1
        if idx < 0 or idx >= len(notes):
            print(f"  {A.RED}[!] Podaj numer notatki.{A.RESET}")
            return
        n = notes[idx]
        if _confirm(f"Usunąć notatkę [{idx+1}] \"{n.get('title','?')}\"?"):
            notes.pop(idx)
            if _notes_save(notes):
                print(f"  {A.GRN}✔ Usunięto.{A.RESET}")
        else:
            print(f"  {A.DIM}Anulowano.{A.RESET}")
        return

    # ── find ──────────────────────────────────────────────────────────────────
    if sub in ("find", "search", "grep"):
        notes = _notes_load()
        query = " ".join(rest).lower()
        if not query:
            print(f"  {A.RED}[!] Podaj szukaną frazę.{A.RESET}")
            return
        results = [
            (i+1, n) for i, n in enumerate(notes)
            if query in n.get("title","").lower() or query in n.get("body","").lower()
        ]
        print()
        box_title(f"  WYNIKI: \"{query}\"  ", f"Znaleziono: {len(results)}", w=w, color=A.MAG)
        if not results:
            print(box_row(f"  {A.DIM}(brak wyników){A.RESET}", w=w, color=A.MAG))
        for nr, n in results:
            hl_title = n.get("title","")
            preview  = n.get("body","")[:60].replace("\n"," ")
            print(box_row(f"  {A.LYLW}[{nr:>2}]{A.RESET}  {A.BOLD}{hl_title}{A.RESET}  {A.DIM}{preview}{A.RESET}", w=w, color=A.MAG))
        print(box_bot(w=w, color=A.MAG))
        print()
        return

    # ── export ────────────────────────────────────────────────────────────────
    if sub == "export":
        notes  = _notes_load()
        target = Path(rest[0]) if rest else Path("notatki_export.txt")
        lines  = []
        for i, n in enumerate(notes, 1):
            lines.append(f"{'='*60}")
            lines.append(f"[{i}] {n.get('title','(brak)')}  •  {n.get('date','')}")
            lines.append(f"{'='*60}")
            lines.append(n.get("body",""))
            lines.append("")
        try:
            target.write_text("\n".join(lines), encoding="utf-8")
            print(f"  {A.GRN}✔ Wyeksportowano {len(notes)} notatek → {target}{A.RESET}")
        except Exception as e:
            print(f"  {A.RED}[!] Błąd: {e}{A.RESET}")
        return

    print(f"  {A.RED}[!] Nieznana podkomenda: {sub}{A.RESET}")
    print(f"  {A.DIM}Dostępne: list, add, show, edit, del, find, export{A.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
#  MODUŁ 2 — KALENDARZ
# ═══════════════════════════════════════════════════════════════════════════════

def _events_load() -> list:
    return _load(EVENTS_FILE, [])

def _events_save(data: list) -> bool:
    return _save(EVENTS_FILE, data)

def _cal_month(year: int, month: int, events: list) -> None:
    """Rysuje kalendarz miesięczny w stylu DOS."""
    import calendar
    w        = _tw()
    days_pl  = ["Pn","Wt","Śr","Cz","Pt","Sb","Nd"]
    months_pl= ["","Styczeń","Luty","Marzec","Kwiecień","Maj","Czerwiec",
                "Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień"]
    today    = datetime.date.today()
    cal      = calendar.monthcalendar(year, month)

    # Zbierz daty wydarzeń w tym miesiącu
    ev_dates: dict[int, list[str]] = {}
    for ev in events:
        try:
            d = datetime.date.fromisoformat(ev.get("date",""))
            if d.year == year and d.month == month:
                ev_dates.setdefault(d.day, []).append(ev.get("title","?"))
        except Exception:
            pass

    title_str = f"  {months_pl[month]} {year}  "
    print()
    print(box_top(title_str, w=w, color=A.CYN))

    # Nagłówek dni tygodnia
    header = "  " + "  ".join(
        f"{A.BOLD}{A.LYLW}{d}{A.CYN}" if i == 6 else
        f"{A.BOLD}{A.LRED}{d}{A.CYN}"  if i == 5 else
        f"{A.BOLD}{A.LWHT}{d}{A.CYN}"
        for i, d in enumerate(days_pl)
    ) + "  "
    print(box_row(header, w=w, color=A.CYN))
    print(box_sep(w=w, color=A.CYN))

    # Tygodnie
    for week in cal:
        cells = []
        for i, day in enumerate(week):
            if day == 0:
                cells.append("   ")
            else:
                is_today  = (day == today.day and month == today.month and year == today.year)
                has_event = day in ev_dates
                num_str   = f"{day:>2}"
                if is_today:
                    cell = f"{A.BG_GRN}{A.BLK}{A.BOLD}{num_str}{A.CYN}"
                elif has_event:
                    cell = f"{A.LMAG}{A.BOLD}{num_str}{A.CYN}"
                elif i == 6:  # niedziela
                    cell = f"{A.LYLW}{num_str}{A.CYN}"
                elif i == 5:  # sobota
                    cell = f"{A.LRED}{num_str}{A.CYN}"
                else:
                    cell = f"{num_str}"
                cells.append(cell + " ")
        row_str = "  " + " ".join(cells)
        print(box_row(row_str, w=w, color=A.CYN))

    print(box_sep(w=w, color=A.CYN))

    # Legenda + wydarzenia tego miesiąca
    today_badge = f"{A.BG_GRN}{A.BLK} dziś {A.RESET}"
    event_badge = f"{A.LMAG}■{A.RESET} wydarzenie"
    sat_badge   = f"{A.LRED}Sb{A.RESET}"
    sun_badge   = f"{A.LYLW}Nd{A.RESET}"
    print(box_row(f"  {today_badge}  {event_badge}  {sat_badge} sobota  {sun_badge} niedziela", w=w, color=A.CYN))

    if ev_dates:
        print(box_sep(w=w, color=A.CYN))
        print(box_row(f"  {A.BOLD}Wydarzenia w tym miesiącu:{A.RESET}", w=w, color=A.CYN))
        for day in sorted(ev_dates):
            for title in ev_dates[day]:
                d_str = f"{year}-{month:02d}-{day:02d}"
                print(box_row(f"    {A.LMAG}◆{A.RESET} {A.DIM}{d_str}{A.RESET}  {A.LWHT}{title}{A.RESET}", w=w, color=A.CYN))

    print(box_bot(w=w, color=A.CYN))
    print()

def cmd_cal(args: list):
    """
    cal                      — bieżący miesiąc z wydarzeniami
    cal <MM> <RRRR>          — wybrany miesiąc
    cal add <data> <tytuł>   — dodaj wydarzenie (data: RRRR-MM-DD)
    cal list [<RRRR>]        — wszystkie wydarzenia
    cal del <nr>             — usuń wydarzenie
    cal today                — dzisiejsze wydarzenia
    """
    sub  = args[0].lower() if args else "show"
    rest = args[1:]
    w    = _tw()
    today = datetime.date.today()

    # ── show / default ────────────────────────────────────────────────────────
    if sub in ("show", "view") or (sub.isdigit() and not rest):
        # cal [MM [RRRR]]
        try:
            month = int(sub) if sub.isdigit() else today.month
            year  = int(rest[0]) if rest else today.year
        except Exception:
            month, year = today.month, today.year
        _cal_month(year, month, _events_load())
        return

    if sub in ("show", "") or not args:
        _cal_month(today.year, today.month, _events_load())
        return

    # ── add ───────────────────────────────────────────────────────────────────
    if sub == "add":
        events = _events_load()
        print()
        box_title("  NOWE WYDARZENIE  ", w=w, color=A.GRN, style=BOX.SINGLE)
        date_str = rest[0] if rest else _ask("Data (RRRR-MM-DD)", _today())
        title    = " ".join(rest[1:]) if len(rest) > 1 else _ask("Tytuł wydarzenia")
        if not title:
            print(f"  {A.RED}Anulowano — tytuł jest wymagany.{A.RESET}")
            return
        try:
            datetime.date.fromisoformat(date_str)
        except ValueError:
            print(f"  {A.RED}[!] Nieprawidłowy format daty. Użyj: RRRR-MM-DD{A.RESET}")
            return
        note   = _ask("Notatka (opcjonalnie)", "")
        repeat = _ask("Powtarzanie (brak/codziennie/tygodniowo/miesięcznie)", "brak")
        ev = {
            "id":     len(events) + 1,
            "date":   date_str,
            "title":  title,
            "note":   note,
            "repeat": repeat,
            "added":  _now_str(),
        }
        events.append(ev)
        if _events_save(events):
            print(f"\n  {A.GRN}✔ Wydarzenie [{len(events)}] dodane: {title} ({date_str}){A.RESET}\n")
        return

    # ── list ──────────────────────────────────────────────────────────────────
    if sub in ("list", "ls", "all"):
        events = _events_load()
        year   = int(rest[0]) if rest and rest[0].isdigit() else None
        shown  = [
            (i+1, ev) for i, ev in enumerate(events)
            if not year or ev.get("date","").startswith(str(year))
        ]
        print()
        box_title("  WSZYSTKIE WYDARZENIA  ", f"Łącznie: {len(shown)}", w=w, color=A.CYN)
        if not shown:
            print(box_row(f"  {A.DIM}(brak wydarzeń){A.RESET}", w=w, color=A.CYN))
        else:
            for nr, ev in shown:
                d   = ev.get("date","?")
                ti  = ev.get("title","?")
                rep = ev.get("repeat","")
                rep_str = f" {A.DIM}[{rep}]{A.RESET}" if rep and rep != "brak" else ""
                print(box_row(
                    f"  {A.LYLW}[{nr:>2}]{A.RESET}  "
                    f"{A.LCYN}{d}{A.RESET}  "
                    f"{A.LWHT}{ti}{A.RESET}{rep_str}", w=w, color=A.CYN))
        print(box_bot(w=w, color=A.CYN))
        print()
        return

    # ── today ─────────────────────────────────────────────────────────────────
    if sub == "today":
        events  = _events_load()
        today_s = _today()
        todayev = [(i+1, ev) for i, ev in enumerate(events) if ev.get("date","") == today_s]
        print()
        box_title(f"  DZISIAJ: {today_s}  ", f"Wydarzeń: {len(todayev)}", w=w, color=A.GRN)
        if not todayev:
            print(box_row(f"  {A.DIM}Brak wydarzeń na dziś.{A.RESET}", w=w, color=A.GRN))
        for nr, ev in todayev:
            note = f"  {A.DIM}{ev.get('note','')}{A.RESET}" if ev.get("note") else ""
            print(box_row(f"  {A.LYLW}[{nr}]{A.RESET}  {A.BOLD}{ev.get('title','?')}{A.RESET}{note}", w=w, color=A.GRN))
        print(box_bot(w=w, color=A.GRN))
        print()
        return

    # ── del ───────────────────────────────────────────────────────────────────
    if sub in ("del", "rm", "delete"):
        events = _events_load()
        idx    = int(rest[0]) - 1 if rest and rest[0].isdigit() else -1
        if idx < 0 or idx >= len(events):
            print(f"  {A.RED}[!] Podaj numer wydarzenia (1–{len(events)}).{A.RESET}")
            return
        ev = events[idx]
        if _confirm(f"Usunąć [{idx+1}] \"{ev.get('title','?')}\" ({ev.get('date','?')})?"):
            events.pop(idx)
            _events_save(events)
            print(f"  {A.GRN}✔ Usunięto.{A.RESET}")
        else:
            print(f"  {A.DIM}Anulowano.{A.RESET}")
        return

    # Domyślnie pokaż bieżący miesiąc (gdy podano np. "cal 4 2026")
    try:
        month = int(sub)
        year  = int(rest[0]) if rest else today.year
        _cal_month(year, month, _events_load())
    except Exception:
        print(f"  {A.RED}[!] Nieznana podkomenda: {sub}{A.RESET}")
        print(f"  {A.DIM}Dostępne: [MM RRRR], add, list, today, del{A.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
#  MODUŁ 3 — LISTA ZADAŃ (TODO)
# ═══════════════════════════════════════════════════════════════════════════════

_PRIORITIES = {"1": "!!!  PILNE", "2": "!!   WYSOKI", "3": "!    NORMALNY", "4": "     NISKI"}
_PRIO_COLORS = {"1": A.LRED, "2": A.LYLW, "3": A.LWHT, "4": A.DIM}
_STATUSES = {"todo": "[ ]", "done": "[✔]", "prog": "[→]", "skip": "[✘]"}
_STATUS_COLORS = {"todo": A.CYN, "done": A.GRN, "prog": A.YLW, "skip": A.DIM}

def _todo_load() -> list:
    return _load(TODO_FILE, [])

def _todo_save(data: list) -> bool:
    return _save(TODO_FILE, data)

def cmd_todo(args: list):
    """
    todo                        — lista zadań (wszystkie)
    todo add <tytuł>            — dodaj zadanie
    todo done <nr>              — oznacz jako zrobione
    todo prog <nr>              — oznacz jako w trakcie
    todo skip <nr>              — pomiń zadanie
    todo del <nr>               — usuń zadanie
    todo clear done             — usuń wszystkie zrobione
    todo prio <nr> <1-4>        — zmień priorytet
    todo pending                — tylko nieukończone
    """
    sub  = args[0].lower() if args else "list"
    rest = args[1:]
    w    = _tw()

    def _status_icon(task: dict) -> str:
        st  = task.get("status", "todo")
        col = _STATUS_COLORS.get(st, A.RESET)
        ico = _STATUSES.get(st, "[ ]")
        return f"{col}{ico}{A.RESET}"

    def _prio_str(task: dict) -> str:
        p   = str(task.get("priority", "3"))
        col = _PRIO_COLORS.get(p, A.RESET)
        txt = _PRIORITIES.get(p, "NORMALNY")
        return f"{col}{txt[0]}{A.RESET}"

    def _print_list(tasks: list, header: str = "LISTA ZADAŃ"):
        print()
        done_count  = sum(1 for t in tasks if t.get("status") == "done")
        total_count = len(tasks)
        box_title(
            f"  {header}  ",
            f"Łącznie: {total_count}  Ukończone: {done_count}  Pozostałe: {total_count - done_count}",
            w=w, color=A.BLU
        )
        if not tasks:
            print(box_row(f"  {A.DIM}(brak zadań — użyj: todo add <tytuł>){A.RESET}", w=w, color=A.BLU))
        else:
            current_prio = None
            for i, t in enumerate(tasks, 1):
                p = str(t.get("priority", "3"))
                if p != current_prio:
                    current_prio = p
                    prio_label = _PRIORITIES.get(p, "NORMALNY").strip()
                    prio_col   = _PRIO_COLORS.get(p, A.RESET)
                    print(box_sep(w=w, color=A.BLU))
                    print(box_row(f"  {prio_col}{A.BOLD}{prio_label}{A.RESET}", w=w, color=A.BLU))
                ico   = _status_icon(t)
                title = t.get("title","?")
                date  = t.get("date","")
                due   = f"  {A.LRED}do:{t.get('due','')}{A.RESET}" if t.get("due") else ""
                print(box_row(
                    f"  {A.LYLW}[{i:>2}]{A.RESET}  {ico}  {title}{due}  {A.DIM}{date}{A.RESET}",
                    w=w, color=A.BLU))
        print(box_bot(w=w, color=A.BLU))
        print(f"\n  {A.DIM}todo add · todo done/prog/skip <nr> · todo del <nr> · todo prio <nr> <1-4>{A.RESET}\n")

    # ── list ──────────────────────────────────────────────────────────────────
    if sub in ("list", "ls", ""):
        tasks = sorted(_todo_load(), key=lambda t: (t.get("priority","3"), t.get("status","todo")))
        _print_list(tasks)
        return

    # ── pending ───────────────────────────────────────────────────────────────
    if sub == "pending":
        tasks = [t for t in _todo_load() if t.get("status","todo") not in ("done","skip")]
        tasks.sort(key=lambda t: t.get("priority","3"))
        _print_list(tasks, "NIEUKOŃCZONE")
        return

    # ── add ───────────────────────────────────────────────────────────────────
    if sub == "add":
        tasks  = _todo_load()
        print()
        box_title("  NOWE ZADANIE  ", w=w, color=A.GRN, style=BOX.SINGLE)
        title  = " ".join(rest) if rest else _ask("Tytuł zadania")
        if not title:
            print(f"  {A.RED}Anulowano.{A.RESET}")
            return
        prio   = _ask("Priorytet (1=pilne, 2=wysoki, 3=normalny, 4=niski)", "3")
        due    = _ask("Termin (RRRR-MM-DD, opcjonalnie)", "")
        task = {
            "id":       len(tasks) + 1,
            "title":    title,
            "priority": prio if prio in ("1","2","3","4") else "3",
            "status":   "todo",
            "date":     _now_str(),
            "due":      due,
        }
        tasks.append(task)
        if _todo_save(tasks):
            print(f"\n  {A.GRN}✔ Zadanie [{len(tasks)}] dodane.{A.RESET}\n")
        return

    # ── status changes ────────────────────────────────────────────────────────
    if sub in ("done", "prog", "skip"):
        tasks = _todo_load()
        idx   = int(rest[0]) - 1 if rest and rest[0].isdigit() else -1
        if idx < 0 or idx >= len(tasks):
            print(f"  {A.RED}[!] Podaj numer zadania (1–{len(tasks)}).{A.RESET}")
            return
        tasks[idx]["status"] = sub
        if sub == "done":
            tasks[idx]["done_at"] = _now_str()
        if _todo_save(tasks):
            ico = _STATUSES.get(sub, "")
            col = _STATUS_COLORS.get(sub, A.RESET)
            print(f"  {col}{ico}{A.RESET}  [{idx+1}] {tasks[idx].get('title','?')}")
        return

    # ── prio ──────────────────────────────────────────────────────────────────
    if sub == "prio":
        tasks = _todo_load()
        idx   = int(rest[0]) - 1 if rest and rest[0].isdigit() else -1
        prio  = rest[1] if len(rest) > 1 else ""
        if idx < 0 or idx >= len(tasks) or prio not in ("1","2","3","4"):
            print(f"  {A.RED}[!] Użycie: todo prio <nr> <1-4>{A.RESET}")
            return
        tasks[idx]["priority"] = prio
        _todo_save(tasks)
        print(f"  {A.GRN}✔ Priorytet [{idx+1}] zmieniony na {_PRIORITIES[prio].strip()}.{A.RESET}")
        return

    # ── del ───────────────────────────────────────────────────────────────────
    if sub in ("del", "rm"):
        tasks = _todo_load()
        idx   = int(rest[0]) - 1 if rest and rest[0].isdigit() else -1
        if idx < 0 or idx >= len(tasks):
            print(f"  {A.RED}[!] Podaj numer zadania.{A.RESET}")
            return
        t = tasks[idx]
        if _confirm(f"Usunąć [{idx+1}] \"{t.get('title','?')}\"?"):
            tasks.pop(idx)
            _todo_save(tasks)
            print(f"  {A.GRN}✔ Usunięto.{A.RESET}")
        else:
            print(f"  {A.DIM}Anulowano.{A.RESET}")
        return

    # ── clear done ────────────────────────────────────────────────────────────
    if sub == "clear" and rest and rest[0] == "done":
        tasks = _todo_load()
        before = len(tasks)
        tasks  = [t for t in tasks if t.get("status") != "done"]
        _todo_save(tasks)
        print(f"  {A.GRN}✔ Usunięto {before - len(tasks)} ukończonych zadań.{A.RESET}")
        return

    print(f"  {A.RED}[!] Nieznana podkomenda: {sub}{A.RESET}")
    print(f"  {A.DIM}Dostępne: list, add, done, prog, skip, del, clear done, prio, pending{A.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
#  MODUŁ 4 — KONTAKTY
# ═══════════════════════════════════════════════════════════════════════════════

def _contacts_load() -> list:
    return _load(CONTACTS_FILE, [])

def _contacts_save(data: list) -> bool:
    return _save(CONTACTS_FILE, data)

def cmd_contacts(args: list):
    """
    contacts                  — lista kontaktów
    contacts add              — dodaj kontakt
    contacts show <nr>        — pokaż szczegóły kontaktu
    contacts find <szukaj>    — szukaj kontaktu
    contacts edit <nr>        — edytuj kontakt
    contacts del <nr>         — usuń kontakt
    contacts export [plik]    — eksport do .txt
    """
    sub  = args[0].lower() if args else "list"
    rest = args[1:]
    w    = _tw()

    # ── list ──────────────────────────────────────────────────────────────────
    if sub in ("list", "ls", ""):
        contacts = _contacts_load()
        print()
        box_title("  KSIĄŻKA ADRESOWA  ", f"Kontaktów: {len(contacts)}  •  {CONTACTS_FILE}", w=w, color=A.MAG)
        if not contacts:
            print(box_row(f"  {A.DIM}(brak kontaktów — użyj: contacts add){A.RESET}", w=w, color=A.MAG))
        else:
            for i, c in enumerate(contacts, 1):
                name  = c.get("name","?")
                phone = c.get("phone","")
                email = c.get("email","")
                info  = "  ".join(filter(None, [phone, email]))
                print(box_row(
                    f"  {A.LYLW}[{i:>2}]{A.RESET}  "
                    f"{A.BOLD}{A.LWHT}{name:<22}{A.RESET}  "
                    f"{A.DIM}{info}{A.RESET}", w=w, color=A.MAG))
        print(box_bot(w=w, color=A.MAG))
        print(f"\n  {A.DIM}contacts add · contacts show <nr> · contacts find <tekst> · contacts del <nr>{A.RESET}\n")
        return

    # ── add ───────────────────────────────────────────────────────────────────
    if sub == "add":
        contacts = _contacts_load()
        print()
        box_title("  NOWY KONTAKT  ", w=w, color=A.GRN, style=BOX.SINGLE)
        name    = _ask("Imię i nazwisko")
        if not name:
            print(f"  {A.RED}Anulowano — imię jest wymagane.{A.RESET}")
            return
        phone   = _ask("Telefon")
        email   = _ask("E-mail")
        company = _ask("Firma / organizacja")
        address = _ask("Adres")
        note    = _ask("Notatka")
        contact = {
            "id":      len(contacts) + 1,
            "name":    name,
            "phone":   phone,
            "email":   email,
            "company": company,
            "address": address,
            "note":    note,
            "added":   _now_str(),
        }
        contacts.append(contact)
        if _contacts_save(contacts):
            print(f"\n  {A.GRN}✔ Kontakt [{len(contacts)}] dodany: {name}{A.RESET}\n")
        return

    # ── show ──────────────────────────────────────────────────────────────────
    if sub in ("show", "view", "info"):
        contacts = _contacts_load()
        idx      = int(rest[0]) - 1 if rest and rest[0].isdigit() else -1
        if idx < 0 or idx >= len(contacts):
            print(f"  {A.RED}[!] Podaj numer kontaktu (1–{len(contacts)}).{A.RESET}")
            return
        c = contacts[idx]
        print()
        box_title(f"  {c.get('name','?')}  ", f"kontakt nr {idx+1}", w=w, color=A.MAG)
        fields = [
            ("Telefon",   c.get("phone","")),
            ("E-mail",    c.get("email","")),
            ("Firma",     c.get("company","")),
            ("Adres",     c.get("address","")),
            ("Notatka",   c.get("note","")),
            ("Dodano",    c.get("added","")),
        ]
        for key, val in fields:
            if val:
                print(box_row(f"  {A.DIM}{key:<10}{A.RESET}  {A.LWHT}{val}{A.RESET}", w=w, color=A.MAG))
        print(box_bot(w=w, color=A.MAG))
        print()
        return

    # ── find ──────────────────────────────────────────────────────────────────
    if sub in ("find", "search"):
        contacts = _contacts_load()
        query    = " ".join(rest).lower()
        if not query:
            print(f"  {A.RED}[!] Podaj szukaną frazę.{A.RESET}")
            return
        results = [
            (i+1, c) for i, c in enumerate(contacts)
            if any(query in str(v).lower() for v in c.values())
        ]
        print()
        box_title(f"  WYNIKI: \"{query}\"  ", f"Znaleziono: {len(results)}", w=w, color=A.MAG)
        if not results:
            print(box_row(f"  {A.DIM}(brak wyników){A.RESET}", w=w, color=A.MAG))
        for nr, c in results:
            info = "  ".join(filter(None, [c.get("phone",""), c.get("email","")]))
            print(box_row(
                f"  {A.LYLW}[{nr:>2}]{A.RESET}  {A.BOLD}{c.get('name','?'):<22}{A.RESET}  {A.DIM}{info}{A.RESET}",
                w=w, color=A.MAG))
        print(box_bot(w=w, color=A.MAG))
        print()
        return

    # ── edit ──────────────────────────────────────────────────────────────────
    if sub == "edit":
        contacts = _contacts_load()
        idx      = int(rest[0]) - 1 if rest and rest[0].isdigit() else -1
        if idx < 0 or idx >= len(contacts):
            print(f"  {A.RED}[!] Podaj numer kontaktu.{A.RESET}")
            return
        c = contacts[idx]
        print()
        box_title(f"  EDYCJA: {c.get('name','?')}  ", w=w, color=A.YLW, style=BOX.SINGLE)
        for field in ("name","phone","email","company","address","note"):
            contacts[idx][field] = _ask(field.capitalize(), c.get(field,""))
        contacts[idx]["edited"] = _now_str()
        if _contacts_save(contacts):
            print(f"\n  {A.GRN}✔ Kontakt [{idx+1}] zaktualizowany.{A.RESET}\n")
        return

    # ── del ───────────────────────────────────────────────────────────────────
    if sub in ("del", "rm"):
        contacts = _contacts_load()
        idx      = int(rest[0]) - 1 if rest and rest[0].isdigit() else -1
        if idx < 0 or idx >= len(contacts):
            print(f"  {A.RED}[!] Podaj numer kontaktu.{A.RESET}")
            return
        c = contacts[idx]
        if _confirm(f"Usunąć [{idx+1}] \"{c.get('name','?')}\"?"):
            contacts.pop(idx)
            _contacts_save(contacts)
            print(f"  {A.GRN}✔ Usunięto.{A.RESET}")
        else:
            print(f"  {A.DIM}Anulowano.{A.RESET}")
        return

    # ── export ────────────────────────────────────────────────────────────────
    if sub == "export":
        contacts = _contacts_load()
        target   = Path(rest[0]) if rest else Path("kontakty_export.txt")
        lines    = []
        for i, c in enumerate(contacts, 1):
            lines.append(f"{'='*60}")
            lines.append(f"[{i}] {c.get('name','?')}")
            for k in ("phone","email","company","address","note"):
                if c.get(k):
                    lines.append(f"  {k.capitalize()}: {c[k]}")
            lines.append("")
        try:
            target.write_text("\n".join(lines), encoding="utf-8")
            print(f"  {A.GRN}✔ Wyeksportowano {len(contacts)} kontaktów → {target}{A.RESET}")
        except Exception as e:
            print(f"  {A.RED}[!] Błąd: {e}{A.RESET}")
        return

    print(f"  {A.RED}[!] Nieznana podkomenda: {sub}{A.RESET}")
    print(f"  {A.DIM}Dostępne: list, add, show, edit, del, find, export{A.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL GŁÓWNY — office
# ═══════════════════════════════════════════════════════════════════════════════

def cmd_office(args: list):
    """
    office    — panel przeglądu wszystkich modułów biurowych
    """
    w      = _tw()
    today  = datetime.date.today()
    now    = datetime.datetime.now()

    notes    = _notes_load()
    events   = _events_load()
    todos    = _todo_load()
    contacts = _contacts_load()

    # Dzisiejsze wydarzenia
    today_ev = [ev for ev in events if ev.get("date","") == today.isoformat()]

    # Nieukończone zadania
    pending  = [t for t in todos if t.get("status","todo") not in ("done","skip")]
    urgent   = [t for t in pending if str(t.get("priority","3")) == "1"]

    print()
    print(box_top(f"  psTERM OFFICE  ·  {now.strftime('%A, %d %B %Y  %H:%M')}  ", w=w, color=A.CYN))
    print(box_row("", w=w, color=A.CYN))

    # Wiersz statystyk
    def stat(label: str, val: str, col: str = "") -> str:
        col = col or A.LCYN
        return f"  {A.DIM}{label}:{A.RESET} {col}{A.BOLD}{val:<5}{A.RESET}"

    row = (
        stat("Notatki",   str(len(notes)),    A.LCYN)  +
        stat("Kalend.",   str(len(events)),   A.LMAG)  +
        stat("Todo",      str(len(pending)),  A.YLW)   +
        stat("Kontakty",  str(len(contacts)), A.GRN)
    )
    print(box_row(row, w=w, color=A.CYN))
    print(box_sep(w=w, color=A.CYN))

    # Dzisiejsze wydarzenia
    print(box_row(f"  {A.BOLD}{A.LMAG}◆ DZIŚ ({today.isoformat()}){A.RESET}", w=w, color=A.CYN))
    if today_ev:
        for ev in today_ev:
            print(box_row(f"    {A.LMAG}›{A.RESET} {ev.get('title','?')}", w=w, color=A.CYN))
    else:
        print(box_row(f"    {A.DIM}(brak wydarzeń na dziś){A.RESET}", w=w, color=A.CYN))

    print(box_sep(w=w, color=A.CYN))

    # Pilne zadania
    print(box_row(f"  {A.BOLD}{A.LRED}!!! PILNE ZADANIA{A.RESET}", w=w, color=A.CYN))
    if urgent:
        for t in urgent[:5]:
            due = f"  {A.LRED}(do: {t.get('due','')}){A.RESET}" if t.get("due") else ""
            print(box_row(f"    {A.LRED}»{A.RESET} {t.get('title','?')}{due}", w=w, color=A.CYN))
    else:
        print(box_row(f"    {A.DIM}(brak pilnych zadań){A.RESET}", w=w, color=A.CYN))

    # Ostatnie notatki
    print(box_sep(w=w, color=A.CYN))
    print(box_row(f"  {A.BOLD}{A.LCYN}📋 OSTATNIE NOTATKI{A.RESET}", w=w, color=A.CYN))
    for i, n in enumerate(reversed(notes[-3:]), 1):
        print(box_row(f"    {A.CYN}›{A.RESET} {n.get('title','?')}  {A.DIM}{n.get('date','')}{A.RESET}", w=w, color=A.CYN))
    if not notes:
        print(box_row(f"    {A.DIM}(brak notatek){A.RESET}", w=w, color=A.CYN))

    print(box_sep(w=w, color=A.CYN))

    # Dostępne komendy
    cmds = [
        ("note",     "Notatnik",         A.LCYN),
        ("cal",      "Kalendarz",        A.LMAG),
        ("todo",     "Lista zadań",      A.YLW),
        ("contacts", "Książka adresowa", A.GRN),
    ]
    print(box_row(f"  {A.BOLD}KOMENDY:{A.RESET}", w=w, color=A.CYN))
    for cmd, label, col in cmds:
        print(box_row(f"    {col}{A.BOLD}{cmd:<12}{A.RESET}  {A.DIM}{label}{A.RESET}", w=w, color=A.CYN))

    print(box_row("", w=w, color=A.CYN))
    print(box_bot(w=w, color=A.CYN))
    print()


# ═══════════════════════════════════════════════════════════════════════════════
#  REJESTRACJA PLUGINU
# ═══════════════════════════════════════════════════════════════════════════════

def register(api):
    """Rejestruje wszystkie komendy biurowe w shellu."""

    @api.command("note", "Notatnik — dodaj, przeglądaj i szukaj notatek",
                 aliases=["notatnik", "notes"])
    def _note(args):
        cmd_note(args)

    @api.command("cal", "Kalendarz — miesięczny widok z wydarzeniami",
                 aliases=["kalendarz", "calendar"])
    def _cal(args):
        cmd_cal(args)

    @api.command("todo", "Lista zadań — priorytety, statusy, terminy",
                 aliases=["task", "tasks", "zadania"])
    def _todo(args):
        cmd_todo(args)

    @api.command("contacts", "Książka adresowa — kontakty z wyszukiwaniem",
                 aliases=["kontakty", "contact", "adr"])
    def _contacts(args):
        cmd_contacts(args)

    @api.command("office", "Panel biurowy — przegląd wszystkich modułów",
                 aliases=["biuro"])
    def _office(args):
        cmd_office(args)

    # Hook startowy — pokaż dzisiejsze wydarzenia po uruchomieniu shella
    def _on_start():
        today_ev = [
            ev for ev in _events_load()
            if ev.get("date","") == datetime.date.today().isoformat()
        ]
        pending_urgent = [
            t for t in _todo_load()
            if t.get("status","todo") not in ("done","skip")
            and str(t.get("priority","3")) == "1"
        ]
        if today_ev or pending_urgent:
            w = _tw()
            print()
            print(box_top("  psTERM OFFICE  ", w=w, color=A.CYN))
            if today_ev:
                for ev in today_ev:
                    print(box_row(f"  {A.LMAG}◆{A.RESET}  Dziś: {A.BOLD}{ev.get('title','?')}{A.RESET}", w=w, color=A.CYN))
            if pending_urgent:
                for t in pending_urgent[:3]:
                    print(box_row(f"  {A.LRED}!{A.RESET}  Pilne: {A.BOLD}{t.get('title','?')}{A.RESET}", w=w, color=A.CYN))
            print(box_bot(w=w, color=A.CYN))
            print()

    api.add_hook("on_start", _on_start)


def unregister(api):
    """Usuwa komendy biurowe przy wyładowaniu pluginu."""
    for name in ("note", "notatnik", "notes",
                 "cal", "kalendarz", "calendar",
                 "todo", "task", "tasks", "zadania",
                 "contacts", "kontakty", "contact", "adr",
                 "office", "biuro"):
        api.unregister_command(name)

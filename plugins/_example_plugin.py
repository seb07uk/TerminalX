"""
Przykladowy plugin TerminalXa z pelna specyfikacja metadanych.
Umieszcz plik .py w ~/.terminalx_plugins/ — zostanie zaladowany automatycznie.
"""

# ── Metadane pluginu (zalecane) ───────────────────────────────────────────────
# Slownik PLUGIN_META jest odczytywany przez system pluginow TerminalXa.
# Wszystkie pola sa opcjonalne, ale zalecane dla dobrego 'plugin info'.

PLUGIN_META = {
    "name":         "example",           # krotka nazwa (bez spacji)
    "version":      "1.0.0",             # semver
    "author":       "Autor Pluginu",     # imie/nick
    "description":  "Przykladowy plugin pokazujacy mozliwosci API shella",
    "tags":         ["przyklad", "demo"],# dowolne tagi
    "requires_api": (2, 0),              # minimalna wersja API TerminalXa
    "homepage":     "",                  # URL repo/docs (opcjonalne)
    "license":      "MIT",               # licencja
}

# Alternatywnie mozna uzyc zmiennych modulowych (niższy priorytet niz PLUGIN_META):
# __version__     = "1.0.0"
# __author__      = "Autor"
# __description__ = "Opis"
# __tags__        = ["tag1"]
# __requires_api__= (2, 0)

def register(api):
    """
    Wywoływana przy ladowaniu pluginu.
    api — obiekt ShellAPI z metodami: command(), print_info(), print_error(),
          unregister_command(), is_root, cwd, history, aliases, builtins,
          add_hook(), shell_version, plugin_api_version
    """

    @api.command("hello", "Przywitaj uzytkownika [plugin przykladowy]",
                 aliases=["hi"])
    def cmd_hello(args):
        """
        hello [imie]   - wyswietla powitanie
        hello          - pyta o imie interaktywnie
        """
        name = " ".join(args) if args else input("Podaj imie: ").strip()
        api.print_info(f"Czesc, {name or 'swiecie'}! (root={api.is_root})")

    @api.command("shellinfo", "Informacje o biezacym stanie shella")
    def cmd_shellinfo(args):
        api.print_raw(f"  Katalog    : {api.cwd}")
        api.print_raw(f"  Tryb root  : {api.is_root}")
        api.print_raw(f"  Komendy    : {len(api.builtins)}")
        api.print_raw(f"  Historia   : {len(api.history)} wpisow")
        api.print_raw(f"  Aliasy     : {len(api.aliases)}")
        api.print_raw(f"  API wersja : {api.plugin_api_version}")

    # Przyklad rejestracji hooka — wywolywany przed kazda komenda
    def my_before_hook(cmd_name, args):
        # Zwroc False zeby przerwac wykonanie komendy, True/None zeby kontynuowac
        pass  # mozna tu logowac, audytowac, walidowac, itp.

    api.add_hook("before_cmd", my_before_hook)

def unregister(api):
    """Wywoływana przy plugin unload / reload — posprzataj po sobie."""
    api.unregister_command("hello")
    api.unregister_command("shellinfo")
    # Usun hooki jesli zostaly zarejestrowane (opcjonalne — shell sam sprząta)

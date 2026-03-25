# TerminalX

**Lekki, rozszerzalny, wieloplatformowy terminal napisany w czystym Pythonie.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Licencja: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Wersja](https://img.shields.io/badge/wersja-35.2-green.svg)](CHANGELOG)
[![Platforma](https://img.shields.io/badge/platforma-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

TerminalX to w pełni funkcjonalny, wieloplatformowy interaktywny shell zawarty w **jednym pliku Pythona**, bez żadnych zewnętrznych zależności (tylko stdlib). Oferuje wbudowany edytor tekstowy, system pluginów, menedżer pakietów, narzędzia deweloperskie, zarządzanie sesjami i ponad 100 wbudowanych komend — przenośny i kompletnie samodzielny.

> **Autor:** Sebastian Januchowski — [github.com/polsoft](https://github.com/polsoft)  
> **Strona domowa:** [github.com/polsoft/TerminalX](https://github.com/polsoft/TerminalX)  
> **Licencja:** MIT

---

## Spis treści

- [Wymagania](#wymagania)
- [Szybki start](#szybki-start)
- [Tryby instalacji](#tryby-instalacji)
- [Zmienne środowiskowe](#zmienne-środowiskowe)
- [Wbudowane komendy](#wbudowane-komendy)
- [System pluginów](#system-pluginów)
- [Menedżer pakietów](#menedżer-pakietów)
- [Konfiguracja](#konfiguracja)
- [Motywy i profile](#motywy-i-profile)
- [Zaawansowane funkcje](#zaawansowane-funkcje)
- [Rozwiązywanie problemów](#rozwiązywanie-problemów)
- [Historia zmian](#historia-zmian)
- [Licencja](#licencja)

---

## Wymagania

| Wymaganie | Szczegóły |
|---|---|
| Python | 3.10 lub nowszy |
| System operacyjny | Windows, Linux, macOS |
| Zależności | Brak (tylko stdlib) |
| Opcjonalne | `windows-curses` dla edytora nano-lite na Windows |

Aby zainstalować opcjonalną obsługę curses na Windows:

```
pip install windows-curses
```

---

## Szybki start

```bash
# Uruchom bezpośrednio
python TerminalX.py

# Uruchom w trybie awaryjnym (safe mode)
python TerminalX.py --safe

# Uruchom w trybie przenośnym (wszystkie dane obok skryptu)
python TerminalX.py --portable

# Wskaż niestandardowy katalog danych
python TerminalX.py --data /ścieżka/do/danych
```

Po uruchomieniu wpisz `help`, aby zobaczyć dostępne komendy, lub `about`, aby uzyskać informacje o shellu.

---

## Tryby instalacji

TerminalX obsługuje kilka scenariuszy wdrożenia.

### Tryb standardowy
Wszystkie dane (historia, aliasy, pluginy, pakiety, konfiguracja) są przechowywane w katalogu domowym (`~/.terminalx_*`).

### Tryb przenośny (Portable)
Aktywowany przez jedno z poniższych:
- Flaga `--portable` przy uruchomieniu
- Ustawienie zmiennej środowiskowej `TERMINALX_DATA`
- Parametr `--data <ścieżka>` przy uruchomieniu
- Obecność folderu `.terminalx_data/` obok skryptu

W trybie przenośnym wszystkie dane są przechowywane w `.terminalx_data/` obok skryptu. Umożliwia to uruchamianie TerminalX z pendrive'a, udziału sieciowego lub kontenera bez konfiguracji systemu hosta.

### Tryb skompilowany (Frozen)
TerminalX wykrywa uruchomienie jako bundle PyInstaller lub archiwum `.pyz` i automatycznie dostosowuje ścieżki.

---

## Zmienne środowiskowe

| Zmienna | Opis |
|---|---|
| `TERMINALX_DATA` | Nadpisuje ścieżkę katalogu danych |
| `TERMINALX_RC` | Ścieżka do niestandardowego pliku RC (skrypt startowy) |
| `TERMINALX_CONFIG` | Ścieżka do niestandardowego pliku konfiguracyjnego (JSON/YAML/INI) |
| `TERMINALX_PROFILE` | Profil do aktywacji przy starcie |
| `TERMINALX_THEME` | Motyw do aktywacji przy starcie |
| `TERMINALX_OFFLINE` | Wymusza tryb offline (`1`) |
| `TERMINALX_OFFLINE_FORCE` | Alias dla `TERMINALX_OFFLINE` |
| `TERMINALX_NO_COLOR` | Wyłącza kolory ANSI (`1`) |
| `NO_COLOR` | Wyłącza kolory ANSI (respektuje [no-color.org](https://no-color.org)) |
| `TERMINALX_VERBOSE` | Włącza tryb szczegółowy (`1`) |
| `TERMINALX_DEBUG` | Włącza tryb debugowania (`1`) |
| `TERMINALX_LOG` | Ustaw na `0`, aby wyłączyć logowanie |

---

## Wbudowane komendy

TerminalX zawiera ponad 100 wbudowanych komend podzielonych na kategorie funkcjonalne.

### System plików

| Komenda | Aliasy | Opis |
|---|---|---|
| `ls` | | Listuje zawartość katalogu z kolorami i ikonami |
| `cd` | | Zmienia bieżący katalog |
| `pwd` | | Wypisuje bieżący katalog roboczy |
| `cat` | | Wyświetla zawartość pliku z podświetlaniem składni |
| `touch` | | Tworzy plik lub aktualizuje datę modyfikacji |
| `mkdir` | `md` | Tworzy katalog (z podkatalogami przy `-p`) |
| `rm` | `del` | Usuwa plik |
| `rmdir` | `rd` | Rekurencyjnie usuwa katalog |
| `cp` | `copy` | Kopiuje plik lub katalog (`-r`, `-v`, `-f`, `-n`) |
| `mv` | `move` | Przenosi lub zmienia nazwę pliku/katalogu |
| `rename` | | Zmienia nazwę pliku |
| `find` | | Wyszukuje pliki według wzorca |
| `grep` | | Szuka wzorców tekstowych w plikach |
| `diff` | | Porównuje dwa pliki linia po linii |
| `stat` | | Wyświetla metadane pliku |
| `du` | | Pokazuje zajętość dysku ścieżki |
| `tree` | | Wyświetla drzewo katalogów |
| `tail` | | Pokazuje ostatnie N linii pliku |
| `head` | | Pokazuje pierwsze N linii pliku |
| `chmod` | | Zmienia uprawnienia pliku |
| `chown` | | Zmienia właściciela pliku |
| `attrib` | | Wyświetla lub zmienia atrybuty pliku |
| `fman` | | Menedżer plików: kopiuj, przenoś, zmień nazwę, podgląd, info, drzewo, szukaj, rozmiar |

### Tekst i przetwarzanie danych

| Komenda | Opis |
|---|---|
| `echo` | Wypisuje tekst na wyjście |
| `json` | Parsuje, formatuje i koloryzuje JSON |
| `yaml` | Parsuje i formatuje YAML |
| `jq` | Zapytania do JSON w stylu jq |
| `base64` / `b64` | Koduje i dekoduje Base64 |
| `hexdump` | Wyświetla zawartość pliku jako hex |
| `hash` | Oblicza sumy kontrolne pliku/tekstu (MD5, SHA-1, SHA-256 itp.) |
| `encode` | Koduje/dekoduje tekst (Base64, URL, HTML, ROT13, hex) |
| `clip` | Kopiuje tekst do schowka |
| `diff` | Porównuje pliki |
| `diffview` | Interaktywny widok różnic side-by-side |
| `jsonview` | Interaktywne drzewo JSON |

### Shell i środowisko

| Komenda | Aliasy | Opis |
|---|---|---|
| `alias` | | Tworzy alias komendy |
| `unalias` | | Usuwa alias |
| `export` | | Ustawia zmienną środowiskową |
| `unset` | | Usuwa zmienną shella |
| `set` | | Listuje lub przełącza opcje shella |
| `env` | | Wyświetla zmienne środowiskowe |
| `printenv` | | Wypisuje konkretną zmienną środowiskową |
| `source` | | Wykonuje skrypt w bieżącej sesji |
| `which` | | Pokazuje ścieżkę komendy |
| `history` | | Przegląda i przeszukuje historię komend |
| `clear` | | Czyści ekran terminala |
| `for-loop` | | Prosta konstrukcja pętli |
| `date` | | Pokazuje lub formatuje bieżącą datę/czas |
| `call` | | Wykonuje zewnętrzny skrypt |

### Informacje o systemie

| Komenda | Opis |
|---|---|
| `whoami` | Pokazuje bieżącego użytkownika |
| `hostname` | Pokazuje nazwę hosta systemu |
| `uname` | Wyświetla informacje o systemie operacyjnym i jądrze |
| `uptime` / `uptime2` | Pokazuje czas działania systemu |
| `sysinfo` / `systeminfo` | Wyświetla informacje o systemie |
| `id` | Pokazuje ID użytkownika i grup |
| `ps` / `ps2` | Listuje uruchomione procesy |
| `free` | Pokazuje użycie pamięci |
| `df` | Pokazuje wolne miejsce na dysku |
| `cpugraph` | Wykres użycia CPU |
| `sysmon` | Monitor systemu w czasie rzeczywistym |
| `procmon` | Monitor procesów |
| `envdetect` | Wykrywa i wyświetla szczegóły bieżącego środowiska |
| `envs` | Listuje zmienne środowiskowe shella |

### Sieć

| Komenda | Opis |
|---|---|
| `ping` | Pinguje hosta |
| `traceroute` | Śledzi trasę sieciową do hosta |
| `netstat` | Pokazuje aktywne połączenia sieciowe |
| `wget` | Pobiera plik z URL |
| `curl` | Przesyła dane z URL |
| `http` | Proste narzędzie do zapytań HTTP |
| `ipconfig` | Pokazuje konfigurację interfejsów sieciowych |
| `netmon` | Monitor ruchu sieciowego |
| `portscan` | Skanuje porty TCP hosta |
| `dns` | Zapytanie DNS |
| `ssh` | Wrapper klienta SSH |
| `serve` | Uruchamia prosty serwer HTTP plików |
| `wss` | Narzędzie serwera WebSocket |

### Narzędzia deweloperskie

| Komenda | Opis |
|---|---|
| `pyrepl` | Wbudowany REPL Pythona |
| `pysh` | Ewaluator wyrażeń Pythona w shellu |
| `timeit` | Mierzy czas wykonania komendy lub wyrażenia Python |
| `debug` | Przełącza lub inspekcjonuje tryb debugowania |
| `verbose` | Przełącza tryb szczegółowy |
| `diag` | Uruchamia diagnostykę |
| `selfcheck` | Weryfikuje integralność shella |
| `build` | Buduje/pakuje shell |
| `finfo` | Informacje i analiza pliku |
| `integrate` | Narzędzia integracji shella |

### Pluginy i pakiety

| Komenda | Opis |
|---|---|
| `plugin` | Zarządza pluginami: instaluj, usuń, listuj, włącz, wyłącz, zaufaj |
| `pkg` | Menedżer pakietów: instaluj, usuń, listuj, aktualizuj (format `.minipkg`) |
| `newcmd` | Interaktywne tworzenie nowej wbudowanej komendy |
| `pip` | Wrapper pip ze integracją shellową |

### Sesje i multipleksowanie

| Komenda | Opis |
|---|---|
| `session` | Zapisuje, przywraca i zarządza sesjami shella |
| `split` | Dzieli terminal na panele |
| `tmux` | Zarządzanie panelami w stylu tmux |
| `sched` | Planuje komendy do cyklicznego wykonywania |
| `watch` | Obserwuje i powtarza komendę według timera |
| `macro` | Nagrywa, odtwarza i zarządza makrami komend |

### UI i wyświetlanie

| Komenda | Aliasy | Opis |
|---|---|---|
| `theme` | | Przełącza motywy kolorystyczne |
| `profile` | | Przełącza profile shella |
| `status` | | Pokazuje/ukrywa pasek statusu |
| `boxstyle` | | Zmienia styl ramek |
| `tui` | | Widżety interfejsu tekstowego |
| `nav` | | Interaktywny nawigator katalogów |
| `gui` | | Uruchamia okno GUI Tkinter |
| `shortcuts` | | Pokazuje skróty klawiszowe |
| `mode` | | Przełącza tryb online/offline |
| `clock` | | Wyświetla zegar na żywo |

### Narzędzia ogólne

| Komenda | Opis |
|---|---|
| `calc` | Kalkulator z ewaluacją wyrażeń |
| `timer` | Odliczanie czasu |
| `note` | Szybki menedżer notatek |
| `todo` | Menedżer listy zadań |
| `weather` | Pokazuje prognozę pogody dla lokalizacji |
| `wset` | Konfiguruje domyślną lokalizację pogody |
| `qr` | Generuje kody QR |
| `uuid` | Generuje UUID |
| `passgen` | Generator haseł |
| `about` | Pokazuje informacje o shellu |
| `version` | Pokazuje szczegóły wersji |
| `changelog` | Pokazuje historię wersji |
| `logs` | Przegląda i zarządza logami shella |
| `logview` | Przeglądarka logów z filtrowaniem |
| `logtail` | Śledzi plik logów shella |
| `logscan` | Skanuje logi według wzorców |
| `logrotate` | Rotuje pliki logów |
| `crashlog` | Przegląda i zarządza raportami błędów |
| `wizard` | Kreator pierwszego uruchomienia |
| `recovery` | Wchodzi lub wychodzi z trybu awaryjnego |
| `help` | Wyświetla pomoc dla komend |

### Komendy specyficzne dla Windows

| Komenda | Opis |
|---|---|
| `tasklist` | Listuje procesy Windows |
| `taskkill` | Kończy proces Windows |
| `sc` | Windows Service Control |
| `shutdown` | Wyłącza lub restartuje Windows |
| `powercfg` | Konfiguracja zasilania |
| `compact` | Kompresja NTFS |
| `net` | Komendy sieciowe Windows |
| `netsh` | Network Shell |
| `arp` | Tablica ARP |
| `pathping` | Narzędzie PathPing |
| `sfc` | System File Checker |
| `dism` | Narzędzie DISM |
| `chkdsk` | Sprawdzanie dysku |
| `bcdedit` | Edytor konfiguracji rozruchu |
| `gpupdate` | Aktualizacja zasad grupy |
| `reg` | Edytor rejestru |
| `diskpart` | Partycjonowanie dysków |
| `format` | Formatowanie woluminu |
| `cipher` | Narzędzie szyfrowania EFS |
| `schtasks` | Harmonogram zadań |
| `fsutil` | Narzędzie systemu plików |
| `setx` | Ustawia trwałe zmienne środowiskowe |
| `start` | Uruchamia program lub komendę |
| `eventvwr` | Podgląd zdarzeń |
| `perfmon` | Monitor wydajności |
| `resmon` | Monitor zasobów |
| `dxdiag` | Diagnostyka DirectX |
| `wmic` | Windows Management Instrumentation |

---

## System pluginów

TerminalX obsługuje ładowanie zewnętrznych pluginów Python z katalogu `.terminalx_plugins/`.

```bash
# Listuj załadowane pluginy
plugin list

# Zainstaluj plugin z pliku
plugin install /ścieżka/do/mójplugin.py

# Zainstaluj plugin z URL (tryb online)
plugin install --url https://example.com/mójplugin.py

# Włącz lub wyłącz plugin
plugin enable mójplugin
plugin disable mójplugin

# Zaufaj pluginowi (wymagane przed uruchomieniem)
plugin trust mójplugin

# Usuń plugin
plugin remove mójplugin
```

Pluginy są objęte systemem zaufania — każdy plugin musi zostać jawnie zatwierdzony przed uruchomieniem. Dane zaufania są przechowywane w `.terminalx_plugin_trust.json`.

### Pisanie pluginu

Plugin to standardowy plik Python rejestrujący komendy przez dekorator `@command`:

```python
# TERMINALX_PLUGIN
# "version": "1.0"
# "description": "Mój przykładowy plugin"
# "author": "Twoje Imię"

@command("hello", "Przywitaj się")
def cmd_hello(args):
    print("Witaj z pluginu!")
```

---

## Menedżer pakietów

TerminalX zawiera wbudowany menedżer pakietów dla plików `.minipkg`.

```bash
# Listuj dostępne pakiety
pkg list

# Zainstaluj pakiet
pkg install mojpakiet

# Zainstaluj z URL (tryb online)
pkg install --url https://example.com/mojpakiet.minipkg

# Usuń pakiet
pkg remove mojpakiet

# Aktualizuj wszystkie pakiety
pkg update
```

Pakiety są przechowywane w `.terminalx_packages/`.

---

## Konfiguracja

Plik konfiguracyjny znajduje się w `~/.terminalx.json` (lub `.terminalx_data/.terminalx.json` w trybie przenośnym). Obsługuje formaty **JSON**, **YAML** i **INI**.

```bash
# Wyświetl bieżącą konfigurację
config show

# Ustaw wartość konfiguracyjną
config set theme dark
config set log_commands true
config set log_max_mb 10

# Przywróć wartości domyślne
config reset
```

### Kluczowe opcje konfiguracji

| Klucz | Domyślnie | Opis |
|---|---|---|
| `theme` | `dark` | Aktywny motyw kolorystyczny |
| `profile` | `default` | Aktywny profil |
| `log_commands` | `true` | Logowanie wykonywanych komend |
| `log_max_mb` | `5` | Maksymalny rozmiar pliku logu (MB) |
| `status_bar` | `true` | Pokazuj pasek statusu |
| `box_style` | `rounded` | Styl ramek |

### Plik RC (skrypt startowy)

Komendy zawarte w `~/.terminalxrc` (lub `.terminalx_data/.terminalxrc`) są wykonywane automatycznie przy starcie — podobnie jak `.bashrc`.

---

## Motywy i profile

### Motywy

```bash
# Listuj dostępne motywy
theme list

# Przełącz motyw
theme dark
theme light
theme monokai
```

### Profile

Profile pozwalają zapisywać i przełączać między kompletnymi konfiguracjami shella.

```bash
# Listuj profile
profile list

# Utwórz profil
profile save mojprofil

# Wczytaj profil
profile load mojprofil

# Usuń profil
profile delete mojprofil
```

---

## Zaawansowane funkcje

### Składnia bash-like

TerminalX obsługuje standardową składnię shella:

```bash
# Potoki
ls | grep .py

# Przekierowania
cat plik.txt > wyjście.txt
cat plik.txt >> log.txt

# Operatory logiczne
mkdir nowykatalog && cd nowykatalog
cd nieistniejący || echo "Katalog nie istnieje"

# Łączenie komend
clear; ls; date

# Podstawianie podshella
echo "Dziś jest $(date)"

# Zmienne
export IMIE=Świat
echo "Witaj $IMIE"
echo "${IMIE:-domyślny}"

# Pętle
for-loop i 1 5; echo "Element $i"; done
```

### Makra

```bash
# Rozpocznij nagrywanie
macro record mojomakro

# ... wykonaj komendy ...

# Zatrzymaj nagrywanie
macro stop

# Odtwórz
macro play mojomakro

# Listuj makra
macro list
```

### Harmonogram

```bash
# Uruchamiaj komendę co 60 sekund
sched add "date" 60

# Listuj zaplanowane zadania
sched list

# Usuń zadanie
sched remove 1
```

### Sesje

```bash
# Zapisz bieżącą sesję
session save mojasesja

# Przywróć sesję
session load mojasesja

# Listuj sesje
session list
```

### Panele podzielonego ekranu

```bash
# Podziel poziomo
split h

# Podziel pionowo
split v

# Przełącz między panelami
split next
```

### Python REPL

```bash
# Uruchom wbudowany REPL Pythona
pyrepl

# Ewaluuj wyrażenie Python inline
pysh 2 + 2
pysh import os; os.getcwd()
```

### Tryb awaryjny

Jeśli shell napotka krytyczny błąd, automatycznie przechodzi w tryb awaryjny. Możesz go też wymusić ręcznie:

```bash
python TerminalX.py --safe
```

W trybie awaryjnym:
```bash
recovery diagnose    # Uruchom diagnostykę
recovery exit        # Wyjdź z trybu awaryjnego i wróć do normalnej pracy
```

---

## Rozwiązywanie problemów

### Shell nie uruchamia się

- Sprawdź wersję Pythona (wymagana 3.10+): `python --version`
- Jeśli kolory wyświetlają śmieciowe znaki, ustaw `NO_COLOR=1` lub `TERMINALX_NO_COLOR=1`
- Spróbuj trybu awaryjnego: `python TerminalX.py --safe`

### Raporty błędów

```bash
# Wyświetl ostatni raport błędu
crashlog

# Wyświetl wszystkie raporty
crashlog list

# Wyczyść raporty
crashlog clear
```

Raporty błędów są zapisywane do `.terminalx_crashlog.txt`.

### Logi

```bash
# Śledź logi na żywo
logtail

# Przeglądaj logi z filtrowaniem
logview

# Wyłącz logowanie
export TERMINALX_LOG=0
```

### Edytor nano-lite nie działa na Windows

Zainstaluj opcjonalną bibliotekę curses:
```
pip install windows-curses
```

---

## Historia zmian

Pełną historię zobaczysz za pomocą:
```bash
changelog
```

Wybrane kamienie milowe:

| Wersja | Najważniejsze zmiany |
|---|---|
| 35.2 | Menedżer plików (`fman`), konfiguracja pogody (`wset`) |
| 34.0 | Bieżące stabilne wydanie |
| 16.0 | Tryb online/offline, system crashlogów |
| 15.0 | Pełny parser bash-like: potoki, przekierowania, podshell, operatory logiczne |
| 9.0 | Edytor nano-lite, menedżer pakietów mini-pkg |

---

## Licencja

TerminalX jest wydany na licencji **MIT**.  
© 2024–2025 Sebastian Januchowski (polsoft.ITS™)

Pełny tekst licencji: [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)

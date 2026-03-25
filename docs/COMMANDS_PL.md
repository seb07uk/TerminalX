# TerminalX — Spis Komend (PL)

> Wersja 35.2 · ponad 130 wbudowanych komend

---

## System plików

| Komenda | Aliasy | Opis |
|---|---|---|
| `ls` | | Listuje zawartość katalogu z kolorami i ikonami |
| `cd` | | Zmienia bieżący katalog |
| `pwd` | | Wypisuje bieżący katalog roboczy |
| `cat` | | Wyświetla zawartość pliku z podświetlaniem składni |
| `touch` | | Tworzy plik lub aktualizuje datę modyfikacji |
| `mkdir` | `md` | Tworzy katalog, w tym podkatalogi (`-p`) |
| `rm` | `del` | Usuwa plik |
| `rmdir` | `rd` | Rekurencyjnie usuwa katalog |
| `cp` | `copy` | Kopiuje plik lub katalog (`-r`, `-v`, `-f`, `-n`) |
| `mv` | `move` | Przenosi lub zmienia nazwę pliku/katalogu |
| `rename` | `ren` | Zmienia nazwę pliku lub katalogu |
| `find` | | Przeszukuje drzewo katalogów według wzorca |
| `grep` | | Przeszukuje pliki według wzorca (regex) |
| `diff` | | Porównuje dwa pliki (unified diff) |
| `stat` | | Wyświetla szczegółowe metadane pliku/katalogu |
| `du` | `diskusage` | Rozmiar katalogu i plików |
| `tree` | | Wyświetla drzewo katalogów |
| `tail` | | Wyświetla koniec pliku (obsługuje śledzenie na żywo `-f`) |
| `head` | | Wyświetla początek pliku |
| `chmod` | | Zmienia uprawnienia pliku (Linux/macOS) |
| `chown` | | Zmienia właściciela pliku (Linux/macOS) |
| `attrib` | | Wyświetla lub zmienia atrybuty pliku (Windows / Linux stat) |
| `fman` | | Menedżer plików: kopiuj, przenoś, zmień nazwę, podgląd, info, drzewo, szukaj, rozmiar |

## Tekst i przetwarzanie danych

| Komenda | Aliasy | Opis |
|---|---|---|
| `echo` | | Wypisuje tekst na wyjście |
| `json` | | Parser, formatter i walidator JSON |
| `yaml` | | Parser i formatter YAML (stdlib, bez pyyaml) |
| `jq` | | Zapytania do JSON w stylu jq (stdlib, bez binarki) |
| `base64` | | Kodowanie i dekodowanie Base64 |
| `b64` | | Alias dla base64 — kodowanie i dekodowanie |
| `hexdump` | | Podgląd binarny pliku (hex + ASCII) |
| `diff` | | Porównanie dwóch plików z kolorowaniem |
| `diffview` | | Porównanie plików side-by-side z kolorowaniem |
| `jsonview` | | Interaktywna przeglądarka i filtrowanie JSON |
| `hash` | | Sumy kontrolne MD5, SHA-1, SHA-256, SHA-512 |
| `encode` | | Kodowanie/dekodowanie tekstu: Unicode, ANSI, UTF-8, cp1250 |
| `clip` | | Kopiuje stdin lub plik do schowka systemowego |

## Shell i środowisko

| Komenda | Aliasy | Opis |
|---|---|---|
| `alias` | | Tworzy alias komendy |
| `unalias` | | Usuwa alias |
| `export` | | Ustawia i eksportuje zmienną środowiskową do procesów potomnych |
| `unset` | | Usuwa zmienną shella lub środowiskową |
| `set` | | Wyświetla lub ustawia zmienne i opcje shella |
| `env` | | Wyświetla środowisko lub uruchamia komendę ze zmienionym środowiskiem |
| `printenv` | | Wypisuje wartość zmiennej środowiskowej |
| `envs` | | Listuje zmienne środowiskowe z filtrowaniem i sortowaniem |
| `source` | | Wczytuje i wykonuje skrypt TerminalX (`.msh` / `.rc`) |
| `call` | | Wywołuje plik wsadowy lub skrypt shella |
| `which` | `where` | Znajduje ścieżkę programu w PATH |
| `history` | | Wyświetla i przeszukuje historię komend |
| `clear` | `cls` | Czyści ekran terminala |
| `for-loop` | | Pętla FOR (odpowiednik FOR w CMD) |
| `date` | `time` | Wyświetla lub ustawia datę i czas systemowy |
| `deactivate` | | Dezaktywuje wirtualne środowisko Python (venv) |
| `setx` | | Trwale ustawia zmienną środowiskową (Windows setx / export Linux) |

## Informacje o systemie

| Komenda | Aliasy | Opis |
|---|---|---|
| `whoami` | | Wyświetla bieżącego użytkownika |
| `hostname` | | Wyświetla lub zmienia nazwę hosta |
| `uname` | | Informacje o systemie operacyjnym i jądrze |
| `uptime` | | Czas pracy systemu i średnie obciążenie |
| `uptime2` | | Czas działania + load average + czas lokalny |
| `sysinfo` | | Pełna diagnostyka: OS, CPU, RAM, dysk, sieć, Python |
| `systeminfo` | | Szczegółowe informacje o systemie operacyjnym |
| `id` | | Wyświetla ID użytkownika i grupy (Linux/macOS) |
| `ps` | | Lista procesów systemowych |
| `ps2` | | Lista procesów z filtrowaniem po nazwie / PID / użytkowniku |
| `free` | | Informacje o pamięci RAM (cross-platform) |
| `df` | | Informacje o dyskach i przestrzeni (cross-platform) |
| `du` | `diskusage` | Rozmiar katalogu i plików |
| `cpugraph` | | Live wykres CPU i RAM w terminalu (odświeżanie co 1s) |
| `sysmon` | | Monitor zasobów systemowych w czasie rzeczywistym |
| `procmon` | | Monitor procesów — mini Task Manager TUI |
| `envdetect` | | Automatyczne wykrywanie środowiska i sugestia profilu |

## Sieć

| Komenda | Aliasy | Opis |
|---|---|---|
| `ping` | | Testuje połączenie (systemowe lub TCP fallback) |
| `traceroute` | `tracert`, `trace` | Trasa pakietów do hosta |
| `netstat` | | Statystyki sieci i aktywne połączenia |
| `wget` | | Pobiera plik z URL (stdlib urllib) |
| `curl` | | Przesyła dane HTTP/HTTPS (stdlib urllib) |
| `http` | | Klient HTTP (curl-like): GET / POST / HEAD / PUT / DELETE |
| `ipconfig` | | Konfiguracja interfejsów sieciowych (Windows / ip addr Linux) |
| `netmon` | | Monitor połączeń sieciowych i interfejsów |
| `portscan` | | Wielowątkowy skaner portów TCP |
| `dns` | | Zapytania DNS: A, AAAA, PTR, MX, NS, ALL |
| `arp` | | Tablica ARP — adresy MAC/IP w sieci lokalnej |
| `pathping` | | Łączony ping + traceroute (Windows pathping / mtr Linux) |
| `ssh` | | Połączenie z hostem przez SSH lub zarządzanie profilami |
| `serve` | | Lokalny serwer REST API / HTTP plików |
| `wss` | | Lokalny serwer WebSocket (RFC 6455) |

## Narzędzia deweloperskie

| Komenda | Aliasy | Opis |
|---|---|---|
| `pyrepl` | | Wbudowany interaktywny REPL Pythona |
| `pysh` | | Zarządzanie modułami `.pysh` (dynamiczne rozszerzenia shella) |
| `timeit` | | Pomiar czasu wykonania komendy shella |
| `debug` | | Włącza/wyłącza tryb debug (pełny trace wykonania) |
| `verbose` | | Włącza/wyłącza tryb verbose (echo komend przed wykonaniem) |
| `diag` | | Diagnostyka systemu: CPU, RAM, dyski, sieć, procesy |
| `finfo` | | Pełne metadane pliku: typ, MIME, kodowanie, hash, statystyki |
| `selfcheck` | | Weryfikuje integralność i spójność wewnętrzną shella |
| `integrate` | | Narzędzia integracji shella (PATH, pliki rc, pulpit) |
| `build` | | Buduje standalone EXE z PyInstaller |
| `builder` | | Tryb Builder — generowanie i zarządzanie modułami shella |
| `project` | | Tworzenie i zarządzanie projektami terminala (polsoft.ITS™) |
| `ai` | | Integracja z AI — pytania, podpowiedzi, wyjaśnienia komend |

## Pluginy i pakiety

| Komenda | Aliasy | Opis |
|---|---|---|
| `plugin` | | Zarządza pluginami: instaluj, usuń, listuj, włącz, wyłącz, zaufaj |
| `pkg` | | Menedżer pakietów: instaluj, usuń, listuj, aktualizuj (`.minipkg`) |
| `pip` | | Wrapper systemowego pip / mini-pip shella |
| `newcmd` | | Kreator: utwórz nową komendę bez edycji kodu shella |

## Sesje i multipleksowanie

| Komenda | Aliasy | Opis |
|---|---|---|
| `session` | | Zapisuje, przywraca i zarządza sesjami shella (styl tmux) |
| `split` | | Pseudo split-screen — podział terminala na panele |
| `tmux` | | Skróty styl tmux do zarządzania sesjami i podziałem |
| `sched` | | Wbudowany harmonogram zadań (cross-platform) |
| `watch` | | Automatyczne zadania wyzwalane zdarzeniami systemowymi |
| `macro` | | Nagrywanie, odtwarzanie i zarządzanie makrami komend |

## UI i wyświetlanie

| Komenda | Aliasy | Opis |
|---|---|---|
| `theme` | | Przełącza, tworzy i zarządza motywami kolorystycznymi |
| `profile` | | Zarządza profilami konfiguracji TerminalX |
| `status` | | Przełącza lub pokazuje pasek statusu |
| `boxstyle` | | Zmienia styl ramek UI (single/round/double/heavy/ascii) |
| `tui` | | Interaktywne menu TUI (interfejs tekstowy) |
| `nav` | | Interaktywna przeglądarka plików TUI |
| `gui` | | Backend GUI przez gniazdo IPC (NDJSON) |
| `shortcuts` | | Wyświetla wszystkie skróty klawiszowe |
| `mode` | | Przełącza tryb online/offline |
| `clock` | | Live zegar cyfrowy w terminalu |

## Narzędzia ogólne

| Komenda | Aliasy | Opis |
|---|---|---|
| `calc` | | Kalkulator wyrażeń matematycznych |
| `timer` | | Stoper, odliczanie i alarm czasowy |
| `note` | | Notatki — dodawaj, przeglądaj, szukaj, usuwaj |
| `todo` | | Lista zadań TODO z priorytetami i statusem |
| `weather` | | Prognoza pogody ASCII w terminalu przez wttr.in |
| `wset` | `weather-set` | Ustawia domyślną lokalizację dla komendy weather |
| `qr` | | Generuje kod QR w terminalu (bloki Unicode lub ASCII art) |
| `uuid` | | Generator UUID v1/v4/v5 i krótkich ID |
| `passgen` | | Generator silnych haseł, fraz passphrase i PIN-ów |
| `archive` | | Tworzenie i rozpakowywanie archiwów |
| `about` | | Informacje o autorze, wersji i licencji |
| `version` | | Wyświetla wersję TerminalX |
| `changelog` | `changes`, `history-log` | Historia zmian TerminalX |
| `help` | `?` | Wyświetla pomoc dla komend |

## Logi i diagnostyka

| Komenda | Aliasy | Opis |
|---|---|---|
| `logs` | | Zaawansowany podgląd i eksport logów shella |
| `logview` | | Wyświetla lokalny log shella z filtrowaniem |
| `logtail` | | Podgląd logów w czasie rzeczywistym |
| `logscan` | | Skanuje plik logu w poszukiwaniu błędów/wzorców |
| `logrotate` | `rotatelog` | Rotuje plik logu shella |
| `crashlog` | | Wyświetla i zarządza raportami błędów |
| `recovery` | | Wchodzi lub wychodzi z trybu awaryjnego |
| `wizard` | | Interaktywny kreator konfiguracji |
| `portable` | | Zarządza trybem przenośnym TerminalX |

## Dostęp i bezpieczeństwo

| Komenda | Aliasy | Opis |
|---|---|---|
| `sudo` | | Uruchamia komendę jako root lub przełącza w tryb root |
| `elevate` | | Podnosi uprawnienia do administratora (UAC/sudo) |
| `cipher` | | Szyfrowanie EFS (Windows) / bezpieczne czyszczenie wolnego miejsca |

## Komendy specyficzne dla Windows

| Komenda | Opis |
|---|---|
| `tasklist` | Lista procesów systemowych (Windows tasklist / ps) |
| `taskkill` | Kończy proces po PID lub nazwie |
| `pkill2` | Zabija proces po nazwie lub PID (z potwierdzeniem) |
| `sc` | Zarządzanie usługami systemowymi (Windows sc / systemctl) |
| `shutdown` | Wyłącza, restartuje lub wylogowuje system |
| `powercfg` | Konfiguracja zasilania i raporty (Windows) |
| `compact` | Kompresja NTFS (Windows) lub info o kompresji (Linux) |
| `net` | Komendy NET systemu Windows (użytkownicy, grupy, usługi, udziały) |
| `netsh` | Konfiguracja sieci Windows (netsh) lub ip/nmcli (Linux) |
| `sfc` | Skan plików systemowych (Windows sfc / debsums Linux) |
| `dism` | DISM — serwisowanie obrazu Windows |
| `chkdsk` | Sprawdza dysk pod kątem błędów (Windows chkdsk / fsck Linux) |
| `bcdedit` | Konfiguracja bootloadera Windows BCD |
| `gpupdate` | Aktualizacja zasad grupy (Windows) |
| `reg` | Edytor rejestru Windows |
| `diskpart` | Zarządzanie dyskami i partycjami |
| `format` | Formatowanie dysku / partycji |
| `schtasks` | Harmonogram zadań Windows (schtasks / cron Linux) |
| `fsutil` | Narzędzia systemu plików (Windows fsutil / stat Linux) |
| `start` | Uruchamia program lub plik w nowym oknie/procesie |
| `eventvwr` | Podgląd zdarzeń systemowych (Windows / journalctl Linux) |
| `perfmon` | Monitor wydajności (Windows perfmon / vmstat-top Linux) |
| `resmon` | Monitor zasobów (Windows resmon / htop Linux) |
| `dxdiag` | Diagnostyka DirectX (Windows) / info OpenGL/GPU (Linux) |
| `wmic` | Interfejs WMI (Windows Management Instrumentation) |

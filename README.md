```markdown
# Port Scanner

A simple but powerful port scanner with a graphical user interface. Built by Bira Engida (15 years old).

## Features

- Scan common ports (21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 5900, 6379, 8080, 8443)
- Service detection (identifies what service runs on each port)
- Adjustable timeout settings
- Show/hide closed ports
- Multi-threaded scanning (doesn't freeze the GUI)
- Progress bar
- Save results to a text file
- Clear output button
- Stop scan button

## Requirements

- Python 3.x
- No external packages needed (uses only standard library)

## Installation

1. Save the script as `port_scanner.py`

2. Run the script:
```bash
python port_scanner.py
```

How to Use

1. Enter an IP address or hostname (example: scanme.nmap.org)
2. Adjust the timeout if needed (default is 1 second)
3. Check "Show closed ports" if you want to see closed ports too
4. Click "Start Scan"
5. Wait for the scan to complete
6. Save results if needed

Safe Targets for Testing

These targets allow port scanning legally:

· scanme.nmap.org - Official Nmap testing target
· localhost or 127.0.0.1 - Your own computer
· testphp.vulnweb.com - Legal testing website

Legal Disclaimer

Only scan devices you own or have permission to test. Scanning unknown systems without permission is illegal in most countries. This tool is for educational purposes only.

Example Output

```
[*] Target: scanme.nmap.org (45.33.32.156)
[*] Started at: 2026-05-08 14:30:25
[*] Scanning 19 common ports...

[+] Port 22 OPEN - SSH
[+] Port 80 OPEN - HTTP
[-] Port 21 CLOSED - FTP
[+] Port 443 OPEN - HTTPS

[*] Found 3 open ports
    - Port 22: SSH
    - Port 80: HTTP
    - Port 443: HTTPS
```

Special Thanks

A huge thank you to my brother for helping me build this project!

Check him out on GitHub: (greattitandev)[https://github.com/greattitandev]

Created By

**Bira Engida (15 years old)**

```
2. Run the script:
```bash
python port_scanner.py

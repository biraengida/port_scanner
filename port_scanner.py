#!/usr/bin/env python3

import socket
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 5900, 6379, 8080, 8443]
SERVICES = {80: "HTTP", 443: "HTTPS", 22: "SSH", 21: "FTP", 3306: "MySQL", 3389: "RDP", 25: "SMTP", 53: "DNS", 23: "Telnet", 110: "POP3", 143: "IMAP", 445: "SMB", 5900: "VNC", 5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt"}

scanning = False
open_ports = []
output_text = None
progress_bar = None
status_label = None
save_button = None
target_entry = None
timeout_var = None
verbose_var = None

def log(message, tag=None):
    global output_text
    output_text.insert(tk.END, message + "\n", tag)
    output_text.see(tk.END)

def clear_output():
    global output_text, open_ports, save_button
    output_text.delete(1.0, tk.END)
    open_ports = []
    save_button.config(state="disabled")

def scan_port(host, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_worker(host, port, timeout, verbose):
    global scanning, open_ports, progress_bar, status_label
    if not scanning:
        return

    if scan_port(host, port, timeout):
        service = SERVICES.get(port, "Unknown")
        log(f"[+] Port {port} OPEN - {service}", "open")
        open_ports.append(port)
    elif verbose:
        service = SERVICES.get(port, "Unknown")
        log(f"[-] Port {port} CLOSED - {service}", "closed")

def run_scan():
    global scanning, open_ports, progress_bar, status_label, save_button, target_entry, timeout_var, verbose_var

    target = target_entry.get().strip()
    if not target:
        messagebox.showerror("Error", "Please enter a target")
        return

    scanning = True
    open_ports = []

    try:
        ip = socket.gethostbyname(target)
        log(f"\n[*] Target: {target} ({ip})")
        log(f"[*] Started at: {datetime.now()}")
        log(f"[*] Scanning {len(COMMON_PORTS)} common ports...\n")
        log("="*50)
    except:
        log(f"[!] Could not resolve hostname: {target}", "error")
        scanning = False
        return

    timeout = timeout_var.get()
    verbose = verbose_var.get()

    progress_bar["maximum"] = len(COMMON_PORTS)
    progress_bar["value"] = 0

    total = len(COMMON_PORTS)
    for idx, port in enumerate(COMMON_PORTS):
        if not scanning:
            log("\n[!] Scan stopped by user")
            break

        scan_worker(ip, port, timeout, verbose)
        progress_bar["value"] = idx + 1
        status_label.config(text=f"Scanning port {port} ({idx+1}/{total})")
        root.update_idletasks()

    if scanning:
        log("\n" + "="*50)
        log(f"[*] Scan completed at: {datetime.now()}")
        log(f"[*] Found {len(open_ports)} open ports")

        if open_ports:
            log("\n[*] Open ports summary:")
            for port in sorted(open_ports):
                service = SERVICES.get(port, "Unknown")
                log(f"    - Port {port}: {service}")
        else:
            log("\n[*] No open ports found")

        save_button.config(state="normal")

    status_label.config(text="Ready")
    scanning = False

def start_scan():
    global scan_button, stop_button
    scan_button.config(state="disabled")
    stop_button.config(state="normal")
    thread = threading.Thread(target=run_scan)
    thread.daemon = True
    thread.start()

def stop_scan():
    global scanning, scan_button, stop_button
    scanning = False
    scan_button.config(state="normal")
    stop_button.config(state="disabled")
    status_label.config(text="Stopping...")

def save_results():
    global open_ports, target_entry

    if not open_ports:
        messagebox.showinfo("Info", "No open ports to save")
        return

    target = target_entry.get().strip()
    filename = f"scan_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    try:
        with open(filename, 'w') as f:
            f.write(f"Port Scan Results for {target}\n")
            f.write(f"Scan completed at: {datetime.now()}\n")
            f.write("="*50 + "\n\n")
            f.write(f"Total open ports: {len(open_ports)}\n\n")
            for port in sorted(open_ports):
                service = SERVICES.get(port, "Unknown")
                f.write(f"Port {port:5d} : {service}\n")
        messagebox.showinfo("Success", f"Results saved to {filename}")
    except:
        messagebox.showerror("Error", "Failed to save results")

root = tk.Tk()
root.title("Port Scanner - Bira Engida (15yo)")
root.geometry("700x600")
root.resizable(True, True)

input_frame = ttk.LabelFrame(root, text="Target", padding=10)
input_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(input_frame, text="IP or Hostname:").pack(side="left", padx=5)
target_entry = ttk.Entry(input_frame, width=30)
target_entry.pack(side="left", padx=5)
target_entry.insert(0, "scanme.nmap.org")

options_frame = ttk.LabelFrame(root, text="Options", padding=10)
options_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(options_frame, text="Timeout (seconds):").pack(side="left", padx=5)
timeout_var = tk.DoubleVar(value=1.0)
timeout_spin = ttk.Spinbox(options_frame, from_=0.5, to=5.0, increment=0.5, textvariable=timeout_var, width=10)
timeout_spin.pack(side="left", padx=5)

verbose_var = tk.BooleanVar()
verbose_check = ttk.Checkbutton(options_frame, text="Show closed ports", variable=verbose_var)
verbose_check.pack(side="left", padx=20)

button_frame = ttk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=5)

scan_button = ttk.Button(button_frame, text="Start Scan", command=start_scan)
scan_button.pack(side="left", padx=5)

stop_button = ttk.Button(button_frame, text="Stop", command=stop_scan, state="disabled")
stop_button.pack(side="left", padx=5)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_output)
clear_button.pack(side="left", padx=5)

save_button = ttk.Button(button_frame, text="Save Results", command=save_results, state="disabled")
save_button.pack(side="left", padx=5)

status_frame = ttk.Frame(root)
status_frame.pack(fill="x", padx=10, pady=5)

progress_bar = ttk.Progressbar(status_frame, mode="determinate")
progress_bar.pack(fill="x", padx=5, pady=5)

status_label = ttk.Label(status_frame, text="Ready")
status_label.pack(pady=5)

output_frame = ttk.LabelFrame(root, text="Scan Results", padding=10)
output_frame.pack(fill="both", expand=True, padx=10, pady=5)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=25)
output_text.pack(fill="both", expand=True)

dev_label = ttk.Label(root, text="Developed by Bira Engida (15 years old)", font=("Arial", 9))
dev_label.pack(pady=5)

output_text.tag_config("open", foreground="green")
output_text.tag_config("closed", foreground="red")
output_text.tag_config("error", foreground="orange")

root.mainloop()

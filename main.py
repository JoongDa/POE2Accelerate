import socket
import subprocess
import platform
import shutil
import os

DOMAIN = "patch-poe2.poecdn.com"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts" if platform.system().lower() == "windows" else "/etc/hosts"
BACKUP_PATH = HOSTS_PATH + ".bak"

def resolve_domain(domain):
    try:
        ips = socket.gethostbyname_ex(domain)[2]
        print(f"Resolving {domain} ...")
        print(f"Found {len(ips)} IP(s): {ips}")
        return ips
    except Exception as e:
        print("Failed to resolve:", e)
        return []

def ping(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        output = subprocess.check_output(["ping", param, "1", ip], stderr=subprocess.STDOUT, universal_newlines=True)
        if "time=" in output:
            time_str = output.split("time=")[1].split("ms")[0].strip()
            return float(time_str)
    except Exception:
        return None
    return None

def select_fastest_ip(ips):
    results = []
    for ip in ips:
        latency = ping(ip)
        print(f"{ip} ping latency: {latency} ms")
        if latency is not None:
            results.append((ip, latency))
    if not results:
        return ips[0]  # fallback
    results.sort(key=lambda x: x[1])
    return results[0][0]

def append_to_hosts(ip, domain):
    try:
        # Backup
        shutil.copy(HOSTS_PATH, BACKUP_PATH)
        print(f"Backup of hosts created at {BACKUP_PATH}")

        with open(HOSTS_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Check if the IP-domain mapping already exists
        entry = f"{ip} {domain}\n"
        if entry in lines:
            print(f"Entry already exists in hosts: {entry.strip()}")
            return

        # Append new line
        with open(HOSTS_PATH, "a", encoding="utf-8") as f:
            f.write(entry)

        print(f"Appended to hosts: {domain} -> {ip}")
    except PermissionError:
        print("Permission denied! Run this script as administrator/root.")
    except Exception as e:
        print("Failed to update hosts:", e)

if __name__ == "__main__":
    ips = resolve_domain(DOMAIN)
    if not ips:
        print("No IP addresses found. Exiting.")
    else:
        fastest_ip = select_fastest_ip(ips)
        print(f"Selected fastest IP: {fastest_ip}")
        append_to_hosts(fastest_ip, DOMAIN)
input("Press Enter to exit...")

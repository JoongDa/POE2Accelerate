import socket
import subprocess
import platform
import shutil
import os
import re

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

def ping(ip, count=3):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        output = subprocess.check_output(
            ["ping", param, str(count), ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        times = []
        for line in output.splitlines():
            match = re.search(r"(\d+\.?\d*)\s*ms", line)
            if match:
                times.append(float(match.group(1)))
        if times:
            return sum(times) / len(times)
    except Exception:
        return None
    return None

def select_fastest_ip(ips):
    results = []
    for ip in ips:
        latency = ping(ip)
        if latency is not None:
            print(f"{ip} average ping latency: {latency:.2f} ms")
            results.append((ip, latency))
        else:
            print(f"{ip} unreachable")
    if not results:
        print("No reachable IPs, fallback to first one.")
        return ips[0]
    results.sort(key=lambda x: x[1])
    return results[0][0]

def append_to_hosts(ip, domain):
    try:
        shutil.copy(HOSTS_PATH, BACKUP_PATH)
        print(f"Backup of hosts created at {BACKUP_PATH}")

        with open(HOSTS_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Remove old entries of the same domain
        lines = [line for line in lines if domain not in line]

        entry = f"{ip} {domain}\n"
        lines.append(entry)

        with open(HOSTS_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"Updated hosts: {domain} -> {ip}")
    except PermissionError:
        print("Permission denied! Run this script as administrator/root.")
    except Exception as e:
        print("Failed to update hosts:", e)

def flush_dns():
    system = platform.system().lower()
    try:
        if "windows" in system:
            subprocess.run("ipconfig /flushdns", shell=True, check=True)
            print("Flushed DNS cache on Windows.")
        elif "linux" in system:
            # systemd-based
            if shutil.which("systemd-resolve"):
                subprocess.run(["systemd-resolve", "--flush-caches"], check=True)
                print("Flushed DNS cache via systemd-resolve.")
            # legacy nscd
            elif shutil.which("nscd"):
                subprocess.run(["sudo", "service", "nscd", "restart"], check=True)
                print("Restarted nscd to flush DNS cache.")
        elif "darwin" in system:  # macOS
            subprocess.run(["dscacheutil", "-flushcache"])
            subprocess.run(["killall", "-HUP", "mDNSResponder"])
            print("Flushed DNS cache on macOS.")
        else:
            print("DNS flush not supported on this OS.")
    except Exception as e:
        print("Failed to flush DNS:", e)

if __name__ == "__main__":
    ips = resolve_domain(DOMAIN)
    if not ips:
        print("No IP addresses found. Exiting.")
    else:
        fastest_ip = select_fastest_ip(ips)
        print(f"Selected fastest IP: {fastest_ip}")
        append_to_hosts(fastest_ip, DOMAIN)
        flush_dns()
    input("Press Enter to exit...")

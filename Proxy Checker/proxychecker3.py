#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request  # Updated for Python 3
import threading  # Threading lib
import socket  # Socket lib
import sys  # System lib
import time  # Time lib
import os  # OS lib

# Disable .pyc file creation
sys.dont_write_bytecode = True

# Colors (simplified for Python 3; placeholders for future enhancements)
red = "[ERROR]"
green = "[SUCCESS]"
yellow = "[WARNING]"
blue = "[INFO]"
defcol = "[DEFAULT]"

def error(msg):
    print(f"{red} - {defcol} {msg}")

def alert(msg):
    print(f"{blue} - {defcol} {msg}")

def action(msg):
    print(f"{green} - {defcol} {msg}")

def errorExit(msg):
    sys.exit(f"{red} Fatal - {msg}")

def get(text):
    return input(f"{blue} {text}")

def saveToFile(proxy):
    with open(outputfile, 'a') as file:
        file.write(proxy + "\n")

def isSocks(host, port, soc):
    proxy = f"{host}:{port}"
    try:
        if socks5(host, port, soc):
            action(f"{proxy} is SOCKS5.")
            return True
        if socks4(host, port, soc):
            action(f"{proxy} is SOCKS4.")
            return True
    except socket.timeout:
        alert(f"Timeout during SOCKS check: {proxy}")
        return False
    except socket.error:
        alert(f"Connection refused during SOCKS check: {proxy}")
        return False

def socks4(host, port, soc):  # Check if a proxy is SOCKS4 and alive
    ipaddr = socket.inet_aton(host)
    packet4 = b"\x04\x01" + port.to_bytes(2, "big") + ipaddr + b"\x00"
    soc.sendall(packet4)
    data = soc.recv(8)
    if len(data) < 2:
        return False
    if data[0] != 0x00 or data[1] != 0x5A:
        return False
    return True

def socks5(host, port, soc):  # Check if a proxy is SOCKS5 and alive
    soc.sendall(b"\x05\x01\x00")
    data = soc.recv(2)
    if len(data) < 2:
        return False
    if data[0] != 0x05 or data[1] != 0x00:
        return False
    return True

def isAlive(pip, timeout):  # Check if a proxy is alive
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req = urllib.request.Request('http://www.google.com')
        urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        error(f"{pip} throws: {e.code}")
        return False
    except Exception as details:
        error(f"{pip} throws: {details}")
        return False
    return True

def checkProxies():
    while toCheck:
        proxy = toCheck.pop(0)
        alert(f"Checking {proxy}")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        host, port = proxy.split(":")
        port = int(port)

        if port < 0 or port > 65535:
            error(f"Invalid port for {proxy}")
            continue

        if isSocks(host, port, s):
            socks.append(proxy)
            saveToFile(proxy)
        else:
            alert(f"{proxy} is not a working SOCKS4/5 proxy.")
            if isAlive(proxy, timeout):
                action(f"Working HTTP/HTTPS proxy found ({proxy})!")
                working.append(proxy)
                saveToFile(proxy)
            else:
                error(f"{proxy} is not working.")
        s.close()

socks = []
working = []
toCheck = []
threads = []
checking = True

proxiesfile = get("Proxy list: ")
outputfile = get("Output file: ")
threadsnum = int(get("Number of threads: "))
timeout = int(get("Timeout (seconds): "))

try:
    with open(proxiesfile, "r") as file:
        toCheck = [line.strip() for line in file]
except FileNotFoundError:
    errorExit(f"Unable to open file: {proxiesfile}")

if os.path.isfile(outputfile):
    while True:
        error("Output file already exists, content will be overwritten!")
        check = get("Are you sure you would like to continue (y/n)?").lower()
        if check in ['y', 'yes']:
            break
        elif check in ['n', 'no']:
            errorExit("Quitting...")

for i in range(threadsnum):
    thread = threading.Thread(target=checkProxies)
    thread.setDaemon(True)
    threads.append(thread)
    action(f"Starting thread {i + 1}")
    thread.start()
    time.sleep(0.25)

action(f"{threadsnum} threads started...")
while checking:
    time.sleep(5)
    if len(threading.enumerate()) - 1 == 0:
        alert("All threads done.")
        action(f"{len(working)} alive proxies.")
        action(f"{len(socks)} SOCKS proxies.")
        action(f"{len(socks) + len(working)} total alive proxies.")
        checking = False
    else:
        alert(f"{len(working)} alive proxies so far.")
        alert(f"{len(socks)} SOCKS proxies so far.")
        alert(f"{len(toCheck)} remaining proxies.")
        alert(f"{len(threading.enumerate()) - 1} active threads...")

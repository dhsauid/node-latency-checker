#!/usr/bin/env python3
"""node-latency-checker

Usage:
    python latency_checker.py
    python latency_checker.py example.com 8.8.8.8

With no arguments, this script checks 8.8.8.8 and 1.1.1.1.
With arguments, it checks each host given on the command line.

For each host it runs the system ping command 4 times and prints
the average latency and the packet loss percentage.
Only Python 3 and the system ping command are required.
"""

import platform
import re
import subprocess
import sys


DEFAULT_HOSTS = ["8.8.8.8", "1.1.1.1"]
PING_COUNT = 4


def ping_host(host, count=PING_COUNT):
    """Ping one host and return (average_ms, packet_loss_percent)."""
    if platform.system().lower() == "windows":
        command = ["ping", "-n", str(count), host]
    else:
        command = ["ping", "-c", str(count), host]
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=30
        )
    except (OSError, subprocess.TimeoutExpired):
        return None, 100.0
    output = result.stdout + result.stderr
    loss = None
    match = re.search(r"(\d+(?:\.\d+)?)% packet loss", output)
    if match:
        loss = float(match.group(1))
    else:
        match = re.search(r"Lost = \d+ \((\d+)% loss\)", output)
        if match:
            loss = float(match.group(1))
    average = None
    match = re.search(r"= [\d.]+/([\d.]+)/[\d.]+/[\d.]+ ms", output)
    if match:
        average = float(match.group(1))
    else:
        match = re.search(r"Average = (\d+)ms", output)
        if match:
            average = float(match.group(1))
    if loss is None:
        loss = 100.0 if average is None else 0.0
    return average, loss


def main(hosts):
    for host in hosts:
        average, loss = ping_host(host)
        if average is None:
            print(f"{host}: no reply (packet loss: {loss:.1f}%)")
        else:
            print(
                f"{host}: average latency {average:.1f} ms, "
                f"packet loss {loss:.1f}%"
            )


if __name__ == "__main__":
    main(sys.argv[1:] or DEFAULT_HOSTS)

# node-latency-checker

A small Python tool to measure server latency and packet loss with the system ping command, so you can compare hosts before choosing one.

## Installation

You only need Python 3. There are no third-party dependencies. The tool uses the system `ping` command, so make sure `ping` is available on your computer.

## Usage

Check the default hosts (8.8.8.8 and 1.1.1.1):

```bash
python latency_checker.py
```

Check specific hosts:

```bash
python latency_checker.py example.com 8.8.8.8
```

## Output

For each host, the script pings it 4 times and prints one line with its average latency in milliseconds and its packet loss percentage, for example:

```text
example.com: average latency 12.3 ms, packet loss 0.0%
8.8.8.8: average latency 15.6 ms, packet loss 0.0%
```

A lower average latency means a faster response, and a lower packet loss percentage means a more stable connection. If a host does not reply, the script reports no reply with a 100.0% packet loss.

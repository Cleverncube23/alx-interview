#!/usr/bin/python3
import sys
import signal
import re

total_size = 0
status_counts = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0

log_pattern = re.compile(
    r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} - \[\S+ \S+\] \"GET /projects/260 HTTP/1\.1\" (\d{3}) (\d+)$"
)

def print_stats():
    global total_size, status_counts
    print(f"File size: {total_size}")
    for status in sorted(status_counts.keys()):
        if status_counts[status] > 0:
            print(f"{status}: {status_counts[status]}")

def signal_handler(sig, frame):
    print_stats()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        line_count += 1
        match = log_pattern.match(line.strip())
        if match:
            status_code = int(match.group(1))
            file_size = int(match.group(2))
            total_size += file_size
            if status_code in status_counts:
                status_counts[status_code] += 1
        
        if line_count % 10 == 0:
            print_stats()

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)

finally:
    print_stats()

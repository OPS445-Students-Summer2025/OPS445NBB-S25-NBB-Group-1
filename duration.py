#!/usr/bin/env python3

# Author: Sadam Adebola
# Contribution: Duration Calculation
# Description: These functions calculate how long a user was logged in,convert the duration to and from seconds, and format the output.
# Used for tracking daily and weekly login durations.

def parse_duration_to_seconds(duration_str):
    parts = duration_str.strip().split(":")
    h = int(parts[0])
    m = int(parts[1])
    s = int(parts[2])
    return h * 3600 + m * 60 + s

print("Testing parse_duration_to_seconds:")
print(parse_duration_to_seconds("01:30:00"))

def format_seconds_to_duration(total_seconds): 
    hours = total_seconds // 3600
    remainder = total_seconds % 3600
    minutes = remainder // 60
    seconds = remainder % 60
    return f"{hours}:{minutes:02d}:{seconds:02d}"

print("Testing format_seconds_to_duration:")
print(format_seconds_to_duration(3661))

from datetime import datetime

def calculate_duration(login_time, logout_time):
    t1 = datetime.strptime(login_time, "%H:%M:%S")
    t2 = datetime.strptime(logout_time, "%H:%M:%S")
    return t2 - t1

print("Testing calculate_duration:")
diff = calculate_duration("10:00:00", "12:30:30")
print(diff)

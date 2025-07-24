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

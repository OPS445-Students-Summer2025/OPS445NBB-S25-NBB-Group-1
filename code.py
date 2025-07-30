  GNU nano 7.2                          3.txt *                                 
#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author:vishesh
'''
import os
import sys
import time
import subprocess
from datetime import datetime

def format_hms(total_seconds):
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def report_duration(grouped):
    total_seconds = 0
    #print("Grouped Entries with Duration:")
    for (user, date, start_time), end_time in grouped.items():
        try:
            start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M:%S")
        except ValueError :
            print_err("Failed to print!")

        duration = (end_dt - start_dt).total_seconds()
        total_seconds += duration
        #print(f"{user},{date},{start_time},{end_time},{int(duration)} seconds")

    #hours = total_seconds // 3600
    #minutes = (total_seconds % 3600) // 60
    #seconds = total_seconds % 60
    #total_time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    #return total_time_str
    return total_seconds

def read_and_group(file_path):
    grouped = {}

    f = open(file_path, 'r')
    for line in f:
        if not line.strip():
            continue  
        try:
            user, date, start_time, end_time, duration, log_remark = line.strip().split(',')
        except ValueError:
            print_err("Failed to print!")

        key = (user, date, start_time)
        if key not in grouped:
            grouped[key] = end_time
        else:
            grouped[key] = max(grouped[key], end_time)  # Keep latest end_time
    f.close()

    return grouped

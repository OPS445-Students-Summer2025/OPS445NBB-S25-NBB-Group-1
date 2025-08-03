#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program:
Author: vishesh
'''

import os
import sys
import time
import subprocess
import argparse
import getpass
from datetime import datetime

def print_report(userid):
    # there is duration in log file (calculated from the time record being written)
    # but the duration is not used in report, instead the duration is calculated 
    # again using group

    try:
        #userid = get_input_user()
        if not check_user_in_sys(userid):
            print_err("Invalid userid!")
      
        today = datetime.now().date()
        total_seconds = 0
        report_lines = []

        report_lines.append(f"user: {userid}")
        report_lines.append("Daily durations:")

        # weekly report means previous 7 days
        # for each day sum the userid login duration
        for i in range(7):
            date_check = datetime.fromordinal(today.toordinal() - i).date()
            file_path = f"{userid}_{date_check}.log"
            if not os.path.exists(file_path):
                continue
            # group userid with same login time with the max logout time
            grouped_entries = read_and_group(file_path)
            # calculate each grouped record duration (logout - login)
            # sum the duration 
            day_seconds = report_duration(grouped_entries)  # must return seconds
            day_hms = format_hms(day_seconds)
            report_lines.append(f"{date_check} - {day_hms}")
            total_seconds += day_seconds # accumlate the daily duration sum

        total_hms = format_hms(total_seconds) # weekly total
        report_lines.append(f"\nTotal Duration (last 7 days): {total_hms}")

        report_filename = f"{userid}_weekly_report_{today}.txt"
        f = open(report_filename, 'w')
        for line in report_lines:
            f.write(line + '\n')
        f.close()

        print(f"Report saved to: {report_filename}")
        return True

    except Exception as e:
        print(f"Error in print_report: {e}")
        return False

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

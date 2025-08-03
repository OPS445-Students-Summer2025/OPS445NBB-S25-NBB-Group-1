#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py
Author: Chung Yin Choi
'''

import os
import sys
import time
import subprocess
import argparse
import getpass
from datetime import datetime

def check_who(userid): # check userid is in who
    try:
        output = subprocess.check_output(["who"], text=True)
        for line in output.strip().split('\n'):
            if line.startswith(userid + " "):
                parts = line.split()
                login_time = f"{parts[3]}:00"
                return login_time
    except:
        return None
    return None

def track_user(userid):
    user = None
    #userid = get_input_user()
    if not check_user_in_sys(userid):
        print_err("Invalid userid!")

    try:
        print(f"Tracking...{userid}")
        while True:            
            login_time = check_who(userid) # return login_time if userid in who
            # Write record to log file if
            # 1 user is logout
            # 2 program stops (by control flag or out of time range)
            # in case of abnormal end such as ctrl-c, crash..., no write to log

            if check_program_stop(): # used to stop program normally withou <ctrl-c>
                print("program stop")
                remark = "*"
                if user is not None and login_time:
                    user.logout_time = datetime.now().strftime("%H:%M:%S")
                    duration = calculate_duration(user)
                    write_log(userid, user.date, user.login_time, user.logout_time, duration, remark)
                sys.exit(1)

            if user is None: # if userid in who and no user object is created
                if login_time:
                    indate = datetime.now().date()
                    user = Userlogined(userid, indate, login_time) # create user object
            else:
                if not login_time: # if userid is not in who and user object 
                    remark = ""
                    user.logout_time = datetime.now().strftime("%H:%M:%S") # save logout time
                    duration = calculate_duration(user)
                    write_log(userid, user.date, user.login_time, user.logout_time, duration, remark)
                    user = None # remove user object

            time.sleep(3)

    except Exception as e:
        print(f"Error in track_user: {e}") 

'''
OPS445 Assignment 2
Program:  
Author:Vishesh
'''


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
    # if userid has same login time, need to group log records to calculate accurate duration
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










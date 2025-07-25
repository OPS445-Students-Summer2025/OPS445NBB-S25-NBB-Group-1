#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
The python code in this file is original work written by
Chung Yin Choi. No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.

Author: Chung Yin Choi
Semester: Summer 2025
Description: This program returns an end date (including day of week), 
given a start date and number of days
'''
import os
import sys
import time
import subprocess
from datetime import datetime

class Userlogined:
    def __init__(self, userid, indate, login_time):
        self.userid = userid
        self.date = indate
        self.login_time = login_time
        self.logout_time = None

def print_err(err):
    print("Error:", err)
    sys.exit(1)

def get_input_user():
    userid = input("Enter userid: ")
    if check_user_in_sys(userid):
        return userid
    else:
        print_err("Invalid userid!")
    return

def check_user_in_sys(userid):
    try:
        f = open("/etc/passwd", "r")
        for line in f:
            if line.startswith(userid + ":"):
                return True
    except FileNotFoundError:
        print_err("File /etc/passwd not found!")
    except PermissionError:
        print_err("Permission denied accessing /etc/passwd!")
    return False

def check_who(userid):
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

def check_program_stop():
    # assume working hour is not cross day
    # assume user can not login within working hour
    try:
        f = open("control.txt", "r")
        line = f.readline().strip().lower()
        parts = line.split(',')       
        stop_flag = parts[0]
        start_time = parts[1]
        end_time = parts[2]
        now = datetime.now().time()
        now = now.strftime("%H:%M:%S")

        if stop_flag == 'true':
            return True
        if start_time and end_time:
            if now < start_time or now > end_time:
                return True        
    except:
        return False
    return False

def write_log(userid, indate,login_time, logout_time,duration,remark):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{userid}_{date_str}.log"

    try:
        f = open(filename, 'a')
        f.write(f"{userid},{indate},{login_time},{logout_time},{duration},{remark}\n")
    except:
        print_err("Failed to write log!")

def calculate_duration(user):
    t1 = datetime.strptime(user.login_time, "%H:%M:%S")
    t2 = datetime.strptime(user.logout_time, "%H:%M:%S")
    return t2 - t1

from datetime import datetime

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

#def print_report():
#    userid = get_input_user()
#    today = datetime.now().strftime("%Y-%m-%d")
#    file_path = f"{userid}_{today}.log"  
#    grouped_entries = read_and_group(file_path)
#    total_seconds = report_duration(grouped_entries)
#    print(f"\nTotal Duration: {total_seconds}")
#    return True


def format_hms(total_seconds):
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def print_report():
    # there is duration in log file (calculated from the time record being written)
    # but the duration is not used in report, instead the duration is calculated 
    # again using group

    try:
        userid = get_input_user()
        today = datetime.now().date()
        total_seconds = 0
        report_lines = []

        report_lines.append(f"user: {userid}")
        report_lines.append("Daily durations:")
        for i in range(7):
            date_check = datetime.fromordinal(today.toordinal() - i).date()
            file_path = f"{userid}_{date_check}.log"
            if not os.path.exists(file_path):
                continue
            grouped_entries = read_and_group(file_path)
            day_seconds = report_duration(grouped_entries)  # must return seconds
            day_hms = format_hms(day_seconds)
            report_lines.append(f"{date_check} - {day_hms}")
            total_seconds += day_seconds

        total_hms = format_hms(total_seconds)
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


def track_user():
    user = None
    userid = get_input_user()

    try:
        while True:
            login_time = check_who(userid)
            # Write record to log file if
            # 1 user is logout
            # 2 program stops (by control flag or out of time range)
            # in case of abnormal end such as ctrl-c, crash..., no write to log

            if check_program_stop():
                print("program stop")
                remark = "*"
                if user is not None and login_time:
                    user.logout_time = datetime.now().strftime("%H:%M:%S")
                    duration = calculate_duration(user)
                    write_log(userid, user.date, user.login_time, user.logout_time, duration, remark)
                sys.exit(1)

            if user is None:
                if login_time:
                    indate = datetime.now().date()
                    user = Userlogined(userid, indate, login_time)
            else:
                if not login_time:
                    remark = ""
                    user.logout_time = datetime.now().strftime("%H:%M:%S")
                    duration = calculate_duration(user)
                    write_log(userid, user.date, user.login_time, user.logout_time, duration, remark)
                    user = None

            time.sleep(3)

    except Exception as e:
        print(f"Error in track_user: {e}")


if __name__ == "__main__":
    print("Select an option:")
    print("1 - Track user")
    print("2 - Print report")
    print("3 - Add/delete user")    
    print("9 - Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        track_user()
    elif choice == '2':
        print_report()            
    elif choice == '9':
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")


    





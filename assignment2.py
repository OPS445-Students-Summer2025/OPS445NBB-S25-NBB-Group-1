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

def print_report():

    return True

def track_user():
    user = None
    userid = get_input_user()
 
    while True:
        login_time = check_who(userid)

        if check_program_stop():
            print("program stop")
            remark = "*"
            if user is not None and login_time:
                user.logout_time = datetime.now().strftime("%H:%M:%S")
                
                duration = calculate_duration(user)

                write_log(userid, user.date, user.login_time, user.logout_time,duration,remark)
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

                write_log(userid, user.date, user.login_time, user.logout_time,duration,remark)
                user = None

        time.sleep(3)

if __name__ == "__main__":
    print("Select an option:")
    print("1 - Track user")
    print("2 - Print report")
    print("3 - add/del user")    
    print("9 - exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        track_user()
    elif choice == '2':
        if print_report():
            print("Report printed!")
    elif choice == '9':
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")


    





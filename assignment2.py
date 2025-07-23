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
    def __init__(self, userid, login_time):
        self.userid = userid
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
                login_time = f"{parts[2]} {parts[3]}:00"
                return login_time
    except:
        return None
    return None

def write_log(userid, login_time, logout_time):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{userid}_{date_str}.log"
    try:
        with open(filename, 'a') as f:
            f.write(f"{userid},{login_time},{logout_time}\n")
    except:
        print_err("Failed to write log!")


if __name__ == "__main__":
    user = None
    userid = get_input_user()

    while True:
        login_time = check_who(userid)

        if user is None:
            if login_time:
                user = Userlogined(userid, login_time)
        else:
            if not login_time:
                user.logout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("logout!")
                write_log(userid, user.login_time, user.logout_time)
                user = None

        time.sleep(3)


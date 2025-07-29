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
from datetime import datetime

class Userlogined:
    def __init__(self, userid, indate, login_time):
        self.userid = userid
        self.date = indate
        self.login_time = login_time
        self.logout_time = None

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


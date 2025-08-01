#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: track_user.py
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


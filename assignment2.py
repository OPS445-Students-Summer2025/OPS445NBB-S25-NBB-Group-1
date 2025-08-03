#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py
Author: Sadam Adebola
'''

import os
import sys
import time
import subprocess
import argparse
import getpass
from datetime import datetime

def check_user_in_sys(userid): # validate userid
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

def check_program_stop(): # control program run
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
    return False # if control file doesn't exist, program continue to run

def calculate_duration(user):
    # calculate login duration
    t1 = datetime.strptime(user.login_time, "%H:%M:%S")
    t2 = datetime.strptime(user.logout_time, "%H:%M:%S")
    return t2 - t1

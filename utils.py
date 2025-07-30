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
from datetime import datetime

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

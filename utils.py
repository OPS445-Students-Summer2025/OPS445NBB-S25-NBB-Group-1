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

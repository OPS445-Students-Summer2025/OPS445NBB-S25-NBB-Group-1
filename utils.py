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

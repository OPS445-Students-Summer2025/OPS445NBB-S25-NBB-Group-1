#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: Do An Truong
Student ID: 166335232
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

def write_log(userid, indate,login_time, logout_time,duration,remark):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{userid}_{date_str}.log"

    try:
        f = open(filename, 'a')
        f.write(f"{userid},{indate},{login_time},{logout_time},{duration},{remark}\n")
    except:
        print_err("Failed to write log!")

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



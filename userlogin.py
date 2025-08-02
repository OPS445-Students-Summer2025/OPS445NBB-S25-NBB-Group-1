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
import argparse
import getpass
from datetime import datetime

class Userlogined: # user object for login session info
    def __init__(self, userid, indate, login_time):
        self.userid = userid
        self.date = indate
        self.login_time = login_time
        self.logout_time = None

def print_err(err):
    print("Error:", err)
    sys.exit(1)

def write_log(userid, indate,login_time, logout_time,duration,remark): # log for statistics
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{userid}_{date_str}.log"

    try:
        f = open(filename, 'a')
        f.write(f"{userid},{indate},{login_time},{logout_time},{duration},{remark}\n")
    except:
        print_err("Failed to write log!")

def config_user():
    # display user menu
    print("---------------------------------------")
    print("User configuration")
    print("---------------------------------------")
    print("Select an option:")
    print("1 - Add user")    
    print("2 - Delete user")    
    print("9 - Exit")
     
    choice = input("Enter your choice: ")
    if choice == '1':
        add_user()
    elif choice == '2':
        delete_user()      
    elif choice == '9':
        sys.exit(0)
    else:
        print("Invalid choice! Please try again.")
             
    return

def add_user():
    # prompt input userid 
    # prompt password with password object
    try:
        username = input("Enter the username: ")
        password = getpass.getpass("Enter the password: ")

        subprocess.run(['sudo','useradd', '-m', username], check=True)        
        subprocess.run(['sudo','chpasswd'], input=f"{username}:{password}".encode(), check=True)

        print(f"User '{username}' created successfully.")

    except Exception:
        print("Error in add_user!")        

def delete_user():
    # prompt input userid
    # valildate userid
    try:
        username = input("Enter the username: ")
        if not check_user_in_sys(username):
            print_err("Invalid userid!")
            sys.exit(1)
        subprocess.run(['sudo', 'userdel', '-r', username], check=True)
        print(f"User '{username}' deleted successfully.")
        
    except Exception:
        print("Error in delete_user!")  

if __name__ == "__main__":
    # add argparse for 2 functions with option
    # track and report functions need userid argument
    # config funtion doesn't need userid argument (prompt input userid)

    parser = argparse.ArgumentParser(description="User time tracking system with function and optional user.")

    parser.add_argument("function", choices=["track", "report", "config"], help="The function to execute (track, report)")
    parser.add_argument("--user", help="Username (required for track or report)")

    args = parser.parse_args()

    if args.function in ["track", "report"] and not args.user:
        parser.error(f"--user is required when function is '{args.function}'")

    if args.function not in ["track", "report"] and args.user:
        parser.error(f"--user is not required when function is '{args.function}'")
    
    try:

        if args.function == 'track':
            track_user(args.user) # track user function

        if args.function == 'report':
            print_report(args.user) # print report function (weekly)
            
        if args.function == 'config': # config (add/delete user)
            config_user()

    except Exception:
        print("Error in main!")     

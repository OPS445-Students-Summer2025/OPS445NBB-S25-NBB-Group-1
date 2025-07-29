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
import getpass
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

            #if check_program_stop():
            #    print("program stop")
            #    remark = "*"
            #    if user is not None and login_time:
            #        user.logout_time = datetime.now().strftime("%H:%M:%S")
            #        duration = calculate_duration(user)
            #        write_log(userid, user.date, user.login_time, user.logout_time, duration, remark)
            #    sys.exit(1)

            if user is None:
                if login_time:
                    indate = datetime.now().date()
                    user = Userlogined(userid, indate, login_time)
            else:
                if not login_time:
                    remark = ""
                    user.logout_time = datetime.now().strftime("%H:%M:%S")
                    #duration = calculate_duration(user)
                    #write_log(userid, user.date, user.login_time, user.logout_time, duration, remark)
                    user = None

            time.sleep(3)

    except Exception as e:
        print(f"Error in track_user: {e}")

def add_user():
    try:
        username = input("Enter the username: ")
        password = getpass.getpass("Enter the password: ")

        subprocess.run(['sudo','useradd', '-m', username], check=True)        
        subprocess.run(['sudo','chpasswd'], input=f"{username}:{password}".encode(), check=True)

        print(f"User '{username}' created successfully.")

    except Exception:
        print("Error in add_user!")        

def delete_user():
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
    print("Select an option:")
    print("1 - Track user")
    print("2 - Print report")
    print("3 - Add user")    
    print("4 - Delete user")    
    print("9 - Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        track_user()
    #elif choice == '2':
        #print_report()        
    elif choice == '3':
        add_user()      
    elif choice == '4':
        delete_user()              
    elif choice == '9':
        sys.exit(0)
    else:
        print("Invalid choice! Please try again.")


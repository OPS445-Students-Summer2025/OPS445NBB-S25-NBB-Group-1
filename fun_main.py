#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: fun_main.py 
Author: Chung Yin Choi
'''

import os
import sys
import time
import subprocess
import getpass
import argparse
from datetime import datetime

def track_user(userid):
    if check_user_in_sys(userid):
        return userid
    else:
        print_err("Invalid userid!")
    return    
    
def print_report(userid):
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

def print_err(err):
    print("Error:", err)
    sys.exit(1)

def add_user():
    return

def delete_user():
    return

def config_user():
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

if __name__ == "__main__":
    #print("---------------------------------------")
    #print("User time tracking system (2025 summer)")
    #print("---------------------------------------")
    #print("Select an option:")
    #print("1 - Track user")
    #print("3 - Add user")    
    #print("4 - Delete user")    
    #print("9 - Exit")

  
    parser = argparse.ArgumentParser(description="User time tracking system with function and optional user.")

    parser.add_argument("function", choices=["track", "report", "config"], help="The function to execute (track, report)")
    parser.add_argument("--user", help="Username (required for track or report)")

    args = parser.parse_args()

    if args.function in ["track", "report"] and not args.user:
        parser.error(f"--user is required when function is '{args.function}'")
    
    try:
        #pass
        if args.function == 'track':
            track_user(args.user)

        if args.function == 'report':
            print_report(args.user)
            
        if args.function == 'config':
            config_user()

        #choice = input("Enter your choice: ")
        #if choice == '1':
        #    track_user()
        #elif choice == '2':
        #    print_report()        
        #elif choice == '3':
        #    add_user()      
        #elif choice == '4':
        #    delete_user()              
        #elif choice == '9':
        #    sys.exit(0)
        #else:
        #    print("Invalid choice! Please try again.")

    except Exception:
        print("Error in main!")     
    


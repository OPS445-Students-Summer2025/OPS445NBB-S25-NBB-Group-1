  GNU nano 7.2                          3.txt *                                 
#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author:vishesh
'''
import os
import sys
import time

def format_hms(total_seconds):
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


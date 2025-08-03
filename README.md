# Winter 2025 Assignment 2
User time tracking system
This program tracks a user login to the system, save login and logout time to log file
It generates weekly duration report (last 7 days)
It adds/deletes user

Arguments for the program
assignment2_dev.py [function] --user [userid]
[function] 
track (run the program in background)
report (generate report)
config (interactive, it prompts input of userid and password)
--user (only required in track or report function)
[userid]
must be a user in /etc/passwd/

References for some imported libraries:
https://docs.python.org/3/library/getpass.html
https://docs.python.org/3/library/argparse.html
https://docs.python.org/3/library/datetime.html

The logic of the program
Track:
Call the program with "userid" to track
User login and logout time is saved to log file (a daily file)
program checks if user exists in /etc/passwd
it will "listen" every 3 seconds - monitor login and logout time 
login time is saved from "who" command
logout time is when user no longer found in "who" command
if program stops but user still login, the report function has special calculation for this
the program only runs within range of start and end time in "control" file
there is a flag in "control" file to gracefully stop the program (without <ctrl-c>)

Report:
Call the program with "userid" to print
program checks if user exists
it will print based on log file of last 7 days
report function provides grouping of userid and login time to calculate duration correctly

Config:
Program prompts for input of user and/or password for creation and deletion of userid

Team members work assignments:
Person 1 - main function and class
Person 2 - track user function
Person 3 - utility functions such as validate userid, check who command, check control file
Person 4 - report printing function


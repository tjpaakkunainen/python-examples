"""
A simple program for logging days / hours for whatever activity.

Give the program path to the .csv file where data should be recorded. 

example: 

python logbook.py logbook.csv

Valid actions are 'l' (log), 'c' (check) and 'q' (quit)
"""

import os
import sys
from csv import reader, writer
import datetime as dt


def main(path_to_file):
    print("\nWelcome to a simple logbook! \n")
    
    logging = command_inquiry(path_to_file)
    
    if not logging:
        quit_msg = ''.join("Quitting program. Do you want to remove the .csv file you created? " 
                           "If so, write 'remove'. Otherwise just click enter to quit program.\n")
        remove_file_inquiry = input(quit_msg)
        if 'remove' in remove_file_inquiry:
            try:
                os.remove(path_to_file)
                print("Removed file.", end=" ")
            except FileNotFoundError:
                print("Couldn't remove file. If it exists, please remove it manually.")

        print("Bye!")        


def command_inquiry(path_to_file):
    while True:
        
        command = input("What do you want to do? [l]og / [c]heck / [q]uit: ")

        if command == "l":
            log_date = date_inquiry() 
            if 'quit' in str(log_date):
                return False
            
            log_hours = hours_inquiry() 
            if 'quit' in log_hours.lower():
                return False

            log_action = action_inquiry()
            
            write_to_log(path_to_file, log_date, log_hours, log_action)

        elif command == "c":
            check(path_to_file)

        elif command == "q":
            return False

        else:
            print(f"You entered '{command}'. Valid commands are l "
                   "for logging, c for checking, and q for quitting.")

def date_inquiry():
    times_inquired = 0
    today = dt.datetime.now()
    while True:
        log_date = input("Date to be logged: ")

        if 'quit' in log_date.lower():
            return log_date.lower()

        if not log_date:
            log_date = f"{today.day}.{today.month}.{today.year}"
            print(f"Logged today: {log_date}")
            return log_date
        
        try:
            log_date_datetime= dt.datetime.strptime(log_date, "%d.%m.%Y")
            log_date_formatted = f"{log_date_datetime.day}.{log_date_datetime.month}.{log_date_datetime.year}"
            print(f"log date formatted: {log_date_formatted}")
            return log_date_formatted
        except ValueError:
            print(f"{log_date} is not valid date. You need to give a valid date, such as 30.1.2023.")
            times_inquired += 1
            if times_inquired > 1:
                print("To quit program, write 'quit'.")
            continue


def hours_inquiry():
    times_inquired = 0
    while True:
        log_hours = input("Hours to be logged: ")
        
        if 'quit' in log_hours.lower():
            return log_hours
        
        log_hours = log_hours.replace(",", ".")
        try:
            if 0 < float(log_hours) <= 24.0:
                return log_hours
            else:
                print(f"You can log 0-24 hours at a time.")
                continue
            
        except ValueError:
            print("You need to give hours in some valid numerical format (e.g. 1, 6.5 or 3,5).")
            times_inquired += 1
            if times_inquired > 1:
                print("To quit program, write 'quit'.")
            continue

def action_inquiry():
    while True:
        log_action = input("Action to be logged: ")
        if len(log_action) <= 1:
            print("You need to log some sort of action.")
            continue
        return log_action


def write_to_log(path_to_file,paiva, tunnit, syy):
    
    log_data = [f"{paiva}", str(tunnit).replace(".", ","), syy]

    with open(path_to_file, "a", encoding="utf_8", newline="") as file:
        logwriter = writer(file)
        logwriter.writerow(log_data)


def check(path_to_file):
    try:
        with open (path_to_file, encoding="utf_8") as file:
            
            print("")
            column_day = "DAY"
            column_hours = "HOURS"
            column_action = "ACTION"
            print(f"{column_day:15} {column_hours:15} {column_action:15}")

            log_reader = reader(file)
            total = 0

            for logged_day, logged_hours, logged_action in log_reader: 
                print(f"{logged_day:15} {logged_hours:15} {logged_action:15}")
                total += float(logged_hours.replace(",", "."))

            total = str(round(total, 1)).replace(".", ",")

            print(f"{'TOTAL':15} {total} \n") 

    except FileNotFoundError:
        print(f"File '{path_to_file}' does not seem to exist yet.")
        print("Log something to create a new file.")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 2 or "--help" in args:
        sys.exit(__doc__)
    try:
        main(*args)
    except ValueError as err: 
            sys.exit(err) 
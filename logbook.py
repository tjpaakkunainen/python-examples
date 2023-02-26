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
from encodings import utf_8
import datetime



def main(path_to_file):
    print(""); print("Welcome to a simple logbook!"); print("")
    while True:
        command = input("What do you want to do? [l]og / [c]heck / [q]uit: ")
        if command == "l":
            log_date = date_inquiry() 
            if log_date == False:
                continue
            log_hours = hours_inquiry() 
            if log_hours == False: 
                continue
            log_action = input("Action to be logged: ") 
            if not log_action:
                print("You need to log some sort of action.")
                continue
            
            write_to_log(path_to_file, log_date, log_hours, log_action)

        if command == "c":
            check(path_to_file)

        if command == "q":
            quit = ''.join("Quitting program. Do you want to remove the .csv file you created? " 
                           "If so, write 'remove'. Otherwise just click enter to quit program. \n")
            remove_file_inquiry = input(quit)
            if 'remove' in remove_file_inquiry:
                try:
                    os.remove(path_to_file)
                    print("Removed file.", end=" ")
                except ValueError:
                    print("Couldn't remove file. Please remove it manually.")
            print("Bye!")        
            break

def date_inquiry():
    today = datetime.datetime.now()
    while True:
        log_date = input("Date to be logged: ")

        if not log_date:
            return today

        if 1 < len(log_date) < 7:
            log_date+=str(today.year)
        
        try:
            log_date_formatted = datetime.datetime.strptime(log_date, "%d.%m.%Y")
            return log_date_formatted
        except ValueError:
            print("You need to give a valid date. Restarting program.")
            return False


def hours_inquiry():
    while True:
        log_hours = input("Hours to be logged: ")
        log_hours = log_hours.replace(",", ".")
        try:
            if 0 < float(log_hours) <= 24.0:
                return log_hours
            else:
                print(f"You can log 0-24 hours at a time. Restarting program.")
                return False
        except ValueError:
            print("You need to give hours in some valid numerical format (e.g. 1, 6.5 or 3,5). Restarting program.")
            return False



def write_to_log(path_to_file,paiva, tunnit, syy):
    
    log_data = [f"{paiva.day}.{paiva.month}.{paiva.year}", str(tunnit).replace(".", ","), syy]

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
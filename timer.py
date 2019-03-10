from datetime import datetime, timedelta
import pickle
import os
import time
import sys
from enum import Enum

# status = Enum('Status', 'STARTED STOPPED')
class status(Enum):
    STARTED = '1'
    STOPPED = '2'
    PAUSED = '3'

VALID_COMMANDS = ['start', 'stop', 'resume', 'tick', 'summarise']

def load_timekeeper(test=False):
    today = datetime.today().strftime("%y-%m-%d")
    if test:
        today = 'test-' + today
    file_path = os.path.join('db', today + '.pkl')
    if os.path.isfile(file_path):
        print("[DEBUG] File exist")
        with open(file_path, 'rb') as file:
            timekeeper = pickle.load(file)
    else:
        print("[DEBUG] File not exist")
        timekeeper = {}
    
    return timekeeper

def save_timekeeper(timekeeper, test=False):
    today = datetime.today().strftime("%y-%m-%d")
    if test:
        today = 'test-' + today
    file_path = os.path.join('db', today + '.pkl')
    with open(file_path, 'wb') as file:
        pickle.dump(timekeeper,file)
    print("[DEBUG] Saved timekeeper")

#START
#PAUSE
#RESUME
#TICK
# {'tag': (status, timelist)}

def timer(timekeeper, argv):
    if len(argv) == 2:
        command, tag = argv[0], argv[1]
        if command not in VALID_COMMANDS:
            print("[ERROR] Not a valid a command")
            exit()

        if tag not in timekeeper.keys():
            if command != "start":
                print("[ERROR] Only valid command for a new tag is 'start'")
            else:
                timekeeper[tag] = [status.STARTED, [datetime.today()]]
                print(f"Started timekeeping for {tag}")
                print(f"Curent time is {timekeeper[tag][1][-1].strftime('%H:%M')}")
        else:        
            if command == "tick":
                if timekeeper[tag][0] == status.STOPPED:
                    print(f"Timer for {tag} is not running. Last run ran for {last2runs(timekeeper,tag)}")
                elif timekeeper[tag][0] == status.STARTED:
                    delta = datetime.today() - timekeeper[tag][1][-1]
                    print(format_delta(delta))
            elif command == 'stop':
                if timekeeper[tag][0] == status.STOPPED:
                    print(f"Timer for {tag} was already stopped at {format_time(timekeeper[tag][1][-1])}")
                else:
                    timekeeper[tag][1].append(datetime.today())
                    timekeeper[tag][0] = status.STOPPED
                    print(f"{tag} stopped. Last run ran for {last2runs(timekeeper,tag)} ")
            elif command == 'resume':
                if timekeeper[tag][0] == status.STARTED:
                    print(f"Timer for {tag} has been running since {format_time(timekeeper[tag][1][-1])}")
                else:
                    print(f"Resumed timekeeping for {tag}. Last run ran for {last2runs(timekeeper,tag)} ")
                    timekeeper[tag][1].append(datetime.today())
                    timekeeper[tag][0] = status.STARTED
            elif command == 'summarise':
                summarise(timekeeper, tag)
            elif command == 'start':
                print(f"Time for {tag} has been kept. Use resume to resume timekeeping.")
            else:
                print(f"You have entered forbidden if-else space")
    elif argv == 'summarise': 
        for tag in timekeeper.keys():
            print('\n')
            summarise(timekeeper, tag)
    else:
        print(f"You have entered forbidden if-else space")
    return timekeeper

def summarise(timekeeper, tag):
    print(f"Summary for {tag}")
    total_time = timedelta()
    timelist = timekeeper[tag][1]
    for i in range(len(timelist)//2):
        delta = timelist[2*i+1]-timelist[2*i]
        print(f"{i}. {format_time(timelist[2*i])} {format_delta(delta)}")
        total_time += delta
    if timekeeper[tag][0] == status.STARTED:
        delta = datetime.today()-timelist[-1]
        total_time += delta
        print(f"{len(timelist)//2+1}. {format_time(timelist[-1])} {format_delta(delta)} - running") 
    print(f"Total time spent - {format_delta(total_time)} ")

def last2runs(timekeeper, tag):
    return format_delta(timekeeper[tag][1][-1] - timekeeper[tag][1][-2])

def format_time(time):
    return time.strftime('%H:%M')

def format_delta(delta):
    seconds = delta.total_seconds()
    return f"{int(seconds//3600)}h {int(seconds//60)}m {int(seconds%60)}s"

def test():
    command_list = ['start','stop','tick','start','resume','tick','stop', 'resume','stop','summarise', 'resume','tick' ,'summarise']
    tag = 'test'
    for i in range(len(command_list)):
        timekeeper = load_timekeeper(True)
        print(f"\nTesting command {command_list[i]}")
        argv = [command_list[i], tag]
        timekeeper = timer(timekeeper, argv)
        time.sleep(1)
        save_timekeeper(timekeeper, True)
    
    tag = 'test2'
    for i in range(len(command_list)):
        timekeeper = load_timekeeper(True)
        print(f"\nTesting command {command_list[i]}")
        argv = [command_list[i], tag]
        timekeeper = timer(timekeeper, argv)
        time.sleep(1)
        save_timekeeper(timekeeper, True)
    
    timekeeper = timer(timekeeper, 'summarise')
    
def main():
    timekeeper = load_timekeeper()
    del sys.argv[0]
    timekeeper = timer(timekeeper, sys.argv)
    save_timekeeper(timekeeper)    

if __name__ == "__main__":
    main()

import click
import os,sys, pickle
from datetime import datetime, timedelta
import logging
from enum import Enum
# logging.basicConfig(level=logging.DEBUG)

class status(Enum):
    STARTED = '1'
    STOPPED = '2'
    PAUSED = '3'

def load_timekeeper():
    # import pdb; pdb.set_trace()
    if os.path.isfile(file_path()):
        logging.debug("File exists")
        with open(file_path(), 'rb') as file:
            timekeeper = pickle.load(file)
    else:
        logging.debug("File does not exist")
        timekeeper = {}
    return timekeeper

def file_path():
    today = datetime.today().strftime("%Y-%d-%m")
    path = os.path.join(os.path.dirname(__file__),'db') 
    if not os.path.isdir(path):
        os.makedirs(path)
    path = os.path.join(path,today + '.pkl')
    return path


@click.group()
@click.pass_context
def main(ctx):
    logging.debug('In main')
    # global timekeeper 
    timekeeper = load_timekeeper()
    ctx.obj = timekeeper
    # save_timekeeper(timekeeper)    

@main.command()
@click.argument('tag', type=str)
@click.pass_obj
def start(timekeeper, tag):
    """Starts a new timer for tag
    
    Arguments:
        tag {string} -- tag for the timer to be referenced with
    """
    logging.debug("In start")
    if tag in timekeeper.keys():
        print(f"Timer data for this tag already exists. Use 'timer resume {tag}' to resume timekeeping.")
    else:
        timekeeper[tag] = [status.STARTED, [datetime.today()]]
        print(f"Started timekeeping for {tag}")
        print(f"Curent time is {timekeeper[tag][1][-1].strftime('%H:%M')}")
        save_timekeeper(timekeeper)
    # return timekeeper
    # import pdb; pdb.set_trace()

@main.command()
@click.argument('tag', type=str)
@click.pass_obj
def tick(timekeeper, tag):
    """Tells the time the tag has been running for in the current session
    
    Arguments:
        tag {string} -- tag for which to get the time for 
    """
    logging.debug("In main")
    if timekeeper[tag][0] == status.STOPPED:
        print(f"Timer for {tag} is not running. Last run ran for {last2runs(timekeeper,tag)}.")
    elif timekeeper[tag][0] == status.STARTED:
        delta = datetime.today() - timekeeper[tag][1][-1]
        print(format_delta(delta))

@main.command()
@click.argument('tag', type=str)
@click.pass_obj
def stop(timekeeper, tag):
    if timekeeper[tag][0] == status.STOPPED:
        print(f"Timer for {tag} was already stopped at {format_time(timekeeper[tag][1][-1])}")
    else:
        timekeeper[tag][1].append(datetime.today())
        timekeeper[tag][0] = status.STOPPED
        print(f"{tag} stopped. Last run ran for {last2runs(timekeeper,tag)} ")
        save_timekeeper(timekeeper)

@main.command()
@click.argument('tag', type=str)
@click.pass_obj
def resume(timekeeper, tag):
    if timekeeper[tag][0] == status.STARTED:
        print(f"Timer for {tag} has been running since {format_time(timekeeper[tag][1][-1])}")
    else:
        print(f"Resumed timekeeping for {tag}. Last run ran for {last2runs(timekeeper,tag)} ")
        timekeeper[tag][1].append(datetime.today())
        timekeeper[tag][0] = status.STARTED
        save_timekeeper(timekeeper)

def save_timekeeper(timekeeper, test=False):
    # import pdb; pdb.set_trace()
    with open(file_path(), 'wb') as file:
        pickle.dump(timekeeper,file)
    logging.debug("File saved")

@main.command()
@click.argument('tag', type=str, default='')
@click.pass_obj
def summarise(timekeeper, tag):
    if tag == '':
        for _tag in timekeeper.keys():
            _summarise(timekeeper, _tag)
            print('\n')
    else:
        _summarise(timekeeper, tag)

def last2runs(timekeeper, tag):
    return format_delta(timekeeper[tag][1][-1] - timekeeper[tag][1][-2])

def format_time(time):
    return time.strftime('%H:%M')

def format_delta(delta):
    seconds = delta.total_seconds()
    return f"{int(seconds//3600)}h {int(seconds//60)}m {int(seconds%60)}s"

def _summarise(timekeeper, tag):
    print(f"Summary for {tag}")
    total_time = timedelta()
    timelist = timekeeper[tag][1]
    for i in range(len(timelist)//2):
        delta = timelist[2*i+1]-timelist[2*i]
        print(f"{i+1}. {format_time(timelist[2*i])} {format_delta(delta)}")
        total_time += delta
    if timekeeper[tag][0] == status.STARTED:
        delta = datetime.today()-timelist[-1]
        total_time += delta
        print(f"{len(timelist)//2+1}. {format_time(timelist[-1])} {format_delta(delta)} - running") 
    print(f"Total time spent - {format_delta(total_time)} ")
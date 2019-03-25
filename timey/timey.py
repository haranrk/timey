import click
import os,sys, pickle
from datetime import datetime, timedelta
import logging
from enum import Enum
# logging.basicConfig(level=logging.DEBUG)

class status(Enum):
    STARTED = '1'
    STOPPED = '2'

def load_timekeeper():
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
    timekeeper = load_timekeeper()
    ctx.obj = timekeeper    

@main.command()
@click.argument('tag', type=str)
@click.pass_obj
def start(timekeeper, tag):
    """Starts a new timer for tag
    
    Arguments:
        tag {string} -- tag for the timer to be referenced with
    """
    logging.debug("In start")
    timekeeper = _start(timekeeper, tag)
    save_timekeeper(timekeeper)

def _start(timekeeper, tag):
    if tag in timekeeper.keys():
        if timekeeper[tag][0] == status.STARTED:
            print(f"Timer for {tag} has been running since {format_time(timekeeper[tag][1][-1])}")
        else:
            print(f"New session for {tag}.\nLast run ran for {last2runs(timekeeper,tag)}.\nCurent time is {timekeeper[tag][1][-1].strftime('%H:%M')}.")
            timekeeper[tag][1].append(datetime.today())
            timekeeper[tag][0] = status.STARTED
            return timekeeper
    else:
        timekeeper[tag] = [status.STARTED, [datetime.today()]]
        print(f"New session for new tag: {tag}.")
        print(f"Curent time is {timekeeper[tag][1][-1].strftime('%H:%M')}.")
        return timekeeper

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
        print(f"{format_delta(delta)} elapsed.\nStarted at {format_time(timekeeper[tag][1][-1])}.")

@main.command()
@click.argument('tag', type=str, default='')
@click.pass_obj
def stop(timekeeper, tag):
    '''Stops the timer for a tag if provided or stops all running tags
    
    Arguments:
        tag {string} -- tag to stop
    '''

    if tag == '':
        for _tag in timekeeper.keys():
            if timekeeper[_tag][0] != status.STOPPED:
                timekeeper = _stop(timekeeper, _tag)
    else:
        timekeeper = _stop(timekeeper, tag)
    save_timekeeper(timekeeper)

def _stop(timekeeper, tag):
    if timekeeper[tag][0] == status.STOPPED:
        print(f"Timer for {tag} was already stopped at {format_time(timekeeper[tag][1][-1])}")
    else:
        timekeeper[tag][1].append(datetime.today())
        timekeeper[tag][0] = status.STOPPED
        print(f"Sessiong for {tag} stopped. Last run ran for {last2runs(timekeeper,tag)}.")
        return timekeeper

@main.command()
@click.argument('tag', type=str)
@click.pass_obj
def switch(timekeeper, tag):
    '''Stops timer for currently running tags and starts a new session for tag 
    
    Arguments:
        tag {string} -- tag to switch timer to
    '''
    for _tag in timekeeper.keys():
        if timekeeper[_tag][0] != status.STOPPED:
            timekeeper = _stop(timekeeper, _tag)
    timekeeper = _start(timekeeper,tag)
    save_timekeeper(timekeeper)

def save_timekeeper(timekeeper, test=False):
    with open(file_path(), 'wb') as file:
        pickle.dump(timekeeper,file)
    logging.debug("File saved")

@main.command()
@click.argument('tag', type=str, default='')
@click.pass_obj
def summarise(timekeeper, tag):
    '''Summarises session history for tag if provided or for all
    
    Arguments:
        tag {string} -- tag to summarise sessions for
    '''

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
    return f"{int(seconds//3600)}h {int(seconds%3600//60)}m {int(seconds%60)}s"

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
[![PyPI version](https://badge.fury.io/py/timey.svg)](https://badge.fury.io/py/timey)
# Timey
Timey is a simple cli timer that helps you keeep track of your life. It's written in python.

## Requirements
`Python` >= 3.6

## Installation
The package is uploaded on PyPi. Therefore, it can be installed with the following command
```bash
pip install timey
```

## Usage 
```
timey [command] [tag]
```
`command` can be any of the following:
1. `start` - Starts a new timer for `tag`.
1. `tick` - Outputs the how long the current session has been running for.
1. `stop` - Stops the timer.

1. `resume` - Starts a new session for `tag`.
1. `summarise` - Summarises all the sessions for `tag`. If tag is not specified, it summarises for all tags present in the current day's log.

`tag` can be any string.

The logs are stored on a day-by-day-basis.
The following is a sample usage of the app
```
$ timey start algo-hw
Started timekeeping for algo-hw
Curent time is 21:21
```
Two hours later
```
$ timey tick algo-hw
2h 0m 00s

$ timey stop algo-hw
algo-hw stopped. Last run ran for 2h 0m 00s

$ timey start gaming
Started timekeeping for gaming
Curent time is 21:21

$ timey summarise
Summary for algo-hw
1. 21:21 2h 0m 00s
Total time spent - 2h 0m 00s

Summary for gaming
1. 23:00 0h 0m 10s - running
Total time spent - 0h 0m 10s

```


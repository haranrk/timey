# Timekeeper
A timer for the terminal made using python. I use this to track how much time I spend on varius tasks. 

## Usage 
```bash
python timer.py [command] [tag]
```
`command` can be any of the following:
1. `start` - Starts a new timer for `tag`.
1. `tick` - Outputs the how long the current session has been running for.
1. `stop` - Stops the timer.

1. `resume` - Starts a new session for `tag`.
1. `summarise` - Summarises all the sessions for `tag`. If tag is not specified, it summarises for all tags present in the current day's log.

`tag` can be any string.

The logs are stored on a day-by-day-basis.

For convenience add this file to the path and create an alias to run it.

### Example usage
Assuming timer is an alias that invokes `timer.py`
```bash
$ timer start algo-hw
Started timekeeping for algo-hw
Curent time is 21:21
```
Two hours later
```bash
$ timer tick algo-hw
2h 0m 00s

$ timer stop algo-hw
algo-hw stopped. Last run ran for 2h 0m 00s

$ timer start gaming
Started timekeeping for gaming
Curent time is 21:21

$ timer summarise
Summary for algo-hw
1. 21:21 2h 0m 00s
Total time spent - 2h 0m 00s

Summary for gaming
1. 23:00 0h 0m 10s - running
Total time spent - 0h 0m 10s

```


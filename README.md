race
========================================================================
### Goal 
Check my skills to resolve task from Informatica Olympiad for the 6th class :)
The task's idea is to find optimal velocity mode with few constraints:
- velocity can be changed by 1 cell per minute (it can be both incremented or decremented)
- finish at the same point as start
- finish velocity must be zero (i.e. pre-last step velocity must 1 cell per minute)
- if there is a turn in the cell - the velocity must let the racer to accomplish current step in the cell (my apologies for messy explanation) 

### Usage
```bash
$ python ./race.py <track_name>
```

### Input
#### track_name
Symbolic name of track to be used for the race e.g. 'simple' or 'olympic'.
Usage hint will be printed if no track name specified.

### Output
Visualizes track, resulting time and velocity schema (i.e. 0123....).
```bash
____________ INIT _______________
1  1  1  1  1  1  1  1
1  0  0  0  0  0  0  1
1  0  0  0  0  0  0  1
1  0  0  0  0  0  0  1
1  0  0  1  1  1  1  1
1  0  0  1  0  0  0  0
1  0  0  1  0  0  0  0
1  0  0  1  0  0  0  0
1  1  1  1  0  0  0  0
__________________________________
We reached finish: (0, 0)
Racer 'Dummy' completed the track 'olympic' in 10 min. with path 012222332
```

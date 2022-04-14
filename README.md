# ezmonitor

## Summary

ezmonitor is a easy program for monitoring MEM and CPU Usage of some process and its chriden process.



## Software Requirements

+ Linux

+ Python >=2.7.10, <3.10  and  Python3 for recommend



## Installation

install from git repo:
```
pip install git+https://github.com/yodeng/ezmonitor.git
```

or just install from Pypi：

```
pip install ezmonitor
```

or install from anaconda repo:

```
conda install -c yodeng ezmonitor
```



## User Guide and Usage

#### 1).  monitor by process id

```
ezmntor [pid]
```

output：

+ sys.stdout logging
+ pid.log 
+ pid.pdf

#### 2). monitor by process name

if more then one process detected by process name, will exists.

```
ezmntor [processName]
```

output：

+ sys.stdout logging
+ pid.log 
+ pid.pdf

#### 3). monitor you command line

```
ezmntor [your command line]
```

output：

+ pid.log 
+ pid.pdf

#### 4). monitor by decorator

```python
from ezmonitor import ezmonitor

@ezmonitor.wrapper()
def youfunction(*args, **kwargs):
	pass
```

output：

+ sys.stdout logging
+ pid.log 
+ pid.pdf



## Demo

![demo](https://user-images.githubusercontent.com/18365846/163108252-0ffdd202-e989-4dfc-b8dc-b74a9a14f70d.svg)

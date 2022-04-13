#!/usr/bin/python
# coding:utf-8
'''Usage: 
    1. ezmntor [pid]
    2. ezmntor [processName]
    3. ezmntor [your command line]
'''

import sys
import os
import subprocess

from .src import *
from .utils import *
from .version import __version__


def main():
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        sys.exit(__doc__.strip()+"\nversion: %s" % __version__)
    h = ParseSingal()
    h.start()
    wd = os.getcwd()
    if len(sys.argv[1:]) > 1:
        cmd = sys.argv[1:]
        p = subprocess.Popen(cmd)
        pid = p.pid
        logfile = os.path.join(wd, "%d.log" % pid)
        m = ezmonitor(pid=pid, logfile=logfile)
        m.run()
        try:
            p.communicate()
        except:
            p.terminate()
    else:
        if sys.argv[1].isdigit():
            proc = psutil.Process(int(sys.argv[1]))
        else:
            procs = pgrep(sys.argv[1])
            if len(procs) > 1:
                sys.exit(
                    "more then one process [%s] match you process name: '%s'" % (procs, sys.argv[1]))
            elif len(procs) == 0:
                sys.exit("none process match you process name: '%s'" %
                         sys.argv[1])
            else:
                proc = psutil.Process(int(procs[0]))
        pid = proc.pid
        logfile = os.path.join(wd, "%d.log" % pid)
        m = ezmonitor(pid=pid, logfile=logfile, verbose=True)
        m.run()
        proc.wait()
    m.plot(os.path.join(os.getcwd(), "%d.pdf" % pid),
           "Monitor Resource for pid: %d" % pid)


if __name__ == "__main__":
    main()

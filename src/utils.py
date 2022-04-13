import os
import sys
import math
import time
import signal
import logging

from threading import Thread


class ParseSingal(Thread):
    def __init__(self):
        super(ParseSingal, self).__init__()
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def run(self):
        time.sleep(1)

    def signal_handler(self, signum, frame):
        os._exit(signum)
        # sys.exit(signum)


def pgrep(name):
    pids = []
    if name:
        with os.popen("pgrep %s" % name) as fi:
            pids = fi.read().split()
    return pids


def log_wrapper(logfile=None, level="info", name=None):
    logger = logging.getLogger(name)
    if level.lower() == "info":
        logger.setLevel(logging.INFO)
    elif level.lower() == "debug":
        logger.setLevel(logging.DEBUG)
    f = logging.Formatter('')
    if logfile is None:
        h = logging.StreamHandler(sys.stdout)  # default: sys.stderr
        f = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s')
    else:
        h = logging.FileHandler(logfile, mode='w')
    h.setFormatter(f)
    logger.addHandler(h)
    return logger


def Gsize(size):
    return round(size/1024.0/1024/1024, 3)


def getProgm(cmd):
    args = cmd.split()
    if len(args) < 2:
        return
    if args[0].endswith("java"):
        for i in args[1:]:
            if i.endswith(".jar"):
                return os.path.basename(i)
    elif os.path.basename(args[0]) in ["python", "python2", "python3"] or args[0].endswith("perl") or args[0].endswith("Rscript"):
        for i in args[1:]:
            if not i.startswith("-"):
                return os.path.basename(i)

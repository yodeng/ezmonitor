# coding:utf-8

import os
import time
import psutil
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from threading import Thread
from collections import OrderedDict

from .utils import *


class ezmonitor(object):

    cpu_tick = 0.3

    def __init__(self, ivs=None, pid=os.getpid(), logfile=None, verbose=False):
        if ivs:
            self.cpu_tick = ivs
        self.pid = pid
        self.logfile = logfile
        self.verbose = verbose

    @classmethod
    def wrapper(cls, tick=0):
        if not tick:
            tick = cls.cpu_tick

        def outer_wrapper(func):
            def inner_wrapper(*args, **kwargs):
                if float(tick) > 0:
                    t = Thread(target=cls._record,
                               args=(os.getpid(), tick, None, False))
                    t.setDaemon(True)
                    t.start()
                return func(*args, **kwargs)
            return inner_wrapper
        return outer_wrapper

    @staticmethod
    def _record(pid=os.getpid(), ivs=1, logfile=None, verbose=False):
        ps = psutil.Process(pid)
        log = log_wrapper(logfile=logfile, name="em1")
        log.info("#TIME\tRSS(GB)\tSHR(GB)\tCPU(n)\tPNAME")
        if verbose:
            log2 = log_wrapper(name="em2")
        while True:
            info = []
            pmem = {}
            rss = rsh = cpu = 0
            try:
                pcs = ps.children(recursive=True)
            except:
                time.sleep(0.2)
                continue
            for p in pcs:
                try:
                    cpu += p.cpu_percent(interval=ivs)
                    m = p.memory_info()
                    rss += m.rss
                    rsh += m.shared
                    # if m.rss >> 20 > 50:  # only record rss more then 50MB
                    pmem[p.name()] = (m.rss, " ".join(p.cmdline()))
                except:
                    continue
            try:
                cpu += ps.cpu_percent(interval=ivs)
                m = ps.memory_info()
                rss += m.rss
                rsh += m.shared
                # if m.rss >> 20 > 50:  # only record rss more then 50MB
                pmem[ps.name()] = (m.rss, " ".join(ps.cmdline()))
            except:
                pass
            time_ = datetime.datetime.today().strftime("%F %X")
            if len(pmem):
                name, mc = sorted(pmem.items(), key=lambda x: x[1])[-1]
                cmd = mc[1]
                pgm = getProgm(cmd)
                if pgm:
                    if pgm == os.path.basename(sys.argv[0]):
                        time.sleep(0.2)
                        continue
                    name = pgm
                info = [time_, Gsize(rss), Gsize(rsh), round(cpu/100, 3), name]
                log.info("\t".join(map(str, info)))
                if verbose:
                    log2.info("%s(GB), %s(GB) %s(cpu) %s",
                              info[1], info[2], info[3], name)

    def run(self):
        t = Thread(target=self._record, args=(
            self.pid, self.cpu_tick, self.logfile, self.verbose))
        t.setDaemon(True)
        t.start()

    def plot(self, outfile=None, title="Monitor Resource"):
        df = pd.read_csv(self.logfile, header=0, sep="\t", names=[
                         "time", "rss", "rsh", "cpu", "name"], index_col=False)
        group = df.groupby(["time"])
        df = group.agg({"rss": np.mean, "rsh": np.mean,
                       "cpu": np.mean, "name": lambda x: x.mode()[0]})
        df["time"] = df.index
        # df["time"] = pd.to_datetime(df['time']).map(lambda x:x.time())
        df["time"] = pd.to_datetime(df['time'])
        timeline = df["time"]
        time_ = []
        t0 = df["time"][0]
        for t in df["time"][:]:
            time_.append(int((t-t0).total_seconds()))
        df["time"] = time_
        name = OrderedDict()
        cn_ = ""
        for i, n in enumerate(df.name):
            if n != cn_:
                name[time_[i]] = n
            cn_ = n
        if time_[i] not in name:
            name[time_[i]] = ""
        ax = df.plot(x="time", secondary_y=[
                     "rss", "rsh"], linewidth=0.3, fontsize=10, mark_right=False)
        ax.set_title(title)
        ax.set_ylabel('Cpu (n)')
        ax.legend(loc=2, fontsize=8)
        ax.right_ax.legend(loc=1, fontsize=8)
        ax.set_xlabel('Timeline')
        ax.grid(linestyle="--", alpha=0.3)
        ax.right_ax.set_ylabel('Mem (GB)')
        ax.set_xticks(ticks=[df.time[0], df.time[len(df.time)-1]])
        ax.set_xticklabels(
            [timeline[0].time(), timeline[len(df.time)-1].time()], rotation=45, fontsize=10)
        y1, y2 = ax.get_ylim()
        y1_, y2_ = ax.right_ax.get_ylim()
        y1 = min(y1, y1_)
        y2 = max(y2, y2_)
        if len(name) > 2:
            nm = list(name.keys())
            for n, i in enumerate(nm[:-1]):
                if n % 2:
                    plt.fill_between([nm[n], nm[n+1]], y1, y2,
                                     facecolor='gray', alpha=0.3)
                else:
                    plt.fill_between([nm[n], nm[n+1]], y1, y2,
                                     facecolor='gray', alpha=0.1)
        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xticks(ticks=list(name.keys()))
        ax2.set_xticklabels(list(name.values()), rotation=45, fontsize=10)
        plt.tick_params(top=False, which="minor", length=1)
        plt.subplots_adjust(left=0.1, right=1.5, top=1.4, bottom=0.25)
        plt.savefig(outfile, format="pdf", bbox_inches='tight')
        plt.figure(figsize=(20, 20))
        plt.show()

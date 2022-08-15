import os
import sys
import time
import shutil
import string
import shutil
import logging
import argparse
import subprocess

from hget import hget

from ._version import __version__


class Utils(object):

    cmds = []

    def call(self, cmd, run=True, verbose=False, shell=True):
        if not shell:
            cmd_string = " ".join(cmd)
        else:
            cmd_string = cmd
        self.__class__.cmds.append(cmd_string.strip())
        if not run:
            if verbose:
                print(cmd_string)
            return
        if verbose:
            subprocess.check_call(cmd, shell=shell, stdout=sys.stdout,
                                  stderr=sys.stderr)
        else:
            with open(os.devnull, "w") as fo:
                subprocess.check_call(cmd, shell=shell, stdout=fo, stderr=fo)

    def mkdirs(self, *path):
        for p in path:
            if not os.path.isdir(p):
                os.makedirs(p)

    def rmpath(self, *path):
        for p in path:
            if os.path.isdir(p):
                shutil.rmtree(p)
            elif os.path.isfile(p):
                os.remove(p)

    def writecmd(self):
        with open(os.path.join(self.workdir, "cmd.sh"), "w") as fo:
            for cmd in self.cmds:
                fo.write(cmd + "\n")

    def uncompress(self, filename, outdir, verbose=True):
        args = "-xf"
        un_dir = os.path.join(
            outdir, os.path.basename(filename).split(".tar.")[0])
        if filename.endswith("bz2"):
            args = "-j" + args[1:]
        if verbose:
            args += "v"
        if os.path.isdir(un_dir):
            keep = False
            for f in os.listdir(un_dir):
                if os.path.islink(os.path.join(un_dir, f)):
                    os.unlink(os.path.join(un_dir, f))
                elif os.path.isdir(os.path.join(un_dir, f)):
                    shutil.rmtree(os.path.join(un_dir, f))
                elif f.endswith(".bz2") or f.endswith(".gz") or f.endswith(".ht"):
                    keep = True
                else:
                    os.remove(os.path.join(un_dir, f))
            if not keep:
                shutil.rmtree(un_dir)
        self.call(["tar", args, filename, "-C", outdir],
                  shell=False, verbose=verbose)


gcc_version = [
    'gcc-10.1.0', 'gcc-10.2.0', 'gcc-10.3.0', 'gcc-10.4.0', 'gcc-11.1.0',
    'gcc-11.2.0', 'gcc-11.3.0', 'gcc-12.1.0', 'gcc-5.1.0', 'gcc-5.2.0',
    'gcc-5.3.0', 'gcc-5.4.0', 'gcc-5.5.0', 'gcc-6.1.0', 'gcc-6.2.0',
    'gcc-6.3.0', 'gcc-6.4.0', 'gcc-6.5.0', 'gcc-7.1.0', 'gcc-7.2.0',
    'gcc-7.3.0', 'gcc-7.4.0', 'gcc-7.5.0', 'gcc-8.1.0', 'gcc-8.2.0',
    'gcc-8.3.0', 'gcc-8.4.0', 'gcc-8.5.0', 'gcc-9.1.0', 'gcc-9.2.0',
    'gcc-9.3.0', 'gcc-9.4.0', 'gcc-9.5.0'
]

gcc_base_url = 'https://mirrors.tuna.tsinghua.edu.cn/gnu/gcc/'


def loger(logfile=None, level="info"):
    logger = logging.getLogger()
    if level.lower() == "info":
        logger.setLevel(logging.INFO)
        f = logging.Formatter(
            '[%(levelname)s %(asctime)s] %(message)s')
    elif level.lower() == "debug":
        logger.setLevel(logging.DEBUG)
        f = logging.Formatter(
            '[%(levelname)s %(threadName)s %(asctime)s %(funcName)s(%(lineno)d)] %(message)s')
    if logfile is None:
        h = logging.StreamHandler(sys.stdout)
    else:
        h = logging.FileHandler(logfile, mode='w')
    h.setFormatter(f)
    logger.addHandler(h)
    return logger


desc = '''
build and install gcc/c++/g++ version in rootless.

support gcc version: 
    ['gcc-10.1.0', 'gcc-10.2.0', 'gcc-10.3.0', 'gcc-10.4.0', 'gcc-11.1.0',
     'gcc-11.2.0', 'gcc-11.3.0', 'gcc-12.1.0', 'gcc-5.1.0', 'gcc-5.2.0',
     'gcc-5.3.0', 'gcc-5.4.0', 'gcc-5.5.0', 'gcc-6.1.0', 'gcc-6.2.0',
     'gcc-6.3.0', 'gcc-6.4.0', 'gcc-6.5.0', 'gcc-7.1.0', 'gcc-7.2.0',
     'gcc-7.3.0', 'gcc-7.4.0', 'gcc-7.5.0', 'gcc-8.1.0', 'gcc-8.2.0',
     'gcc-8.3.0', 'gcc-8.4.0', 'gcc-8.5.0', 'gcc-9.1.0', 'gcc-9.2.0',
     'gcc-9.3.0', 'gcc-9.4.0', 'gcc-9.5.0']
'''


def parseArg():
    parser = argparse.ArgumentParser(
        description=desc.strip())
    parser.add_argument("-g", "--gcc", required=True,
                        help="which gcc version to install", metavar="<str>")
    parser.add_argument("-d", "--download-dir", required=True,
                        help="download directory for all gcc packages", metavar="<str>")
    parser.add_argument("-i", "--install-dir", required=True,
                        help="install directory", metavar="<str>")
    parser.add_argument("-t", "--threads", default=10, type=int,
                        help="threads number of build gcc, 10 by default", metavar="<int>")
    parser.add_argument('-v', '--version',
                        action='version', version="v" + __version__)
    return parser.parse_args()

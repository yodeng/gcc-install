#!/usr/bin/env python
'''
Usage:
    gcc-install [-h] -g <str> -d <str> -i <str> [-v]

allowed gcc_version:
    ['gcc-5.1.0', 'gcc-5.2.0', 'gcc-5.3.0', 'gcc-5.4.0', 'gcc-5.5.0',
     'gcc-6.1.0', 'gcc-6.2.0', 'gcc-6.3.0', 'gcc-6.4.0', 'gcc-6.5.0',
     'gcc-7.1.0', 'gcc-7.2.0', 'gcc-7.3.0', 'gcc-7.4.0', 'gcc-7.5.0',
     'gcc-8.1.0', 'gcc-8.2.0', 'gcc-8.3.0', 'gcc-8.4.0', 'gcc-8.5.0',
     'gcc-9.1.0', 'gcc-9.2.0', 'gcc-9.3.0', 'gcc-9.4.0', 'gcc-9.5.0'
     'gcc-10.1.0', 'gcc-10.2.0', 'gcc-10.3.0', 'gcc-10.4.0',
     'gcc-11.1.0', 'gcc-11.2.0', 'gcc-11.3.0',
     'gcc-12.1.0']
'''

import os
import sys

from .src import *


def main():
    args = parseArg()
    log = loger()
    version = args.gcc
    download_dir = args.download_dir
    install_dir = args.install_dir
    gc = BuildGCC(version, download_dir)
    log.info(
        "starting download %s and all dependancy", version)
    gc.download_gcc()
    log.info("download %s success", version)
    time.sleep(3)
    log.info("starting build %s", version)
    gc.build(install_dir)
    log.info("install %s success: %s", version, install_dir)


if __name__ == "__main__":
    main()

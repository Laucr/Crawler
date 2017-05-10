# -*- coding:utf-8 -*-
# author : stalker_
# 05-04-17

import time
import json
import os

DEBUG_MODE = True


def print_msg(*kw):
    if DEBUG_MODE:
        print time.asctime(time.localtime(time.time())), [k for k in kw]
    elif isinstance(kw[0], Exception):
        print time.asctime(time.localtime(time.time())), kw
    else:
        pass


def load_log(log_dir):
    log = open(os.path.abspath(log_dir))
    raw_data = log.readlines()
    targets = [json.loads(i) for i in raw_data]
    log.close()
    return targets

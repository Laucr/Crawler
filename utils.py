# -*- coding:utf-8 -*-
# author : stalker_
# 05-04-17

import time

DEBUG_MODE = True


def print_msg(*kw):
    if DEBUG_MODE:
        print time.asctime(time.localtime(time.time())), [k for k in kw]
    elif isinstance(kw[0], Exception):
        print time.asctime(time.localtime(time.time())), kw
    else:
        pass

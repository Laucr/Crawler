# -*- coding:utf-8 -*-
# author : stalker_
# 04-25-17

import json
import os

BOARDS = [
    "Canon",
    "Fuji_Xerox",
    "Konica_Minolta",
    "Kyocera",
    "Ricoh",
    "Sharp",
    "Toshiba"
]
LOG_DIR = os.path.abspath('./printers')

targets = {}

for board in BOARDS:
    log = open(os.path.join(LOG_DIR, board) + '.log')
    raw_data = log.readlines()
    targets[board] = [json.loads(i) for i in raw_data]
    log.close()

# total = reduce(lambda x, y: x + y, [len(targets[i]) for i in targets])
# print total

for board in targets:
    port_count = {}
    for item in targets[board]:
        if item["port"] not in port_count:
            port_count[item["port"]] = 1
        else:
            port_count[item["port"]] += 1

    print board
    for port in port_count:
        print "port:", port, port_count[port]

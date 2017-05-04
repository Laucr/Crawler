# -*- coding:utf-8 -*-
# author : stalker_
# 04-25-17

import json

import collect

eye = collect.ZoomEyeAPI()
res = eye.search('Toshiba device:"printer"')
# res = eye.search('fuji xerox device:"printer"')
# res = eye.search('Sharp device:"printer"')
# res = eye.search('RICOH device:"printer"')
# res = eye.search('Canon device:"printer"')
# res = eye.search('Konica Minolta device:"printer"')
# res = eye.search('Kyocera device:"printer"')
toshiba = open("Toshiba.log", 'w')
for item in res:
    print item
    toshiba.write(json.dumps(item))
    toshiba.write('\n')
toshiba.close()
eye.resources_info()

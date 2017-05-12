import utils

# targets = utils.load_log("../targets/Canon.log")
# cn_spoor = [{"ip": t["ip"], "port": t["port"]} for t in targets if t["country"] == "China"]
#
# vul = 0
# for spoor in cn_spoor:
#     instance = canon.Canon(spoor["ip"], spoor["port"])
#     try:
#         if instance.execute():
#             vul += 1
#     except Exception, e:
#         utils.print_msg(e)
#     del instance
#
# utils.print_msg("Total:", len(cn_spoor), "Vulnerable:", vul)
#
# k = konica.Konica("131.247.15.116")
# try:
#     k.ping()
#     if k.alive:
#         k.req_login()
# except Exception, e:
#     utils.print_msg(e)

import beastie
import os
import json

canon = utils.load_log("../targets/Canon.log")
fuji = utils.load_log("../targets/Fuji_Xerox.log")
konica = utils.load_log("../targets/Konica_Minolta.log")
kyocera = utils.load_log("../targets/Kyocera.log")
ricoh = utils.load_log("../targets/Ricoh.log")
sharp = utils.load_log("../targets/Sharp.log")
toshiba = utils.load_log("../targets/Toshiba.log")

spoors = {"canon": canon,
          "fuji": fuji,
          "konica": konica,
          "kyocera": kyocera,
          "ricoh": ricoh,
          "sharp": sharp,
          "toshiba": toshiba}

for spoor in spoors:

    alive_spoor = open(os.path.join("../targets/",  spoor + ".alive"), 'w')
    for _item in spoors[spoor]:
        spoor_instance = beastie.BasePrinter(_item["ip"], _item["port"], ".")
        try:
            spoor_instance.ping()
            if spoor_instance.alive:
                alive_spoor.write(json.dumps(_item))
                alive_spoor.write("\n")
        except Exception, e:
            utils.print_msg(e)

    alive_spoor.close()


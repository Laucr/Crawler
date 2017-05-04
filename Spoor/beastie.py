# -*- coding:utf-8 -*-
# author : stalker_
# 05-04-17
import requests

from utils import print_msg


class BasePrinter:
    """
    :param ip: target ip address
    :type ip: str
    :param port: target port
    :type port: int
    :param den: dir where to save data
    :type den: str
    """

    def __init__(self, ip, port, den):
        self.ip = ip
        self.port = port
        self.nest = den

    """
    :return status code of pinging target
    :except http errors
    """

    def ping(self):
        try:
            probe = requests.get("http//" + self.ip + str(self.port), verify=False)
            return probe.status_code
        except Exception, e:
            print_msg(e)

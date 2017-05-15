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
    def __init__(self, ip, port, den="."):
        self.ip = ip
        self.port = port
        self.den = den
        self.alive = True

    """
    :return status code of pinging target
    :except http errors
    """

    def ping(self):
        try:
            if self.port != 80:
                req_port = requests.get("http://" + self.ip + ":" + str(self.port), verify=False)
                if req_port.status_code != 200 and req_port.status_code != 302:
                    req_80 = requests.get("http://" + self.ip + ":" + str(80), verify=False)
                    if req_80.status_code != 200 and req_80.status_code != 302:
                        self.alive = False
                        raise TargetDownException
                    else:
                        self.port = 80

            else:
                req_port = requests.get("http://" + self.ip + ":" + str(self.port), verify=False)
                if req_port.status_code != 200 and req_port.status_code != 302:
                    self.alive = False
                    raise TargetDownException

        except Exception, e:
            print_msg(e)

    @staticmethod
    def test_exist(res):
        """
        :param res: response of func:requests.get/request.post
        :type res: requests.Response
        """
        if res.status_code == 404:
            raise PageNotFoundError


class LoginError(Exception):
    def __str__(self):
        return repr("Printer Login Failed.")

    def __init__(self):
        Exception.__init__(self)


class PageNotFoundError(Exception):
    def __str__(self):
        return repr("Requested page returns 404 not found.")

    def __init__(self):
        Exception.__init__(self)


class VersionError(Exception):
    def __str__(self):
        return repr("Konica version error.")

    def __init__(self):
        Exception.__init__(self)


class TargetDownException(Exception):
    def __str__(self):
        return repr("Target is not alive.")

    def __init__(self):
        Exception.__init__(self)
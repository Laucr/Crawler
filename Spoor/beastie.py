# -*- coding:utf-8 -*-
# author : stalker_
# 05-04-17

import requests
from utils import print_msg
from requests import ConnectionError


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

    @staticmethod
    def req_port(ip_addr, port):
        try:
            ret_code = requests.get("http://" + ip_addr + ":" + str(port), verify=False, timeout=30).status_code
            if ret_code != 200 and ret_code != 302:
                return False
            else:
                return True
        except ConnectionError:
            return False

    @staticmethod
    def req_default(ip_addr):
        try:
            ret_code = requests.get("http://" + ip_addr, verify=False, timeout=30).status_code
            if ret_code != 200 and ret_code != 302:
                return False
            else:
                return True
        except ConnectionError, e:
            print_msg(e)
            return False

    def ping(self):
        if self.port != 80 and self.port != 443:
            self.alive = self.req_default(self.ip)
            if not self.alive:
                self.alive = self.req_port(self.ip, self.port)
            else:
                self.port = 80
        else:
            self.alive = self.req_default(self.ip)
            if self.alive:
                self.port = 80

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
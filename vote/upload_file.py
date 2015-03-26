# coding=utf-8
import os
import time
import json
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


class FileOperation(object):
    def __init__(self, file_content, dir_name="/", file_name=None, bucket_name="vote1"):
        self._file_content = file_content
        if not file_name:
            self._file_name = self._file_content.name
        else:
            self._file_name = file_name
        self._bucket_name = bucket_name
        self._dir_name = dir_name
        self._new_name = str(int(time.time())) + self._file_name
        self._upload_url = "https://v0.api.upyun.com/" + self._bucket_name \
                           + self._dir_name + self._new_name
        self._file_url = "http://" + self._bucket_name + ".b0.upaiyun.com" + self._dir_name + self._new_name

    def save(self): 
        header = {"Mkdir": "true"}
        r = requests.put(self._upload_url, data=self._file_content, auth=('***', '***'), headers=header)
        print r.content, r.status_code
        return {"state": "SUCCESS", "type": "jpg", "original": self._file_name,
                "title": self._new_name, "url": self._file_url, "size": 1000}

    def get_storage_path(self):
        return self._dir_name + self._new_name

    def get_file_url(self):
        return self._file_url

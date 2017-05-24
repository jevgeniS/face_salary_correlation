import httplib
import json
import urllib

import time
import requests


class QuotaExceededException(Exception):
    pass

class FaceApiClient(object):

    def __init__(self):
        self.BASE_URL = "https://westus.api.cognitive.microsoft.com"

    def detect_by_file(self, stream):
        headers=self.get_headers()
        headers['Content-Type']= 'application/octet-stream'
        params=self.get_params()
        response = requests.post(self.BASE_URL+"/face/v1.0/detect?%s" % params, data=stream, headers=headers)
        try:
            return self.handle_response(response)
        except QuotaExceededException:
            time.sleep(65)
            return self.detect_by_file(stream)

    def detect(self, img_url):
        headers = self.get_headers()
        headers['Content-Type'] = 'application/json'
        params = self.get_params()
        body="{\"url\":\""+img_url+"\"}"
        response = requests.post(self.BASE_URL + "/face/v1.0/detect?%s" % params, data=body, headers=headers)
        try:
            return self.handle_response(response)
        except QuotaExceededException:
            time.sleep(65)
            return self.detect(img_url)


    def handle_response(self, response):
        status_code = response.status_code
        data = response.json()

        if status_code == 200:
            return data

        if status_code == 429:
            raise QuotaExceededException()

        if status_code == 400:
            return None

        raise Exception(data)

    def get_params(self):
        return urllib.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'true',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion',
        })

    def get_headers(self):
        return \
            {
                'Ocp-Apim-Subscription-Key': '02cbbefe77434ac096fd699fe7b55854',
            }

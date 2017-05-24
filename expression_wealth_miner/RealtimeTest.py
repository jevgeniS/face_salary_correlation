import cv2
import sys

from Analyzer import Analyzer
from face_api.DataParser import DataParser
from face_api.face_api_client import FaceApiClient


class RealtimeTest(object):


    def run_test(self):
        clf=Analyzer().create_clf(regen_pred_model=False)
        client = FaceApiClient()
        parser = DataParser()

        while True:
            raw_input("Press Enter to estimate your salary :)")

            img_path=self.create_photo()
            stream = open(img_path, 'rb')
            try:
                response = client.detect_by_file(stream)
            finally:
                stream.close()
            features = parser.parse_response_to_df(response, None)
            answer = clf.predict(features)
            print answer






    def create_photo(self):
        img_name='face.png'
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()

        img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
        cv2.imwrite(img_name, img)
        cv2.imshow('image', img)
        cap.release()
        cv2.destroyAllWindows()
        return img_name
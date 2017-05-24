import numpy as np
import pandas as pd
from processing.columns_selector import get_columns
class FeatureGenerator(object):
    def generate(self):

        step =0.1
        frame = pd.DataFrame()
        t=int(1/step)

        for i in range(0, t+1):
            for ii in range(0, t+1-i):
                iii=t-i-ii
                row = pd.DataFrame(columns=get_columns())
                 # with 0s rather than NaNs
                row['faceAttributes.emotion.contempt']=pd.Series([i/float(t)])
                row['faceAttributes.emotion.happiness']=pd.Series([ii/float(t)])
                row['faceAttributes.emotion.neutral']=pd.Series([iii/float(t)])
                row = row.fillna(0)
                frame = pd.concat([frame, row])

        return frame


    def generate_2f(self):

        step =0.01
        frame = pd.DataFrame()
        t=int(1/step)

        for i in range(0, t+1):
            ii=t-i
            row = pd.DataFrame(columns=get_columns())
             # with 0s rather than NaNs
            row['faceAttributes.emotion.neutral']=pd.Series([i/float(t)])
            row['faceAttributes.emotion.happiness']=pd.Series([ii/float(t)])
            #row['faceAttributes.emotion.neutral']=pd.Series([iii/float(t)])
            row = row.fillna(0)
            frame = pd.concat([frame, row])

        return frame

    def generate_1f(self):

        step =0.01
        frame = pd.DataFrame()
        t=int(1/step)

        for i in range(0, t+1):
            row = pd.DataFrame(columns=get_columns())
             # with 0s rather than NaNs
            row['faceAttributes.emotion.happiness']=pd.Series([i/float(t)])
            #row['faceAttributes.emotion.happiness']=pd.Series([ii/float(t)])
            #row['faceAttributes.emotion.neutral']=pd.Series([iii/float(t)])
            row = row.fillna(0)
            frame = pd.concat([frame, row])

        return frame
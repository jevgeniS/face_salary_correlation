from pandas.io.json import json_normalize

import pandas as pd

class DataParser(object):

    def parse_response_to_df(self, response, country):
        if response is not None and len(response) > 0:
            faces = pd.DataFrame()
            for f in response:
                face = json_normalize(f)
                face['country'] = country
                faces = pd.concat([faces, face])

            return faces
        return None

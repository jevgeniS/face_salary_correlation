import os

import pandas as pd


class DataRequester(object):

    def read_faces_from_urls(self):
        input_fname = r"..\img urls_v2.txt"
        output_file = r"face_features_v2.csv"

        with open(input_fname) as f:
            content = f.readlines()

        for i, row in enumerate(content):
            if row == None or row == "\n":
                break

            d = row.split("_")
            salary = int(d[0][1:].replace(" ", ""))
            country = d[1]
            img_url = d[2]

            faces = self.request(img_url, country, salary)
            if faces!=None:

                lines = open(input_fname).readlines()
                lines = [l for l in lines if l != row]
                if os.path.isfile(output_file):
                    existing_faces = pd.read_csv(output_file, sep=';')
                else:
                    existing_faces = pd.DataFrame()
                new_faces = pd.concat([existing_faces, faces])
                pd.DataFrame.to_csv(new_faces, output_file, sep=';', index=False)
                open(input_fname, 'w').writelines(lines)


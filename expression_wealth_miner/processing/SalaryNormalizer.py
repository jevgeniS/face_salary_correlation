import pandas as pd
class SalaryNormalizer(object):
    def __init__(self):
        self.ranks = pd.read_csv("nyc_index.csv", sep=';')
    def map(self, country, salary):
        if country== 'Haiti' or country == 'Papua New Guinea':
            return 0
        for index, row in self.ranks.iterrows():

            if row['Country']==country:
                cost_index = float(row['Cost of Living Index'])/100
                return salary/cost_index

        raise Exception('Salary index mapping not found for '+country)

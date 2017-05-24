import pandas as pd

from ml.Classifier import Classifier
from ml.FeatureGenerator import FeatureGenerator
from processing.DataRequester import DataRequester
from processing.SalaryNormalizer import SalaryNormalizer
from processing.columns_selector import get_columns
import matplotlib.pyplot as plt
import numpy as np
import pickle

class Analyzer(object):

    def prepare_train_data(self):
        raw_data = pd.read_csv("face_features_v2.csv", sep=';')
        return self.prepare_data(raw_data)

    def prepare_data(self, raw_data):
        norm_salaries = []
        norm_salaries_per_family = []
        normalizer = SalaryNormalizer()
        errors = set()
        error_faces = 0
        for index, row in raw_data.iterrows():
            try:
                norm_salary = normalizer.map(row['country'], row['salary'])
                number_of_faces = len(raw_data[raw_data['img_url'] == (row['img_url'])])
                norm_salaries_per_family.append(norm_salary)
                norm_salaries.append(norm_salary / number_of_faces)
            except Exception:
                errors.add(row['country'])
                error_faces += 1
        print "Faces with errors ("+str(error_faces)+"):"+str(errors)
        raw_data['norm_salary'] = norm_salaries
        raw_data['norm_salaries_per_family']=norm_salaries_per_family
        data = raw_data[raw_data['norm_salary'] > 0]
        print "Face samples read: "+str(len(data))
        return data


    def store_pred_model(self, cls):
        filename = 'pred_model.sav'
        pickle.dump(cls, open(filename, 'wb'))

    def load_pred_model(self):
        filename = 'pred_model.sav'
        return pickle.load(open(filename, 'rb'))

    def create_clf(self, regen_pred_model=True):

        if regen_pred_model:
            data = self.prepare_train_data()
            clf = Classifier()
            clf.train(data)
            self.store_pred_model(clf)
        else:
            clf = Classifier(self.load_pred_model())
        return clf


    def generate_features_and_test(self, clf):
        gen_data = FeatureGenerator().generate()
        gen_data_predictions = clf.predict(gen_data)
        gen_data['predicted_salary'] = gen_data_predictions
        self.plot(gen_data)

    def plot_salaries_distribution(self, salaries):
        from scipy.stats import gaussian_kde
        data = salaries
        density = gaussian_kde(data)
        xs = np.linspace(0, max(salaries), 200)
        density.covariance_factor = lambda: .25
        density._compute_covariance()
        plt.plot(xs, density(xs))
        plt.show()

    def plot(self, data):

        width = 0.80  # the width of the bars: can also be len(x) sequence
        data=data.sort(['predicted_salary'])
        ind = range(len(data))
        happiness=data["faceAttributes.emotion.happiness"].tolist()
        neutral=data["faceAttributes.emotion.neutral"].tolist()
        contempt=data["faceAttributes.emotion.contempt"].tolist()
        p1 = plt.bar(ind, happiness, width, color='#64e572',  alpha=0.4, linewidth=0)
        p2 = plt.bar(ind, neutral, width, color='#ff9655', bottom=happiness, alpha=0.4, linewidth=0)

        p3 = plt.bar(ind, contempt, width, color='#FFCC00', bottom=np.array(neutral)+np.array(happiness), alpha=0.4, linewidth=0)

        salaries=data['predicted_salary']
        max_salary=max(salaries)
        salaries = [s/float(max_salary) for s in salaries]
        p4=plt.plot(ind, salaries, aa=True)

        plt.ylabel('Emotion proportions')
        plt.title('Correlation between emotions and monthly income')
        plt.legend((p1[0], p2[0], p3[0], p4[0]), ('Happiness','Neutral','Contempt','Monthly income'), loc='lower right')

        plt.show()
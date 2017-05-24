from sklearn import svm, preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

from processing.columns_selector import get_columns


class Classifier(object):
    def __init__(self, clf=None):
        self.clf = clf

    def train_clf(self, training_data, targets):
        cls = RandomForestRegressor(n_estimators=100)
        # cls = DecisionTreeClassifier()

        cls.fit(training_data, targets)

        return cls

    def cross_validate(self, training_data, targets):
        chunks = 5
        chunk_size = len(training_data) / chunks
        errors = []
        for i in range(chunks):
            test_data_start = chunk_size * i
            test_data_end = test_data_start + chunk_size
            test_data = training_data[test_data_start:test_data_end]
            tra_data1 = training_data[:test_data_start]
            tra_data2 = training_data[test_data_end:]
            training_targets = pd.concat([targets[:test_data_start], targets[test_data_end:]])
            test_targets = targets[test_data_start:test_data_end]
            #cls = svm.SVR(kernel='rbf')
            cls= RandomForestRegressor(n_estimators=100, random_state=1)
            # cls = DecisionTreeClassifier()

            cls.fit(pd.concat([tra_data1, tra_data2]), training_targets)
            predicted_salaries = cls.predict(test_data)
            for i, ps in enumerate(predicted_salaries):
                errors.append(abs(test_targets.values[i] - ps))

        error = str(sum(errors) / float(len(errors)))
        print "Avg error is " + error


    def train(self, data):
        columns = get_columns()

        salaries = data["norm_salary"]
        features = data[columns]



        self.clf=self.train_clf(features, salaries)

        for i, e in enumerate(list(features)):
            print e +":"+ str(self.clf.feature_importances_[i])

        self.cross_validate(features, salaries)
        return self.clf

    def predict(self, test_data):
        columns = get_columns()
        features = test_data[columns]
        return self.clf.predict(features)

    def translate_features(self, features):
        str_columns = list(features.select_dtypes(include=['object']).columns)
        for c in str_columns:
            le = preprocessing.LabelEncoder()
            le.fit(features[c])

            features[c] = le.transform(features[c])

        return features
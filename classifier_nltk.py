#%%

import pandas as pd
import numpy as np
import string
from sklearn.feature_extraction.text import CountVectorizer
import ast
from sklearn.svm import SVC
import nltk
import scraper
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

#%%

df1 = pd.read_csv('datasets/completed_all_cleaned.csv')
df2 = pd.read_csv('datasets/received_all_cleaned.csv')
df = pd.concat([df1, df2]).reset_index(drop=True)

import pandas as pd
import numpy as np
import string
from sklearn.feature_extraction.text import CountVectorizer
import ast
from sklearn.svm import SVC
import nltk
import scraper
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

# %%

df1 = pd.read_csv('datasets/completed_all_cleaned.csv')
df2 = pd.read_csv('datasets/received_all_cleaned.csv')
df = pd.concat([df1, df2]).reset_index(drop=True)

# %%

X = df[['Occupation score', 'Colby score', 'Occupation score adjusted']]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y)

print('training examples', len(X_train))
print('test examples', len(X_test))

param_grid = [
    {'C': [0.1, 1, 10, 100, 1000], 'kernel': ['linear']},
    {'C': [0.1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
]

clf = GridSearchCV(SVC(), param_grid)

clf.fit(X_train, y_train)

print('best params', clf.best_params_)

clf = SVC().set_params(**clf.best_params_)
clf.fit(X_train, y_train)
print('train score:', clf.score(X_train, y_train))
print('test score:', clf.score(X_test, y_test))

# %%

# class Classifier:
#     def __init__(self, clf=SVC(), kwargs_dict=None):
#         '''
#
#         :param clf: classifier algorithm. Defaulted to Support vector Machine
#         '''
#
#
#         if kwargs_dict:
#             self.clf = clf.set_params(**kwargs_dict)
#         else:
#             self.clf = clf
#
#     def use_best_params(self, grid_params):


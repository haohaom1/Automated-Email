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
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib


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

param_grid = {'max_depth': np.arange(3, 10)}

clf = GridSearchCV(DecisionTreeClassifier(), param_grid)

clf.fit(X_train, y_train)

print('best params', clf.best_params_)

print('train score:', clf.score(X_train, y_train))
print('test score:', clf.score(X_test, y_test))

joblib.dump(clf, 'best_classifier.pkl')
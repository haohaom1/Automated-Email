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
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier


# %%


df1 = pd.read_csv('datasets/completed_all_cleaned.csv')
df2 = pd.read_csv('datasets/received_all_cleaned.csv')

df1 = df1[(df1['Occupation score'] > 0) | (df1['Colby score'] > 0)]
df2 = df2[(df2['Occupation score adjusted'] < 0.7) & (df2['Colby score'] < 1)]

df = pd.concat([df1, df2]).reset_index(drop=True)

# %%

X = df[['Occupation score', 'Colby score', 'Occupation score adjusted']]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y)

print('training examples', len(X_train))
print('test examples', len(X_test))

param_grid = [
    {'C': [0.1, 1, 10, 100], 'kernel': ['linear']},
    {'C': [0.1, 1, 10, 100], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
]

clf = GridSearchCV(SVC(), param_grid)

clf.fit(X_train, y_train)

print('best params', clf.best_params_)

print('train score:', clf.score(X_train, y_train))
print('test score:', clf.score(X_test, y_test))

clf = SVC(**clf.best_params_, probability=True)
clf.fit(X_train, y_train)
# saves the classifier
# joblib.dump(clf, 'Classifiers/SVC_7_30.pkl')





#%% Decision Tree
X_train, X_test, y_train, y_test = train_test_split(X, y)
param_grid = {'max_depth': np.arange(3, 10)}

clf = GridSearchCV(DecisionTreeClassifier(), param_grid)

clf.fit(X_train, y_train)

print('best params', clf.best_params_)

print('train score:', clf.score(X_train, y_train))
print('test score:', clf.score(X_test, y_test))

#%% Logistic Regression
X_train, X_test, y_train, y_test = train_test_split(X, y)
param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000], 'tol': [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]}

clf = GridSearchCV(LogisticRegression(), param_grid)

clf.fit(X_train, y_train)

print('best params', clf.best_params_)

print('train score:', clf.score(X_train, y_train))
print('test score:', clf.score(X_test, y_test))

joblib.dump(clf, 'Classifiers/LR_7_30.pkl')

#%% KNN clustering

X_train, X_test, y_train, y_test = train_test_split(X, y)
param_grid = {'n_neighbors': np.arange(2, 10),
              'weights': ['uniform', 'distance'],
               'p': np.arange(1, 5)}

clf = GridSearchCV(KNeighborsClassifier(), param_grid)

clf.fit(X_train, y_train)

print('best params', clf.best_params_)

print('train score:', clf.score(X_train, y_train))
print('test score:', clf.score(X_test, y_test))

# joblib.dump(clf, 'Classifiers/KNN_7_30.pkl')
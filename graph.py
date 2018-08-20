import pandas as pd
import numpy as np
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import seaborn
plt.style.use('seaborn')


clf = joblib.load('Classifiers/SVC_7_30.pkl')



#%% Visualizing Completed Data probabilities and accuracy with histograms
df = pd.read_csv('backtest/priority_all_cleaned.csv')
data = df[['Occupation score', 'Occupation score adjusted', 'Colby score']].values

proba = np.max(clf.predict_proba(data), 1)
df['confidence'] = proba


plt.hist(proba)
plt.title('Distribution of Confidence in Priority Emails')
plt.xlabel('Confidence')
plt.ylabel('Count')
plt.savefig('visualization/priority_confidence.png')

plt.show()

#%% Viewing Right and wrongly labelled confidences at the same time

df = pd.read_csv('datasets/received_all_cleaned.csv')
data = df[['Occupation score', 'Occupation score adjusted', 'Colby score']].values

pred = clf.predict(data)
labels = df['label']
conf = np.max(clf.predict_proba(data), 1)

correct_labels = []
wrong_labels = []

for p, l, c in zip(pred, labels, conf):
    if p == l:
        correct_labels.append(c)
    else:
        wrong_labels.append(c)

plt.hist([wrong_labels, correct_labels], histtype='bar', color=['red', 'blue'],
         label=['wrong_label', 'correct_label'], bins=10)
plt.title('Confidence of Correctly and Incorrectly Labelled Emails in Received Using SVC')
plt.xlabel('Confidence')
plt.ylabel('Count')
plt.legend()
plt.savefig('visualization/received_confidence_all_svc.png')
plt.show()




#%% Generic Function for histogram

def generate_histogram(df, clf, folder_name, clf_type):
    data = df[['Occupation score', 'Occupation score adjusted', 'Colby score']].values
    pred = clf.predict(data)
    labels = df['label']
    conf = np.max(clf.predict_proba(data), 1)

    correct_labels = []
    wrong_labels = []

    for p, l, c in zip(pred, labels, conf):
        if p == l:
            correct_labels.append(c)
        else:
            wrong_labels.append(c)

    plt.hist([wrong_labels, correct_labels], histtype='bar', color=['red', 'blue'],
             label=['wrong_label', 'correct_label'], bins=10)
    plt.title('Confidence of Correctly and Incorrectly Labelled Emails in {} Using {}'.format(folder_name, clf_type))
    plt.xlabel('Confidence')
    plt.ylabel('Count')
    plt.legend()
    plt.savefig('visualization/{}_confidence_all_{}.png'.format(folder_name, clf_type))
    plt.show()

#%% Histogram for Logistic Regression

df = pd.read_csv('datasets/completed_all_cleaned.csv')
clf = joblib.load('Classifiers/LR_7_30.pkl')
generate_histogram(df, clf=clf, folder_name='completed', clf_type='Logistic_regression')

#%% Graphs time spent at each iteration

times = np.load('backtest/time_costs.npy').item()
num_emails = times['num_emails']
del times['num_emails']

# plt.pie(times.values(), labels=times.keys(), explode=(0, 0.05, 0, 0))
plt.bar(times.keys(), times.values(), alpha=0.5, color='darkblue')

plt.show()

#%%


df = pd.read_csv('datasets/completed_all.csv')
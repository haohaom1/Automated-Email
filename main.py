#%%
from emailreader import Emailreader
import pandas as pd
import numpy as np
from scraper import Scraper
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from sklearn.externals import joblib
import time
import classifier


#%% Username and password for the email
username = 'prospectstudent@colby.edu'
password = 'Student.2017'

scraper = Scraper()
reader = Emailreader()
mail = reader.login_email(username, password)

#%% Creates a database from past emails
def create_training_set():
    received_emails = pd.read_csv('datasets/received_constituents.csv')
    received_emails = scraper.clean_urls(received_emails)
    df = scraper.create_scores_data(received_emails, label=0)
    df.to_csv('datasets/received_all.csv', index=False)

    completed_emails = pd.read_csv('datasets/completed_constituents.csv')
    completed_emails = scraper.clean_urls(completed_emails)
    df = scraper.create_scores_data(completed_emails, label=1)
    df.to_csv('datasets/completed_all.csv', index=False)

#%% Cleans database of past emails
def clean_training_set():
    df = pd.read_csv('datasets/completed_all.csv')
    df.dropna(inplace=True)
    # df = df[(df['Occupation score'] > 0) | (df['Colby score'] > 0)]
    df.reset_index(drop=True, inplace=True)
    df.to_csv('datasets/completed_all_cleaned.csv', index=False)

    df = pd.read_csv('datasets/received_all.csv')
    df.dropna(inplace=True)
    # df = df[~((df['Occupation score adjusted'] > 1) | (df['Colby score'] > 1))]
    df.reset_index(drop=True, inplace=True)
    df.to_csv('datasets/received_all_cleaned.csv', index=False)
# #



#%% Creating dataset from the Priority Mail section
def test_classifier():
    # times dict for graphing
    times = {}

    # extracting mail objects from email
    time_prev = time.time()
    mail_name = 'Priority Mail'
    priority_mails_df = reader.get_emails_from_folder(mail=mail, folder_name=mail_name)

    elasped_time = time.time() - time_prev
    time_prev = time.time()
    times['email_objs'] = np.around(elasped_time, 3)


    # extracting urls from mail objects
    priority_mails_links = reader.get_links(priority_mails_df)
    priority_mails_links.to_csv('backtest/priority_constituents.csv')   # saves links

    elasped_time = time.time() - time_prev
    times['urls'] = np.around(elasped_time, 3)
    time_prev = time.time()

    # extracting scores from links
    df = scraper.create_scores_data(priority_mails_links).dropna()
    df.to_csv('backtest/priority_all.csv')  # saves all scores

    elasped_time = time.time() - time_prev
    time_prev = time.time()
    times['scores'] = np.around(elasped_time, 3)

    # classifying the data
    clf = joblib.load('Classifiers/LR_7_30.pkl')
    labels, probas = classifier.score(df=df, clf=clf, return_proba=True)

    print('probas', probas)

    # save scores and probas
    np.savetxt('backtest/labels.txt', labels, fmt='%d')
    np.savetxt('backtest/probas.txt', probas, fmt='%f')

    elasped_time = time.time() - time_prev
    time_prev = time.time()
    times['classification'] = np.around(elasped_time, 3)

    times['num_emails'] = len(priority_mails_df)

    print(times)

    np.save('backtest/time_costs.npy', times)

#%%
# def test_classify_mails():
clf = joblib.load('Classifiers/SVC_7_30.pkl')
df = classifier.classify_mails(mail, classifier=clf, folder='Priority Mail', cap_at=5)


#%%
if __name__ == '__main__':
    # create_training_set()
    # clean_training_set()
    # test_classifier()
    pass


#%%

# # %% Creating dataset from the Priority Mail section
#
# # times dict for graphing
# times = {}
#
# # extracting mail objects from email
# time_prev = time.time()
# mail_name = 'Priority Mail'
# priority_mails_df = reader.get_emails_from_folder(mail, mail_name, cap_at=10)
#
# elasped_time = time.time() - time_prev
# time_prev = time.time()
# times['email_objs'] = np.around(elasped_time, 3)
#
# # extracting urls from mail objects
# priority_mails_links = reader.get_links(priority_mails_df)
#
# elasped_time = time.time() - time_prev
# times['urls'] = np.around(elasped_time, 3)
# time_prev = time.time()
#
# # extracting scores from links
# # df = scraper.create_scores_data(priority_mails_links).dropna()
# # df.to_csv('backtest/priority_all.csv')  # saves all scores
# df = pd.read_csv('backtest/priority_all.csv')
#
# elasped_time = time.time() - time_prev
# time_prev = time.time()
# times['scores'] = np.around(elasped_time, 3)
#
# # classifying the data
# clf = joblib.load('Classifiers/LR_7_30.pkl')
# labels, probas = classifier.score(df=df, clf=clf, return_proba=True)
# probas = np.max(probas, axis=1)
#
# print('probas', probas)
#
# elasped_time = time.time() - time_prev
# time_prev = time.time()
# times['classification'] = np.around(elasped_time, 3)
#
# times['num_emails'] = len(priority_mails_df)
#
# print(times)
#
# #%%
#
# priority_mails_links['urls'][3]

#%%

from datetime import datetime

datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
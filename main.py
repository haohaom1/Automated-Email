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

# scraper = Scraper()

# received_emails = pd.read_csv('datasets/received_constituents.csv')
# received_emails = scraper.clean_urls(received_emails)
# df = scraper.create_scores_data(received_emails, 0)
# df.to_csv('datasets/received_all.csv', index=False)


# completed_emails = pd.read_csv('datasets/completed_constituents.csv')
# completed_emails = scraper.clean_urls(completed_emails)
# df = scraper.create_scores_data(completed_emails, 1)
# df.to_csv('datasets/completed_all.csv', index=False)

# df = pd.read_csv('datasets/completed_all.csv')
# df.dropna(inplace=True)
# df = df[(df['Occupation score'] > 0) | (df['Colby score'] > 0)]
# df.reset_index(drop=True, inplace=True)
# df.to_csv('datasets/completed_all_cleaned.csv', index=False)
#
# df = pd.read_csv('datasets/received_all.csv')
# df.dropna(inplace=True)
# df = df[~((df['Occupation score'] > 1) | (df['Colby score'] > 1))]
# df.reset_index(drop=True, inplace=True)
# df.to_csv('datasets/received_all_cleaned.csv', index=False)
# #



#%% Creating dataset from the Priority Mail section

# times dict for graphing
times = {}

# extracting mail objects from email
time_prev = time.time()
mail_name = 'Priority Mail'
priority_mails_df = reader.get_emails_from_folder(mail, mail_name, cap_at=5)

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
clf = joblib.load('Classifiers/DecTree_7_28.pkl')
labels, probas = classifier.score(df=df, clf=clf, return_proba=True)

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





#%%
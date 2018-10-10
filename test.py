import multiprocessing
import time
import signal
import threading
import pandas as pd
#%%
from emailreader import Emailreader
import pandas as pd
import numpy as np
from scraper import Scraper
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from sklearn.externals import joblib
import classifier
from datetime import datetime
import os
import warnings



scraper = Scraper()
reader = Emailreader()
username = 'prospectstudent@colby.edu'
password = 'Student.2017'
mail = reader.login_email(username, password)

#%%
# x = zip(np.random.choice(a=[1], size=10), np.random.randn(10))
text = 'Hi my name is mike and i love programming And and And Mike mike '
occs = ['mike', 'and', 'afda']

# score = scraper.get_matched_occs(text, occs, n=5)
# sum([s[1] for s in score])

text = scraper.clean_words(text)
counts = sum([text.count(occ) for occ in occs])
counts

# vec = CountVectorizer()
# vec.fit_transform([text])
# score = vec.transform(occs).toarray()#.sum()
# score_sum = score.sum()
#%%
counts

#%%
from itertools import groupby
x = sorted(x, key=lambda k: k[0])
a = [list(zip(*group)) for key, group in groupby(x, key=lambda k: k[0]==0)]
a

#%%


mails_df = reader.get_emails_from_folder(mail, folder_name='Priority Mail', latest_first=True, cap_at=3)
links = reader.get_links(mails_df)
scores_df = scraper.create_scores_data(links, split_up_links=True)


#%%
scores_df['text'][1]
#%%

scraper.scrape_words_from_urls(urls=['http://kbnd.com/kbnd-news/local-news-feed/379903'], split_up_links=False)

#%%

import pandas as pd
# df = pd.read_csv('logs/2018-08-16 23:42:13_logs.csv')
df = pd.read_csv('logs/2018-08-24 15:01:02_logs.csv')
#%%

df1 = df.reset_index().set_index(['index', 'id'])

#%%
import string
scraper.clean_words(['Clean this Sentealsdfkja #@32 ', 'hi@#', 'fhit'])
'Asdf@#@'.lower().translate(str.maketrans('', '', string.punctuation))
#%%
# df = classifier.create_csv_for_raiser('logs/2018-08-14 21:57:57_logs.csv', return_merged_df=True)

#%%

# %%

text = 'Are sentiments apartments decisively the especially alteration. Thrown shy denote ten ladies though ask saw.'
occs = ['are', 'the', 'ten', 'hi']

scraper.get_matched_occs(text, occs, 2)


#%%

df = pd.read_csv('logs/2018-08-13 20:21:54_logs.csv')
df1 = classifier.create_csv_for_raiser('logs/2018-08-13 20:21:54_logs.csv')
df['description'] = df.apply(lambda row: get_description(fname=row['first_name'], lname=row['last_name'], arg=row['arg']), axis=1).reset_index(drop=True)


#%%
#Username and password for the email
username = 'prospectstudent@colby.edu'
password = 'Student.2017'

scraper = Scraper()
reader = Emailreader()
mail = reader.login_email(username, password)


clf = joblib.load('Classifiers/LR_7_30.pkl')
df1 = classifier.classify_mails(mail, clf=clf, folder='Priority Mail',
                                cap_at=10, log_data=True, to_raiser=False, move=True)

#%%
df1.loc[df1['moved']]

#%%

classifier.create_csv_for_raiser('logs/2018-08-14 21:57:57_logs.csv')#.to_csv('raisers_edge/test_log.csv', index=False)


#%%

df = pd.read_csv('logs/2018-08-13 20:21:54_logs.csv')
df1 = classifier.create_csv_for_raiser('logs/2018-08-13 20:21:54_logs.csv')

#%%
constituent_df = pd.read_csv('datasets/OrganizationRelationships_NickNamesAdded_5.24.2018.csv')

# gets the description of the consitutent
def get_description(fname, lname, arg):
    mdf = constituent_df[((constituent_df['FIRST'] == fname)
                          & (constituent_df['LAST'] == lname))].iloc[arg]

    return '{} in the News'.format(mdf['CONSTIT CODE'])



get_description('Andrew', 'Davis', 0)


#%%

df2 = classifier.create_csv_for_raiser('logs/2018-08-14 16:31:32_logs.csv')


#%%
# def test_classify_mails():
# clf = joblib.load('Classifiers/SVC_7_30.pkl')
# df = classifier.classify_mails(mail, classifier=clf, folder='Priority Mail', cap_at=5, threshold=0.85, log_data=True)


#%%
# import multiprocessing
#
# def worker(procnum, return_dict):
#     '''worker function'''
#     print (str(procnum) + ' represent!')
#     return_dict[procnum] = procnum + 1
#
#
# if __name__ == '__main__':
#     manager = multiprocessing.Manager()
#     return_dict = manager.dict()
#     jobs = []
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i,return_dict))
#         jobs.append(p)
#         p.start()
#
#     for proc in jobs:
#         proc.join()
#
#
#     print (return_dict.values())


# # Your foo function
# def foo(n):
#
#     for i in range(100000 * n):
#         print ("Tick")
#         time.sleep(1)
#
# def handler(signum, frame):
#     print ("Forever is over!")
#     raise RuntimeError("end of time")
#
#
# for i in range(3):
#
#     signal.signal(signal.SIGALRM, handler)
#     signal.alarm(2)
#
#     try:
#         foo(1)
#     except Exception:
#         print ('end of time')
#     else:
#         signal.alarm(0)
#
# print('working threads', threading.enumerate())
#
#
#
#
# #
# # # if __name__ == '__main__':
# # # Start foo as a process'
# # def terminate_function(wait_time=5):
# #     p = multiprocessing.Process(target=foo, args=(10,))
# #     p.start()
# #
# #
# #     # Wait a maximum of 10 seconds for foo
# #     # Usage: join([timeout in seconds])
# #     p.join(wait_time)
# #
# #     # If thread is active
# #     if p.is_alive():
# #         print ("foo is running... let's kill it...")
# #
# #         # Terminate foo
# #         p.terminate()
# #         p.join()
# #
# # terminate_function()


# %%
df = pd.read_csv('backtest/priority_all.csv')
df.columns

#%% Creating dataset from the Priority Mail section

# extracting mail objects from email
mail_name = 'Priority Mail'
priority_mails_df = reader.get_emails_from_folder(mail, mail_name, cap_at=5)

# extracting urls from mail objects
priority_mails_links = reader.get_links(priority_mails_df)

# extracting scores from links
df = scraper.create_scores_data(priority_mails_links, split_up_links=True).dropna()
# df = pd.read_csv('backtest/priority_all.csv')

# classifying the data
clf = joblib.load('Classifiers/LR_7_30.pkl')
labels, probas = classifier.score(df=df, clf=clf, return_proba=True)

print('probas', probas)
print('labels', labels)

df['confidence'] = probas
df['label'] = labels

#%%

df1 = df.set_index(['id'])


#%%

df.groupby('id')['label'].max()

#%%
# df1 = pd.read_csv('logs/2018-08-02 15:46:51.csv')
pd.read_csv('datasets/OrganizationRelationships_NickNamesAdded_5.24.2018.csv')

#%%

df1 = classifier.classify_mails_from_data(mail, df=df, folder='Priority Mail')

df2 = df1.groupby(['id'])['label'].max().reset_index()

#%%

df1.join(df2, on='id', how='inner')

# df2 = df2.align(df1.set_index(['id']), join='inner')
#
# df2

#%%

df1 = df.url.apply(pd.Series).stack().reset_index(level=1, drop=True).to_frame('url_temp')
df1 = df.join(df1).reset_index(drop=True)
df1 = df1.drop(['url'], axis=1).rename(index=str, columns={'url_temp': 'url'})

# index_dict = dict(zip(df.index.tolist(), df.id.tolist()))
#
# df1 = pd.concat([pd.Series(row['id'], row['url']) for _, row in df.iterrows()]).reset_index()
# df1.columns = ['links', 'id']
# df1 = df1.groupby(['id']).sum()
# df2 = df.merge(df1, left_on='id', right_index=True, how='outer')'


#%%



#%%

pd.Series(data=[False, False, False]).max()
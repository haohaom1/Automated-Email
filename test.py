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
import webbrowser
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests


##%%
scraper = Scraper()
reader = Emailreader()
username = 'prospectstudent@colby.edu'
password = 'Student.2017'
mail = reader.login_email(username, password)
#%%

# mails_df = reader.get_emails_from_folder(mail, folder_name='Priority Mail', latest_first=True, cap_at=3)
# #%%
# [reader.move_email_to_folder(mail, 'Priority Mail', 'To Be Moved', uid) for uid in mails_df['id']]
# #%%
# mails_df_2 = reader.get_emails_from_folder(mail, folder_name='To Be Moved', latest_first=True, cap_at=3)
#
# #%%
# [reader.move_email_to_folder(mail, 'To Be Moved', 'Priority Mail', uid) for uid in mails_df['id']]

keys = ['acadia' 'advisers' 'association' 'cancer' 'center' 'foundation'
 'friends' 'holderness' 'kettering' 'memorial' 'selected' 'ski' 'sloan'
 'snowboard']
words = ['have', 'an', 'existing', 'account', 'already', 'have', 'a', 'subscription', 'dont', 'have', 'an', 'account', 'get', 'the', 'news', 'let', 'friends', 'in', 'your', 'social', 'network', 'know', 'what', 'you', 'are', 'reading', 'about', 'pilots', 'safety', 'experts', 'and', 'others', 'have', 'cautioned', 'against', 'early', 'speculation', 'regarding', 'the', 'cause', 'of', 'the', 'crash', 'that', 'killed', 'all', 'three', 'on', 'board', 'a', 'link', 'has', 'been', 'sent', 'to', 'your', 'friends', 'email', 'address', 'a', 'link', 'has', 'been', 'posted', 'to', 'your', 'facebook', 'feed', 'to', 'find', 'out', 'more', 'about', 'facebook', 'commenting', 'please', 'read', 'the', 'conversation', 'guidelines', 'and', 'faqs', 'andrew', 'davis', '32', 'was', 'killed', 'in', 'a', 'small', 'jet', 'crash', 'in', 'southern', 'indiana', 'along', 'with', 'wayne', 'estopinal', 'and', 'sandra', 'holland', 'johnsonphoto', 'teg', 'architechs', 'andrew', 'dale', 'davis', 'the', 'pilot', 'killed', 'in', 'a', 'small', 'jet', 'crash', 'in', 'southern', 'indiana', 'last', 'week', 'was', 'conscientious', 'about', 'safety', 'and', 'had', 'a', 'clean', 'flight', 'record', 'free', 'of', 'any', 'accidents', 'or', 'enforcement', 'actions', 'according', 'to', 'fellow', 'pilots', 'and', 'federal', 'aviation', 'administration', 'records', 'davis', '32', 'was', 'flying', 'two', 'passengers', 'friday', 'when', 'the', 'cessna', '525a', 'crashed', 'minutes', 'after', 'takeoff', 'from', 'clark', 'regional', 'airport', 'flight', 'tracking', 'site', 'flightaware', 'shows', 'it', 'was', 'at', 'about', '6000', 'feet', 'when', 'it', 'suddenly', 'changed', 'course', 'and', 'then', 'disappeared', 'from', 'radar', 'davis', 'was', 'a', 'corporate', 'pilot', 'at', 'teg', 'architects', 'he', 'was', 'flying', 'wayne', 'estopinal', '63', 'the', 'head', 'of', 'the', 'jeffersonville', 'firm', 'and', 'a', 'founder', 'of', 'the', 'louisville', 'city', 'fc', 'soccer', 'team', 'and', 'teg', 'vice', 'president', 'sandra', 'holland', 'johnson', '54', 'of', 'shreveport', 'louisiana', 'all', 'three', 'were', 'killed', 'more', 'about', 'andrew', 'davis', 'pilot', 'was', 'beloved', 'father', 'and', 'husband', 'workers', 'monday', 'were', 'hauling', 'parts', 'of', 'the', 'demolished', 'plane', 'from', 'a', 'densely', 'wooded', 'area', 'west', 'of', 'unincorporated', 'memphis', 'about', '16', 'miles', 'north', 'of', 'louisville', 'pilots', 'safety', 'experts', 'and', 'others', 'have', 'cautioned', 'against', 'early', 'speculation', 'about', 'the', 'cause', 'of', 'the', 'crash', 'the', 'national', 'transportation', 'safety', 'board', 'will', 'spend', 'months', 'studying', 'the', 'crash', 'before', 'determining', 'a', 'likely', 'cause', 'the', 'faa', 'said', 'monday', 'that', 'it', 'had', 'no', 'records', 'of', 'accidents', 'incidents', 'or', 'enforcement', 'actions', 'related', 'to', 'davis', 'davis', 'had', 'been', 'with', 'teg', 'architects', 'since', 'february', '2018', 'according', 'to', 'the', 'company', 'before', 'that', 'he', 'had', 'worked', 'as', 'a', 'corporate', 'pilot', 'at', 'soin', 'international', 'and', 'muncie', 'aviation', 'co', 'according', 'to', 'teg', 'soin', 'president', 'vishal', 'soin', 'said', 'in', 'an', 'email', 'that', 'davis', 'worked', 'there', 'for', 'about', '3', '12', 'years', 'and', 'never', 'had', 'any', 'safety', 'or', 'job', 'performance', 'issues', 'andrew', 'was', 'a', 'true', 'family', 'man', 'and', 'devoted', 'man', 'of', 'faith', 'soin', 'said', 'he', 'was', 'an', 'extremely', 'conscientious', 'pilot', 'and', 'had', 'an', 'unrelenting', 'passion', 'for', 'aviation', 'davis', 'graduated', 'in', '2008', 'from', 'indiana', 'state', 'university', 'with', 'a', 'bachelors', 'degree', 'in', 'aerospace', 'administration', 'and', 'professional', 'aviation', 'flight', 'technology', 'the', 'university', 'confirmed', 'monday', 'at', 'teg', 'davis', 'worked', 'alongside', 'mike', 'vollmer', 'the', 'companys', 'other', 'corporate', 'pilot', 'the', 'two', 'had', 'previously', 'worked', 'together', 'at', 'soin', 'when', 'davis', 'switched', 'to', 'teg', 'he', 'encouraged', 'vollmer', 'to', 'join', 'him', 'at', 'the', 'jeffersonville', 'architectural', 'firm', 'he', 'was', 'a', 'relentless', 'father', 'and', 'husband', 'vollmer', 'said', 'of', 'davis', 'everything', 'he', 'did', 'focused', 'around', 'his', 'family', 'and', 'his', 'faith', 'the', 'damage', 'it’s', 'terribly', 'fragmented', 'crews', 'work', 'clark', 'county', 'plane', 'crash', 'site', 'vollmer', 'said', 'davis', 'was', 'easy', 'to', 'get', 'along', 'with', 'and', 'was', 'always', 'telling', 'stories', 'i', 'used', 'to', 'joke', 'with', 'him', 'that', 'he', 'wasn’t', 'old', 'enough', 'to', 'have', 'that', 'many', 'stories', 'he', 'said', 'he', 'said', 'davis', 'was', 'always', 'focused', 'on', 'safety', 'and', 'procedure', 'he', 'had', 'checklists', 'for', 'checklists', 'vollmer', 'said', 'the', 'cessna', '525a', 'had', 'recently', 'been', 'in', 'for', 'minor', 'routine', 'maintenance', 'he', 'said', 'he', 'and', 'davis', 'in', 'november', 'held', 'a', 'safety', 'training', 'standdown', 'and', 'had', 'invited', 'other', 'tenants', 'at', 'clark', 'regional', 'to', 'join', 'paul', 'lucas', 'a', 'teg', 'pilot', 'from', '2007', 'to', '2014', 'said', 'he', 'flew', 'the', 'cessna', 'for', 'more', 'than', 'five', 'years', 'beginning', 'when', 'it', 'was', 'delivered', 'new', 'from', 'the', 'factory', 'in', '2009', 'he', 'said', 'the', 'plane', 'had', 'two', 'crew', 'seats', 'and', 'seven', 'seats', 'for', 'passengers', 'he', 'said', 'the', 'corporate', 'jet', 'has', 'a', 'history', 'of', 'being', 'a', 'very', 'safe', 'reliable', 'aircraft', 'lucas', 'stressed', 'that', 'he', 'has', 'been', 'gone', 'from', 'the', 'company', 'for', 'four', 'years', 'but', 'said', 'the', 'plane', 'was', 'reliable', 'and', 'doesn’t', 'remember', 'significant', 'problems', 'estopinal', 'himself', 'a', 'private', 'pilot', 'was', 'focused', 'on', 'safety', 'lucas', 'said', 'earlier', 'investigators', 'start', 'searching', 'for', 'clues', 'in', 'deadly', 'indiana', 'plane', 'crash', 'overview', 'heres', 'everything', 'we', 'know', 'about', 'the', 'southern', 'indiana', 'plane', 'crash', 'he', 'was', 'a', 'hardcharging', 'guy', 'but', 'when', 'it', 'came', 'to', 'airplanes', 'we', 'were', 'in', 'charge', 'lucas', 'said', 'he', 'got', 'the', 'things', 'that', 'sometimes', 'as', 'a', 'corporate', 'pilot', 'are', 'difficult', 'to', 'convey', 'to', 'your', 'management', 'team', 'lucas', 'spoke', 'reverently', 'of', 'estopinal', 'praising', 'his', 'former', 'boss', 'for', 'giving', 'him', 'an', 'opportunity', 'to', 'be', 'chief', 'pilot', 'at', 'age', '24', 'i', 'swore', 'i', 'would', 'never', 'let', 'that', 'man', 'and', 'his', 'family', 'down', 'lucas', 'said', 'lucas', 'said', 'he', 'used', 'to', 'fly', '300', 'to', '400', 'hours', 'per', 'year', 'in', 'the', 'cessna', '525a', 'he', 'said', 'the', 'typical', 'flight', 'was', 'within', 'about', '600', 'miles', 'of', 'clark', 'county', 'although', 'we', 'had', 'the', 'airplane', 'all', 'over', 'the', 'country', 'all', 'four', 'corners', 'of', 'continental', 'us', 'lucas', 'said', 'theres', 'a', 'natural', 'human', 'reaction', 'to', 'try', 'to', 'rationalize', 'what', 'could', 'have', 'happened', 'in', 'the', 'crash', 'but', 'he', 'said', 'he', 'hopes', 'people', 'will', 'wait', 'to', 'speculate', 'and', 'allow', 'investigators', 'to', 'do', 'their', 'jobs', 'reporter', 'alfred', 'miller', 'contributed', 'reporting', 'allison', 'ross', '5025824241', 'arosscourierjournalcom', 'twitter', 'allisonsross', 'support', 'strong', 'local', 'journalism', 'by', 'subscribing', 'today', 'courierjournalcomallisonr', 'more', 'wayne', 'estopinal', 'dead', 'in', 'indiana', 'plane', 'crash', 'leaves', 'lasting', 'legacy', 'see', 'also', 'how', 'to', 'pay', 'respects', 'to', 'architect', 'wayne', 'estopinal', 'who', 'died', 'in', 'jet', 'crash', 'a', 'link', 'has', 'been', 'posted', 'to', 'your', 'facebook', 'feed', 'link', 'httpswwwcourierjournalcomstorynewslocal20181203southernindianaplanecrashpilotrecordcleannoaccidents2195020002']
sum([k for k in keys if k in words])


#%%
df = pd.read_csv(r'logs\2018-11-08 13.09.54_logs.csv')
df.head(15)
#%%
# print(df.columns)
classifier.move_emails(mail, df)
# reader.move_email_to_folder(mail, 'Priority Mail', 'Completed', b'1896')
#%%


url = 'http://www.ifre.com/bobs-big-bet-barclays-purchase-of-lehman-brothers-10-years-later/21356030.fullarticle'
url = 'https://finexaminer.com/2018/11/29/as-amphenol-new-cl-a-aph-stock-rose-holder-buffington-mohr-mcneal-increased-holding-nxstage-medical-nxtm-shareholder-glazer-capital-has-lowered-its-position-by-515673-as-share-price-rose/'
hdr = {'User-Agent': 'Mozilla/5.0'}


page = requests.get(url).text
soup = BeautifulSoup(page, 'lxml')  # creates a BS4 object
words = []
for paragraph in soup.find_all('p'):
    words += paragraph.text.split()
print('success')

# scraper.get_text_from_url(url, clean=False)

# try:
#     r = requests.get(url, timeout=10.0)
# except requests.Timeout as err:
#     print(err)
# except requests.RequestException as err:
#     print(err)

#%%
import requests
MAX_RETRIES = 20

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
session.mount('https://', adapter)
session.mount('http://', adapter)

r = session.get(url)
soup = BeautifulSoup(r, 'lxml')


#%%
a = 'b\'123'
str.encode(a)
print(a)
a.decode()

#%%
mail.list()
mail.select('INBOX')
#%%
df['id'].apply(lambda s: s.decode())

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
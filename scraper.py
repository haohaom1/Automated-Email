
# coding: utf-8

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import warnings
from urllib.error import HTTPError, URLError
import ast
import signal
import ssl


# ## Scrapes data off of website


class Scraper:

    def __init__(self):
        self.common_words = set(nltk.corpus.stopwords.words('english'))

        try:
            path = 'datasets/OrganizationRelationships_NickNamesAdded_5.24.2018.csv'
            self.constituents_df = pd.read_csv(path, index_col=0, low_memory=False)
        except FileNotFoundError:
            warnings.warn('unable to find Constituents data. Please use set_constituents_path to locate the datafile')

        self.num_features = 3  # determines the number of features to use



    def get_text_from_url(self, url):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        hdr['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'

        try:

            req = Request(url, headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page, 'lxml')  # creates a BS4 object

            words = []
            for paragraph in soup.find_all('p'):
                words += paragraph.text.split()

            words = [''.join(c.lower() for c in s if c not in string.punctuation) for s in
                     words]  # strip punctuaions and lower cases words

            return words

        # suspicious website
        except ssl.CertificateError:
            return ''

        except ValueError:
            raise ValueError('Make sure the Dataframe passed has been cleaned. Use Scraper.clean_urls() '
                             'on the dataframe to clean it')


    def get_text_with_nltk(self, url):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, 'lxml')  # creates a BS4 object

        words = []
        for paragraph in soup.find_all('p'):
            words += paragraph.text.split()

        return nltk.word_tokenize(words)

    def set_constituents_path(self, path):

        self.constituents_df = pd.read_csv(path, index_col=0, low_memory=False)
        return self.constituents_df


    ## This will extract important words from an occupation
    def extract_orgs(self, df, ordering=False):

        df = df.dropna()
        orgs = [df[col] for col in df.index if 'ORG' in col]
        orgs = [x for x in orgs if x]   # cleans out None's and '' 's

        if not orgs:
            warnings.warn('Given constituent has no valid occupation')
            return orgs

        ordered_orgs = [s.split() for s in orgs]

        if not ordering:
            orgs = sum(ordered_orgs, [])
            orgs = ' '.join(orgs) # turns orgs into a sentence
            orgs = nltk.word_tokenize(orgs)
            orgs = [''.join(c.lower() for c in s if c not in string.punctuation) for s in orgs]  # strip punctuaions and lower cases words
            orgs = list(set(orgs))  # removes duplicates
            orgs = [j for j in orgs if j not in self.common_words]  # strips away common words

            return np.unique(orgs)
        else:
            return ordered_orgs

    # Cleans the dataframe. Call This when importing
    def clean_urls(self, df):
        df['urls'] = df['urls'].apply(lambda x: ast.literal_eval(x))
        df = df[df['urls'].map(len) > 0].reset_index(drop=True)
        return df


    # creates a Work Count Vectorizer, which calculates a score from the list of occupations
    # params: keys - list of strings to use as the key
    # params: words - list of all relevant words scraped from the website

    # return: score
    def occupation_score(self, keys, words):
        vec = CountVectorizer()
        vec.fit_transform(keys)
        score = vec.transform(words).toarray().sum() #/ len(keys)
        adj_score = score / len(keys)
        return score, adj_score


    # creates a Colby Count Vectorizer, which calculates a score based on how often 'Colby' appears in the text
    # params: words - list of all relevant words scraped from the website
    def colby_score(self, words):
        words = ' '.join(words)
        score = words.count('colby college')
        return score


    # returns [occupation_score, colby_score] for all matched people in directory, summed along the axis 0
    # shape num_matched_ppl by 2 (num_features)

    # param: words - list of all relevant words scraped from the website

    # return scores: the scores of all matched persons
    # return args: the row index of
    def total_score(self, words, matched_df):

        self.num_features = 3
        scores = np.zeros((len(matched_df), self.num_features))

        for row in range(len(matched_df)):
            occs = self.extract_orgs(matched_df.iloc[row])

            scores[row, :] = [*self.occupation_score(occs, words), self.colby_score(words)]
        #         print('row', row)

        # finds the argument of the person that has the highest score
        # used to back track the matched person
        dists = np.sum(np.square(scores), axis=1)  # euclidean distance

        arg = np.argmax(dists)  # returns the index of matched_df with the highest score

        return scores, arg



    ## returns a dataframe of all people that match the first and last name

    def create_matched_df(self, fname, lname):
        df1 = self.constituents_df.loc[(self.constituents_df['FIRST'] == fname) & (self.constituents_df['LAST'] == lname)]
        df2 = self.constituents_df.loc[(self.constituents_df['NICKNAME'] == fname) & (self.constituents_df['LAST'] == lname)]
        matched_df = pd.concat([df1, df2])

        matched_df.reset_index(inplace=True)
        return matched_df



    def score_all_urls(self, urls, matched_df, sum_array=False):
        # returns nan if the person is not matched in the database
        if matched_df.empty:
            warnings.warn('Unable to find in database')

            return np.array([np.nan] * self.num_features), np.nan

        # for handling when the function takes too long to respond
        def handler(signum, frame):
            raise TimeoutError("Unable to load website")

        scores = np.zeros((len(urls), self.num_features))  # score matrix
        args = np.zeros((len(urls), 1))  # args matrix; the row is the most likely matched recipient

        for row, url in enumerate(urls):

            # terminates the function if it runs for more than 60 seconds
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(60)

            try:
                words = self.get_text_from_url(url)
                if not words:
                    warnings.warn('suspicious website detected')
                    return np.array([np.nan] * self.num_features), np.nan

                score, arg = self.total_score(words, matched_df)
                score = score.sum(axis=0)  # sums all the scores

                scores[row, :] = score
                args[row, :] = arg
            except:
                warnings.warn('Unable to load {} for {} {}'.format(url, matched_df['FIRST'][0], matched_df['LAST'][0]))
                return np.array([np.nan] * self.num_features), np.nan

            signal.alarm(0)

        if sum_array:
            maxarg = np.argmax(np.sqrt(np.square(scores).sum(1)))
            return scores.sum(0) / np.sqrt(len(scores)), args[maxarg]

        return scores, args


    def create_scores_data(self, df, label=None):

        '''

        :param df: dataframes containing first name, last name, and urls
        :param label: label of result. either 1 or 0
        :return: scores dataframe with added Occupation score and Colby score as features
        '''

        scores = []
        args = []
        urls = []

        for i in range(len(df)):
            print('processing row {}'.format(i))

            test_data = df.iloc[i]
            mdf = self.create_matched_df(test_data['first_name'], test_data['last_name'])

            # kill this function if it's running for too long
            s, arg = self.score_all_urls(test_data['urls'], mdf, sum_array=True)

            scores.append((s[0], s[1], s[2]))
            args.append(arg)
            urls.append(test_data['urls'])

        assert(len(df) == len(scores))  # verifies that the length of each are the same

        scores_df = pd.DataFrame(scores, columns=['Occupation score', 'Occupation score adjusted', 'Colby score'])
        # scores_df['first_name'] = df.loc[:len(scores_df), 'first_name']
        # scores_df['last_name'] = df.loc[:len(scores_df), 'last_name']
        scores_df['first_name'] = df['first_name']
        scores_df['last_name'] = df['last_name']

        scores_df['urls'] = df['urls']

        scores_df['args'] = args

        if label:
            scores_df['label'] = label

        return scores_df

# coding: utf-8

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import string
import nltk
import warnings
from urllib.error import HTTPError, URLError
import ast
import ssl
import threading_timer
from datetime import datetime

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

    # exits the function after 60 seconds; throws keyboard interrupt error if happens.
    @threading_timer.exit_after(60)
    def get_text_from_url(self, url, clean=True):
        hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}

        try:

            # with urlopen(url) as html:
            #     html = html.read()
            # bs = BeautifulSoup(html, "lxml")

            req = Request(url, headers=hdr)
            with urlopen(req) as page:
                page = page.read()
            soup = BeautifulSoup(page, 'lxml')  # creates a BS4 object

            words = []
            for paragraph in soup.find_all('p'):
                words += paragraph.text.split()

            if clean:
                words = [''.join(c.lower() for c in s if c not in string.punctuation) for s in
                         words]  # strip punctuaions and lower cases words

            return words

        # suspicious website
        except ssl.CertificateError:
            return ''

        except ValueError:
            warnings.warn('Make sure the Dataframe passed has been cleaned. Use Scraper.clean_urls() '
                             'on the dataframe to clean it')

    # strip punctuations and lower case from a string
    def clean_words(self, string_words):
        return string_words.lower().translate(str.maketrans('', '', string.punctuation))

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
    # df is a pd Series that contains orgs
    def extract_orgs(self, df, ordering=False):

        names = df[['FIRST', 'NICKNAME', 'LAST']].tolist()
        names = [n.lower() for n in names if isinstance(n, str)]

        df = df.dropna()
        orgs = [df[col] for col in df.index if 'ORG' in col]
        orgs = [x for x in orgs if x]   # cleans out None's and '' 's

        if not orgs:
            warnings.warn('Given constituent has no valid occupation')
            return orgs

        ordered_orgs = [s.split() for s in orgs]

        if not ordering:
            orgs = sum(ordered_orgs, [])
            orgs = ' '.join(orgs)   # turns orgs into a sentence
            orgs = nltk.word_tokenize(orgs)
            orgs = [''.join(c.lower() for c in s if c not in string.punctuation) for s in orgs]  # strip punctuaions and lower cases words
            orgs = list(set(orgs))  # removes duplicates
            orgs = [j for j in orgs if j not in self.common_words and len(j) > 2]  # strips away common words and len words > 2
            orgs = [j for j in orgs if j not in names]      # strip away words that have the constituent's name in it

            return np.unique(orgs)
        else:
            return ordered_orgs

    # Cleans the dataframe. Call This when importing
    def clean_urls(self, df):
        df['url'] = df['url'].apply(lambda x: ast.literal_eval(x))
        df = df[df['url'].map(len) > 0].reset_index(drop=True)
        return df

    # takes in text, and returns the top n words matched with # of times matched with occupation text
    def get_matched_occs(self, text, occs, n=5):
        '''

        :param text: string, text data
        :param occs: list of string, occupation text
        :param n: int, number of items wanted
        :return: list of tuples containing (occ, # times matched)
        '''
        text = self.clean_words(text)
        counts = [text.count(occ) for occ in occs]

        # show either the max number of elements available, or n, which ever is smaller
        n = min(len([x for x in counts if x > 0]), n)

        # sorts the list, then returns the first n elements
        return sorted(list(zip(occs, counts)), key=lambda x: x[1], reverse=True)[:n]


    # creates a Work Count Vectorizer, which calculates a score from the list of occupations
    # params: keys - list of strings to use as the key
    # params: words - list of all relevant words scraped from the website

    # return: score, adjusted score
    def occupation_score(self, keys, words):
        # vec = CountVectorizer()
        # vec.fit_transform(keys)
        # score = vec.transform(words).toarray().sum()
        words = self.clean_words(' '.join(words))
        score = sum([words.count(key) for key in keys])

        adj_score = score / len(keys)
        return score, adj_score


    # params: words - list of all relevant words scraped from the website
    # return: the number of times colby college appeared
    def colby_score(self, words):
        words = ' '.join(words)
        score = words.count('colby college')
        return score


    # returns [occupation_score, colby_score] for all matched people in directory, summed along the axis 0
    # shape num_matched_ppl by 2 (num_features)

    # param: words - list of all relevant words scraped from the website

    # return scores: the scores of all matched persons
    # return args: the row index of the best matched constituent
    def total_score(self, words, matched_df):

        self.num_features = 3
        scores = np.zeros((len(matched_df), self.num_features))

        for row in range(len(matched_df)):
            occs = self.extract_orgs(matched_df.iloc[row])

            scores[row, :] = [*self.occupation_score(occs, words), self.colby_score(words)]

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

    def scrape_words_from_urls(self, urls, split_up_links):
        # scrapes words from a list of urls
        # returns a list of list of words

        print('starting scrape', datetime.now())

        if split_up_links:
            urls = [urls]

        list_of_words = []

        # urls is a 1D list of urls
        # returns a list of list of words
        for url in urls:

            try:
                words = self.get_text_from_url(url, clean=False)
                if not words:
                    warnings.warn('suspicious website detected')

                    if split_up_links:
                        return None
                    list_of_words.append('')

                words = ' '.join(words)

                if split_up_links:
                    return words
                list_of_words.append(words)

            except (URLError, HTTPError, KeyboardInterrupt) as error:
                warnings.warn('Unable to load {}'.format(url))
                print(error)
                print('reached', datetime.now())
                if split_up_links:
                    return None
                list_of_words.append('')

        print('end scrape', datetime.now())
        return list_of_words


    # def scrape_words_from_urls_v2(self, urls, split_up_links):
    #     # scrapes words from a list of urls
    #     # returns a list of list of words
    #
    #
    #     # for handling when the function takes too long to respond
    #     def handler(signum, frame):
    #         warnings.warn("Unable to load website")
    #
    #     # terminates the function if it runs for more than 60 seconds
    #     signal.signal(signal.SIGALRM, handler)
    #     signal.alarm(60)
    #
    #     list_of_words = []
    #
    #     # urls is a 1D list of urls
    #     # returns a list of list of words
    #     if split_up_links:
    #         for url in urls:
    #             try:
    #                 words = self.get_text_from_url(url)
    #                 if not words:
    #                     warnings.warn('suspicious website detected')
    #                     words.append('')
    #
    #                 list_of_words.append(words)
    #
    #             except:
    #                 warnings.warn('Unable to load {}'.format(url))
    #                 list_of_words.append('')
    #
    #             # resets alarm
    #             signal.alarm(0)
    #
    #     # urls is a list of list of urls, one list per email
    #     # returns a list of list of list of words
    #     else:
    #
    #         for url_list in urls:
    #
    #             temp_words = []
    #             for url in url_list:
    #                 try:
    #                     words = self.get_text_from_url(url)
    #                     if not words:
    #                         warnings.warn('suspicious website detected')
    #                         words.append('')
    #
    #                     temp_words.append(words)
    #
    #                 except:
    #                     warnings.warn('Unable to load {}'.format(url))
    #                     temp_words.append('')
    #
    #                 # resets alarm
    #                 signal.alarm(0)
    #
    #             list_of_words.append(temp_words)
    #
    #     return list_of_words

    def score_all_urls(self, words, matched_df, sum_array=False, links_split_up=False):
        '''

        :param words: list of strings or strings of words scraped from the links
        :param matched_df:
        :param sum_array:
        :param links_split_up: if the links were split up
        :return:
        '''
        # returns nan if the person is not matched in the database
        if matched_df.empty:
            warnings.warn('Unable to find in database')

            return np.array([np.nan] * self.num_features), np.nan

        if not words:
            warnings.warn('suspicious website detected')
            return np.array([np.nan] * self.num_features), np.nan

        if links_split_up:
            words = self.clean_words(words).split()
        else:
            words = [self.clean_words(words_per_link).split() for words_per_link in words]

        # decideds logic based on whether the words were split up
        if links_split_up:
            # words parameter is a list of words, for only one link

            score, arg = self.total_score(words, matched_df)

            scores = np.atleast_2d(score)
            args = np.atleast_2d(arg)

        else:
            # words parameter is a list of list of words, for multiple links

            scores = np.zeros((len(words), self.num_features))  # score matrix
            args = np.zeros((len(words), 1))  # args matrix; the row is the most likely matched recipient

            for row, words_per_link in enumerate(words):
                score, arg = self.total_score(words_per_link, matched_df)
                score = score.sum(axis=0)  # sums all the scores

                scores[row, :] = score
                args[row, :] = arg

        # print('score', scores)

        if sum_array:
            maxarg = np.argmax(np.sqrt(np.square(scores).sum(1)))
            return scores.sum(0) / len(scores), args[maxarg].item()

        return scores, args


    def create_scores_data(self, df, label=None, split_up_links=False):

        '''

        :param df: dataframes containing first name, last name, and urls
        :param split_up_links: whether to have a list of links or to explode the list of links
        :return: scores dataframe with added Occupation score and Colby score as features
        '''

        # makes a deep copy of the dataframe
        df = df.copy()


        if split_up_links:
            temp_df = df['url'].apply(pd.Series).stack().reset_index(level=1, drop=True).to_frame('url_temp')
            temp_df = df.join(temp_df).reset_index(drop=True)
            temp_df = temp_df.drop(['url'], axis=1).rename(index=str, columns={'url_temp': 'url'})

            df = temp_df

        texts = []
        for i, url in enumerate(df['url']):
            texts.append(self.scrape_words_from_urls(url, split_up_links))
            print('loaded row', i)
        df['text'] = texts
        # df['text'] = df['url'].apply(lambda x: self.scrape_words_from_urls(x, split_up_links=split_up_links))

        scores = []
        args = []
        urls = []
        constituent_id = []

        for i in range(len(df)):
            print('processing link {}'.format(i))

            current_row = df.iloc[i]

            mdf = self.create_matched_df(current_row['first_name'], current_row['last_name'])

            # kill this function if it's running for too long
            s, arg = self.score_all_urls(words=current_row['text'], matched_df=mdf, sum_array=True,
                                         links_split_up=split_up_links)

            scores.append((s[0], s[1], s[2]))
            args.append(arg)
            urls.append(current_row['url'])

            if not np.isnan(arg):
                c_id = mdf.iloc[int(arg)]['ID']

            # arg does not exist for the constituent
            else:
                c_id = np.NAN
            constituent_id.append(c_id)


        assert(len(df) == len(scores))  # verifies that the length of each are the same

        # add lists of urls if we didn't split up links
        if not split_up_links:
            df['url'] = urls
        df['arg'] = args

        # adds the scores
        df[['Occupation score', 'Occupation score adjusted', 'Colby score']] = pd.DataFrame(scores, index=df.index)
        df['constituent_id'] = constituent_id

        # if given a label (for training) add label as a column
        if label:
            df['label'] = label

        return df

import pandas as pd
from sklearn.externals import joblib

from scraper import Scraper
from emailreader import Emailreader
from datetime import datetime
import numpy as np

import pathlib

scraper = Scraper()
reader = Emailreader()

# constituent_df = pd.read_csv(pathlib.PureWindowsPath(pathlib.Path('datasets/OrganizationRelationships_NickNamesAdded_5.24.2018.csv'))
# )
constituent_df = 'datasets/OrganizationRelationships_NickNamesAdded_5.24.2018.csv'


def score(df, clf, return_proba=False, remove_nan=True):
    '''
    scores the given data with the given classifer
    if nan values exist in df, then label and proba will be also nan

    :param df: the dataframe containing constituent information
    :param clf: path to the saved classifier
    :return: prediction labels, and confidence (1D list)

    '''

    # print('before dropna', df)

    if remove_nan:
        df = df.dropna()

    X = df[['Occupation score', 'Occupation score adjusted', 'Colby score']].values

    # print('dat values', X)

    labels = clf.predict(X)

    if return_proba:
        proba = clf.predict_proba(X)
        proba = np.max(proba, axis=1)
        return labels, proba

    return labels

# # YET TO BE IMPLEMENTED: classify emails using a preprocessed dataframe of scores
def classify_mails_from_data(mail, df, folder, labels=None, uids=None,
                             probas=None, to_raiser=True, move=False, threshold=0.85):
    '''
    moves the emails to their respective location based on the decision by the classifier
    Assumes the emails have already been processed,

    0 means Received folder
    1 means Completed folder

    :param df: Dataframe containing first name, last name, arg, url, email
               ids, scores, and labels
    :param folder: the folder the set of emails are from
    :param labels: the labels given to each link
    :param uids: the unique id of each email
    :param probas: the confidence of each decision
    :param to_raiser: whether or not to return a dataframe
    :param threshold: optional: the level of confidence threshold for a decision to be made
    :param move: whether to move the email. Used for debugging
    '''

    df = df.copy()

    times = []
    decisions = []

    # print('df', df)

    for _, row in df.iterrows():

        if row['label'] == 0 and row['confidence'] > threshold and move:
            target_folder = 'Received'
            decisions.append(True)
        elif row['label'] == 1 and row['confidence'] > threshold and move:
            target_folder = 'Completed'
            decisions.append(True)
        else:
            target_folder = 'Further Review Needed'
            decisions.append(False)

        # moves the email based on the decision
        if move:
            reader.move_email_to_folder(mail=mail, orig_folder=folder, target_folder=target_folder, email_uid=row['id'])

        time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        times.append(time)

    df['time'] = times
    df['moved'] = decisions

    if to_raiser:
        pass

    return df


def classify_mails(mail, folder, clf=None, cap_at=None, latest_first=True, threshold=0.85,
                   log_data=False, to_raiser=False, log_filename=False,
                   move=True, split_up_links=True):
    '''
    Iterates through emails from a given folder, and moves it accordingly

    :param mail: The IMAP mail object. Must be logged in, and contains the Completed and Received Folders
    :param folder: name of folder for emails
    :param clf: The classifier used to classify emails
    :param cap_at: How many mails to read
    :param latest_first: Whether or not to read the latest emails first
    :param threshold: The confidence threshold for a decision to be made. Defaulted to 0.9
    :param to_raiser: Whether or not to create a csv to be used to record in to Raiser's Edge Database
    :param log_filename: Whether or not to return a path to the filename of the logs
    :param split_up_links: Whether or not to split up the list links that are in the same email
    :return: dataframe containing UID of the emails, Scores, probability,
    and confidence, decision, and timestamp, constituent info, sorted by confidence,
    '''

    if not clf:
        clf = joblib.load('Classifiers/LR_7_30.pkl')

    mails_df = reader.get_emails_from_folder(mail, folder_name=folder, latest_first=latest_first, cap_at=cap_at)
    links = reader.get_links(mails_df)

    scores_df = scraper.create_scores_data(links, split_up_links=True)

    invalids = scores_df[scores_df['Colby score'].isnull()]
    if move:
        for uid in invalids['id']:
            reader.move_email_to_folder(mail, folder, target_folder='Further Review Needed', email_uid=uid)

    # dropnas
    scores_df.dropna(inplace=True)

    labels, probas = score(df=scores_df, clf=clf, return_proba=True)

    # print('labels', labels)
    # print('probas', probas)
    # print('index', scores_df.index)

    # adds the relevant columns of information
    scores_df['confidence'] = probas
    scores_df['label'] = labels

    df = classify_mails_from_data(mail=mail, df=scores_df, folder=folder, threshold=threshold, move=move)

    # turn constituent_id to int
    df['constituent_id'] = df['constituent_id'].astype(np.int64)

    # gets the actual words from the urls
    # IF TIME PERMITTED USE WORDS FROM THE START TO BE MORE EFFICIENT
    df['text'] = df['url'].apply(lambda x: ' '.join(scraper.get_text_from_url(x, clean=False, include_url=True)))

    # documents the mail source
    df['folder'] = folder


    # sorts df by probability
    # df.sort_values(['proba'], inplace=True)

    # logs the data
    if log_data:
        # moved_df = df[df['moved']]

        # logs the data if the dataframe is not empty
        if not df.empty:
            date = datetime.strftime(datetime.now(), '%Y-%m-%d %H.%M.%S')

            # saves to the logs
            # windows_path = pathlib.PureWindowsPath(pathlib.Path('logs/{}_logs.csv'.format(date)))
            windows_path = 'logs/{}_logs.csv'.format(date)
            df.to_csv(windows_path, index=False)

            # if to_raiser is true AND there is an available data from logs, then return the data to be
            # exported to Raisers edge as well
            if to_raiser:
                window_path = pathlib.PureWindowsPath(pathlib.Path('logs/{}_logs.csv'.format(date)))
                return df, create_csv_for_raiser(windows_path)

            if log_filename:
                return df, '{}_logs.csv'.format(date)

    return df


def create_csv_for_raiser(logs=None, df=None, return_merged_df=False):

    if not df:
        df = pd.read_csv(logs)
    else:
        df = df.copy()

    # only convert emails that are moved into the Completed Folder
    df = df.loc[(df['moved']) & (df['label'] == 1)]
    # df = df.loc[df['label'] == 1]


    # returns null if there are no values in the log to be moved
    if df.empty:
        if return_merged_df:
            return df, df
        return df

    dates = datetime.strftime(datetime.now(), '%m/%d/%Y')
    move_or_change = 'N/A'
    publication = 'Publicly/Communictn'
    author = 'xfu21'

    headers = ['date', 'move/status change (or n/a)', 'type', 'author']
    data = [dates, move_or_change, publication, author]

    for h, d in zip(headers, data):
        df[h] = d

    # df[headers] = pd.DataFrame([dates, move_or_change, publication, author], index=df.index)
    # df['text'] = df['url'].apply(lambda x: ' '.join(scraper.get_text_from_url(x, clean=False)))

    # gets the description of the consitutent
    def get_description(fname, lname, arg):

        # makes sure that argument is a integer
        arg = int(arg)

        constituent = scraper.create_matched_df(fname=fname, lname=lname).iloc[arg]

        return '{} in the News'.format(constituent['CONSTIT CODE'])

    df['description'] = df.apply(lambda row: get_description(fname=row['first_name'],
                                                             lname=row['last_name'],
                                                             arg=row['arg']),
                                 axis=1).values.tolist()

    headers = headers + ['description', 'text', 'constituent_id']
    raisers_df = df.loc[:, headers]
    raisers_df.rename(index=int, columns={'constituent_id': 'id'}, inplace=True)

    if return_merged_df:

        return raisers_df, df

    return raisers_df


def move_emails(mail, df):
    '''
    Uses the Raiser CSV to determine which emails to move to which folder
    '''

    # converts str to boolean
    df['moved'] = df['moved'].apply(lambda x: x == 'True')

    for _, row in df.iterrows():
        folder = row['folder']
        email_uid = str.encode(str(row['id']))

        if row['label'] == 0 and row['moved']:
            target_folder = 'Received'
        elif row['label'] == 1 and row['moved']:
            target_folder = 'Completed'
        else:
            target_folder = 'Further Review Needed'

        # print('moving from', folder, 'to', target_folder)
        # print(row['id'], type(row['id']))
        # byte_id = str.encode('1779')
        # print(byte_id, type(byte_id))

        ### COMMENT OUT the line below to prevent emails from being moved
        reader.move_email_to_folder(mail=mail, orig_folder=folder, target_folder=target_folder, email_uid=email_uid)
        print('moved emails')
def score(df, clf, return_proba=False):
    '''
    scores the given data with the given classifer

    :param clf_link: path to the saved classifier
    :return: prediction labels for every
    '''

    df = df.dropna()
    X = df[['Occupation score', 'Occupation score adjusted', 'Colby score']]

    labels = clf.predict(X)

    if return_proba:
        proba = clf.predict_proba(X)
        return labels, proba

    return labels

# %%

# class Classifier:
#     def __init__(self, clf=SVC(), kwargs_dict=None):
#         '''
#
#         :param clf: classifier algorithm. Defaulted to Support vector Machine
#         '''
#
#
#         if kwargs_dict:
#             self.clf = clf.set_params(**kwargs_dict)
#         else:
#             self.clf = clf
#
#     def use_best_params(self, grid_params):


# # create function that gives the probabilities of each datapoint

import pandas as pd
import numpy as np
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import seaborn
plt.style.use('seaborn')
#%%

clf = joblib.load('Classifiers/DecTree_7_28.pkl')


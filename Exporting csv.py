'''
This file is used to concatenate logs generated to be exported to Raisers Edge
'''
#%%
import pandas as pd
import os
#%%
files = os.listdir('raisers_edge/')
df = pd.concat([pd.read_csv('raisers_edge/' + f) for f in files]).drop_duplicates().reset_index(drop=True)
#%%
df[df['text'].len() < 2]
#%%
df.to_excel('to_raiser/all_completed_11-27-2018.xlsx', index=False)
#%%
pd.read_csv('raisers_edge/2018-11-14 14.46.51_raiser.csv')
#%%
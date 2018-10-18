import emailreader
import pandas as pd
import numpy as np
import classifier
from scraper import Scraper

#%% Sets up packages
username = 'prospectstudent@colby.edu'
password = 'Student.2017'
scraper = Scraper()

reader = emailreader.Emailreader()

mail = reader.login_email(username=username, password=password)

#%% Retrieves emails
received_emails = reader.get_emails_from_folder(mail=mail, folder_name='Received', cap_at=5, latest_first=True)
completed_emails = reader.get_emails_from_folder(mail, folder_name='Completed', cap_at=5, latest_first=True)

## %% Retrieves the urls and words
received_links = reader.get_links(received_emails)
completed_links = reader.get_links(completed_emails)

##%% Retrieves the scores
received_df = scraper.create_scores_data(received_links, label=0)
completed_df = scraper.create_scores_data(completed_links, label=1)

#%%
completed_df = completed_df[completed_df.first_name != '.']
received_df = received_df[received_df.first_name != '.']

received_df = received_df[received_df.first_name != 'Colby']
completed_df = completed_df[completed_df.first_name != 'Colby']

completed_df.reset_index(drop=True, inplace=True)
received_df.reset_index(drop=True, inplace=True)
#%%
received_df.to_csv('datasets_october/received_constituents.csv', index=False)
completed_df.to_csv('datasets_october/completed_constituents.csv', index=False)#%%

import emailreader
import pandas as pd
import numpy as np
#%%
# In[2]
username = 'prospectstudent@colby.edu'
password = 'Student.2017'

reader = emailreader.Emailreader()

mail = reader.login_email(username=username, password=password)

received_emails = reader.get_emails_from_folder(mail=mail, folder_name='Received', cap_at=2000, latest_first=False)
completed_emails = reader.get_emails_from_folder(mail, folder_name='Completed', latest_first=False)
#%%

received_df = reader.get_links(received_emails)
completed_df = reader.get_links(completed_emails)


completed_df = completed_df[completed_df.first_name != '.']
received_df = received_df[received_df.first_name != '.']

received_df = received_df[received_df.first_name != 'Colby']
completed_df = completed_df[completed_df.first_name != 'Colby']

completed_df.reset_index(drop=True, inplace=True)
received_df.reset_index(drop=True, inplace=True)
#%%
received_df.to_csv('datasets/received_constituents.csv', index=False)
completed_df.to_csv('datasets/completed_constituents.csv', index=False)#%%
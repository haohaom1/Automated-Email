# coding: utf-8

# ### This will serve as a package to help read emails


# import necesary packages
import pandas as pd
import numpy as np
import imaplib
import email
import re


# In[2]:
class Emailreader:


    def login_email(self, username=None, password=None):
        '''
        params: username and password
        return: the imap mail object
        '''


        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(username, password)

        self.mail = mail
        # Out: list of "folders" aka labels in gmail.
        # mail.select("inbox") # connect to inbox.
        return mail


    # In[4]:

    def switch_folders(self, mail, folder_name):
        '''
        Switches the folders of the email
        '''
        mail.select('"Google Alerts/{}"'.format(folder_name))

    def get_emails_from_folder(self, mail, folder_name, latest_first=True, cap_at=None):
        '''
        params: mail - imap mail object
        params: folder_name
        return: pandas series containing the email uid as the index and the email_message object as the data
        '''
        mail.select('"Google Alerts/{}"'.format(folder_name))
        result, data = mail.uid('search', None, "ALL")  # search and return uids instead

        ids = data[0].split()
        if latest_first:
            ids = list(reversed(ids))

        num_emails = len(ids)

        if cap_at:
            ids = ids[:min(len(ids), cap_at)]

        data = [mail.uid('fetch', uid, '(RFC822)')[1] for uid in ids]
        raw_emails = [str(d[0][1], 'utf-8') for d in data]
        email_messages = [email.message_from_string(raw) for raw in raw_emails]

        df = pd.DataFrame({'mail': email_messages,
                           'id': ids})

        print('You have {} messages in folder {}'.format(num_emails, folder_name))

        return df

    def get_email_from_uid(self, mail, folder_name, uid):
        '''
        returns the email object of given uid in a folder

        :param mail: the imap mail object. Must be logged in
        :param folder_name: the folder the email is in
        :param uid: the unique id of the email
        :return: The given email with the uid.
        '''

        pass

    # In[8]:


    def get_text_from_email(self, email_msg, clean_text=True):
        if email_msg.is_multipart():
            s = ''
            for payload in email_msg.get_payload():
                s += payload.get_payload()
        else:
            s = email_msg.get_payload()

        if clean_text:
            s = s.replace('\r\n', '').replace('=', '')
        return s



    # gets the urls straight from the raw texts
    def get_url_from_text(self, raw_text):
        return re.findall('(?<=url3D)(.*?)(?=\\\\u0026)', raw_text)


    def get_links(self, email_df):
        '''
        Stores all the links from a given email

        params:
        email_df: pd series containing mail objects retrieved from get_emails_from_folder

        return: dataframe with the following columns: [Fname, Lname, list_of_links]
        '''

        # print(email_df)

        list_of_raw_text = [self.get_text_from_email(msg) for msg in email_df['mail']]
        list_of_urls = [self.get_url_from_text(txt) for txt in list_of_raw_text]
        ids = email_df['id']

        subjects = [msg['Subject'] for msg in email_df['mail']]

        names = []
        for i, subject in enumerate(subjects):
            try:
                names.append(re.findall('"(.*?)"', subject)[0])
            except IndexError:
                print(subject)
                names.append('.')

        fnames = [name.split()[0] for name in names]
        lnames = [name.split()[-1] for name in names]

        df = pd.DataFrame(np.column_stack([fnames, lnames, list_of_urls, ids]),
                          columns=['first_name', 'last_name', 'url', 'id'])
        return df


    # # Method for moving an email
    def move_email_to_folder(self, mail, orig_folder, target_folder, email_uid):

        if orig_folder.lower() == 'inbox':
            mail.select('"INBOX"')
        else:
            mail.select('"Google Alerts/{}"'.format(orig_folder))

        # result, data = mail.uid('search', None, "ALL")  # search and return uids instead
        #
        # resp, data = mail.fetch(email_uid, "(UID)")

        result = mail.uid('COPY', email_uid, '"Google Alerts/{}"'.format(target_folder))

        if result[0] == 'OK':
            mov, data = mail.uid('STORE', email_uid, '+FLAGS', '(\Deleted)')
            mail.expunge()

        else:
            print('mail was not moved. Something went wrong')

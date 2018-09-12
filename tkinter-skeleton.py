# Skeleton Tk interface example
# Written by Mike Fu
# Updated for python 3
#
#  python36
#  py36-numpy
#  py36-readline
#  py36-tkinter
#

'''
TO DO LIST

- implement the dialog box for classify emails
- Need ID for constituent

IDEAS FOR FUTURE

- Display words that are matched by that alumni
- Display words that the alumni is matched with

'''

import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox

import textwrap

import pandas as pd
import numpy as np
from sklearn.externals import joblib

from datetime import datetime

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import classifier
from scraper import Scraper
from emailreader import Emailreader

scraper = Scraper()
reader = Emailreader()
username = 'prospectstudent@colby.edu'
password = 'Student.2017'
mail = reader.login_email(username, password)

import os
import shutil

# create a class to build and manage the display
class DisplayApp:

    def __init__(self, width, height):

        # create a tk object, which is the root window
        self.root = tk.Tk()

        # width and height of the window
        self.initDx = width
        self.initDy = height

        # set up the geometry for the window
        self.root.geometry("%dx%d+50+30" % (self.initDx, self.initDy))

        # set the title of the window
        self.root.title("Automated Email Reader")

        # set the maximum size of the window for resizing
        self.root.maxsize(1600, 900)

        # declares global variables
        self.declareGlobalVars()

        # setup the menus
        self.buildMenus()

        # build the left panel
        # self.buildLeftPanel()

        # build the right panel
        self.buildRightPanel()

        # builds the main Panel
        self.buildMainPanel()

        # build the Canvas
        # self.buildCanvas()

        # bring the window to the front
        # self.root.lift()

        # - do idle events here to get actual canvas size
        # self.root.update_idletasks()

        # now we can ask the size of the canvas
        # print(self.canvas.winfo_geometry())

        # set up the key bindings
        self.setBindings()

    # initializes all the global variables
    def declareGlobalVars(self):

        # the current selected log to be analyzed
        self.current_log = None
        self.df = None

        # the canvas objects being shown in the main frame right now
        self.objs = []

        # matplotlib objects
        # self.canvas = FigureCanvasTkAgg(fig, master=self.leftmainframe)
        # self.canvas.show()
        # self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def buildMenus(self):

        # create a new menu
        menu = tk.Menu(self.root)

        # set the root menu to our new menu
        self.root.config(menu=menu)

        # create a variable to hold the individual menus
        menulist = []

        # create a file menu
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        menulist.append(filemenu)

        # create another menu for kicks
        cmdmenu = tk.Menu(menu)
        menu.add_cascade(label="Command", menu=cmdmenu)
        menulist.append(cmdmenu)

        # menu text for the elements
        # the first sublist is the set of items for the file menu
        # the second sublist is the set of items for the option menu
        menutext = [['conf', 'score', 'Quit  Ctl-Q'],
                    ['Clear', '-', '-']]

        # menu callback functions (note that some are left blank,
        # so that you can add functions there if you want).
        # the first sublist is the set of callback functions for the file menu
        # the second sublist is the set of callback functions for the option menu
        menucmd = [[self.handleConfidence, self.handleViewScore, self.handleQuit],
                   [self.clear, None, None]]

        # build the menu elements and callbacks
        for i in range(len(menulist)):
            for j in range(len(menutext[i])):
                if menutext[i][j] != '-':
                    menulist[i].add_command(label=menutext[i][j], command=menucmd[i][j])
                else:
                    menulist[i].add_separator()

    # create the canvas object
    def buildCanvas(self):
        self.canvas = tk.Canvas(self.root, width=self.initDx, height=self.initDy)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        return

    # handles the logic for when a widget is selected
    def onselect(self, event):
        w = event.widget

        # for when the logs listbox is selected
        if w == self.logs_lbox:
            index = int(w.curselection()[0])
            value = w.get(index)
            # print('You selected item %d: "%s"' % (index, value))
            self.current_log = 'logs/' + value
            self.df = pd.read_csv(self.current_log)

            self.buildBottomTable()

        # for when the bottom table is selected
        elif w == self.tree:
            self.refreshFrame(self.rightmainframe)

            curItem = self.tree.focus()
            row_num = self.tree.item(curItem)['text']
            scores = self.df[['Occupation score', 'Occupation score adjusted', 'Colby score']].iloc[row_num]

            # print(self.tree.item(curItem))

            scores_tree = ttk.Treeview(self.rightmainframe, height=1)

            # makes the identifier smaller
            scores_tree['show'] = 'headings'

            n = len(scores.index)
            scores_tree["columns"] = tuple(range(n))

            # sets the column headers
            for i, col in enumerate(scores.index):
                scores_tree.column(i, width=100, stretch=True, anchor='center')
                scores_tree.heading(i, text=col)

            scores_tree.insert('', 0, values=tuple(scores.values))

            scores_tree.pack(side=tk.TOP)



    # build a frame and put controls in it
    # CURRENTLY NOT BEING USED
    def buildLeftPanel(self):

        '''
        Contains Buttons that display the results of the classification
        '''

        ### Control ###
        # make a control frame on the left
        leftcntlframe = tk.Frame(self.root)
        leftcntlframe.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.Y)

        # make a separator frame
        sep = tk.Frame(self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.Y)

        # use a label to set the size of the left panel
        label = tk.Label(leftcntlframe, text="Control Panel", width=20)
        label.pack(side=tk.TOP, pady=10)

        # make a menubutton
        # self.colorOption = tk.StringVar(self.root)
        # self.colorOption.set("black")
        # colorMenu = tk.OptionMenu(leftcntlframe, self.colorOption,
        #                           "black", "blue", "red", "green")  # can add a command to the menu
        # colorMenu.pack(side=tk.TOP)

        ## Makes the buttons on the left control frame: Home, Logs, Scoring Metric, Time Usage, and Confidence Level

        leftbuttons = []    # list of button objects on the left side

        commands = [None, None, None, None, self.handleConfidence]  # the command tied to each button
        texts = ['Home', 'Logs', 'Scoring\nMetric', 'Time\nUsage', 'Confidence\nLevel']

        for text, com in zip(texts, commands):
            button = tk.Button(leftcntlframe, text=text, pady=15, height=1, width=10,
                               command=com)
            button.pack(side=tk.TOP)  # default side is top

            leftbuttons.append(button)

        return

    def buildRightPanel(self):

        '''
        Functions: Contains buttons to functions that help classify the emails
        '''

        rightcntlframe = tk.Frame(self.root)
        rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # make a separator frame
        sep = tk.Frame(self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # use a label to set the size of the right panel
        label = tk.Label(rightcntlframe, text="Right Panel", width=20)
        label.pack(side=tk.TOP, pady=10)

        # Makes the buttons on the right control frame:
        commands = [self.handleClassifyEmails, self.handleViewScore,
                    self.handleConfidence, self.handleDisplayCSV,
                    self.handleArchive]  # the command tied to each button

        texts = ['Classify\nEmails', 'View Scores',
                 'Confidence\nLevels', 'Raiser CSV',
                 'Archive Logs']     # Classify emails will bring up a pop menu that determines
                                                                      # how many emails to classify

        for text, com in zip(texts, commands):
            button = tk.Button(rightcntlframe, text=text, pady=15, height=1, width=10,
                               command=com)
            button.pack(side=tk.TOP)

        # creates listbox
        self.logs_lbox = tk.Listbox(rightcntlframe, selectmode=tk.SINGLE, name='logs_listbox')
        all_logs = sorted(os.listdir('logs/'), reverse=True)    # makes sure the most recent log is first
        for filename in all_logs:
            if filename.endswith('csv'):
                self.logs_lbox.insert(tk.END, filename)
        self.logs_lbox.pack(side=tk.TOP, pady=10)


    def buildMainPanel(self):

        '''
        Displays the main CSV file to be transported to Raiser Edge
        '''

        ### Builds the main panel, which will display the CSV to be uploaded to raisers edge

        self.mainframe = tk.Frame(self.root)
        self.mainframe.pack(side=tk.TOP, padx=2, pady=5, fill=tk.BOTH)

        self.bottomFrame = tk.Frame(self.root)
        self.bottomFrame.pack(side=tk.BOTTOM, padx=2, pady=5, fill=tk.BOTH)

        # builds tree
        # self.buildBottomTable()

        self.rightmainframe = tk.Frame(self.root, pady=10, padx=5)
        self.rightmainframe.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        # tk.Label(self.rightmainframe, text="", width=20).pack()

        self.leftmainframe = tk.Frame(self.root, pady=10)
        self.leftmainframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # self.leftmainframe.grid(row=0, column=0)


        # self.rightmainframe.lift()
        # self.leftmainframe.lift()

        # b = tk.Button(self.mainframe, text='Download CSV', pady=15, height=1, width=15)
        # b.pack(side=tk.TOP)

    def buildBottomTable(self):

        if isinstance(self.df, pd.DataFrame):

            # delete previous tables, if ones exist
            self.refreshFrame(self.bottomFrame)

            self.tree = ttk.Treeview(self.bottomFrame)

            # makes the identifier smaller
            self.tree['show'] = 'headings'

            # changes the row height
            s = ttk.Style()
            s.configure('Treeview', rowheight=30)

            def builddemotable():
                self.tree["columns"] = ("one", "two")
                self.tree.column(1, width=100)
                self.tree.heading(1, text="column A")
                self.tree.column("two", width=100)
                self.tree.heading("two", text="column B")

                self.tree.insert("", 0, text="Line 1", values=("1A", "1b"), tags='shaded')

                id2 = self.tree.insert("", 1, "dir2", text="Dir 2", values=('test a', 'test b'))
                self.tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A", "2B"))

                ##alternatively:
                self.tree.insert("", 3, "dir3", text="Dir 3", tags='shaded')
                self.tree.insert("dir3", 3, text=" sub dir 3", values=("3A", " 3B"))

            df = self.df.loc[:, ['id', 'time', 'first_name', 'last_name', 'confidence', 'label', 'moved', 'text']]

            # formats a long string to make it display better
            def process_text(string, length=50, total_string_size=100):
                string = string[:total_string_size]
                return '\n'.join(textwrap.wrap(string, length)) + '...'

            # preprocesses the dataframe
            df = df.rename(index=int, columns={'first_name': 'first', 'last_name': 'last', 'time': 'date'})  # make the columns shorter
            df['text'] = df['text'].apply(process_text)    # limits the characters in the text column
            df['confidence'] = df['confidence'].apply(lambda x: np.around(x, 3))    # rounds the confidence
            df['date'] = df['date'].apply(lambda x: x.split()[0])       # only shows the date and not the time

            # builds the columns and sets the width
            num_col = len(df.columns)
            self.tree['columns'] = tuple(range(num_col))
            for i, col in enumerate(df.columns):

                # give extra width to text
                width = 500 if col == 'text' else 100
                stretch = col == 'text'

                self.tree.column(i, width=width, minwidth=0, stretch=stretch)
                self.tree.heading(i, text=col)

            # builds the contents of the table
            for i, row in df.iterrows():
                shaded = 'even_row' if i % 2 == 0 else 'odd_row'
                self.tree.insert('', i, text=i, values=tuple(row), tag=shaded)

            # builddemotable()

            self.tree.tag_configure('even_row', background='lightgrey')
            self.tree.pack(fill=tk.X, padx=5, pady=5)

            # binds Button1 to the tree
            self.tree.bind('<<TreeviewSelect>>', self.onselect)


    def embedChart(self, master, fig=None, side=tk.TOP, legends=None, title=None):

        # delete previous graphs, if ones exist
        self.refreshFrame(master)

        if not fig:

            fig = Figure(figsize=(3, 3), dpi=100)
            ax = fig.add_subplot(111)

            data = (20, 35, 30, 35, 27)

            ind = np.arange(5)  # the x locations for the groups
            width = .5

            rects1 = ax.bar(ind, data, width)


        if legends:
            fig.legend()

        if title:
            fig.title(title)

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.show()
        canvas.get_tk_widget().pack(side=side, fill=tk.BOTH, expand=1)


        # toolbar = NavigationToolbar2TkAgg(canvas=canvas, window=master)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # updates canvas
        # master.lift()
        # master.update_idletasks()
        # self.root.update_idletasks()
        # self.rightmainframe.lift()

    def refreshFrame(self, frame, obj=None):
        '''
        deletes previous instances of a widget, or all widgets in a frame
        '''
        # delete previous obj, if ones exist
        window_children = frame.winfo_children()
        if window_children:
            for c in window_children:
                if obj:
                    if isinstance(c, obj):
                        c.destroy()
                else:
                    c.destroy()

    # uses a recursion method to clear all the frames
    def clear(self):

        for frame in [self.bottomFrame, self.leftmainframe, self.rightmainframe]:
            self.refreshFrame(frame)

        # def recursive_clear(parent_frame):
        #     window_children = parent_frame.winfo_children()
        #     if window_children:
        #         for c in window_children:
        #             # if isinstance(c, tk.Frame):
        #             #     recursive_clear(c)
        #             # else:
        #             #     c.destroy()
        #             c.destroy()
        #
        # recursive_clear(self.mainframe)
        # recursive_clear(self.bottomFrame)


    def setBindings(self):
        # bind command sequences to the root window
        self.root.bind('<Control-q>', self.handleQuit)

        # binds the logs listbox to onselect
        self.logs_lbox.bind('<<ListboxSelect>>', self.onselect)


    def handleQuit(self, event=None):
        print('Terminating')
        self.root.destroy()


    def handleViewScore(self):

        if self.current_log is None:
            messagebox.showwarning('Warning', 'Please select or create a valid log')
            return
        #
        # df = pd.read_csv(self.current_log)

        self.embedChart(self.leftmainframe)

    def handleDisplayCSV(self):
        if self.current_log is None:
            messagebox.showwarning('Warning', 'Please select or create a valid log')
            return

        raiser_df = classifier.create_csv_for_raiser(logs=self.current_log, return_merged_df=False)

        if raiser_df.empty:
            # No available data
            messagebox.showwarning('Warning', 'No data available to export to Raiser\'s Edge')
            return

        d = RaiserDialog(self.root, df=raiser_df, title='Raiser Edge CSV')

    def handleConfidence(self):
        if self.df is None:
            messagebox.showwarning('Warning', 'Please select or create a valid log')
            return

        fig = Figure(figsize=(3, 3), dpi=100)
        ax = fig.add_subplot(111)

        data = self.df['confidence']
        labels = self.df['label']

        ax.hist(data, bins=10, range=(0.5, 1))

        self.embedChart(self.leftmainframe, fig=fig)

        # print('children', self.rightmainframe.winfo_children())

        # self.rightmainframe.lift()
        # self.rightmainframe.update()

    def handleClassifyEmails(self):
        '''
        Classifies the emails and creates logs
        '''

        d = ClassifyDialog(self.root, title='Classify Emails Automatically')

        # adds the newest logs to
        try:
            self.logs_lbox.insert(0, d.filename)
        except AttributeError:  # if the user pressed cancel
            pass

        pass

    def handleArchive(self):
        '''
        Archives the emails from the logs to the archived_logs
        '''
        # saves paths for the logs
        filename = self.logs_lbox.get(self.logs_lbox.curselection()[0])
        print('filename', filename)
        current_path = 'logs/' + filename
        new_path = 'archived_logs/' + filename
        # move logs from logs/ to archived_logs/
        shutil.move(current_path, new_path)

        # deletes item from listbox
        item = self.logs_lbox.curselection()
        self.logs_lbox.delete(item)

        # refreshes frames
        for frame in self.leftmainframe, self.rightmainframe, self.bottomFrame:
            self.refreshFrame(frame)

        self.df = None
        self.current_log = None


    # def handleButton1(self):
    #     print('handling command button:', self.colorOption.get())
    #
    # def handleMenuCmd1(self):
    #     print('handling menu command 1')
    #
    # def handleMouseButton1(self, event):
    #     print('handle mouse button 1: %d %d' % (event.x, event.y))
    #     self.baseClick = (event.x, event.y)
    #
    # def handleMouseButton2(self, event):
    #     self.baseClick = (event.x, event.y)
    #     print('handle mouse button 2: %d %d' % (event.x, event.y))
    #
    # def handleMouseButton3(self, event):
    #     self.baseClick = (event.x, event.y)
    #     print('handle mouse button 3: %d %d' % (event.x, event.y))
    #
    # # This is called if the first mouse button is being moved
    # def handleMouseButton1Motion(self, event):
    #     # calculate the difference
    #     diff = (event.x - self.baseClick[0], event.y - self.baseClick[1])
    #
    #     # update base click
    #     self.baseClick = (event.x, event.y)
    #     print('handle button1 motion %d %d' % (diff[0], diff[1]))
    #
    # # This is called if the second button of a real mouse has been pressed
    # # and the mouse is moving. Or if the control key is held down while
    # # a person moves their finger on the track pad.
    # def handleMouseButton2Motion(self, event):
    #     print('handle button 2 motion %d %d' % (event.x, event.y))
    #
    # def handleMouseButton3Motion(self, event):
    #     print('handle button 3 motion %d %d' % (event.x, event.y))

    def main(self):
        print('Entering main loop')
        self.root.mainloop()


# Parent class for dialog box
class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title='Title'):
        self.usercancelled = False       # boolean that determines whether the user pressed the cancel button

        simpledialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        pass

    def apply(self):
        pass

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.apply()

        self.usercancelled = False      # user has not pressed cancel

        self.parent.focus_set()
        self.destroy()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.usercancelled = True       # user has not pressed cancel
        self.destroy()

# dialog box for displaying CSVs
class RaiserDialog(simpledialog.Dialog):

    def __init__(self, parent, csv_path=None, df=None, title='Title'):

        preset_path = 'raisers_edge/' + datetime.strftime(datetime.now(), '%Y-%m-%d') + '_raiser.csv'
        self.path = tk.StringVar(master=parent,
                                 value=preset_path,
                                 name='pathVar')    # path of raiser file to be exported

        if df is None:
            self.df = pd.read_csv(csv_path)
        else:
            self.df = df

        simpledialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        ## Builds the Table to display the CSV

        # builds two different frames
        top_frame = tk.Frame(master=master)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        bottom_frame = tk.Frame(master=master)
        bottom_frame.pack(side=tk.TOP)
        error_frame = tk.Frame(master=master)
        error_frame.pack(side=tk.BOTTOM)

        values = self.df.values

        # builds column and row names
        for c, col_name in enumerate(self.df.columns, start=1):
            tk.Label(top_frame, text=col_name).grid(row=0, column=c)

        for r, index_name in enumerate(self.df.index, start=1):
            tk.Label(top_frame, text=index_name).grid(row=r, column=0)

        # adds the values

        for i, val_row in enumerate(values, start=1):
            for j, val in enumerate(val_row, start=1):

                # reformat the string if it is the text column
                if isinstance(val, str):
                    val = val[:40] + '...'
                tk.Label(top_frame, text=val).grid(row=i, column=j)


        label = tk.Label(bottom_frame, text='Path: ')
        label.pack(side=tk.LEFT)


        e = tk.Entry(bottom_frame, textvariable=self.path, exportselection=0, width=35)
        e.pack(side=tk.LEFT)

        self.errorlabel = tk.Label(error_frame, text='Please make sure the filename ends in .csv',
                                   fg='red', font='Helvetica 10 italic')
        self.errorlabel.pack(side=tk.BOTTOM)
        self.errorlabel.pack_forget()

    def buttonbox(self):
        '''
        override if you do not want the standard buttons
        '''

        box = tk.Frame(self)

        w = tk.Button(box, text="Download", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def validate(self):
        try:
            if self.path.get()[-4:] == '.csv':
                return True
            else:
                self.errorlabel.pack()
                print('Please make sure the filename ends in .csv')
                return False
        except:
            # self.errorlabel.config(state=tk.NORMAL)
            return False

    def apply(self):
        '''
        Downloads the raiser edge csv into the folder called raisers_edge
        '''

        self.df.to_csv(self.path.get(), index=False)
        print('downloaded at ', self.path.get())


class ClassifyDialog(simpledialog.Dialog):

    def __init__(self, parent, title='Title'):

        self.folder = tk.StringVar(value='Priority Mail')
        self.cap_at = tk.IntVar(value=0)
        self.checked = tk.IntVar(value=1)

        simpledialog.Dialog.__init__(self, parent, title)

    def body(self, master):

        folders = ('Priority Mail', 'INBOX')
        tk.Label(master, text='Choose a Folder:').grid(row=0, column=0)
        menu = tk.OptionMenu(master, self.folder, *folders)
        menu.config(width=10)
        menu.grid(row=0, column=1)

        tk.Label(master, text='Classify How Many Emails:').grid(row=1, column=0)
        tk.Entry(master, textvariable=self.cap_at).grid(row=1, column=1)

        # tk.Label(master, text='Create Logs (Highly Recommended)').grid(row=2, column=0)
        # checkbutton = tk.Checkbutton(master, text='Create Logs (Highly Recommended)',
        #                              variable=self.checked)
        # checkbutton.grid(row=2, column=1)

    def validate(self):
        if self.checked.get() > 0:
            return True
        else:
            return False


    def apply(self):
        print('Classifying {} mails in the folder {}'.format(self.cap_at.get(), self.folder.get()))

        _, self.filename = classifier.classify_mails(mail, folder=self.folder.get(),
                                                     cap_at=self.cap_at.get(), log_data=True,
                                                     to_raiser=False, log_filename=True,
                                                     threshold=0.99)
        print('logs saved at' + self.filename)


if __name__ == "__main__":
    dapp = DisplayApp(1200, 675)
    dapp.main()


# Skeleton Tk interface example
# Written by Mike Fu
# Updated for python 3
#
#  python36
#  py36-numpy
#  py36-readline
#  py36-tkinter
#
import tkinter as tk

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
        self.root.title("Automated Email Project")

        # set the maximum size of the window for resizing
        self.root.maxsize(1600, 900)

        # setup the menus
        self.buildMenus()

        # build the controls
        self.buildControls()

        # build the Canvas
        self.buildCanvas()

        # bring the window to the front
        self.root.lift()

        # - do idle events here to get actual canvas size
        self.root.update_idletasks()

        # now we can ask the size of the canvas
        print(self.canvas.winfo_geometry())

        # set up the key bindings
        self.setBindings()

        # set up the application state
        self.objects = []  # list of data objects that will be drawn in the canvas
        self.data = None  # will hold the raw data someday.
        self.baseClick = None  # used to keep track of mouse movement


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
        menutext = [['-', '-', 'Quit  Ctl-Q'],
                    ['Command 1', '-', '-']]

        # menu callback functions (note that some are left blank,
        # so that you can add functions there if you want).
        # the first sublist is the set of callback functions for the file menu
        # the second sublist is the set of callback functions for the option menu
        menucmd = [[None, None, self.handleQuit],
                   [self.handleMenuCmd1, None, None]]

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

    # build a frame and put controls in it
    def buildControls(self):

        ### Control ###
        # make a control frame on the right
        rightcntlframe = tk.Frame(self.root)
        rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # make a separator frame
        sep = tk.Frame(self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # use a label to set the size of the right panel
        label = tk.Label(rightcntlframe, text="Control Panel", width=20)
        label.pack(side=tk.TOP, pady=10)

        # make a menubutton
        self.colorOption = tk.StringVar(self.root)
        self.colorOption.set("black")
        colorMenu = tk.OptionMenu(rightcntlframe, self.colorOption,
                                  "black", "blue", "red", "green")  # can add a command to the menu
        colorMenu.pack(side=tk.TOP)

        # make a button in the frame
        # and tell it to call the handleButton method when it is pressed.
        button = tk.Button(rightcntlframe, text="Press Me",
                           command=self.handleButton1)
        button.pack(side=tk.TOP)  # default side is top

        return

    def setBindings(self):
        # bind mouse motions to the canvas
        self.canvas.bind('<Button-1>', self.handleMouseButton1)
        self.canvas.bind('<Control-Button-1>', self.handleMouseButton2)
        self.canvas.bind('<Shift-Button-1>', self.handleMouseButton3)
        self.canvas.bind('<B1-Motion>', self.handleMouseButton1Motion)
        self.canvas.bind('<Control-B1-Motion>', self.handleMouseButton2Motion)
        self.canvas.bind('<Shift-B1-Motion>', self.handleMouseButton3Motion)

        # bind command sequences to the root window
        self.root.bind('<Control-q>', self.handleQuit)

    def handleQuit(self, event=None):
        print('Terminating')
        self.root.destroy()

    def handleButton1(self):
        print('handling command button:', self.colorOption.get())

    def handleMenuCmd1(self):
        print('handling menu command 1')

    def handleMouseButton1(self, event):
        print('handle mouse button 1: %d %d' % (event.x, event.y))
        self.baseClick = (event.x, event.y)

    def handleMouseButton2(self, event):
        self.baseClick = (event.x, event.y)
        print('handle mouse button 2: %d %d' % (event.x, event.y))

    def handleMouseButton3(self, event):
        self.baseClick = (event.x, event.y)
        print('handle mouse button 3: %d %d' % (event.x, event.y))

    # This is called if the first mouse button is being moved
    def handleMouseButton1Motion(self, event):
        # calculate the difference
        diff = (event.x - self.baseClick[0], event.y - self.baseClick[1])

        # update base click
        self.baseClick = (event.x, event.y)
        print('handle button1 motion %d %d' % (diff[0], diff[1]))

    # This is called if the second button of a real mouse has been pressed
    # and the mouse is moving. Or if the control key is held down while
    # a person moves their finger on the track pad.
    def handleMouseButton2Motion(self, event):
        print('handle button 2 motion %d %d' % (event.x, event.y))

    def handleMouseButton3Motion(self, event):
        print('handle button 3 motion %d %d' % (event.x, event.y))

    def main(self):
        print('Entering main loop')
        self.root.mainloop()


if __name__ == "__main__":
    dapp = DisplayApp(1200, 675)
    dapp.main()


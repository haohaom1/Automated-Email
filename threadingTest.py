import threading
import tkinter as tk
import time
import multiprocessing
import threading_timer
import sys
from datetime import datetime

class DisplayApp:

    def __init__(self, width=200, height=200):

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

        tk.Button(self.root, text='press me', command=self.bar2).pack()

    # @threading_timer.exit_after(3)
    def bar(self, arg):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            print("working on %s" % arg)
            break

        print("Stopping as you wish.")
        return

    def bar2(self):
        t = threading.Thread(target=self.bar, args=("task",))
        t.start()
        time.sleep(5)
        t.do_run = False
        t.join()

    def main(self):
        self.root.mainloop()


if __name__ == '__main__':
    dapp = DisplayApp()
    dapp.main()


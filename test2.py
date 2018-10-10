import tkinter as tk
import tkinter.ttk as ttk
import time
import threading

#Define your Progress Bar function,
def task(root):
    ft = ttk.Frame()
    ft.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
    pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
    pb_hD.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
    pb_hD.start(50)
    root.mainloop()

# Define the process of unknown duration with root as one of the input And once done, add root.quit() at the end.
def process_of_unknown_duration(root):
    time.sleep(5)
    print ('Done')
    root.destroy()

# Now define our Main Functions, which will first define root, then call for call for "task(root)" --- that's your progressbar, and then call for thread1 simultaneously which will  execute your process_of_unknown_duration and at the end destroy/quit the root.

def Main():
    root = tk.Tk()
    t1=threading.Thread(target=process_of_unknown_duration, args=(root,))
    t1.start()
    task(root)  # This will block while the mainloop runs
    t1.join()

#Now just run the functions by calling our Main() function,
if __name__ == '__main__':
    Main()
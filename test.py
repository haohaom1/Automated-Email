import multiprocessing
import time
import signal
import threading


# import multiprocessing
#
# def worker(procnum, return_dict):
#     '''worker function'''
#     print (str(procnum) + ' represent!')
#     return_dict[procnum] = procnum + 1
#
#
# if __name__ == '__main__':
#     manager = multiprocessing.Manager()
#     return_dict = manager.dict()
#     jobs = []
#     for i in range(5):
#         p = multiprocessing.Process(target=worker, args=(i,return_dict))
#         jobs.append(p)
#         p.start()
#
#     for proc in jobs:
#         proc.join()
#
#
#     print (return_dict.values())


# Your foo function
def foo(n):

    for i in range(100000 * n):
        print ("Tick")
        time.sleep(1)

def handler(signum, frame):
    print ("Forever is over!")
    raise RuntimeError("end of time")


for i in range(3):

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(2)

    try:
        foo(1)
    except Exception:
        print ('end of time')
    else:
        signal.alarm(0)

print('working threads', threading.enumerate())




#
# # if __name__ == '__main__':
# # Start foo as a process'
# def terminate_function(wait_time=5):
#     p = multiprocessing.Process(target=foo, args=(10,))
#     p.start()
#
#
#     # Wait a maximum of 10 seconds for foo
#     # Usage: join([timeout in seconds])
#     p.join(wait_time)
#
#     # If thread is active
#     if p.is_alive():
#         print ("foo is running... let's kill it...")
#
#         # Terminate foo
#         p.terminate()
#         p.join()
#
# terminate_function()



from sys import platform
from subprocess import check_output

if not platform == 'linux':
    import win32gui,win32process

from time import sleep
import psutil
import os


def get_pid(process):
    if not platform == 'linux':
        hwnd = win32gui.FindWindow(None, process)
        threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid
    else:
        pid = None

        for proc in psutil.process_iter():
            if process in proc.name():
                pid = proc.pid
                break

        return pid
    

def kill_peerflix():
    for x in range(20):
        try:
            PID = get_pid('peerflix') 

            if (PID) > 0:
                p = psutil.Process(PID)
                p.terminate()
                print('fim')
        except:
            pass


def start_peerflix(magnetic):
    kill_peerflix()
    sleep(5)
    magnetic = '"' + magnetic + '"'
    
    if not platform == 'linux':
        os.popen(f'start cmd /k peerflix {magnetic}')
    else:
        os.popen(f'peerflix {magnetic}')




    


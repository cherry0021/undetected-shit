import datetime
import random
import os
import time
import requests

def formatted_time(t, hours = False):
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    if hours:
        return '{:d}:{:02d}:{:02d}'.format(h, m, s)
    else: 
        return '{:02d}:{:02d}'.format(m, s)

def countdown(t, message='Waiting'):
    while t:
        mins, secs = divmod(t, 60) 
        hours, mins = divmod(mins, 60)
        timer = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs) 
        print(f'\r{message}: {timer}', end="") 
        time.sleep(1) 
        t -= 1
    print('')
    
def data_countdown(message='More Data Collected', time_gap=None):
    print(f'\r{message}', end="")
    
    if time_gap:
        time.sleep(time_gap)

def execution_time(start_time, message=''):
    print('\nExecution Completed\nReport:\n================================')  
    print('Execution time:', datetime.timedelta(seconds= int(time.time() - start_time)))

    if message:
        print(message)
        
def required_time(start_time, message='Required time'):
    print(f'{message} :', datetime.timedelta(seconds= int(time.time() - start_time)))

def what_is_my_ip():
    res = requests.get('https://api.ipify.org/?format=json')
    
    if res.status_code == 200:
        data = res.json()
        return data['ip']
    else:
        print("can't get api.ipify.org", res)
        return None
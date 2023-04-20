

from flask import Flask, request
import random
import json
# from gates.gate02 import check
# from bins import mydict, get_bin_info
import re
from pydantic import BaseModel, Json
# from py_adyen_encrypt import encryptor
import urllib
import asyncio
from urllib.parse import unquote
from gates.dax import process_all as dax_process_all
from playwright.sync_api import sync_playwright
from playwright_recaptcha import recaptchav2
from lumi import Lumi
import string
import tempfile
import json
import psutil
from gates.utils.browser_profile import generate_profile


def terminate_session():
    for proc in psutil.process_iter():
        try:
            if 'firefox' in proc.name() and 'playwright' in ' '.join(proc.cmdline()):
                print('Firefox with Playwright is running')
                proc.kill()
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    else:
        print('Firefox with Playwright is not running')

terminate_session()
profile = generate_profile()
#----------endpoints functions----------
def daxko_gate(card):
    return  json.dumps(dax_process_all(card, profile))   

app = Lumi()



# @app.route("/")
# async def start():
#     return "HELLO !"



# class daxko_info():
#     card: str
#     gate_info: str
#     user_info: str
# def daxs(a, b):
#     return a + b

app.register(daxko_gate, route="/daxko")






app.runServer(host="0.0.0.0", port=8585, threads=16)




















# def daxko():
#     daxko_info = request.get_json()
#     response =  process_check(daxko_info['card'])
#     respo = response
#     result = None
#     message = None
#     response_json = None
#     info = f"Target card -> {daxko_info['card']}"
    
#     if '"success":true' in str(respo):
#         result = "Approved"
#         message = "This card is live and working."
#     elif '"success":false' in str(respo):
#         result = "Declined"
#         message = respo
#     else: 
#         result = "Error"
#         message = "There's something error while checking. please try again."
    
#     response_json = {'"result"': result,
#             '"Message"': message, 
#             '"info"': info}    
#     return json.dumps(response_json)
    
# if __name__ == "__main__": 
#     app.run()

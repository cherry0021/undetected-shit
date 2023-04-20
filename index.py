

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
from gates.dax import process_check as dax
from playwright.sync_api import sync_playwright
from playwright_recaptcha import recaptchav2
from lumi import Lumi
import json

def daxko(card):
    return  json.dumps(dax(card))   

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

app.register(daxko, route="/daxko")


app.runServer(host="0.0.0.0", port=8585)
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

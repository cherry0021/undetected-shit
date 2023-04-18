import argparse
import asyncio
from re import escape
from utils.proxy_manager import get_enumproxy
from fake_useragent import UserAgent
from playwright.async_api import Playwright, async_playwright, expect

ua = UserAgent()

args = [
                "--deny-permission-prompts",
                "--no-default-browser-check",
                "--no-first-run",
                "--deny-permission-prompts",
                "--disable-popup-blocking",
                "--ignore-certificate-errors",
                "--no-service-autorun",
                f"--user-agent={ua['Firefox']}",
                "--headless=new", 
                "--view_port=640,480",
                ]

proxy = {"server": "http://"+get_enumproxy()}
async def run(playwright: Playwright) -> None:
    browser = await playwright.firefox.launch(headless=False,
                    proxy=proxy, args=args )
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://store.pariyatti.org/one-time-donation")
    cc_locator = await page.query_selector_all("div[class='sumome-react-wysiwyg-component sumome-react-wysiwyg-outside-horizontal-resize-handles sumome-react-wysiwyg-outside-vertical-resize-handles sumome-react-wysiwyg-close-button sumome-react-wysiwyg-popup-image sumome-react-wysiwyg-image'] div[class='sumome-react-wysiwyg-move-handle'] div div")
    await cc_locator()
    
    await page.frame_locator("iframe[name=\"giveforms\"]").locator("span").filter(has_text="Custom Amount").click()
    await page.frame_locator("iframe[name=\"giveforms\"]").get_by_label("Custom Amount").fill("5")
    await page.locator("div:nth-child(10) > .sumome-react-wysiwyg-move-handle > div > div").click()
    await page.frame_locator("iframe[name=\"giveforms\"]").locator("label").filter(has_text="By submitting this form I accept that my data will be managed in accordance with").click()
    await page.frame_locator("iframe[name=\"giveforms\"]").get_by_role("button", name="Next Step").click()
    await page.frame_locator("iframe[name=\"giveforms\"]").get_by_label("First Name (*)").click()
    await page.frame_locator("iframe[name=\"giveforms\"]").get_by_label("First Name (*)").fill("asdasda")
    await page.frame_locator("iframe[name=\"giveforms\"]").get_by_label("Last Name (*)").click()    
    await page.frame_locator("iframe[name=\"giveforms\"]").get_by_label("Last Name (*)").fill("dasdsad")
    await page.frame_locator("iframe[name=\"giveforms\"]").locator("#gf-input-email123").click()
    await page.frame_locator("iframe[name=\"giveforms\"]").locator("#gf-input-email123").fill("asdasda@gmail.com")
    await page.frame_locator("iframe[name=\"giveforms\"]").get_by_role("button", name="Next Step").click()

    
    # await page.frame_locator("iframe[name=\"giveforms\"]").frame_locator("iframe[name=\"__privateStripeFrame16818\"]").get_by_placeholder("MM/YY").click()
    # await page.frame_locator("iframe[name=\"giveforms\"]").frame_locator("iframe[name=\"__privateStripeFrame16818\"]").get_by_placeholder("MM/YY").fill("12 / 22")
    # await page.frame_locator("iframe[name=\"giveforms\"]").frame_locator("iframe[name=\"__privateStripeFrame16818\"]").get_by_placeholder("MM/YY").click()
    # await page.frame_locator("iframe[name=\"giveforms\"]").frame_locator("iframe[name=\"__privateStripeFrame16818\"]").get_by_placeholder("MM/YY").fill("12 / 25")
    # await page.frame_locator("iframe[name=\"giveforms\"]").frame_locator("iframe[name=\"__privateStripeFrame16818\"]").get_by_placeholder("MM/YY").press("Tab")
    # await page.frame_locator("iframe[name=\"giveforms\"]").frame_locator("iframe[name=\"__privateStripeFrame16819\"]").get_by_role("textbox", name="Credit or debit card CVC/CVV").fill("000")
    # await page.frame_locator("iframe[name=\"giveforms\"]").get_by_role("button", name="Donate $5.00 Now").click()

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
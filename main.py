import json
import os
import time

import datetime

import pytz
from playwright.async_api import async_playwright, TimeoutError
import asyncio
import requests
from loguru import logger as log

# Configure the logger with a minimum level and additional filtering
log.add("app.log", level="DEBUG", rotation="1 MB", compression="zip", backtrace=True, diagnose=True)
log.add("app.log", level="INFO", filter=lambda record: record["level"].name == "INFO")

bidding_result = {}  # This contain the Bidding result....

support = "https://t.me/Aladdin_payment_bot"

developer = f"<b><a href='{support}'>Use this link</a></b>"
bot_token = "BOT TOKEN"
note = "<i>(🔖Please Note The Developer have resrticted bidding to your setting only)</i>"


async def get_user_data(page):
    # bidding_result["User Info"] = {}

    user_info = {}

    # Locate the user name and user ID from the HTML provided

    # Get the user name from the class attribute inner text
    username = '.username'
    await page.wait_for_selector(username, timeout=1000)
    username_element = await page.query_selector(username)
    user_info["User Name"] = await username_element.inner_text()

    # Locate the user ID from the class attribute user_id
    user_id = '.userid'
    await page.wait_for_selector(user_id)
    user_id_element = await page.query_selector(user_id)
    user_info["User ID"] = await user_id_element.inner_text()

    # Get the Genie Point, Genie Wallet, and Flexi Wallet values

    # Locate the user details rows with class attribute "user-details-row"
    user_details_row = '.user-details-row'
    await page.wait_for_selector(user_details_row, timeout=1000)
    user_details_elements = await page.query_selector_all(user_details_row)

    for user_details in user_details_elements:
        # Get the title and value in each "h5" tag in the user details row
        title_element = await user_details.query_selector('.user-details-title')
        value_element = await user_details.query_selector('.user-details-value')

        title = await title_element.inner_text()
        value = await value_element.inner_text()

        user_info[title] = value

    # # Convert user_info to a JSON string
    # user_info_json = json.dumps(user_info)
    print(user_info)
    return user_info


def get_gmt_time():
    utc_now = datetime.datetime.utcnow()  # Get the current UTC time
    gmt = pytz.timezone('GMT')  # Define the GMT timezone
    gmt_now = utc_now.astimezone(gmt)  # Convert UTC to GMT
    formatted_time = gmt_now.strftime("%B %d, %Y %H:%M:%S GMT")  # Format the time as a string
    day_of_week = gmt_now.strftime("%A")  # Get the day of the week as a string
    return formatted_time, day_of_week


async def format_user_info_html(page):
    user_info = await get_user_data(page)

    user_info_html = f"""
<b>👨🏾‍💼Acount Details</b>:\n
<b>User Name: </b> {user_info['User Name']}\n
<b>User ID: </b> {user_info['User ID']}\n
<b>Genie Point: </b> {user_info['Genie Point']}\n
<b>Genie Wallet: </b> {user_info['Genie Wallet']}\n
<b>Flexi Wallet: </b> {user_info['Flexi Wallet']}
    """
    return user_info_html


def bidding_result_html():
    info = f"""
<b>GP Quantity:</b> {bidding_result.get("GP_QUANTITY")}

<b>GP Amount:</b> {bidding_result.get("Gp_Type")}

<b>GP ROI:</b> {bidding_result.get("GP_ROI")}

<b>GP PLUS:</b> {bidding_result.get("GP_PLUS")}
    """

    return info


def send_message_user(chat_id, message):
    parse_mode = "HTML"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode  # Include parse_mode field if provided
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        log.info("User Message sent successfully!")

    except Exception as e:
        print(e)
    # except requests.exceptions.RequestException as e:
    #     log.error("Failed to send the message to user error:", e)


def send_message_developer(message):
    parse_mode = "HTML"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    chat_id = "-934294168"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        log.info("Developer  Message sent successfully!")
    except requests.exceptions.RequestException as e:
        log.error("Failed to send the message to user error: ", e)






async def accept_alert(page, chat_id):
    """
    Check if an alert dialog is present on the page and close it.

    if there is not the code continues
    """
    try:
        close_button_selector = "button[data-dismiss='modal']"

        await page.wait_for_selector(close_button_selector)



        for _ in range(10):

            close_button = await page.query_selector(close_button_selector)

            print("Attempting to Closing Modals....", "close Button selector is :", close_button)

            if close_button:
                await close_button.click(force=True)
                print("Closing Modals....")
                await asyncio.sleep(.01)

                if await close_button.is_visible():
                    print("Button is still visible after clicking.")
                else:
                    print("Button is no longer visible after clicking.")
                    log.info("Done Closing Advertisement, Proceeding......")
                    break

            else:
                log.info("Done Closing Advertisement Proceding......")
                break
...


"""
The Rest of the code in not here if you need it please contact me

akinloluojo1@gmail.com



"""

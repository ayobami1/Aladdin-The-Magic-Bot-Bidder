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
bot_token = "6416467738:AAFXTFBy0XpxRbVo2SUNJ5UnEcf-FKbI134"
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





        # await page.wait_for_selector(close_button_selector)
        # close_button = await page.query_selector(close_button_selector)


                #     pass
        # while not await page.query_selector(close_button_selector):
        #     close_button = await page.query_selector(close_button_selector)
        #
        #     # print(close_button)
        #
        #     if close_button:
        #         await close_button.scroll_into_view_if_needed()
        #         await close_button.click(force=True)
        #         log.info("Closing Modals")
        #         await asyncio.sleep(.01)
        #     else:
        #         log.error("Close button not found!")
        #         break
        #
        # log.info("Modal closed completely Now other can run ")
        #
        # return True


    except TimeoutError as t:
        log.info("The Time to process to wait for the modeal button to be visible has passed !")

    except Exception as e:
        log.error(f"No modal to close at this time Modal is a kind of advert continue ! {e}")
        send_message_developer("<b>NOTIFICATION</b>\n There is a Timeout 30 Sec after trying to Close the Ads so is either there is no ads or there is an Error")
        send_message_user(chat_id=chat_id, message=f"ERROR: \n\nPlease send this message to the developer {developer} Message -- <b>NOTIFICATION</b>\n There is a Timeout 30 Sec after trying to Close the Ads so is either there is no ads or there is an Error")

        return False





#
# async def accept_alert(page, chat_id):
#     """
#     Check if an alert dialog is present on the page and close it.
#
#     if there is not the code continues
#     """
#     try:
#         close_button_selector = "button[data-dismiss='modal']"
#         await page.wait_for_selector(close_button_selector)
#         close_button = await page.query_selector(close_button_selector)
#
#         while await close_button.is_visible():
#             close_button = await page.query_selector(close_button_selector)
#
#             # print(close_button)
#
#             if close_button:
#                 await close_button.scroll_into_view_if_needed()
#                 await close_button.click(force=True)
#                 log.info("Closing Modals")
#                 await asyncio.sleep(.01)
#             else:
#                 log.error("Close button not found!")
#         log.info("Modal closed completely Now other can run ")
#
#         return True
#
#     except Exception as e:
#         log.error(f"No modal to close at this time Modal is a kind of advert continue ! {e}")
#         send_message_developer(
#             "<b>NOTIFICATION</b>\n There is a Timeout 30 Sec after trying to Close the Ads so is either there is no ads or there is an Error")
#         send_message_user(chat_id=chat_id,
#                           message=f"ERROR: \n\nPlease send this message to the developer {developer} Message -- <b>NOTIFICATION</b>\n There is a Timeout 30 Sec after trying to Close the Ads so is either there is no ads or there is an Error")
#
#         return False
#

async def magic_clicker(page, gp_amount, gp_quantity, gp_plus, chat_id, gp_plus_btn):
    """
    Perform the magic clicker operation to bid with the specified GP amount and quantity.

    Args:
        page: The Playwright page instance.
        gp_amount: The GP amount to bid (default is 50.0) (Float).
        gp_quantity: The quantity between 1-10 (default is 1) (int) .
    """

    "Set the Gp Qunatitiy in the bidding Result dict"
    bidding_result["GP_QUANTITY"] = gp_quantity

    # We set the Default to 50.0
    if not isinstance(gp_amount, float):
        gp_amount = float(50.0)

    # we also set the defalt to 1
    if not isinstance(gp_quantity, int):
        gp_quantity = int(1)

    # since we are first looking for gp plus we set the Gp Amount to be Equals to Gp Plus to search

    if gp_plus_btn:
        gp_amount = gp_plus

    "Before scrolling into view Close every Advertisement modal "

    # # this  is used to close the advert buttons
    # await accept_alert(page, chat_id)

    "Then Scroll into View , like scrol down"
    # js_scroll_down = "window.scrollBy(0, window.innerHeight);"
    # await page.evaluate(js_scroll_down)
    # await asyncio.sleep(1)

    "Define the Consign, Confirm and Okay Button in a single function"

    async def consign_confirm_bids_button():
        # Wait for the Consign Buttons and confirm buttons

        confirm_btn_selector = 'button.primary-btn.confirmation-btn'
        await page.wait_for_selector(confirm_btn_selector, timeout=3000)
        await page.click(confirm_btn_selector)

        consign_btn_selector = 'button.primary-btn[onclick*="getROI"]'
        await page.wait_for_selector(consign_btn_selector, timeout=3000)
        await page.click(consign_btn_selector)

        ok_btn_selector = 'button.primary-btn[onclick*="reloadmyurl"]'
        await page.wait_for_selector(ok_btn_selector, timeout=3000)
        await page.click(ok_btn_selector)

    async def click_bidding_button(found_card, index, chat_id):

        try:

            # Click instantly on the Bidding button
            bidding_btn = f'button.btn.primary-btn.w-100.submitSnatch-{index}'
            # await page.wait_for_selector(bidding_btn)
            await page.click(bidding_btn)

            """
            Now we have Updated annoucement that involve Two new buttons # Genie point and Genie Plus piont Wallet
            """

            # We first check the Genie Point Wallet
            try:

                if not gp_plus_btn:

                    log.info("Bidding using GP_Point_btn")
                    Genie_point_id = "#confirmation_genie_point"  # Locate the Genie point Button and click it
                    await page.wait_for_selector(Genie_point_id, timeout=3000)
                    await page.click(Genie_point_id)

                # then Click the

                else:

                    log.info("Bidding Using gp_plus_btn")
                    Genie_point_plus_id = "#confirmation_free_credit"

                    await page.wait_for_selector(Genie_point_plus_id, timeout=3000)
                    await page.click(Genie_point_plus_id)

            except Exception as e:

                send_message_user(chat_id,
                                  message=f"Error : Please send this error to the Developer {developer}\nMessage {str(e)} Seems the Button after Clicking Bidding Button Issue ")
                send_message_developer(message=f"issue with the Bidding After clicking bidding buttton {str(e)}")

            # Wait for the Consign Buttons and confirm buttons
            await consign_confirm_bids_button()
            # await asyncio.sleep(1)

            return True

            # The First thing we do here after clicking the bidding button is we wait wait for the
            # Dialogue box to be Shown most times it is Insufficeint or too much to bid for
            # Any how once we have error we close it with the okay button in p#NewFailedmsgg tag


        except TimeoutError as e:
            print("Error message element not found within 3 seconds. Proceeding with the rest of the code.")

            try:
                error_message_selector = 'p#NewFailedmsgg'
                await page.wait_for_selector(error_message_selector)
                error_message_element = await page.query_selector(error_message_selector)

                if await error_message_element.is_visible():
                    error_message_text = await error_message_element.inner_text()
                    log.error(f"Error message: {error_message_text}")

                    # cehck if we have use gp_plus_btn or not if then send message only base on the GP_PLus

                    if gp_plus_btn:
                        send_message_user(chat_id=chat_id,
                                          message=f"🔔 <b>GP PLUS NOTIFICATION</b>:\n\nError message: 🛑 {error_message_text} <i>\n\n(Please check your GP Plus balance the amount you can bid must be equivalanet to your Gp Plus balance)</i>\n\nGP Plus : {gp_plus}\n\n{'-' * 60}{await format_user_info_html(page)}")
                    else:
                        send_message_user(chat_id=chat_id,
                                          message=f"🔔 <b>GP POINT NOTIFICATION</b>:\n\nError message: 🛑 {error_message_text} <i>\n\n(Please check your balance the amount you can bid must be equivalanet to your balance)</i>\n\nGP Point : {gp_amount}\n\n{'-' * 60}{await format_user_info_html(page)}")

                    # close the modal error
                    button_selector = '[onclick="reloadmyurl(\'NewFailedModal\')"]'
                    await page.click(button_selector)
                else:
                    print("Not Visible")

            except Exception as e:
                send_message_user(chat_id, message=str(e))
                log.info(e)
                return False

    async def enter_bidding_amount(gp_amount, found_card, index, chat_id):
        # We access the snatch card the input box to type in the bidding
        # print(index)
        try:
            bidding_result["GP_AMOUNT"] = gp_amount

            await found_card.wait_for_selector(f'.input-box.input-key{index}')
            input_element = await found_card.query_selector(f'.input-box.input-key{index}')

            if input_element:
                await input_element.fill("")
                await input_element.fill(str(gp_amount))
                if await click_bidding_button(found_card, index, chat_id=chat_id):
                    log.info(
                        f"🔔 NOTIFICATION: \nCongratulations!💎you just Bidded. Here are your details: {bidding_result}")

                    # Check if gp Plus btn is true

                    if gp_plus_btn:
                        send_message_user(chat_id,
                                          message=f"🔔 <b>GP PLUS NOTIFICATION</b>: \n\n<b>Congratulations!💎</b>\n\nYou just Bidded for your GP PLus Wallet. Here are your details:\n{bidding_result_html()}\nPlease cross-check your Account to make sure your Bids correlate.\n\n{'-' * 60}{await format_user_info_html(page)}")
                    else:
                        send_message_user(chat_id,
                                          message=f"🔔 <b>GP POINT NOTIFICATION</b>: \n\n<b>Congratulations!💎</b>\n\nYou just Bidded For your GP Point wallet. Here are your details:\n{bidding_result_html()}\nPlease cross-check your Account to make sure your Bids correlate.\n\n{'-' * 60}{await format_user_info_html(page)}")

                    return True
            else:
                return False
        except Exception as e:
            log.error(f"No .input-box.input-key{index} Element is available at this time --> {e} ")

    async def is_bidding_button_clickable(found_card):

        try:

            await found_card.wait_for_selector('.btn.primary-btn')
            card_btn = await found_card.query_selector('.btn.primary-btn')
            # print(await card_btn.inner_text())

            card_btn_att = await card_btn.get_attribute("class")
            # print(card_btn_att)

            if "grey-btn" in str(card_btn_att.strip()):
                "The found Card has not a clickable button so return false to keep searching!"
                # print("Not Clickable")
                return False
            else:

                # The found Card has a clickable button
                # print("Confirm")
                return True, card_btn
        except Exception as e:
            log.error(
                f"We could not found .btn.primary-btn' which is responsible for checking if a button is clickable or not --> {e} ")

            send_message_user(chat_id, message=f"Error: {e}\n you can re schedule of forward to Developer {developer}")

    try:

        """
        This function starts the magic clicker operation by first looking for the snatch card on the page.
        If a snatch card is found, it proceeds to execute other functions like:
        1. is_bidding_button_clickable(card): to check if the bidding button is clickable.
        2. enter_bidding_amount(gp_quantity, found_card, index=card_index, chat_id=chat_id): 
           to enter the GP quantity and prepare for bidding.
        3. click_bidding_button(): to consign and place the bid.

        If a snatch card is not found or no suitable card is found with the entered GP amount,
        it will handle the situation and return appropriate messages.
        """

        try:
            # await asyncio.sleep(2)
            cards = await page.query_selector_all('div.col-6.col-xl-3.col-lg-6')
            # wait = await page.wait_for_selector('div.col-6.col-xl-3.col-lg-6')

        except Exception as e:
            log.error(f"Hey Dear user I have check there is no snatch card to bid\nThat is the affiliate bid \
            is empty today I will be back tomorrow ")

            if gp_plus_btn:

                send_message_user(chat_id=chat_id,
                                  message=f"🔔 <b>GP PLUS NOTIFICATION</b>:\n\nHey Dear  user, \nAfter trying to bid i found out there is no snatch card to bid At the moment\nI will be back Later or Re schedule to better timing")

                send_message_developer(
                    message=f"🔔 <b>GP PLUS NOTIFICATION</b> This user have  issue with Snatch card not visible")
            else:
                send_message_user(chat_id=chat_id,
                                  message=f"🔔 <b>GP POINT NOTIFICATION</b>:\n\nHey Dear  user, \nAfter trying to bid i found out there is no snatch card to bid At the moment\nI will be back Later or Re schedule to better timing")

                send_message_developer(
                    message=f"🔔 <b>GP POINT NOTIFICATION</b>This user have  issue with Snatch card not visible")

            # Call the the function to send request update to telegram users

            return

        # print("Total number of Cards ", len(cards), "\n\n")
        found_card = None
        card_index = 0
        track_gp = {}

        for index, card in enumerate(cards):
            snatch_card = await card.query_selector('div.snatch-card')
            gp_type = await snatch_card.query_selector('h4')
            gp_roi = await snatch_card.query_selector("h5")
            gp_type_text = await gp_type.inner_text()  # Get the inner text

            if gp_plus_btn:

                bidding_result["Gp_Type"] = None  # await gp_type.inner_text()
                bidding_result["GP_ROI"] = await gp_roi.inner_text()
                bidding_result["GP_PLUS"] = gp_type_text  # await gp_type.inner_text()

            else:
                bidding_result["Gp_Type"] = gp_type_text  # Use the stored inner text
                bidding_result["GP_ROI"] = await gp_roi.inner_text()
                bidding_result["GP_PLUS"] = None

            gp_amount_from_card = float(gp_type_text.replace(' GP', ""))
            # print("gp_amount_from_card: ", gp_amount_from_card, "\nGp_input_amount", gp_amount)

            track_gp[f"GP AMOUNT FROM CARD {index}"] = gp_amount_from_card
            track_gp[f"USER GP INPUT AMOUNT {index}"] = gp_amount
            # log.info(f"GP AMOUNT FROM CARD : {gp_amount_from_card},  USER GP INPUT AMOUNT : {gp_amount} ")

            """

           Check if the input GP amount matches the GP amount on the snatch card.
           If the amounts match, check if the bidding button is clickable.
           The is_bidding_button_clickable(card) function checks the button's status.
           If the button is red, it is clickable; if it is grey, it is not clickable.

           """
            await asyncio.sleep(1)
            if gp_amount == gp_amount_from_card and await is_bidding_button_clickable(card):
                found_card = card
                card_index = index

                break
            else:

                track_gp[f"GP AMOUNT FROM CARD {index}"] = gp_amount_from_card
                track_gp[f"USER GP INPUT AMOUNT {index}"] = gp_amount

            #    pass

        log.info(f"RESULT FROM TRACK SNATCH GP : {track_gp}")

        if found_card:

            # If a suitable card is found, enter the bidding amount and proceed to bid
            await enter_bidding_amount(gp_quantity, found_card, index=card_index, chat_id=chat_id)
        else:
            # If no suitable card is found, print a message and return appropriate feedback
            log.info(f"No card found with the entered GP amount: {gp_amount}")
            if gp_plus_btn:
                send_message_user(chat_id=chat_id,
                                  message=f"🔔 <b>GP PLUS NOTIFICATION</b>: \n\nError Message: \n\nHey check your Profile setting and Update it seems there is no value that matches {gp_plus} GP you have saved  or it exit  and is not clickable is not available or Talk to the Developer {developer}\n\nOr you can wait for the next one hour\n\n{note}\n{'*' * 30}\nRESULT FROM TRACK SNATCH GP : {track_gp}")
            # return f"There is no value that matches {gp_amount} and the clickable is not available"
            else:
                send_message_user(chat_id=chat_id,
                                  message=f"🔔 <b>GP POINT NOTIFICATION</b>: \n\nError Message: \n\nHey check your Profile setting and Update it seems there is no value that matches {gp_amount} GP you have saved  or it exit  and is not clickable is not available or Talk to the Developer {developer}\n\nor you can wait for the next one hour\n\n{note},\n{'*' * 30}\nRESULT FROM TRACK SNATCH GP : {track_gp}")



    except Exception as e:
        print(e)
        log.error("From the Magic Click ", str(e))
        send_message_developer("from magic clicker there is a pro with Snatch cards")
        pass


async def bot_operation(page, gp_amount, gp_quantity, gp_plus, chat_id,genei_point):
    try:

        # Navigate to the Affilaite link
        # await page.wait_for_selector('li.morph-text a[href="https://38aladdin.shop/home/member"]', timeout=60000)
        await page.click('li.morph-text a[href="https://38aladdin.shop/home/member"]')

        # await asyncio.sleep(1)

        # await get_user_data(page)

        # log the User  data on the Screem
        # print(await get_user_data(page))
        if not genei_point:
            # Start the Magic Clicking
            # this  is used to close the advert buttons
            await accept_alert(page, chat_id)
            await magic_clicker(page, gp_amount, gp_quantity, gp_plus, chat_id=chat_id, gp_plus_btn=True)

            # "We need to Reload page and Close any Advertisement"
            # await  page.reload(timeout=60000, wait_until='load')

            # asyncio.sleep()

        # Start the Magic Clicking
        else:
            await accept_alert(page, chat_id)
            await magic_clicker(page, gp_amount, gp_quantity, gp_plus, chat_id=chat_id, gp_plus_btn=False)
            return True
    except Exception as e:
        log.info(e)
        send_message_user(chat_id,
                          message=f"Please Send this Notification to the Dev ASAP {developer}\n\n ERROR : `Affiliate Button not Clickable li.morph-text a[href=\"https://38aladdin.shop/home/member\"] `")
        return False


async def login_user(page, email, password, chat_id, user_name):
    """
    Log in the user with the specified email and password.

    Args:
        page: The Playwright page instance.
        email: The email to log in (default is "babaneeh17@gmail.com").
        password: The password to log in (default is ""babanee94"").
    """
    js_click_login_button = """
    const loginButton = document.querySelector('button.submit_btn.btn.btn-primary.btn-block');
    if (loginButton) {
      loginButton.click();
      true; // Return true if the element was found and clicked
    } else {
      false; // Return false if the element was not found
    }
    """

    try:
        await page.fill('input[name="identity"]', "")  # Clears the email input box
        await page.type('input[name="identity"]', email)  # , delay=20)

        await page.fill('input[name="password"]', "")  # Clears the password input box
        await page.type('input[name="password"]', password)  # , delay=20)

        login_button_clicked = await page.evaluate(js_click_login_button)
        if login_button_clicked:
            print("Login button clicked successfully!")
        else:
            print("Login button not found!")
            send_message_user(chat_id,
                              message=f"There was an error while login you in please forward this message to <b><a href='{support}'>this link</a></b> --- `Error After Clicking the Login Button`")

        # Add a small delay after clicking the login button to allow the page to load
    # await page.wait_for_timeout(1000)  # Adjust the delay time as needed (e.g., 1000ms = 1 second)

    except Exception as e:
        log.info("Error During Loggin in :", e)
        send_message_user(chat_id,
                          message=f"There was an error while login you in please forward this message to <b><a href='{support}'>this link</a></b> --- `Error After Clicking the Login Button`")

    try:

        # Now we will check if the Login is successful or if success continue
        # if not Success or inncorret password we will notify the user of the issues

        error_box_selector = 'div#error_box'
        # error_box = await  page.query_selector(error_box_selector)
        # if await page.wait_for_selector(error_box_selector):
        await page.wait_for_selector(error_box_selector)
        error_box_element = await page.query_selector('div#error_box')
        error_message = await error_box_element.inner_text()
        error_message = error_message.strip().lower()
        # print("FROM THE ERROR TAG :.", error_message)

        if error_message == "logged in successfully":

            return True


        elif error_message == "temporarily locked out. try again later.":
            print("Login is Temporarily locked  Please try again.", error_message)
            message = f"🔔 <b>NOTIFICATION</b>: \n\nHey while trying to  login i encounter this error:  {error_message}\n\nReason: You have try an incorrect Login more that three times\n\nPlease wait some more and or reschedule in one hour time"
            send_message_user(chat_id, message=message)
            send_message_developer(message=f"{chat_id} could not log in {user_name} because of {error_message}")

            return False

        else:
            print("Login was not successful. Please try again.", error_message)
            message = f"🔔 <b>NOTIFICATION</b>: \n\nHey while trying to  login i enounter this error:  {error_message}\n\nPlease Check your Email and Password properly"
            send_message_user(chat_id, message=message)
            send_message_developer(message=f"{chat_id} could not log in {user_name}")

            return False





    except Exception as e:

        message = f"🔔 <b>NOTIFICATION</b>: \n\nHey while trying to  login i enounter this error: `Error box not found within 3 seconds. Retry and check your password.`\n\nPlease Check your Email and Password properly"
        send_message_user(chat_id, message=message)
        send_message_developer(message=message)

        # return False


async def main(headless, email: str, password: str, gp_amount: float, gp_quantity: int, user_id, user_name, gp_plus,genei_point):
    """


    :param headless:  playwright page instances
    :param email:  the is  a str for user email
    :param password: this is a str for user password
    :param gp_amount: This is a float it must be float (default is 50.0)
    :param gp_quantity: This is int the quantity want to bid for (default is 1)
    :return: returns nothing
    """

    async with async_playwright() as p:
        """ Save the Browser cache To a caching Directory"""
        user_data_dir = "browsing_restricted_ip"
        "LOAD THE PROXIES"
        start_time = time.time()

        browser = await p.chromium.launch()
        browser = await browser.new_context()

        # Grant permission to the location
        await browser.grant_permissions(["geolocation"])

        page = await browser.new_page()

        url = "https://38aladdin.shop/"

        try:
            await page.goto(url, timeout=60000, wait_until='load')
        except Exception as e:
            send_message_developer(
                message=f"This user {user_id} with  {user_name} could not navigate to url --> `60 Sec Time out already !`")
            send_message_user(user_id,
                              message="🔔 <b>NOTIFICATION</b>: \n\nDear during accessing and after retrying i could not access your profile due to server error or over load wil retry and feed you back thanks man")
            pass
            # Dear during accessing and after retrying i could not access your profile due to server error or over
            # load wil retry and feed you back thanks man

        # await page.wait_for_load_state(state='load', timeout=120000)
        # JavaScript code to find the login icon by its class and click it
        js_click_login_icon = """
        const loginIcon = document.querySelector('i.fa.fa-sign-in-alt.fa-lg');
        if (loginIcon) {
          loginIcon.click();
          true; // Return true if the element was found and clicked
        } else {
          false; // Return false if the element was not found
        }
        """

        try:
            # Execute the JavaScript code on the page
            login_icon_clicked = await page.evaluate(js_click_login_icon)

            if login_icon_clicked:
                print("Login icon clicked successfully!")

                if not await login_user(page, email, password, chat_id=user_id, user_name=user_name):
                    log.error("Issue after clicking the Login Icon button !")
                    # if the login was not successful is due to incorrect details or other login reason so we terminate
                    # early to
                    return

                # while not await login_user(page, email, password):
                #     await asyncio.sleep(20)
                #     print(" Wait for 5 sec and Trying for three !")
                #     pass
            else:
                print("Login icon not found!")
                send_message_developer(message="Login Button Icon have been  Disabled 🙂")

            # Check if the Error box is visible

        except Exception as e:
            print("Error:", e)

        await  bot_operation(page, gp_amount, gp_quantity, gp_plus, chat_id=user_id,genei_point=genei_point)

        # while not await bot_operation(page):
        #     # please try two times
        #     await bot_operation(page)
        end_time = time.time()
        log.info(f"{int(end_time - start_time)} Sec. Start time:  {start_time} End time : {end_time}")


        await page.close()
        await browser.close()


async def get_paid_user_data(test):
    if test:
        result = requests.get("http://ayocrpt.pythonanywhere.com/user_data_crypt_test")
        log.debug(f"______Test Mode Activated_____ ({get_gmt_time()[0]})\n")

    else:
        result = requests.get("http://ayocrpt.pythonanywhere.com/user_data_gp_point")
        log.debug(f"_______Deployment  Mode Activated_______ ({get_gmt_time()[0]})\n")

    if result.status_code == 200:
        data = result.json()  # Decode the JSON response into a list of dictionaries
        if len(data) == 0:
            return []
        else:
            return data

        # # Now you can iterate through the list and access individual dictionaries
        # for entry in data:
        #     user_data = entry["user_data"]  # Access the "user_data" dictionary for each entry
        #     print(user_data)
    else:
        log.info("Failed to retrieve data. Status code:", result.status_code)


async def main_wrapper(user_data, task_queue, semaphore):
    async with semaphore:
        # Extract user data
        email = user_data.get("email", "")
        password = user_data.get("password", "")
        gp_amount = user_data.get("gp_amount", "")
        gp_quantity = user_data.get("gp_quantity", "")
        user_name = user_data.get("user_name", "")
        user_id = user_data.get("user_id", "")
        gp_plus = user_data.get("gp_plus", 0)
        genei_point = user_data.get('genei_point', False)

        # print(type(gp_plus), user_id)

        if isinstance(gp_plus, str):

            gp_plus = 0

        if genei_point:
            msg = "🔔<b>GP POINT NOTIFICATION</b>:"
        else:
            msg = "🔔<b> GP PLUS NOTIFICATION</b>:"


        date, day =get_gmt_time()
        send_message_user(chat_id=user_id,
                          message=f"{msg} \nDear User 😎\n\nIt is beautiful {day}\n\n{date} !\n\nTrust you enjoyed yesterday\n\nI am Preparing to Bidding for you please relax 🤩  !")



        # Call the main function with the extracted user data
        await main(headless=False, email=email, password=password, gp_amount=gp_amount, gp_quantity=gp_quantity,
                   user_name=user_name, user_id=user_id, gp_plus=gp_plus, genei_point=genei_point)





        # Mark the task as done
        task_queue.task_done()


async def run_users(test):
    start = time.time()
    try:

        log.info("Getting list of Paid User Data to bid.......\n ")
        # List of user data to be used for each user
        user_data_list = await get_paid_user_data(test)

        if not user_data_list:
            log.success("Exiting Playwright.......")
            send_message_developer(message="There is no User data to Automate check the user_data.json")
            return

        log.info(f"Total User to Process at this time is {len(user_data_list)}\n")

        date, day = get_gmt_time()
        send_message_developer(
            message=f"Total User to Process today: {len(user_data_list)}\n\nDate : {date}\n\nDay: {day}")


        # Create a semaphore to limit the number of concurrent tasks
        # Create a queue to store the tasks for each user
        task_queue = asyncio.Queue()

        # Create a semaphore to control the maximum number of concurrent tasks
        semaphore = asyncio.Semaphore(1)

        # Start a task for each user data and add it to the queue
        for user_data in user_data_list:
            task = asyncio.create_task(main_wrapper(user_data["user_data"], task_queue, semaphore))
            task_queue.put_nowait(task)

        # Wait for all tasks to complete
        await task_queue.join()
        end = time.time()
        log.info(f"Total task was completed in: {(end - start) / 60} Mins. ")

    except Exception as t:
        log.error(f"Line 807 ------- {str(t)}")
        # Retry if there is an exception
        # await task_queue.join()


def start_main(test):
    if test:
        send_message_developer(message="🔔 <b>NOTIFICATION</b>\n\nYou are Good to Go Dev Man 😎\n\nThis is a Test Mode")
        asyncio.run(run_users(test))

    else:
        asyncio.run(run_users(test))

from flask import Flask, request
from main import start_main
# from gp_plus_main import start_main_plus
import requests
from loguru import logger as log
import threading

app = Flask(__name__)

# Configure the logger
log.add("flask_app.log", level="INFO", rotation="1 MB", compression="zip", backtrace=True, diagnose=True)


# Your send_message_developer function
def send_message_developer(message):
    bot_token = "BOT TOKEN "
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
        log.info("Developer Message sent successfully!")
    except requests.exceptions.RequestException as e:
        log.error("Failed to send the developer message: ", e)


@app.route("/gp_point_bids", methods=["GET"])
def display_point():
    try:
        deploy = request.args.get('deploy')
        # message = "From Flask234t"

        if deploy == 'true':
            # send_message_developer(message)
            log.info("Starting GP Point main in deployment mode")
            send_message_developer("Starting GP Point main in deployment mode")
            thread = threading.Thread(target=start_main, kwargs={"test": False})
            thread.start()
        else:
            # send_message_developer(message)
            log.info("Starting GP Point main in test mode")
            send_message_developer("Starting GP Point main in test mode")
            thread = threading.Thread(target=start_main, kwargs={"test": True})
            thread.start()

        return "Code Successfully Run. GP Point 😎"
    except Exception as e:
        log.error("An error occurred:", e)
        send_message_developer(f"An error occurred: {e}")
        return f"An error occurred: {e}", 500

#
# @app.route("/gp_plus_bids", methods=["GET"])
# def display_plus():
#     try:
#         deploy = request.args.get('deploy')
#
#         if deploy == 'true':
#             log.info("Starting GP Plus main in deployment mode")
#             send_message_developer("Starting GP Plus main in deployment mode")
#             thread = threading.Thread(target=start_main_plus, kwargs={"test": False})
#             thread.start()
#         else:
#             log.info("Starting GP Plus main in test mode")
#             send_message_developer("Starting GP Plus main in test mode")
#             thread = threading.Thread(target=start_main_plus, kwargs={"test": True})
#             thread.start()
#
#         return "Code Successfully Run. GP Plus 😎"
#     except Exception as e:
#         log.error("An error occurred:", e)
#         send_message_developer(f"An error occurred: {e}")
#         return f"An error occurred: {e}", 500


@app.route('/')
def hello_world():
    return "Hello Ayocrypt 😎"


if __name__ == "__main__":
    app.run()

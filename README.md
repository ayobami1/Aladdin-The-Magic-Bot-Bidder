# Flask Application Documentation - Version 1

This document provides an overview and detailed explanation of the Flask application code. The application initializes a Flask server to handle incoming requests and execute specific actions based on the endpoints accessed.

## Table of Contents

- [Introduction](#introduction)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Function: send_message_developer](#function-send_message_developer)
- [Endpoint: /gp_point_bids](#endpoint-gp_point_bids)
- [Endpoint: /](#endpoint-)
- [Running the Application](#running-the-application)

## Introduction

This Flask application serves as a server for running specific tasks, sending notifications, and managing requests.

## Dependencies

- Flask: Web application framework for creating and running the server.
- requests: Library for making HTTP requests.
- loguru: Logging library for improved logging capabilities.
- threading: Module for creating and managing threads.

## Configuration

The application includes a configuration to set up logging using the loguru library. Logs are written to a file named "flask_app.log" with rotation, compression, and diagnostic features enabled.

## Function: send_message_developer

This function sends a message to a developer's Telegram bot using the Telegram Bot API. The function takes a message as input, prepares the required data, and sends the message using the requests library. If the message fails to send, an error is logged.

## Endpoint: /gp_point_bids

- Method: GET
- Purpose: Initiates a specific action based on the "deploy" query parameter.
- Actions:
  - If "deploy" is set to 'true', starts the "start_main" function in a new thread with deployment mode.
  - If "deploy" is not set or set to any other value, starts the "start_main" function in a new thread with test mode.
- Returns: A message indicating the code was run successfully or an error message.

## Endpoint: /

- Method: GET
- Purpose: Displays a simple greeting message.

## Running the Application

To run the application, execute the following code in the terminal:

```bash
python app.py

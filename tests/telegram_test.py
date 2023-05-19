# import undetected_chromedriver as uc
# import libs
import os
from time import sleep

import pandas as pd
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MKT_TOP = os.getenv("MKT_TOP")


# 'https://api.telegram.org/bot{BOT_TOKEN}'
# send message
def sedn_general(message, link=None):
    u_link = f"[Link]({link})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}\n{u_link}&parse_mode=Markdown"
    print(u_link)
    requests.get(url)


def send_topic(message, link=None):
    u_link = f"[Link]({link})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=***{message}***\n{u_link}&message_thread_id={MKT_TOP}&parse_mode=Markdown"
    requests.get(url)


link = "https://pytba.readthedocs.io/en/latest/sync_version/index.html"
send_topic("topica mensage", link)

sedn_general("general message", link)

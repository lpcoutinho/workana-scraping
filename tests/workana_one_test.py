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


# init driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# driver = uc.Chrome()

# maximizar a janela do navegador
driver.maximize_window()


# send message
def sen_message(message, link=None):
    if link is not None:
        u_link = f"[{message}]({link})"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={u_link}\Detalhes do job&parse_mode=Markdown"
        # url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}\n{u_link}&parse_mode=Markdown'
        requests.get(url)
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    requests.get(url)


print("Esta é a mensagem inicial. Antes do loop...")
sen_message("Esta é a mensagem inicial. Antes do loop...")

know_job_title = set()
while True:
    try:
        # go to workana
        driver.get(f"https://www.workana.com/jobs?language=pt&page={1}")

        # title
        job_title = driver.find_element(
            By.XPATH, f'//*[@id="projects"]/div[{2}]/div[1]/h2/a/span'
        )
        job_title = job_title.get_attribute("title")
        print("Tutilo:", job_title)

        # job_link
        job_link = driver.find_element(
            By.XPATH, f'//*[@id="projects"]/div[{2}]/div[1]/h2/a'
        )
        job_link = job_link.get_attribute("href")
        print(job_link)

        if job_title not in know_job_title:
            know_job_title.add(job_title)
            sen_message(job_title, job_link)
        else:
            sen_message("Trabalho já informado")
        sleep(10)
    except:
        pass


# https://api.telegram.org/bot<token>/getUpdates

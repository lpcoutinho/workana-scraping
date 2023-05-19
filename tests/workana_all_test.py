# import libs
import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService

# import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MKT_TOP = os.getenv("MKT_TOP")

# init session
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# maximizing browser window
driver.maximize_window()

categories = {
    "Marketing e Vendas": MKT_TOP,
    "Design e Multimedia": "74",
    "TI e Programação ": "75",
    "Tradução e conteúdos": "76",
    "Engenharia e Manufatura": "77",
    "Finanças e Administração": "78",
    "Suporte Administrativo": "",
}

# 'https://api.telegram.org/bot{BOT_TOKEN}'
# send message
# def send_general(link):
#     u_link = f'[Link]({link})'
#     url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={u_link}&parse_mode=Markdown'
#     print(u_link)
#     requests.get(url)


# def send_topic(message, link=None):
#     TOPIC = int
#     u_link = f'[Link]({link})'
#     url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}\n{u_link}&message_thread_id={TOPIC}&parse_mode=Markdown'
#     requests.get(url)


# print('Iniciando loop...')
# send_general('Iniciando loop...')

know_job_title = set()
# list to store datas for dataframe
data = []

# list to store performance data
perf = []

print("Iniciando raspagem de dados no Workana\n")

while True:
    try:
        # to check script performance
        start_time = time.time()

        # iterating through the pages - usually 50 pages
        for p in range(1, 51):
            # to check script performance
            start_loop = time.time()

            # go to jobs
            driver.get(f"https://www.workana.com/jobs?language=pt&page={p}")

            print(f"https://www.workana.com/jobs?language=pt&page={p}")

            # wait
            time.sleep(2)

            # iterating through the objects
            for i in range(2, 11):
                try:
                    job_title = driver.find_element(
                        By.XPATH, f'//*[@id="projects"]/div[{i}]/div[1]/h2/a/span'
                    )
                    job_title = job_title.get_attribute("title")
                except NoSuchElementException:
                    job_title = f"Erro no título {i} da página{p}"
                    print(f"Erro em job_title {i} da p{p}")

                try:
                    job_date = driver.find_element(
                        By.XPATH, f'//*[@id="projects"]/div[{i}]/div[1]/h5'
                    )
                    job_date = job_date.get_attribute("title")
                except NoSuchElementException:
                    job_date = f"Erro na data {i} da página{p}"
                    print(f"Erro em job_date {i} da p{p}")

                try:
                    job_link = driver.find_element(
                        By.XPATH, f'//*[@id="projects"]/div[{i}]/div[1]/h2/a'
                    )
                    job_link = job_link.get_attribute("href")
                except NoSuchElementException:
                    job_link = f"Erro no link {i} da página{p}"
                    print(f"Erro em job_link {i} da p{p}")

                try:
                    job_bids = driver.find_element(
                        By.XPATH, f'//*[@id="projects"]/div[{i}]/div[2]/div[1]/span[2]'
                    )
                    job_bids = job_bids.text.split(" ")[1]
                except NoSuchElementException:
                    job_bids = f"Erro no orçamento {i} da página{p}"
                    print(f"Erro em job_bids {i} da p{p}")

                try:
                    job_budget = driver.find_element(
                        By.XPATH, f'//*[@id="projects"]/div[{i}]/div[3]/h4/span'
                    )
                    job_budget = job_budget.text
                except NoSuchElementException:
                    job_budget = f"Erro no budget {i} da página{p}"
                    print(f"Erro em job_budget {i} da p{p}")

                try:
                    job_desc = driver.find_element(
                        By.XPATH, f'//*[@id="projects"]/div[{i}]/div[2]/div[2]/div'
                    )
                    job_desc = job_desc.text
                except NoSuchElementException:
                    job_desc = f"Erro no job_desc {i} da página{p}"
                    print(f"Erro em job_desc {i} da p{p}")

                # get job skills
                job_sk = []

                try:
                    skills = driver.find_element(
                        By.XPATH, f'//*[@id="projects"]/div[{i}]/div[2]/div[3]/div'
                    )
                    skills = skills.find_elements(By.TAG_NAME, "a")

                    for skill in skills:
                        job_sk.append(skill.text)

                    job_sk = ", ".join(job_sk)
                except NoSuchElementException:
                    print(f"Erro em skills {i} da p{p}")
                    job_sk.append("N/I")

                # create data list
                data_tmp = {
                    "Job": job_title,
                    "Publish Date": job_date,
                    "Skills": job_sk,
                    "Budget": job_budget,
                    "Bids": job_bids,
                    "Summary": job_desc,
                    "Link": job_link,
                }

                data.append(data_tmp)

                # send message
                if job_title not in know_job_title:
                    know_job_title.add(job_title)
                    # print(know_job_title)
                    message = f"[{job_title}]({job_link})\n{job_budget}"
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
                    requests.get(url)
                else:
                    print(f"Trabalho já informado: {job_title}")

            # print(i)
            # print(know_job_link)

            # to check script performance
            end_loop = time.time()
            duration_loop = end_loop - start_loop
            print(f"Página {p} levou {duration_loop} segundos para ser carregada\n")

            # create performance list
            perf_tmp = {"#Loop": {p}, "End Loop": duration_loop}
            perf.append(perf_tmp)

        # to analysis script performance
        end_time = time.time()
        duration_t_s = end_time - start_time
        duration_t_m = duration_t_s / 60
        print(f"O tempo total para raspar os dados foi de {duration_t_m} minutos\n")

        time.sleep(3)
    except:
        pass

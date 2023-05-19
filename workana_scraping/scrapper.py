# import libs
import os
import time

import pandas as pd
import requests
from clear import Clear
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configurar as opções do Chrome para executar em modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TI_TOP = os.getenv("TI_TOP")
DSGN_TOP = os.getenv("DSGN_TOP")
MKT_TOP = os.getenv("MKT_TOP")
ENG_TOP = os.getenv("ENG_TOP")
CTD_TOP = os.getenv("CTD_TOP")
JD_TOP = os.getenv("JD_TOP")
ADM_TOP = os.getenv("ADM_TOP")


categories = {
    "TI e Programação": TI_TOP,
    "Design e Multimedia": DSGN_TOP,
    "Marketing e Vendas": MKT_TOP,
    "Engenharia e Manufatura": ENG_TOP,
    "Tradução e conteúdos": CTD_TOP,
    "Jurídico": JD_TOP,
    "Finanças e Administração": ADM_TOP,
}

# convert keys to list
t_keys = list(categories.keys())

# convert values to list
t_values = list(categories.values())


class Scrapper:
    def workana():
        # init driver
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
        )

        # maximizar a janela do navegador
        driver.maximize_window()

        # list to store datas for dataframe
        data = []

        # list to store performance page loop
        perf_page = []

        # list to store performance script loop
        perf_script = []
        print("Iniciando raspagem de dados no Workana\n")

        # accept cookies
        driver.get(f"https://www.workana.com/jobs?language=pt&page=1")
        time.sleep(1)
        driver.find_element(By.XPATH, f'//*[@id="onetrust-accept-btn-handler"]').click()
        driver.find_element(
            By.XPATH, f'//*[@id="app"]/div/div[4]/div/div/button'
        ).click()

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

                    print(
                        f"Acesando: https://www.workana.com/jobs?language=pt&page={p}\n"
                    )

                    # wait
                    time.sleep(2)

                    # iterating through the objects
                    for i in range(2, 11):
                        # get title
                        try:
                            job_title = driver.find_element(
                                By.XPATH,
                                f'//*[@id="projects"]/div[{i}]/div[1]/h2/a/span',
                            )
                            job_title = job_title.get_attribute("title")
                        except NoSuchElementException:
                            job_title = f"Erro no título {i} da página{p}"
                            print(f"Erro em job_title {i} da p{p}")

                        # get published date
                        try:
                            job_date = driver.find_element(
                                By.XPATH, f'//*[@id="projects"]/div[{i}]/div[1]/h5'
                            )
                            job_date = job_date.get_attribute("title")
                        except NoSuchElementException:
                            job_date = f"Erro na data {i} da página{p}"
                            print(f"Erro em job_date {i} da p{p}")

                        # get link
                        try:
                            job_link = driver.find_element(
                                By.XPATH, f'//*[@id="projects"]/div[{i}]/div[1]/h2/a'
                            )
                            job_link = job_link.get_attribute("href")
                        except NoSuchElementException:
                            job_link = f"Erro no link {i} da página{p}"
                            print(f"Erro em job_link {i} da p{p}")

                        # get bids
                        try:
                            job_bids = driver.find_element(
                                By.XPATH,
                                f'//*[@id="projects"]/div[{i}]/div[2]/div[1]/span[2]',
                            )
                            job_bids = job_bids.text.split(" ")[1]
                        except NoSuchElementException:
                            job_bids = f"Erro no orçamento {i} da página{p}"
                            print(f"Erro em job_bids {i} da p{p}")

                        # get budget
                        try:
                            job_budget = driver.find_element(
                                By.XPATH, f'//*[@id="projects"]/div[{i}]/div[3]/h4/span'
                            )
                            job_budget = job_budget.text
                        except NoSuchElementException:
                            job_budget = f"Erro no budget {i} da página{p}"
                            print(f"Erro em job_budget {i} da p{p}")

                        # click on 'see more'
                        try:
                            see_more = driver.find_element(
                                By.XPATH,
                                f'//*[@id="projects"]/div[{i}]/div[2]/div[2]/div/span[1]/a',
                            )
                        except:
                            pass

                        # get description
                        if see_more.is_displayed():
                            try:
                                see_more.click()

                                job_desc = driver.find_element(
                                    By.XPATH,
                                    f'//*[@id="projects"]/div[{i}]/div[2]/div[2]/div',
                                )
                                job_desc_more = driver.find_element(
                                    By.XPATH,
                                    f'//*[@id="projects"]/div[{i}]/div[2]/div[2]/div/span[2]',
                                )
                                job_desc = job_desc.text + job_desc_more.text
                            except:
                                print(f"error 'see more' in p:{p} i:{i}")
                        else:
                            job_desc = driver.find_element(
                                By.XPATH,
                                f'//*[@id="projects"]/div[{i}]/div[2]/div[2]/div',
                            )
                            job_desc = job_desc.text

                        # get job skills
                        job_sk = []

                        try:
                            skills = driver.find_element(
                                By.XPATH,
                                f'//*[@id="projects"]/div[{i}]/div[2]/div[3]/div',
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
                            "Updated": False,
                        }

                        # #CSV path
                        csv_path = "workana_scraping/data/data_raw.csv"

                        # CSV exists
                        file_exists = False

                        if os.path.exists(csv_path):
                            file_exists = True

                        # link is in CSV
                        link_exists = False

                        if file_exists:
                            df = pd.read_csv(csv_path)
                            if df["Link"].eq(data_tmp["Link"]).any():
                                link_exists = True
                                # update row
                                df.loc[
                                    df["Link"] == data_tmp["Link"],
                                    [
                                        "Job",
                                        "Publish Date",
                                        "Skills",
                                        "Budget",
                                        "Bids",
                                        "Summary",
                                        "Updated",
                                    ],
                                ] = [
                                    data_tmp["Job"],
                                    data_tmp["Publish Date"],
                                    data_tmp["Skills"],
                                    data_tmp["Budget"],
                                    data_tmp["Bids"],
                                    data_tmp["Summary"],
                                    True,
                                ]
                                # print(f'link: {link_exists}')

                                # save update
                                df.to_csv(csv_path, index=False)

                        # append newline if file does not exist or if link is not present in CSV
                        if not file_exists or not link_exists:
                            df_new_row = pd.DataFrame([data_tmp])
                            df_new_row.to_csv(
                                csv_path,
                                mode="a",
                                index=False,
                                header=not file_exists,
                            )

                            # extract data
                            df_new_row["Category"] = df_new_row["Summary"].str.extract(
                                "Categoria:\s*(.*)\n"
                            )

                            # send messages to Telegram
                            def send_general():
                                message = f"[Link]({job_link})"
                                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
                                print(job_link)
                                requests.get(url)

                            def send_topic(topic):
                                message = f"[Link]({job_link})"
                                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&message_thread_id={topic}&parse_mode=Markdown"
                                requests.get(url)

                            # send messages to general topic
                            send_general()

                            # send messages to topics
                            if df_new_row["Category"][0] == t_keys[0]:
                                print(f"Mensagem publicada no tópico {t_keys[0]}\n")
                                send_topic(t_values[0])

                            if df_new_row["Category"][0] == t_keys[1]:
                                print(f"Mensagem publicada no tópico {t_keys[1]}\n")
                                send_topic(t_values[1])

                            if df_new_row["Category"][0] == t_keys[2]:
                                print(f"Mensagem publicada no tópico {t_keys[2]}\n")
                                send_topic(t_values[2])

                            if df_new_row["Category"][0] == t_keys[3]:
                                print(f"Mensagem publicada no tópico {t_keys[3]}\n")
                                send_topic(t_values[3])

                            if df_new_row["Category"][0] == t_keys[4]:
                                print(f"Mensagem publicada no tópico {t_keys[4]}\n")
                                send_topic(t_values[4])

                            if df_new_row["Category"][0] == t_keys[5]:
                                print(f"Mensagem publicada no tópico {t_keys[5]}\n")
                                send_topic(t_values[5])

                            if df_new_row["Category"][0] == t_keys[6]:
                                print(f"Mensagem publicada no tópico {t_keys[6]}\n")
                                send_topic(t_values[6])

                    # to check script performance
                    end_loop = time.time()
                    duration_loop = end_loop - start_loop
                    print(
                        f"Página {p} levou {duration_loop} segundos para ser carregada\n"
                    )

                    # create performance page CSV
                    perf_tmp = {"#Loop": {p}, "Duration Loop(sec)": duration_loop}

                    csv_path = "workana_scraping/data/performance/p_page.csv"

                    if not os.path.exists(csv_path):
                        df = pd.DataFrame([perf_tmp])
                        df.to_csv(csv_path, index=False)
                    else:
                        df = pd.DataFrame([perf_tmp])
                        df.to_csv(csv_path, mode="a", header=False, index=False)

            except:
                pass
            print("####### FIM #######")
            # to analysis script performance
            end_time = time.time()
            duration_t_s = end_time - start_time
            duration_t_m = duration_t_s / 60
            print(f"O tempo total para raspar os dados foi de {duration_t_m} minutos\n")

            # create performance page CSV
            perf_tmp = {"Duration Script(min)": duration_t_m}
            csv_path = "workana_scraping/data/performance/p_script.csv"

            if not os.path.exists(csv_path):
                df = pd.DataFrame([perf_tmp])
                df.to_csv(csv_path, index=False)
            else:
                df = pd.DataFrame([perf_tmp])
                df.to_csv(csv_path, mode="a", header=False, index=False)


# Scrapper.workana()

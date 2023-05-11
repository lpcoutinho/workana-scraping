# import libs
import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# init session
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# maximizing browser window
driver.maximize_window()

# list to store datas for dataframe
data = []

# to analysis script performance
start_time = time.time()
print("Iniciando raspagem de dados no Workana\n")

# iterating through the pages - usually 50 pages
for p in range(1, 51):
    # to check script performance
    start_loop = time.time()

    # go to jobs
    driver.get(f"https://www.workana.com/jobs?language=pt&page={p}")

    print(f"https://www.workana.com/jobs?language=pt&page={p}")

    # wait
    time.sleep(3)

    # iterating through the objects
    for i in range(2, 11):
        try:
            job_title = driver.find_element(
                By.XPATH, f'//*[@id="projects"]/div[{i}]/div[1]/h2/a/span'
            )
            job_title = job_title.get_attribute("title")
            # print('Title:',job_title)
        except NoSuchElementException:
            job_title = f"Erro no título {i} da página{p}"
            print(f"Erro em job_title {i} da p{p}")

        try:
            job_date = driver.find_element(
                By.XPATH, f'//*[@id="projects"]/div[{i}]/div[1]/h5'
            )
            job_date = job_date.get_attribute("title")
            # print('Published at:',job_date)
        except NoSuchElementException:
            job_date = f"Erro na data {i} da página{p}"
            print(f"Erro em job_date {i} da p{p}")

        try:
            job_link = driver.find_element(
                By.XPATH, f'//*[@id="projects"]/div[{i}]/div[1]/h2/a'
            )
            job_link = job_link.get_attribute("href")
            # print(job_link)
        except NoSuchElementException:
            job_link = f"Erro no link {i} da página{p}"
            print(f"Erro em job_link {i} da p{p}")

        try:
            job_bids = driver.find_element(
                By.XPATH, f'//*[@id="projects"]/div[{i}]/div[2]/div[1]/span[2]'
            )
            job_bids = job_bids.text.split(" ")[1]
            # print('Bids:',job_bids)
        except NoSuchElementException:
            job_bids = f"Erro no orçamento {i} da página{p}"
            print(f"Erro em job_bids {i} da p{p}")

        try:
            job_budget = driver.find_element(
                By.XPATH, f'//*[@id="projects"]/div[{i}]/div[3]/h4/span'
            )
            job_budget = job_budget.text
            # print('Budget:',job_budget)
        except NoSuchElementException:
            job_budget = f"Erro no budget {i} da página{p}"
            print(f"Erro em job_budget {i} da p{p}")

        try:
            job_desc = driver.find_element(
                By.XPATH, f'//*[@id="projects"]/div[{i}]/div[2]/div[2]/div'
            )
            job_desc = job_desc.text
            # print(job_desc)
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
            s = "Não informado"
            job_sk.append(s)

        # create data list
        data_temp = {
            "Job": job_title,
            "Publish Date": job_date,
            "Skills": job_sk,
            "Budget": job_budget,
            "Bids": job_bids,
            "Summary": job_desc,
            "Link": job_link,
        }

        data.append(data_temp)

        # print(f'\n{i}')

    # to check script performance
    end_loop = time.time()
    duration_loop = end_loop - start_loop
    print(f"Página {p} levou {duration_loop} segundos para ser carregada\n")


# # to check script performance
end_time = time.time()
duration_t_s = end_time - start_time
duration_t_m = duration_t_s / 60
print(f"O tempo total para raspar os dados foi de {duration_t_m} minutos\n")

# create workana dataframe
df_raw = pd.DataFrame(data)
df_raw.head(1)

# create performance dataframe
perf = {
    "Init Script": start_time,
    "Init Loop": start_loop,
    "End Loop": end_loop,
    "End Script": end_time,
}
df_perf = pd.DataFrame(data)
df_perf.head(1)

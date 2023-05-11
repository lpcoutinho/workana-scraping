# Workana Scraping
## 🎯 Objetivo 
Extrair dados de trabalhos ofertados a profissionais freelancers na plataforma Workana.

De cada trabalho é preciso coletar:
- [x] Título
- [x] Skills
- [x] Propostas
- [x] Resumo
- [x] Data
- [x] Budget
- [x] Links
- [x] Categorias
- [x] Subcategoria

## 🛠️ Tools
- bash
- Vscode
- Python 3.11.2
- Poetry 1.4.0
- Jupyter Notebook
- Selenium 4.9.0
- Pandas 2.0.1

> [Leia a Documentação](references.md)

# Extração de Dados com Selenium

> [Leia a Documentação do Selenium](https://www.selenium.dev/documentation/)

Neste texto mostrarei como fiz para coletar os dados de trabalhos ofertados na plataforma Workana. Para verificar o caminho até este ponto do projeto consulte: 
- [Scrap one job](../notebooks/scrap_workana_one_job.ipynb) 
- [Scrap one page](../notebooks/scrap_workana_one_page.ipynb)

Enquanto o notebook base para este texto é: 
- [Scrap all jobs](../notebooks/scrap_workana_all_jobs.ipynb)

## Instalação
Antes de começar, é preciso instalar os pacotes que fazem o projeto funcionar. Você pode fazer isso usando o gerenciador de pacotes pip ou poetry:

```bash
pip install -r requirements.txt
```

```bash
poetry install
```

## Configuração
Por padrão, para utilizar o Selenium é preciso um driver específico para cada navegador que desejamos utilizar. O driver deve ser baixado e adicionado ao PATH do sistema.

Porém essa etapa pode ser pulada se você utilizar a bibliotca ***Webdriver Manager*** que inicia sozinha uma sessão do navegador quando preciso.

Assim, podemos importar as bibliotecas,  instanciar e configurar uma nova sessão para iniciar a coleta de dados.

```python
# import libs
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# init session
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# maximizing browser window
driver.maximize_window()
```

## Coletando os dados

De cada trabalho [o objetivo é.](#objetivo)

### URL base

https://www.workana.com/jobs?language=pt&page=1

Observando a ***URL_BASE*** pelo driver pude perceber que os trabalhos são apresentados em conjuntos de 9 trabalhos por página dentro do universo de 50 páginas.

Deste modo foi criado um laço que percorre as páginas, iniciando em 1 até 50. Foi adicionado o tempo de espera entre páginas de 3 segundos para ter certeza que tudo foi carregado dentro da plataforma antes de coletar os dados.

```python
for p in range(1,51):

    # go to jobs
    driver.get(f'https://www.workana.com/jobs?language=pt&page={p}')
    
    print(f'https://www.workana.com/jobs?language=pt&page={p}')
    
    # wait
    time.sleep(3)
```

### Onde estão as informaçõe
#### **class="project-header"**

Nos elementos filhos da `<div class="project-header"></div>` podemos encontrar data, link e título dos trabalhos.

#### **class="project-body"**

Nos elementos filhos da `<div class="project-body"></div>` podemos encontrar data e o tempo desde a publicação, número de propostas, texto de resumo(as vezes texto todo), skills com seus links de referência.

Dentro de `<span class="expander-details"></span>"` pode ser encontrado categoria, subcategoria, 'alcance do Projeto', 'é projeto ou trabalho', 'tenho atualmente', 'disponibilidade', 'funções necessárias' e outras informações.


#### **class="project-actions floating"**

Nos elementos filhos da `<div class="project-actions floating"></div>` podemos encontrar budget, o valor oferecido como orçamento.


### O caminho XPATH
É possível pegar as informações dos trabalhos com o XPATH básico `//*[@id="projects"]/div[{i}]/`

>[Script falhando nas primeiras vezes](doubts.md#script-falhando-nas-primeiras-vezes)

Onde ***i*** é maior ou igual a 2 e menor ou igual a 10, valores referentes as quantidades de jobs exibidos em cada página.

#### Data
```python
job_date = driver.find_element(By.XPATH, f'//*[@id="projects"]/div[{2}]/div[1]/h5')
job_date = job_date.get_attribute('title')
print('Publicação:',job_date)
```

#### Link
```python
job_link = driver.find_element(By.XPATH, f'//*[@id="projects"]/div[{2}]/div[1]/h2/a')
job_link = job_link.get_attribute('href')
print(job_link)
```

#### Título
```python
job_title = driver.find_element(By.XPATH, f'//*[@id="projects"]/div[{2}]/div[1]/h2/a/span')
job_title = job_title.get_attribute('title')
print('Tutilo:',job_title)
```

#### Qtd de Propostas Feitas
```python
job_bids = driver.find_element(By.XPATH, f'//*[@id="projects"]/div[{2}]/div[2]/div[1]/span[2]')
job_bids = job_bids.text.split(' ')[1]
print('Propostas:',job_bids)
```

#### Resumo
```python
job_desc = driver.find_element(By.XPATH, f'//*[@id="projects"]/div[{2}]/div[2]/div[2]/div')
job_desc = job_desc.text 
print(job_desc)
```

#### Skills
Em alguns momentos a div que armazena as Skills não aparece. Deste  modo é preciso informar um valor padrão para ser inserido nos dados quando isto ocorrer.
```python
# get job skills 
    job_sk = []

    try:
        skills = driver.find_element(By.XPATH, f'//*[@id="projects"]/div[{i}]/div[2]/div[3]/div')
        skills = skills.find_elements(By.TAG_NAME, 'a')
    
        for skill in skills:
            job_sk.append(skill.text)

        job_sk = ', '.join(job_sk)
    except NoSuchElementException:
        job_sk.append('Não informado')
```

#### Budget do job
```python
job_budget = driver.find_element(By.XPATH, f'//*[@id="projects"]/div[{2}]/div[3]/h4/span')
job_budget = job_budget.text
print('Valor:',job_budget)
```

## Construindo dataframe com os dados coletados

Usaremos Pandas para transformar as informações extraidos do Workana em um dataframe a fim de facilitar a manipulação dos dados. Para isso é preciso transformar as informações coletadas em uma lista que será lida pelo método da biblioteca Pandas que cria um dataframe.

> [Leia a documentação do Pandas](https://pandas.pydata.org/docs/)

### Transformando os dados em lista
```python
data_temp = {'Job': job_title,'Publish Date': job_date, 'Skills': job_sk,  'Budget':job_budget, 
                'Bids': job_bids, 'Summary': job_desc, 'Link': job_link}

data =[]
data.append(data_temp)
```

# Criando e visualizando um dataframe
```python
df =pd.DataFrame(data)
df.head()
```

## Conclusão
Neste ponto já é possível ter acesso as primeiras informações coletadas do Workana em um dataframe. Agora é preciso tratar estes dados para que seja possível utilizá-los em algorítimos estatísticos.
[Continue para a sessão de tratamento de dados](transform_data.md).

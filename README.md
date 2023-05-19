# Workana Scraping Project
## O Problema
- Consultar os trabalhos publicados no Workana periodicamente
- Permitir fácil visualização e filtro dos dados
- Disponibilizar online as informações e análises tratadas

O projeto é desenvolvido em diversas etapas e para facilitar sua compreensão cada uma das etapas está documentada e disponibilizada nesta estrutura.

A primeira atividade consiste em raspar os dados da plataforma Workana de modo que seja possível criar um DataSet para futuras análises.

Em [Road Map](#road-map) você pode verificar cada etapa e consultar sua documentação.

## A estrutura
O projeto for organizado para facilitar o acesso às informações e atividades desenvolvidas. Etapas e categorias de atividades estão dispostas em diretórios referentes a cada atividade.

Em ***docs/*** estão os documentos textuais desenvolvidos ao longo da atividade que explicam e justificam as metodologias utilizadas.

No diretório ***notebooks/*** ficarão disponíveis os arquivos ***jupyter*** que foram utilizados ao longo das atividades.

Os scripts e arquivos ***\*.py*** estarão no diretório ***workana_scraping/***.

Enquanto os dados armazenados poderão ser acessados no diretório ***workana_scraping/data***.

## Road Map
### Fase 1
1. [x] Extrair dados
    - [Scrap workana.com/jobs](/docs/scrap_workana.md)
2. [x] Armazenar e exportar dados
    - Dados armazenados e exportados em arquivos CSV
3. [x] Tratar
    - [Tratando as informações coletados](/docs/transform_data.md)

### Fase 2
- [x] Telegram bot
- [ ] Minerar dados 
- [ ] Visualizar
- [ ] Disponibilizar

## To Do
-   [x] Makefile para formatar códigos
-   [x] Pré-commit para formatar
-   [ ] Container Docker
-   [ ] Armazenar em PostgreSQL
-   [ ] Automatizar execução com Cron
-   [ ] Atualizar CSV com os dados extraidos
    -   [ ] Concatenar novos dados
    -   [ ] Atualizar coluna Bids  

## Execute o projeto

### Instale os requerimentos
Você pode fazer isso usando o gerenciador de pacotes pip ou poetry:

```bash
pip install -r requirements.txt
```

```bash
poetry install
```
### Configure as variáveis de ambiente
Crie o arquivo ***.env*** na raíz do projeto e popule com as credenciais do seu bot.

```bash
BOT_TOKEN = xxxxxx
CHAT_ID = xxxxxx
TI_TOP = xxxxxx
DSGN_TOP = xxxxxx
MKT_TOP = xxxxxx
ENG_TOP = xxxxxx
CTD_TOP = xxxxxx
JD_TOP = xxxxxx
ADM_TOP = xxxxxx
```

### Execute o scrapper
Este script realiza a raspagem de dados dos trabalhos disponíveis no workana e os envia para um grupo no Telegram.

```bash
python workana_scraping/scrapper.py
```

### Execute o bot
Está disponível um bot para conversas individuais que retorna trabalhos disponíveis nas ultimas 24 separados por categoria.

```bash
python workana_scraping/bot_telegram.py
```

## Dúvidas

As dúvidas relevantes que surgirem ao longo do trabalho serão armazenadas e discutidas em outro espaço. Para acessar [clique aqui](/docs/doubts.md) 
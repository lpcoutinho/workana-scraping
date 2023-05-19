# Bot Telegram
Neste projeto estão disponíveis dois bots, um que roda junto com o scrapper.py e outro quer é executado sozinho. O primeiro envia mensagens para um grupo do Telegram e utiliza a biblioteca ***requests*** enquanto o segundo fucniona como uma conversa individual utilizando a biblioteca ***pyTelegramBotAPI***. Ambos serão descritos abaixo.

## As Credenciais

### O Token

Para construir um bot no telegram é preciso acessar o BotFather, esta é uma ferramenta essencial para criar e gerenciar bots no Telegram. BotFather facilita o processo de criação, fornecendo um token de acesso exclusivo para o bot e permitindo personalizações adicionais. Ao seguir os passos abaixo, você poderá criar um bot e obter o token necessário para programá-lo e interagir com a API do Telegram.

1. Abra o Telegram e procure o BotFather na barra de pesquisa. Geralmente, ele é encontrado digitando "@BotFather" na busca.

2. Inicie uma conversa com o BotFather e clique em "Iniciar" ou envie o comando "/start" para começar.

3. Envie o comando "/newbot" para criar um novo bot. O BotFather irá solicitar que você escolha um nome para o bot.

4. Após escolher o nome, o BotFather irá pedir que você forneça um nome de usuário para o seu bot. O nome de usuário deve ser único e terminar com a palavra "bot" (por exemplo, "meubot_bot").

5. Após escolher o nome de usuário, o BotFather irá gerar um token de acesso exclusivo para o seu bot. Esse token é uma sequência de caracteres que você precisará para se comunicar com a API do Telegram usando o bot. **GUARDE O TOKEN**

Opcionalmente, o BotFather oferece uma série de comandos adicionais para personalizar o seu bot, como adicionar uma descrição, definir uma foto de perfil, definir comandos personalizados e muito mais. Você pode explorar esses comandos adicionais se desejar.

### Chat Id
Para enviar mensagens a um grupo ou conversa específica precisamos do seu chat id. Siga os passos:

1. Envie uma mensagem para o seu bot no Telegram. O texto da mensagem pode ser qualquer coisa. Seu histórico de bate-papo deve incluir pelo menos uma mensagem para obter o chat id.

2. Cole o seguinte link no seu navegador. Substitua <API-access-token> pelo token de acesso à API que você identificou ou criou na seção anterior:

https://api.telegram.org/bot<API-access-token>/getUpdates?offset=0

3. Identifique o ID numérico do chat encontrando-o dentro do objeto JSON do chat. No exemplo abaixo, o chat id é 123456789.

```bash
{  
   "ok":true,
   "result":[  
      {  
         "update_id":XXXXXXXXX,
         "message":{  
            "message_id":2,
            "from":{  
               "id":XXXXXXXXX,
               "first_name":"Mushroom",
               "last_name":"Kap"
            },
            "chat":{  
               "id":123456789,
               "first_name":"Mushroom",
               "last_name":"Kap",
               "type":"private"
            },
            "date":1487183963,
            "text":"hi"
         }
      }
   ]
}
```

### Topic
Para pegar as credenciais dos tópicos utilize o mesmo endereço informado acima e busque por ***message_thread_id***. Em nosso caso o id do tópico é 123.
```bash
{
  "ok": true,
  "result": [
    {
      "update_id": XXXXXXXXX,
      "message": {
        "message_id": 4560,
        "from": {
          "id": XXXXXXXXX,
          "is_bot": false,
          "first_name": "Lpcoutinho",
          "username": "LpCoutinho",
          "language_code": "pt-br"
        },
        "chat": {
          "id": -123456789,
          "title": "FreelaJob",
          "is_forum": true,
          "type": "supergroup"
        },
        "date": 1684440162,
        "message_thread_id": 123,
        "forum_topic_created": {
          "name": "Marketing e vendas",
          "icon_color": 16478047
        },
        "is_topic_message": true
    },
    ]
}
```
## O bot em grupos

Optei por enviar os trabalhos publicados no Workana automaticamente assim que os dados são obtidos pelo nosso ***scrapper.py***. Estes trabalhos são separados por categorias e de acordo com a categoria do trabalho é enviado para um tópico no grupo do Telegram, além de serem enviados todos os trabalhos para o tópico geral.

### Separando por categorias
Para separar os trabalhos em categoria utilizei regex para extrair as informações de categoria dentro da coluna *Summary*. Isso também pode ser feito para extrair subcategorias e eoutras informações que desejarmos.

```python
# extract data
df_new_row["Category"] = df_new_row["Summary"].str.extract("Categoria:\s*(.*)\n")
```

### Funções de envio de mensagens
Em resumo, essas funções recebem um link e envia uma mensagem contendo esse link para um chat específico no Telegram, usando a API do Telegram e a biblioteca ***requests***. É importante garantir que as variáveis ***BOT_TOKEN***, ***CHAT_ID*** e ***topic*** sejam substituídas pelos valores corretos antes de executar essa função.

```python
# send messages to general topic
def send_general():
    message = f"[Link]({job_link})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    requests.get(url)
```

```python
# send messages to topics
def send_topic(topic):
    message = f"[Link]({job_link})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&message_thread_id={topic}&parse_mode=Markdown"
    requests.get(url)
```
### Enviando as mensagens
Para enviar as mensagens é muito simples. Todo novo trabalho é enviado para o tópico General e para o grupo de sua categoria. Usei ***Pandas*** para filtrar as categorias e criei condicionais que enviam mensagens para cada categoria específica de trabalho.

```python
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
```

## O bot em conversas individuais
Para construir o bot que interage em conversas individuais usaremos a biblioteca ***pyTelegramBotAPI***, conhecida como ***telebot*** sua função é facilitar a criação de bots. Construída em cima da API do Telegram, fornece uma interface simples e intuitiva para interagir com o serviço de mensagens. 

O ***telebot*** possui uma arquitetura flexível que suporta extensões e integrações com outros serviços e bibliotecas. Isso possibilita a criação de bots avançados e personalizados que atendem às necessidades específicas dos usuários.

### Importe as bibliotecas
```python
import os

import pandas as pd
import telebot
from clear import Clear
from dotenv import load_dotenv
```

### Criando o bot
Optei por armazenar as credenciais em um arquivo de configuração ***.env***. Para ter acesso as informações contidas neste arquivo utilizo a biblioteca ***dotenv*** e carrego estas informações no meu bot antes de criá-lo.

```python
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
```

### Construindo mensagens
Usamos o decorador `@bot.message_handler()` para definir o comando que chamará a função que envia uma mensagem ao Telegram. No exemplo abaixo crio o menu que pode ser acionado com os comandos `/help` ou `/start`

```python
@bot.message_handler(commands=["help", "start"])
def send_help(message):
    help_text = "🤖 Olá! Bora conseguir um freela?\n"
    help_text += "Sou um bot que captura e envia trabalhos disponíveis nas últimas 24h no Workana.\n\n"
    help_text += "Ainda estou em desenvolvimento, caso queira sugerir modificações fique a vontade para entrar em contato em /info.\n"
    help_text += "\nAqui está uma lista de comandos que eu entendo:\n"
    # help_text += "/start - Comece a interagir\n"
    help_text += "/help - Precisando de ajuda?\n"
    help_text += "/info - Obter informações sobre o bot\n"
    help_text += "/apoio - Para apoiar este projeto\n"
    help_text += "/last - Informações do último trabalho publicado\n"
    help_text += f"/ti - Trabalhos na categoria *{categories[0]}* \n"
    help_text += f"/design - Trabalhos na categoria *{categories[1]}* \n"
    help_text += f"/marketing - Trabalhos na categoria *{categories[2]}* \n"
    help_text += f"/engenhraia - Trabalhos na categoria *{categories[3]}* \n"
    help_text += f"/conteudos - Trabalhos na categoria *{categories[4]}* \n"
    help_text += f"/juridico - Trabalhos na categoria *{categories[5]}* \n"
    help_text += f"/adm - Trabalhos na categoria *{categories[6]}* \n"
    bot.reply_to(message, help_text, parse_mode="Markdown")
```

### Mensagens das últimas 24h
Para configurar que o bot envie apenas os trabalhos publicados nas ultimas 24h utilizei ***Pandas*** para criar uma classe que modifica as datas do dataframe para o padrão ***date_time*** e em seguida filtro os dados para exibir informações inseridas neste período de tempo.


```python
df = Clear.clear()

# current date and time
hour_now = pd.Timestamp.now()
# date and time 24 hours ago
date_24h_ago = hour_now - pd.Timedelta(hours=24)
# filter data from the last 24 hours
df = df[df["Publish Date"] >= date_24h_ago]
```

### Último trabalho e filtro por categorias
Para enviar mensagem com o último trabalho é possível criar um filtro simples com ***Pandas***

```python
# last job
@bot.message_handler(commands=["last"])
def get_last_job(message):
    job = df.loc[0, "Job"]
    link = df.loc[0, "Link"]
    print(type(link))

    bot.reply_to(message, f"[{job}]({link})", parse_mode="markdown")
```

Já para os trabalhos filtrados criei uma lista com as categorias e em seguida filtrei o dataframe para enviar as mensagens de acordo com nossa necessidade.

```python
categories = [
    "TI e Programação",
    "Design e Multimedia",
    "Marketing e Vendas",
    "Engenharia e Manufatura",
    "Tradução e conteúdos",
    "Jurídico",
    "Finanças e Administração",
]

# jobs by categorie
@bot.message_handler(commands=["ti"])
def get_last_ti(message):
    categoria_especifica = categories[0]
    dados_categoria = df[df["Category"] == categoria_especifica]

    for index, row in dados_categoria.iterrows():
        link = row["Link"]
        job = row["Job"]
        # print(link)
        bot.reply_to(message, f"[{job}]({link})", parse_mode="markdown")
```

## Concluindo

Até o momento temos dois bots disponíveis mas o único que roda automaticamente é o que está inserido em ***scrapper.py***. Ao rodar o script mencionado são enviadas automaticamente mensagens para o grupo do Telegram configurado.

Caso queira executar o segundo bot é necessário que execute o script com:

```bash
python bot_telegram.py
```

- [As referências](/docs/references.md)
- [O scrapper](/docs/scrap_workana.md)

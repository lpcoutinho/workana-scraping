import os

import pandas as pd
import telebot
from clear import Clear
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

df = Clear.clear()

categories = [
    "TI e Programação",
    "Design e Multimedia",
    "Marketing e Vendas",
    "Engenharia e Manufatura",
    "Tradução e conteúdos",
    "Jurídico",
    "Finanças e Administração",
]


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


# current date and time
hour_now = pd.Timestamp.now()
# date and time 24 hours ago
date_24h_ago = hour_now - pd.Timedelta(hours=24)
# filter data from the last 24 hours
df = df[df["Publish Date"] >= date_24h_ago]


# last job
@bot.message_handler(commands=["last"])
def get_last_job(message):
    job = df.loc[0, "Job"]
    link = df.loc[0, "Link"]
    print(type(link))

    bot.reply_to(message, f"[{job}]({link})", parse_mode="markdown")


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


@bot.message_handler(commands=["design"])
def get_last_ti(message):
    categoria_especifica = categories[1]
    dados_categoria = df[df["Category"] == categoria_especifica]

    for index, row in dados_categoria.iterrows():
        link = row["Link"]
        job = row["Job"]
        # print(link)
        bot.reply_to(message, f"[{job}]({link})", parse_mode="markdown")


@bot.message_handler(commands=["marketing"])
def get_last_ti(message):
    categoria_especifica = categories[2]
    dados_categoria = df[df["Category"] == categoria_especifica]

    for index, row in dados_categoria.iterrows():
        link = row["Link"]
        job = row["Job"]
        # print(link)
        bot.reply_to(message, f"[{job}]({link})", parse_mode="markdown")


@bot.message_handler(commands=["engenharia"])
def get_last_ti(message):
    categoria_especifica = categories[3]
    dados_categoria = df[df["Category"] == categoria_especifica]

    for index, row in dados_categoria.iterrows():
        link = row["Link"]
        job = row["Job"]
        # print(link)
        bot.reply_to(message, f"[{job}]({link})", parse_mode="markdown")


@bot.message_handler(commands=["conteudos"])
def get_last_ti(message):
    categoria_especifica = categories[4]
    dados_categoria = df[df["Category"] == categoria_especifica]

    for index, row in dados_categoria.iterrows():
        link = row["Link"]
        job = row["Job"]
        # print(link)
        bot.reply_to(message, f"[{job}]({link})", parse_mode="markdown")


@bot.message_handler(commands=["juridico"])
def get_last_ti(message):
    categoria_especifica = categories[5]
    dados_categoria = df[df["Category"] == categoria_especifica]

    for index, row in dados_categoria.iterrows():
        link = row["Link"]
        job = row["Job"]
        # print(link)
        bot.reply_to(message, f"[{job}]({link})", parse_mode="markdown")


@bot.message_handler(commands=["adm"])
def get_last_ti(message):
    categoria_especifica = categories[6]
    dados_categoria = df[df["Category"] == categoria_especifica]

    for index, row in dados_categoria.iterrows():
        link = row["Link"]
        job = row["Job"]
        # print(link)
        bot.reply_to(message, f"[{job}]({link})", parse_mode="markdown")


linkedin = "https://www.linkedin.com/in/luizpaulocoutinho/"


@bot.message_handler(commands=["info"])
def info(message):
    bot.reply_to(
        message,
        f"ℹ️ FreelaJobs ℹ️\n\nEste bot é desenvolvido por <b>Luiz Paulo Coutinho</b>.\nFique a vontade para entrar em contato no Linkedin. {linkedin}",
        parse_mode="HTML",
    )


@bot.message_handler(commands=["apoio"])
def info(message):
    bot.reply_to(message, f"🤑 Apoie o projeto, me envie um pix!")


bot.infinity_polling()

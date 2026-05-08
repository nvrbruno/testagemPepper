# -*- coding: utf-8 -*-

import os
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

from dotenv import load_dotenv
from naoqi import ALProxy


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

load_dotenv(
    os.path.join(BASE_DIR, "..", "..", ".env")
)

ip = os.getenv("IP")
porta = int(os.getenv("PORT"))

sender = os.getenv("EMAIL_SENDER")
password = os.getenv("EMAIL_PASSWORD")
recipient = os.getenv("EMAIL_RECIPIENT")

arquivo = os.path.join(
    BASE_DIR,
    "assets",
    "logo.png"
)


def get_tts():
    try:
        return ALProxy("ALTextToSpeech", ip, porta)
    except Exception as e:
        print("Aviso: nao foi possivel conectar ao Pepper: {}".format(e))
        return None


subject = "Email Teste"
body = """Linha 1
Linha 2
Linha 3"""

msg = MIMEMultipart()

msg["From"] = sender
msg["To"] = recipient
msg["Subject"] = subject

texto = MIMEText(
    body,
    "plain"
)

msg.attach(texto)


with open(arquivo, "rb") as f:

    img = MIMEImage(f.read())

    img.add_header(
        "Content-Disposition",
        "attachment",
        filename=os.path.basename(arquivo)
    )

    msg.attach(img)


try:

    servidor = smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    )

    servidor.ehlo()

    servidor.login(
        sender,
        password
    )

    servidor.sendmail(
        sender,
        recipient,
        msg.as_string()
    )

    servidor.quit()

    print("Email enviado")

    tts = get_tts()
    if tts:
        tts.say("Email enviado")

except Exception as e:

    print("Erro ao enviar email: {}".format(e))

    tts = get_tts()
    if tts:
        tts.say("Erro ao enviar email")
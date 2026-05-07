# -*- coding: utf-8 -*-
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from naoqi import ALProxy

# Carrega o .env da raiz do projeto
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

ip        = os.getenv("IP")
porta     = int(os.getenv("PORT"))
sender    = os.getenv("EMAIL_SENDER")
password  = os.getenv("EMAIL_PASSWORD")
recipient = os.getenv("EMAIL_RECIPIENT")

# Voz do Pepper
tts = ALProxy("ALTextToSpeech", ip, porta)


def send_email(sender, password, recipient, subject, body, file_path=None):
    # Monta o email
    msg = MIMEMultipart()
    msg["From"]    = sender
    msg["To"]      = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Anexa arquivo se informado
    if file_path:
        with open(file_path, "rb") as f:
            anexo = MIMEBase("application", "octet-stream")
            anexo.set_payload(f.read())
        encoders.encode_base64(anexo)
        anexo.add_header("Content-Disposition", "attachment", filename=os.path.basename(file_path))
        msg.attach(anexo)

    # Envia pelo Gmail
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(sender, password)
    servidor.sendmail(sender, recipient, msg.as_string())
    servidor.quit()


try:
    send_email(
        sender    = sender,
        password  = password,
        recipient = recipient,
        subject   = "Email Teste",
        body      = """Linha 1
Linha 2
Linha 3""",
        file_path = "./assets/SESI_MAKERTHON_LOGO.png"
    )
    tts.say("Email enviado com sucesso")

except Exception as e:
    print("Erro ao enviar email:", e)
    tts.say("Erro ao enviar email")
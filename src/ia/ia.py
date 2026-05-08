# -*- coding: utf-8 -*-
import os
import sys
import requests
import unicodedata
from dotenv import load_dotenv
from naoqi import ALProxy

# Carrega o .env da raiz do projeto
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

ip       = os.getenv("IP")
porta    = int(os.getenv("PORT"))
api_key  = os.getenv("GROQ_API_KEY")
url      = os.getenv("GROQ_URL")

# Conecta ao Pepper
tts            = ALProxy("ALTextToSpeech", ip, porta)
animated_speech = ALProxy("ALAnimatedSpeech", ip, porta)
tts.setLanguage("Portuguese")


def limpar_texto(texto):
    if isinstance(texto, str):
        texto = texto.decode('utf-8', 'ignore')
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    texto = texto.replace(u'\u201c', '"').replace(u'\u201d', '"')
    texto = texto.replace(u'\u2018', "'").replace(u'\u2019', "'")
    texto = texto.replace(u'\u2013', '-').replace(u'\u2014', '-')
    if isinstance(texto, unicode):
        texto = texto.encode('ascii', 'ignore')
    return texto


historico = [
    {"role": "system", "content": "Voce e a Pepper, robo assistente simpatico. IMPORTANTE: Responda SOMENTE com letras sem acento (a,e,i,o,u e nao a,e,i,o,u com acento), sem cedilha, sem caracteres especiais, sem pontuacao especial. Use apenas letras simples do alfabeto ingles, numeros, virgula e ponto final."}
]

print("Pepper IA!")
print("Digite 'sair' para fechar.\n")

while True:
    # Lê input do usuário
    try:
        msg = raw_input("Voce: ")
        if isinstance(msg, str):
            msg = msg.decode(sys.stdin.encoding or 'utf-8', 'ignore')
        msg = limpar_texto(msg)
    except Exception as e:
        print("Erro ao ler input: " + str(e))
        continue

    if msg.lower() == "sair":
        break

    historico.append({"role": "user", "content": msg})

    # Envia para a API do Groq
    headers = {"Authorization": "Bearer " + api_key, "Content-Type": "application/json"}
    data    = {"model": "llama-3.3-70b-versatile", "messages": historico, "temperature": 0.7}

    try:
        r      = requests.post(url, headers=headers, json=data)
        texto  = r.json()["choices"][0]["message"]["content"]
        historico.append({"role": "assistant", "content": texto})

        texto_limpo = limpar_texto(texto)
        print("\nPepper: " + texto_limpo + "\n")

        if isinstance(texto_limpo, unicode):
            texto_limpo = texto_limpo.encode('ascii', 'ignore')

        # Fala com animação, fallback para tts simples
        try:
            animated_speech.say(str(texto_limpo))
        except:
            tts.say(str(texto_limpo))

    except Exception as e:
        print("Erro: " + str(e))
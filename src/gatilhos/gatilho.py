# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from naoqi import ALProxy

# Carrega o .env da raiz do projeto
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

ip    = os.getenv("IP")
porta = int(os.getenv("PORT"))

# Troque para a palavra que quiser reconhecer
PALAVRA_GATILHO = "Pepper"

# Conecta ao Pepper
sr  = ALProxy("ALSpeechRecognition", ip, porta)
mem = ALProxy("ALMemory", ip, porta)
tts = ALProxy("ALTextToSpeech", ip, porta)

sr.setLanguage("Portuguese")
sr.setVocabulary([PALAVRA_GATILHO], False)
sr.subscribe("gatilho_voz")

print("Ouvindo... fale '" + PALAVRA_GATILHO + "' para ativar.\n")

try:
    while True:
        resultado = mem.getData("WordRecognized")

        if resultado and resultado[0] == PALAVRA_GATILHO and resultado[1] > 0.4:
            print("Gatilho ativado!")

            # Cole sua funcao aqui
            tts.say("Gatilho ativado")

            mem.insertData("WordRecognized", ["", 0.0])

except KeyboardInterrupt:
    print("Encerrando...")
    sr.unsubscribe("gatilho_voz")
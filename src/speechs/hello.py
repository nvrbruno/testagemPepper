# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from naoqi import ALProxy

# Carrega o .env da raiz do projeto (1 nível acima)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

ip    = os.getenv("IP")
porta = int(os.getenv("PORT"))

tts = ALProxy("ALTextToSpeech", ip, porta)
tts.say("Hello, world!")
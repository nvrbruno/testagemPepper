# -*- coding: utf-8 -*-
import os
import time
from dotenv import load_dotenv
from naoqi import ALProxy

# Carrega o .env da raiz do projeto
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

ip    = os.getenv("IP")
porta = int(os.getenv("PORT"))

# Conecta ao Pepper
try:
    tts = ALProxy("ALTextToSpeech", ip, porta)
    print("Conectado ao robo com sucesso!")
except Exception as e:
    print("Erro ao conectar:", e)
    exit(1)

# Testes de voz
print("[TESTE 1] Fala basica...")
tts.say("Hello, my name is Pepper")
time.sleep(2)

print("[TESTE 2] Falando lentamente...")
tts.setParameter("speed", 80)
tts.say("I am speaking slowly")
time.sleep(2)

print("[TESTE 3] Falando rapidamente...")
tts.setParameter("speed", 120)
tts.say("Now I am speaking very fast")
time.sleep(2)

print("[TESTE 4] Ajustando volume...")
tts.setParameter("speed", 100)
tts.setVolume(0.5)
tts.say("I am speaking quietly")
tts.setVolume(1.0)
tts.say("Now I am back to normal volume")
time.sleep(2)

print("[TESTE 5] Tom agudo e grave...")
tts.say("\\vct=150\\I have a high pitched voice")
time.sleep(1)
tts.say("\\vct=70\\Now I have a deep voice")
time.sleep(2)

print("[TESTE 6] Com pausa...")
tts.say("First part. \\pau=1000\\ Second part")

print("\n[SUCESSO] Todos os testes completados!")
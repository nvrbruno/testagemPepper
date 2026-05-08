# -*- coding: utf-8 -*-
import os
import time
from dotenv import load_dotenv
from naoqi import ALProxy

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

IP   = os.getenv("IP")
PORT = int(os.getenv("PORT"))

motion = ALProxy("ALMotion", IP, PORT)
motion.setStiffnesses("Body", 1.0)

DELAY = 1.5  # segundos entre cada movimento

# moveTo(x, y, theta) — x: frente/trás | y: lateral | theta: rotação
def andar_frente():
    # anda 30cm para frente
    motion.moveTo(0.3, 0.0, 0.0)

def andar_tras():
    # anda 30cm para trás
    motion.moveTo(-0.3, 0.0, 0.0)

def andar_esquerda():
    # desloca 20cm para a esquerda
    motion.moveTo(0.0, 0.2, 0.0)

def andar_direita():
    # desloca 20cm para a direita
    motion.moveTo(0.0, -0.2, 0.0)


if __name__ == "__main__":
    motion.moveInit()

    andar_frente()
    time.sleep(DELAY)

    andar_tras()
    time.sleep(DELAY)

    andar_esquerda()
    time.sleep(DELAY)

    andar_direita()
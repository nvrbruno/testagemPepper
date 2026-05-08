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

def cabeca_esquerda():
    # vira a cabeça para a esquerda
    motion.angleInterpolation("HeadYaw", 0.5, 0.6, True)

def cabeca_direita():
    # vira a cabeça para a direita
    motion.angleInterpolation("HeadYaw", -0.5, 0.6, True)

def cabeca_cima():
    # inclina a cabeça para cima
    motion.angleInterpolation("HeadPitch", -0.3, 0.6, True)

def cabeca_baixo():
    # inclina a cabeça para baixo
    motion.angleInterpolation("HeadPitch", 0.3, 0.6, True)

def cabeca_centro():
    # retorna a cabeça para a posição neutra
    motion.angleInterpolation(["HeadYaw", "HeadPitch"], [0.0, 0.0], [0.5, 0.5], True)


if __name__ == "__main__":
    cabeca_esquerda()
    time.sleep(DELAY)

    cabeca_direita()
    time.sleep(DELAY)

    cabeca_cima()
    time.sleep(DELAY)

    cabeca_baixo()
    time.sleep(DELAY)

    cabeca_centro()
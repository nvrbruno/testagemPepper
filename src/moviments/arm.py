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

def braco_esquerdo_cima():
    # levanta o braço esquerdo
    motion.angleInterpolation("LShoulderPitch", 0.0, 0.8, True)

def braco_esquerdo_baixo():
    # abaixa o braço esquerdo
    motion.angleInterpolation("LShoulderPitch", 1.5, 0.8, True)

def braco_direito_cima():
    # levanta o braço direito
    motion.angleInterpolation("RShoulderPitch", 0.0, 0.8, True)

def braco_direito_baixo():
    # abaixa o braço direito
    motion.angleInterpolation("RShoulderPitch", 1.5, 0.8, True)

def bracos_neutro():
    # retorna ambos os braços para a posição neutra
    motion.angleInterpolation(
        ["LShoulderPitch", "RShoulderPitch"],
        [1.5, 1.5],
        [0.8, 0.8],
        True
    )


if __name__ == "__main__":
    braco_esquerdo_cima()
    time.sleep(DELAY)

    braco_esquerdo_baixo()
    time.sleep(DELAY)

    braco_direito_cima()
    time.sleep(DELAY)

    braco_direito_baixo()
    time.sleep(DELAY)

    bracos_neutro()
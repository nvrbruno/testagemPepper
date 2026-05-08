# -*- coding: utf-8 -*-

import os
import time
from dotenv import load_dotenv
from naoqi import ALProxy

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

IP = os.getenv("IP")
PORT = int(os.getenv("PORT"))

motion = ALProxy("ALMotion", IP, PORT)

motion.setStiffnesses("Body", 1.0)

def mover(juntas, angulos, tempos):
    motion.angleInterpolation(juntas, angulos, tempos, True)

def MOVIMENTO_001():
    motion.moveInit()
    motion.moveTo(0.10, 0.0, 0.06)

    juntas = [
        "HeadYaw", "HeadPitch",
        "LShoulderPitch", "RShoulderPitch",
        "LShoulderRoll", "RShoulderRoll",
        "LElbowRoll", "RElbowRoll",
        "LWristYaw", "RWristYaw"
    ]

    angulos = [
        [0.0, -0.05, 0.02],
        [-0.12, -0.08, -0.10],
        [1.55, 1.38, 1.32],
        [1.55, 1.38, 1.32],
        [0.10, 0.18, 0.14],
        [-0.10, -0.18, -0.14],
        [-0.25, -0.48, -0.42],
        [0.25, 0.48, 0.42],
        [-0.20, -0.05, -0.10],
        [0.20, 0.05, 0.10]
    ]

    tempos = [[0.6, 1.4, 2.2]] * len(juntas)

    mover(juntas, angulos, tempos)

def MOVIMENTO_002():
    motion.moveInit()
    motion.moveTo(0.05, 0.0, 0.18)

    juntas = [
        "RShoulderPitch",
        "RShoulderRoll",
        "RElbowYaw",
        "RElbowRoll",
        "RWristYaw",
        "HeadYaw",
        "HeadPitch"
    ]

    angulos = [
        [0.95, 0.72, 0.62],
        [-0.20, -0.42, -0.55],
        [0.90, 1.35, 1.75],
        [0.90, 1.30, 1.52],
        [0.20, 0.60, 0.95],
        [0.0, 0.10, 0.05],
        [-0.08, -0.03, -0.05]
    ]

    tempos = [[0.6, 1.4, 2.2]] * len(juntas)

    mover(juntas, angulos, tempos)

def MOVIMENTO_003():
    motion.moveInit()
    motion.moveTo(0.02, 0.0, 0.32)

    juntas = [
        "HeadYaw", "HeadPitch",
        "LShoulderPitch", "RShoulderPitch",
        "LShoulderRoll", "RShoulderRoll",
        "LElbowRoll", "RElbowRoll",
        "LWristYaw", "RWristYaw"
    ]

    angulos = [
        [0.0, -0.18, 0.12],
        [-0.05, -0.12, -0.04],
        [1.45, 0.95, 1.10],
        [1.45, 0.88, 1.00],
        [0.18, 0.42, 0.28],
        [-0.18, -0.42, -0.28],
        [-0.45, -0.95, -0.72],
        [0.45, 0.95, 0.72],
        [-0.10, -0.35, -0.15],
        [0.10, 0.35, 0.15]
    ]

    tempos = [[0.6, 1.4, 2.2]] * len(juntas)

    mover(juntas, angulos, tempos)

def MOVIMENTO_004():
    motion.moveInit()
    motion.moveTo(0.14, -0.01, -0.08)

    juntas = [
        "HeadYaw", "HeadPitch",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowYaw", "RElbowRoll",
        "RWristYaw",
        "LShoulderPitch", "LShoulderRoll",
        "LElbowRoll"
    ]

    angulos = [
        [0.0, 0.10, 0.05],
        [-0.08, -0.03, -0.05],
        [1.05, 0.72, 0.62],
        [-0.20, -0.42, -0.55],
        [0.90, 1.35, 1.75],
        [0.90, 1.30, 1.52],
        [0.20, 0.60, 0.95],
        [1.40, 1.48, 1.44],
        [0.16, 0.24, 0.20],
        [-0.35, -0.52, -0.46]
    ]

    tempos = [[0.5, 1.3, 2.0]] * len(juntas)

    mover(juntas, angulos, tempos)

def MOVIMENTO_005():
    motion.moveInit()
    motion.moveTo(0.0, 0.0, -0.22)

    juntas = [
        "HeadYaw", "HeadPitch",
        "LShoulderPitch", "RShoulderPitch",
        "LShoulderRoll", "RShoulderRoll",
        "LElbowRoll", "RElbowRoll"
    ]

    angulos = [
        [0.0, 0.18, 0.08],
        [0.02, 0.18, 0.10],
        [1.55, 1.68, 1.58],
        [1.10, 0.95, 1.05],
        [0.12, 0.08, 0.10],
        [-0.18, -0.08, -0.12],
        [-0.32, -0.22, -0.28],
        [0.65, 0.88, 0.72]
    ]

    tempos = [[0.8, 1.8, 2.8]] * len(juntas)

    mover(juntas, angulos, tempos)

def MOVIMENTO_006():
    motion.moveInit()
    motion.moveTo(0.04, 0.05, 0.10)

    juntas = [
        "HeadYaw", "HeadPitch",
        "LShoulderPitch", "LShoulderRoll",
        "LElbowYaw", "LElbowRoll",
        "LWristYaw",
        "RShoulderPitch", "RShoulderRoll"
    ]

    angulos = [
        [-0.08, 0.10, -0.05],
        [-0.04, -0.10, -0.02],
        [1.45, 0.82, 1.10],
        [0.18, 0.55, 0.32],
        [-0.80, -1.55, -1.10],
        [-0.25, -0.92, -0.55],
        [-0.10, -0.75, -0.25],
        [1.20, 1.05, 1.12],
        [-0.12, -0.18, -0.15]
    ]

    tempos = [[0.5, 1.4, 2.2]] * len(juntas)

    mover(juntas, angulos, tempos)

def MOVIMENTO_007():
    motion.moveInit()
    motion.moveTo(-0.03, -0.02, 0.18)

    juntas = [
        "HeadYaw", "HeadPitch",
        "LShoulderPitch", "LShoulderRoll",
        "LElbowYaw", "LElbowRoll",
        "LWristYaw",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowYaw", "RElbowRoll"
    ]

    angulos = [
        [0.0, 0.04, 0.0],
        [0.05, 0.16, 0.10],
        [1.55, 1.28, 1.40],
        [0.10, 0.22, 0.16],
        [-0.90, -1.10, -1.00],
        [-0.18, -0.42, -0.32],
        [-0.05, -0.15, -0.08],
        [1.02, 0.78, 0.88],
        [-0.22, -0.45, -0.38],
        [1.00, 1.45, 1.30],
        [0.95, 1.42, 1.28]
    ]

    tempos = [[0.8, 1.9, 3.0]] * len(juntas)

    mover(juntas, angulos, tempos)

def MOVIMENTO_008():
    motion.moveInit()
    motion.moveTo(0.06, 0.03, -0.10)

    juntas = [
        "HeadYaw", "HeadPitch",
        "LShoulderPitch", "LShoulderRoll",
        "LElbowYaw", "LElbowRoll",
        "LWristYaw",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowRoll"
    ]

    angulos = [
        [-0.06, 0.08, -0.04],
        [-0.02, -0.08, -0.04],
        [1.50, 1.15, 1.28],
        [0.12, 0.32, 0.18],
        [-0.75, -1.05, -0.90],
        [-0.20, -0.48, -0.35],
        [-0.08, -0.25, -0.12],
        [1.42, 1.30, 1.36],
        [-0.12, -0.18, -0.14],
        [0.65, 0.82, 0.72]
    ]

    tempos = [[0.8, 1.8, 2.8]] * len(juntas)

    mover(juntas, angulos, tempos)

def MOVIMENTO_009():
    motion.moveInit()
    motion.moveTo(0.03, 0.0, 0.26)

    juntas = [
        "HeadYaw", "HeadPitch",
        "LShoulderPitch", "LShoulderRoll",
        "LElbowYaw", "LElbowRoll",
        "LWristYaw",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowYaw", "RElbowRoll"
    ]

    angulos = [
        [0.0, -0.12, 0.02],
        [-0.05, -0.10, -0.04],
        [1.30, 0.82, 0.95],
        [0.18, 0.48, 0.28],
        [-0.90, -1.50, -1.20],
        [-0.25, -0.85, -0.52],
        [-0.10, -0.65, -0.25],
        [1.10, 0.92, 1.00],
        [-0.20, -0.38, -0.28],
        [1.00, 1.35, 1.18],
        [0.92, 1.42, 1.20]
    ]

    tempos = [[0.5, 1.3, 2.0]] * len(juntas)

    mover(juntas, angulos, tempos)

def MOVIMENTO_010():
    motion.moveInit()
    motion.moveTo(0.08, 0.0, 0.20)

    juntas = [
        "HeadYaw", "HeadPitch",
        "LShoulderPitch", "LShoulderRoll",
        "LElbowYaw", "LElbowRoll",
        "LWristYaw",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowYaw", "RElbowRoll",
        "RWristYaw"
    ]

    angulos = [
        [0.0, -0.10, 0.0],
        [-0.04, -0.08, -0.02],
        [1.35, 0.92, 1.08],
        [0.18, 0.52, 0.26],
        [-0.90, -1.50, -1.10],
        [-0.25, -0.82, -0.48],
        [-0.10, -0.65, -0.18],
        [1.02, 0.82, 0.92],
        [-0.22, -0.45, -0.36],
        [1.00, 1.42, 1.25],
        [0.95, 1.38, 1.22],
        [0.10, 0.35, 0.18]
    ]

    tempos = [[0.6, 1.6, 2.8]] * len(juntas)

    mover(juntas, angulos, tempos)

    motion.moveInit()
    motion.moveTo(0.0, 0.0, -0.12)

    juntas = [
        "HeadYaw",
        "HeadPitch",
        "LShoulderPitch",
        "LShoulderRoll",
        "RShoulderPitch",
        "RShoulderRoll"
    ]

    angulos = [
        [0.0],
        [-0.04],
        [1.48],
        [0.14],
        [1.10],
        [-0.24]
    ]

    tempos = [[1.2]] * len(juntas)

    mover(juntas, angulos, tempos)

MOVIMENTO_001()
time.sleep(1.5)

MOVIMENTO_002()
time.sleep(1.5)

MOVIMENTO_003()
time.sleep(1.5)

MOVIMENTO_004()
time.sleep(1.5)

MOVIMENTO_005()
time.sleep(1.5)

MOVIMENTO_006()
time.sleep(1.5)

MOVIMENTO_007()
time.sleep(1.5)

MOVIMENTO_008()
time.sleep(1.5)

MOVIMENTO_009()
time.sleep(1.5)

MOVIMENTO_010()

motion.setStiffnesses("Body", 0.0)
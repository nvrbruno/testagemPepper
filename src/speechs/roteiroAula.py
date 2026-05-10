# -*- coding: utf-8 -*-
 
import os
import time
from dotenv import load_dotenv
from naoqi import ALProxy
 
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
 
# ── Conexão ────────────────────────────────────────────────────────────────────
IP   = os.getenv("IP")
PORT = int(os.getenv("PORT"))
 
# ── Parâmetros de fala (edite aqui) ───────────────────────────────────────────
SPEECH_SPEED   = 85       # velocidade de fala: 50 (lento) → 150 (rápido)
SPEECH_PITCH   = 0.9      # tom de voz: 0.5 (grave) → 4.0 (agudo) | 1.0 = normal
SPEECH_VOLUME  = 0.75     # volume: 0.0 (mudo) → 1.0 (máximo)
SPEECH_LANG    = "Portuguese"            # idioma instalado no robô/simulador
PAUSE_DURATION = 0.8      # duração das pausas dramáticas em segundos
 
# ── Proxies ────────────────────────────────────────────────────────────────────
motion  = ALProxy("ALMotion",       IP, PORT)
tts     = ALProxy("ALTextToSpeech", IP, PORT)
posture = ALProxy("ALRobotPosture", IP, PORT)
 
# Aplica parâmetros de fala
tts.setLanguage(SPEECH_LANG)
tts.setParameter("speed",      SPEECH_SPEED)
tts.setParameter("pitchShift", SPEECH_PITCH)
tts.setParameter("volume",     SPEECH_VOLUME)
 
motion.setStiffnesses("Body", 1.0)
posture.goToPosture("StandInit", 0.6)
 
# ── Utilitários ────────────────────────────────────────────────────────────────
def mover(juntas, angulos, tempos):
    motion.angleInterpolation(juntas, angulos, tempos, True)
 
def pausa():
    time.sleep(PAUSE_DURATION)
 
def falar_e_mover(texto, fn_movimento):
    """Dispara fala em background (NAOqi nativo) e executa movimento em paralelo."""
    tts.post.say(texto)
    fn_movimento()
 
def so_falar(texto):
    tts.say(texto)
 
# ── Movimentos ─────────────────────────────────────────────────────────────────
 
def MOVIMENTO_001():
    """Postura neutra, corpo ereto, braços relaxados."""
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
 
def MOVIMENTO_007():
    """Mão no peito — emoção/convicção."""
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
 
def MOVIMENTO_016():
    """Apontar levemente para frente — afirmação."""
    juntas = [
        "HeadYaw", "HeadPitch",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowYaw", "RElbowRoll",
        "RWristYaw",
        "LShoulderPitch", "LShoulderRoll",
        "LElbowRoll"
    ]
    angulos = [
        [0.0, 0.05, 0.0],
        [-0.10, -0.05, -0.08],
        [0.80, 0.55, 0.65],   # braço direito avança para frente
        [-0.10, -0.20, -0.14],
        [1.05, 1.45, 1.25],
        [0.35, 0.55, 0.45],
        [0.10, 0.20, 0.14],
        [1.45, 1.38, 1.42],   # braço esquerdo relaxado
        [0.12, 0.18, 0.14],
        [-0.30, -0.42, -0.35]
    ]
    tempos = [[0.5, 1.2, 1.8]] * len(juntas)
    mover(juntas, angulos, tempos)
 
def MOVIMENTO_018():
    """Braço firme com corte no ar — ênfase forte."""
    juntas = [
        "HeadYaw", "HeadPitch",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowYaw", "RElbowRoll",
        "RWristYaw",
        "LShoulderPitch", "LShoulderRoll",
        "LElbowRoll"
    ]
    angulos = [
        [0.0, 0.0, 0.0],
        [-0.08, -0.04, -0.06],
        [0.60, 0.30, 0.45],   # braço levantado
        [-0.05, -0.15, -0.08],
        [1.10, 1.52, 1.30],
        [0.28, 0.55, 0.38],
        [-0.30, -0.55, -0.40],  # "corte" no ar
        [1.48, 1.35, 1.42],
        [0.10, 0.18, 0.14],
        [-0.28, -0.45, -0.35]
    ]
    tempos = [[0.4, 0.9, 1.5]] * len(juntas)  # movimentos mais rápidos = ênfase
    mover(juntas, angulos, tempos)
 
def MOVIMENTO_036():
    """Mão sobre o peito + leve inclinação — respeito e fechamento."""
    juntas = [
        "HeadYaw", "HeadPitch",
        "LShoulderPitch", "LShoulderRoll",
        "LElbowYaw", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll",
        "RElbowRoll",
        "HipPitch"             # leve inclinação do tronco
    ]
    angulos = [
        [0.0, 0.02, 0.0],
        [0.05, 0.20, 0.14],    # cabeça levemente baixa
        [1.55, 1.20, 1.35],    # braço esquerdo sobe até o peito
        [0.08, 0.18, 0.12],
        [-0.85, -1.05, -0.95],
        [-0.15, -0.38, -0.28],
        [1.42, 1.30, 1.36],    # braço direito relaxado ao lado
        [-0.12, -0.18, -0.14],
        [0.60, 0.80, 0.68],
        [-0.08, -0.18, -0.12]  # leve inclinação para frente
    ]
    tempos = [[1.0, 2.2, 3.5]] * len(juntas)  # movimentos lentos = solenidade
    mover(juntas, angulos, tempos)
 
# ── Roteiro de Napoleão ────────────────────────────────────────────────────────
 
def roteiro_napoleao():
 
    # --- Bloco 1: Apresentação ---
    falar_e_mover(
        "Eu sou Napoleão Bonaparte. "
        "De origens simples, ergui-me em meio ao caos da França revolucionária.",
        MOVIMENTO_001
    )
    pausa()
 
    falar_e_mover(
        "Não nasci rei... tornei-me líder pela força da estratégia e da vontade.",
        MOVIMENTO_016
    )
    pausa()
 
    # --- Bloco 2: O grande feito ---
    falar_e_mover(
        "Quando a França mergulhou na instabilidade, vi ali uma oportunidade. "
        "Organizei exércitos, venci batalhas e mostrei que disciplina supera o caos.",
        MOVIMENTO_018
    )
    pausa()
 
    falar_e_mover(
        "Cada vitória não era apenas militar... era política. "
        "Eu consolidava poder, restaurava ordem e construía um império.",
        MOVIMENTO_016
    )
    pausa()
 
    falar_e_mover(
        "Mas não foi apenas conquista. Foi visão. "
        "Eu acreditava que podia moldar o destino de uma nação inteira.",
        MOVIMENTO_007
    )
    pausa()
 
    falar_e_mover(
        "E por um tempo... eu consegui.",
        MOVIMENTO_018
    )
    pausa()
 
    # --- Bloco 3: Visão de mundo ---
    falar_e_mover(
        "O mundo pertence àqueles que agem. "
        "Sorte favorece os preparados, mas a coragem define os vencedores.",
        MOVIMENTO_016
    )
    pausa()
 
    falar_e_mover(
        "Eu sempre acreditei no mérito... não no acaso.",
        MOVIMENTO_007
    )
    pausa()
 
    # --- Bloco 4: Curiosidade ---
    falar_e_mover(
        "Poucos sabem, mas eu valorizava profundamente a educação e o conhecimento estratégico.",
        MOVIMENTO_001
    )
    pausa()
 
    falar_e_mover(
        "Livros, para mim, eram armas tão poderosas quanto canhões.",
        MOVIMENTO_016
    )
    pausa()
 
    # --- Bloco 5: Encerramento ---
    falar_e_mover(
        "Meu nome ecoa na história. Não por acaso... mas por decisão.",
        MOVIMENTO_036
    )
    pausa()
 
    so_falar("Construa o seu destino.")
 
# ── Execução ───────────────────────────────────────────────────────────────────
 
try:
    roteiro_napoleao()
finally:
    posture.goToPosture("StandInit", 0.5)
    motion.setStiffnesses("Body", 0.0)
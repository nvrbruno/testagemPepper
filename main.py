# -*- coding: utf-8 -*-
import os
import sys
import time
import smtplib
import requests
import unicodedata
import webbrowser

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

from dotenv import load_dotenv
from naoqi import ALProxy


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACAO GLOBAL
# ═══════════════════════════════════════════════════════════════════════════

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

IP   = os.getenv("IP")
PORT = int(os.getenv("PORT"))

EMAIL_SENDER    = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD  = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

API_KEY  = os.getenv("API_KEY")
GROQ_URL = os.getenv("GROQ_URL")


# ═══════════════════════════════════════════════════════════════════════════
# PROXIES GLOBAIS (cada um conectado individualmente)
# ═══════════════════════════════════════════════════════════════════════════

def _conectar_proxy(nome_servico):
    try:
        proxy = ALProxy(nome_servico, IP, PORT)
        print("  [OK] " + nome_servico)
        return proxy
    except Exception as e:
        print("  [--] {} indisponivel: {}".format(nome_servico, e))
        return None

print("Conectando proxies em {}:{}...".format(IP, PORT))

sr              = _conectar_proxy("ALSpeechRecognition")
mem             = _conectar_proxy("ALMemory")
tts             = _conectar_proxy("ALTextToSpeech")
motion          = _conectar_proxy("ALMotion")
posture         = _conectar_proxy("ALRobotPosture")
animated_speech = _conectar_proxy("ALAnimatedSpeech")
tablet          = _conectar_proxy("ALTabletService")

# Capacidades disponíveis
TEM_VOZ      = sr is not None and mem is not None and tts is not None
TEM_MOTION   = motion is not None
TEM_POSTURA  = posture is not None
TEM_TABLET   = tablet is not None
TEM_ANIMACAO = animated_speech is not None

PEPPER_CONECTADA = TEM_VOZ or TEM_MOTION

if PEPPER_CONECTADA:
    print("\nPepper conectada!")
    print("  Voz:    {}".format("sim" if TEM_VOZ else "nao (Choregraphe?)"))
    print("  Motion: {}".format("sim" if TEM_MOTION else "nao"))
    print("  Tablet: {}".format("sim" if TEM_TABLET else "nao (Choregraphe?)"))
    if tts:
        tts.setLanguage("Portuguese")
    if motion:
        motion.setStiffnesses("Body", 1.0)
    if sr:
        sr.setLanguage("Portuguese")
else:
    print("\nPepper nao conectada - nenhum servico disponivel")


# ═══════════════════════════════════════════════════════════════════════════
# 1 - ENVIAR EMAIL
# ═══════════════════════════════════════════════════════════════════════════

def enviar_email():
    subject = "Email Teste"
    body    = "Linha 1\nLinha 2\nLinha 3"

    msg = MIMEMultipart()
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = EMAIL_RECIPIENT
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    arquivo_logo = os.path.join(BASE_DIR, "src", "emails", "assets", "logo.png")
    if os.path.exists(arquivo_logo):
        with open(arquivo_logo, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-Disposition", "attachment",
                           filename=os.path.basename(arquivo_logo))
            msg.attach(img)

    try:
        servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        servidor.ehlo()
        servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)
        servidor.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        servidor.quit()
        print("Email enviado")
        if tts:
            tts.say("Email enviado com sucesso")
    except Exception as e:
        print("Erro ao enviar email: {}".format(e))
        if tts:
            tts.say("Erro ao enviar email")


# ═══════════════════════════════════════════════════════════════════════════
# 2 - FALAR HELLO WORLD
# ═══════════════════════════════════════════════════════════════════════════

def falar_hello_world():
    print("Hello, world!")
    if tts:
        tts.say("Hello, world!")


# ═══════════════════════════════════════════════════════════════════════════
# 3 - CONVERSAR COM IA
# ═══════════════════════════════════════════════════════════════════════════

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


def conversar_ia():
    if not TEM_VOZ:
        print("Reconhecimento de voz indisponivel (Choregraphe?). Use a opcao 3 - Conversar com IA (terminal).")
        return

    tts.setVolume(0.8)
    tts.setParameter("speed", 90)
    tts.setParameter("pitchShift", 1.1)

    historico = [
        {"role": "system", "content": (
            "Voce e a Pepper, robo assistente simpatico. "
            "IMPORTANTE: Responda SOMENTE com letras sem acento, "
            "sem cedilha, sem caracteres especiais, sem pontuacao especial. "
            "Use apenas letras simples do alfabeto ingles, numeros, virgula e ponto final."
        )}
    ]

    tts.say("Modo conversa ativado. Pode falar!")
    print("Pepper IA ativada. Fale com ela!\n")

    try:
        sr.unsubscribe("gatilho_voz")
    except:
        pass
    time.sleep(0.5)

    sr.setVocabulary(["sair conversa"], True)
    sr.subscribe("modo_conversa")

    try:
        while True:
            resultado = mem.getData("WordRecognized")
            if resultado and resultado[1] > 0.4 and resultado[0] == "sair conversa":
                tts.say("Encerrando conversa")
                print("Conversa encerrada pelo usuario")
                break
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        sr.unsubscribe("modo_conversa")
        time.sleep(0.5)
        _reativar_gatilhos()


def conversar_ia_terminal():
    configuracao_animacao = {"bodyLanguageMode": "contextual"}

    if tts:
        tts.setVolume(0.8)
        tts.setParameter("speed", 90)
        tts.setParameter("pitchShift", 1.1)

    historico = [
        {"role": "system", "content": (
            "Voce e a Pepper, robo assistente simpatico. "
            "IMPORTANTE: Responda SOMENTE com letras sem acento, "
            "sem cedilha, sem caracteres especiais, sem pontuacao especial. "
            "Use apenas letras simples do alfabeto ingles, numeros, virgula e ponto final."
        )}
    ]

    print("Pepper IA! Digite 'sair' para fechar.\n")

    while True:
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

        headers = {
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": historico,
            "temperature": 0.7
        }

        try:
            r     = requests.post(GROQ_URL, headers=headers, json=data)
            texto = r.json()["choices"][0]["message"]["content"]
            historico.append({"role": "assistant", "content": texto})

            texto_limpo = limpar_texto(texto)
            print("\nPepper: " + texto_limpo + "\n")

            if tts:
                if isinstance(texto_limpo, unicode):
                    texto_limpo = texto_limpo.encode('ascii', 'ignore')
                try:
                    if animated_speech:
                        animated_speech.say(str(texto_limpo), configuracao_animacao)
                    else:
                        tts.say(str(texto_limpo))
                except:
                    tts.say(str(texto_limpo))

        except Exception as e:
            print("Erro: " + str(e))


# ═══════════════════════════════════════════════════════════════════════════
# 4 - ANDAR FRENTE
# ═══════════════════════════════════════════════════════════════════════════

def andar_frente():
    if not TEM_MOTION:
        print("Motion indisponivel")
        return
    if TEM_POSTURA:                        # levanta antes de andar (necessario no Choregraphe)
        posture.goToPosture("Stand", 0.8)
    motion.moveInit()
    motion.moveTo(0.3, 0.0, 0.0)


# ═══════════════════════════════════════════════════════════════════════════
# 5 - ANDAR TRAS
# ═══════════════════════════════════════════════════════════════════════════

def andar_tras():
    if not TEM_MOTION:
        print("Motion indisponivel")
        return
    if TEM_POSTURA:                        # levanta antes de andar (necessario no Choregraphe)
        posture.goToPosture("Stand", 0.8)
    motion.moveInit()
    motion.moveTo(-0.3, 0.0, 0.0)


# ═══════════════════════════════════════════════════════════════════════════
# 6 - ABRIR TABLET
# ═══════════════════════════════════════════════════════════════════════════

def abrir_tablet():
    caminho_html = os.path.join(BASE_DIR, "src", "tablet", "index.html")

    if not os.path.exists(caminho_html):
        print("index.html nao encontrado")
        if tts:
            tts.say("Arquivo do tablet nao encontrado")
        return

    if TEM_TABLET:
        try:
            url = "file:///" + caminho_html.replace("\\", "/")
            try:
                tablet.enableWifi()
            except:
                pass
            tablet.showWebview(url)
            print("Interface carregada no tablet!")
        except Exception as e:
            print("Erro no tablet: " + str(e))
            webbrowser.open("file:///" + caminho_html.replace("\\", "/"))
    else:
        print("Tablet indisponivel (Choregraphe?) - abrindo no navegador local")
        webbrowser.open("file:///" + caminho_html.replace("\\", "/"))


# ═══════════════════════════════════════════════════════════════════════════
# 7 - ROTEIRO NAPOLEAO
# ═══════════════════════════════════════════════════════════════════════════

def mover(juntas, angulos, tempos):
    if not TEM_MOTION:
        return
    motion.angleInterpolation(juntas, angulos, tempos, True)


def pausa():
    time.sleep(0.8)


def falar_e_mover(texto, fn_movimento):
    if tts:
        tts.post.say(texto)
    else:
        print(texto)
    fn_movimento()


def so_falar(texto):
    if tts:
        tts.say(texto)
    else:
        print(texto)


def MOVIMENTO_001():
    juntas  = ["HeadYaw","HeadPitch","LShoulderPitch","RShoulderPitch",
               "LShoulderRoll","RShoulderRoll","LElbowRoll","RElbowRoll",
               "LWristYaw","RWristYaw"]
    angulos = [[0.0,-0.05,0.02],[-0.12,-0.08,-0.10],[1.55,1.38,1.32],
               [1.55,1.38,1.32],[0.10,0.18,0.14],[-0.10,-0.18,-0.14],
               [-0.25,-0.48,-0.42],[0.25,0.48,0.42],[-0.20,-0.05,-0.10],
               [0.20,0.05,0.10]]
    tempos  = [[0.6,1.4,2.2]] * len(juntas)
    mover(juntas, angulos, tempos)


def MOVIMENTO_007():
    juntas  = ["HeadYaw","HeadPitch","LShoulderPitch","LShoulderRoll",
               "LElbowYaw","LElbowRoll","LWristYaw","RShoulderPitch",
               "RShoulderRoll","RElbowYaw","RElbowRoll"]
    angulos = [[0.0,0.04,0.0],[0.05,0.16,0.10],[1.55,1.28,1.40],
               [0.10,0.22,0.16],[-0.90,-1.10,-1.00],[-0.18,-0.42,-0.32],
               [-0.05,-0.15,-0.08],[1.02,0.78,0.88],[-0.22,-0.45,-0.38],
               [1.00,1.45,1.30],[0.95,1.42,1.28]]
    tempos  = [[0.8,1.9,3.0]] * len(juntas)
    mover(juntas, angulos, tempos)


def MOVIMENTO_016():
    juntas  = ["HeadYaw","HeadPitch","RShoulderPitch","RShoulderRoll",
               "RElbowYaw","RElbowRoll","RWristYaw","LShoulderPitch",
               "LShoulderRoll","LElbowRoll"]
    angulos = [[0.0,0.05,0.0],[-0.10,-0.05,-0.08],[0.80,0.55,0.65],
               [-0.10,-0.20,-0.14],[1.05,1.45,1.25],[0.35,0.55,0.45],
               [0.10,0.20,0.14],[1.45,1.38,1.42],[0.12,0.18,0.14],
               [-0.30,-0.42,-0.35]]
    tempos  = [[0.5,1.2,1.8]] * len(juntas)
    mover(juntas, angulos, tempos)


def MOVIMENTO_018():
    juntas  = ["HeadYaw","HeadPitch","RShoulderPitch","RShoulderRoll",
               "RElbowYaw","RElbowRoll","RWristYaw","LShoulderPitch",
               "LShoulderRoll","LElbowRoll"]
    angulos = [[0.0,0.0,0.0],[-0.08,-0.04,-0.06],[0.60,0.30,0.45],
               [-0.05,-0.15,-0.08],[1.10,1.52,1.30],[0.28,0.55,0.38],
               [-0.30,-0.55,-0.40],[1.48,1.35,1.42],[0.10,0.18,0.14],
               [-0.28,-0.45,-0.35]]
    tempos  = [[0.4,0.9,1.5]] * len(juntas)
    mover(juntas, angulos, tempos)


def MOVIMENTO_036():
    juntas  = ["HeadYaw","HeadPitch","LShoulderPitch","LShoulderRoll",
               "LElbowYaw","LElbowRoll","RShoulderPitch","RShoulderRoll",
               "RElbowRoll","HipPitch"]
    angulos = [[0.0,0.02,0.0],[0.05,0.20,0.14],[1.55,1.20,1.35],
               [0.08,0.18,0.12],[-0.85,-1.05,-0.95],[-0.15,-0.38,-0.28],
               [1.42,1.30,1.36],[-0.12,-0.18,-0.14],[0.60,0.80,0.68],
               [-0.08,-0.18,-0.12]]
    tempos  = [[1.0,2.2,3.5]] * len(juntas)
    mover(juntas, angulos, tempos)


def roteiro_napoleao():
    if TEM_MOTION:
        motion.setStiffnesses("Body", 1.0)
    if TEM_POSTURA:
        posture.goToPosture("StandInit", 0.6)
    if tts:
        tts.setParameter("speed", 85)
        tts.setParameter("pitchShift", 0.9)
        tts.setParameter("volume", 0.75)

    falar_e_mover("Eu sou Napoleao Bonaparte. De origens simples, ergui-me em meio ao caos da Franca revolucionaria.", MOVIMENTO_001)
    pausa()
    falar_e_mover("Nao nasci rei... tornei-me lider pela forca da estrategia e da vontade.", MOVIMENTO_016)
    pausa()
    falar_e_mover("Quando a Franca mergulhou na instabilidade, vi ali uma oportunidade. Organizei exercitos, venci batalhas e mostrei que disciplina supera o caos.", MOVIMENTO_018)
    pausa()
    falar_e_mover("Cada vitoria nao era apenas militar... era politica. Eu consolidava poder, restaurava ordem e construia um imperio.", MOVIMENTO_016)
    pausa()
    falar_e_mover("Mas nao foi apenas conquista. Foi visao. Eu acreditava que podia moldar o destino de uma nacao inteira.", MOVIMENTO_007)
    pausa()
    falar_e_mover("E por um tempo... eu consegui.", MOVIMENTO_018)
    pausa()
    falar_e_mover("O mundo pertence aqueles que agem. Sorte favorece os preparados, mas a coragem define os vencedores.", MOVIMENTO_016)
    pausa()
    falar_e_mover("Eu sempre acreditei no merito... nao no acaso.", MOVIMENTO_007)
    pausa()
    falar_e_mover("Poucos sabem, mas eu valorizava profundamente a educacao e o conhecimento estrategico.", MOVIMENTO_001)
    pausa()
    falar_e_mover("Livros, para mim, eram armas tao poderosas quanto canhoes.", MOVIMENTO_016)
    pausa()
    falar_e_mover("Meu nome ecoa na historia. Nao por acaso... mas por decisao.", MOVIMENTO_036)
    pausa()
    so_falar("Construa o seu destino.")

    if TEM_POSTURA:
        posture.goToPosture("StandInit", 0.5)
    if TEM_MOTION:
        motion.setStiffnesses("Body", 0.0)


# ═══════════════════════════════════════════════════════════════════════════
# MAPA DE COMANDOS DE VOZ
# ═══════════════════════════════════════════════════════════════════════════

COMANDOS_VOZ = {
    "mande um email":      enviar_email,
    "fale o hello world":  falar_hello_world,
    "vamos conversar":     conversar_ia,
    "ande para frente":    andar_frente,
    "ande para tras":      andar_tras,
    "abra o tablet":       abrir_tablet,
    "roteiro napoleao":    roteiro_napoleao,
}


# ═══════════════════════════════════════════════════════════════════════════
# SISTEMA DE GATILHOS POR VOZ
# ═══════════════════════════════════════════════════════════════════════════

def _reativar_gatilhos():
    sr.setVocabulary(list(COMANDOS_VOZ.keys()) + ["encerrar sistema"], False)
    sr.subscribe("gatilho_voz")


def sistema_gatilhos_voz():
    vocabulario = list(COMANDOS_VOZ.keys()) + ["encerrar sistema"]

    sr.setVocabulary(vocabulario, False)
    sr.subscribe("gatilho_voz")

    print("Sistema de voz ativado! Comandos disponiveis:")
    for cmd in COMANDOS_VOZ:
        print("  - " + cmd)
    print("  - encerrar sistema")
    print("\nOuvindo...\n")

    tts.say("Sistema ativado. Pode falar!")

    try:
        while True:
            resultado = mem.getData("WordRecognized")

            if resultado and resultado[1] > 0.4:
                comando = resultado[0]

                if comando in COMANDOS_VOZ:
                    print("Comando detectado: " + comando)
                    mem.insertData("WordRecognized", ["", 0.0])
                    COMANDOS_VOZ[comando]()

                elif comando == "encerrar sistema":
                    print("Encerrando sistema de voz")
                    tts.say("Encerrando. Ate logo!")
                    mem.insertData("WordRecognized", ["", 0.0])
                    break

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Interrompido pelo usuario")
    finally:
        try:
            sr.unsubscribe("gatilho_voz")
        except:
            pass


# ═══════════════════════════════════════════════════════════════════════════
# MENU TERMINAL
# ═══════════════════════════════════════════════════════════════════════════

def menu_terminal():
    opcoes = {
        "1": ("Enviar email",                enviar_email),
        "2": ("Falar hello world",           falar_hello_world),
        "3": ("Conversar com IA (terminal)", conversar_ia_terminal),
        "4": ("Andar frente",                andar_frente),
        "5": ("Andar tras",                  andar_tras),
        "6": ("Abrir tablet",                abrir_tablet),
        "7": ("Roteiro Napoleao",            roteiro_napoleao),
    }

    caps = []
    if TEM_MOTION:   caps.append("motion")
    if TEM_VOZ:      caps.append("voz")
    if tts:          caps.append("tts")
    if TEM_TABLET:   caps.append("tablet")
    status = "Conectada [{}]".format(", ".join(caps)) if PEPPER_CONECTADA else "NAO conectada"

    while True:
        print("\n" + "="*45)
        print("MENU PRINCIPAL  [{}]".format(status))
        print("="*45)
        for num, (label, _) in sorted(opcoes.items()):
            print("{}  - {}".format(num, label))
        print("0  - Sair")
        print("="*45)

        try:
            escolha = raw_input("Escolha: ")
        except NameError:
            escolha = input("Escolha: ")

        if escolha == "0":
            print("Encerrando")
            break
        elif escolha in opcoes:
            opcoes[escolha][1]()
        else:
            print("Opcao invalida")


# ═══════════════════════════════════════════════════════════════════════════
# PONTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════════════

if PEPPER_CONECTADA and TEM_VOZ:
    # Pepper fisica completa: oferece escolha entre menu e voz
    print("\nEscolha o modo de operacao:")
    print("  1 - Menu terminal (controle pelo teclado)")
    print("  2 - Sistema de voz (controle por fala)")
    try:
        modo = raw_input("Modo [1/2]: ").strip()
    except NameError:
        modo = input("Modo [1/2]: ").strip()

    if modo == "2":
        sistema_gatilhos_voz()
    else:
        menu_terminal()

elif PEPPER_CONECTADA:
    # Choregraphe: motion/tts disponiveis, mas sem voz nem tablet
    print("\nModo Choregraphe detectado - abrindo menu terminal")
    menu_terminal()

else:
    # Sem conexao nenhuma
    print("\nPepper nao conectada - movimentos serao ignorados")
    menu_terminal()
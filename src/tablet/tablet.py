# -*- coding: utf-8 -*-
import os
import sys
import webbrowser
from dotenv import load_dotenv

# Carrega o .env da raiz do projeto
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

ip   = os.getenv("IP")
porta = int(os.getenv("PORT"))

# Adiciona biblioteca do Choregraphe
caminho_lib = r"C:\Program Files (x86)\Softbank Robotics\Choregraphe Suite 2.5\lib"
if os.path.exists(caminho_lib):
    sys.path.append(caminho_lib)

# Tenta importar o naoqi
try:
    from naoqi import ALProxy
    NAOQI_DISPONIVEL = True
except ImportError:
    NAOQI_DISPONIVEL = False


def abrirNavegadorLocal(caminho_html):
    url = "file:///" + caminho_html.replace("\\", "/")
    webbrowser.open(url)


def main():
    caminho_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

    if not os.path.exists(caminho_html):
        print("index.html nao encontrado em: " + caminho_html)
        return

    if NAOQI_DISPONIVEL:
        try:
            tablet = ALProxy("ALTabletService", ip, porta)
            url    = "file:///" + caminho_html.replace("\\", "/")

            try:
                tablet.enableWifi()
            except:
                pass

            tablet.showWebview(url)
            print("Interface carregada no tablet do Pepper!")

        except Exception as e:
            print("Erro ao conectar no tablet: " + str(e))
            abrirNavegadorLocal(caminho_html)
    else:
        abrirNavegadorLocal(caminho_html)


if __name__ == "__main__":
    main()
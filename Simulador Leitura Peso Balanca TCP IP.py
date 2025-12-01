import time
import socket
from datetime import datetime, timedelta

HOST = "0.0.0.0"
PORT = 9000
TIMEOUT_OCIOSO = 600   
def gerar_valores():
    valor = 0

    while True:
        # 1. SUBIDA GRADATIVA
        while valor < 40000:
            if valor < 10000:
                incremento = 1200; intervalo = 0.05
            elif valor < 20000:
                incremento = 900; intervalo = 0.07
            elif valor < 30000:
                incremento = 700; intervalo = 0.10
            else:
                incremento = 300; intervalo = 0.20

            valor += incremento
            if valor > 40000:
                valor = 40000

            yield f")0  {valor:05d}    00\r"
            time.sleep(intervalo)

        # 2. Parado
        for _ in range(40):
            yield ")0  40000    00\r"; time.sleep(0.1)

        # 3. DESCIDA
        while valor > 0:
            if valor > 30000:
                decremento = 300; intervalo = 0.20
            elif valor > 20000:
                decremento = 700; intervalo = 0.10
            elif valor > 10000:
                decremento = 900; intervalo = 0.07
            else:
                decremento = 1200; intervalo = 0.05

            valor -= decremento
            if valor < 0:
                valor = 0

            yield f")0  {valor:05d}    00\r"
            time.sleep(intervalo)

        yield ")0  40001    00\r"; time.sleep(0.5)
        yield ")0  00000    00\r"; time.sleep(1)

        for _ in range(50):
            yield ")0  00000    00\r"; time.sleep(0.1)


def iniciar_servidor():
    print(f"Servidor TCP iniciado em {HOST}:{PORT}")
    print("Aguardando conexão... (CTRL+C para encerrar manualmente)")

    ultimo_evento = datetime.now()

    while True:
        # ⏳ Se ficar 10 min sem receber conexão → encerrar
        if datetime.now() - ultimo_evento > timedelta(seconds=TIMEOUT_OCIOSO):
            print("Nenhuma conexão por mais de 10 minutos. Encerrando servidor.")
            return

        try:
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.settimeout(5)  
            servidor.bind((HOST, PORT))
            servidor.listen(1)

            try:
                conn, addr = servidor.accept()
            except socket.timeout:
                continue  

            print(f"Cliente conectado: {addr}")
            ultimo_evento = datetime.now()

            with conn:
                for linha in gerar_valores():
                    try:
                        conn.sendall(linha.encode("utf-8"))
                    except:
                        print("Cliente desconectou. Aguardando nova conexão...")
                        break 

        except KeyboardInterrupt:
            print("\nServidor encerrado manualmente (CTRL+C).")
            return
        finally:
            servidor.close()


if __name__ == "__main__":
    iniciar_servidor()

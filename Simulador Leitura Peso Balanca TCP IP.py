import time
import socket

HOST = "0.0.0.0"
PORT = 9000

def gerar_valores():
    valor = 0

    while True:

        #
        # 1. SUBIDA GRADATIVA (caminhão entrando na balança)
        #
        while valor < 40000:

            # Quanto mais perto do topo, mais lento
            if valor < 10000:
                incremento = 1200
                intervalo = 0.05
            elif valor < 20000:
                incremento = 900
                intervalo = 0.07
            elif valor < 30000:
                incremento = 700
                intervalo = 0.10
            else:
                incremento = 300
                intervalo = 0.20 

            valor += incremento
            if valor > 40000:
                valor = 40000

            yield f")0  {valor:05d}    00\r"
            time.sleep(intervalo)

        #
        # 2. PARADO NA BALANÇA — estabilização
        #
        for _ in range(40):  # ~4 segundos parado
            yield ")0  40000    00\r"
            time.sleep(0.1)

        #
        # 3. DESCIDA GRADATIVA — caminhão saindo da balança
        #
        while valor > 0:
            if valor > 30000:
                decremento = 300
                intervalo = 0.20
            elif valor > 20000:
                decremento = 700
                intervalo = 0.10
            elif valor > 10000:
                decremento = 900
                intervalo = 0.07
            else:
                decremento = 1200
                intervalo = 0.05

            valor -= decremento
            if valor < 0:
                valor = 0

            yield f")0  {valor:05d}    00\r"
            time.sleep(intervalo)

        #
        # 4. ENVIA 40001 E ZERA
        #
        yield ")0  40001    00\r"
        time.sleep(0.5)

        yield ")0  00000    00\r"
        time.sleep(1)

        #
        # 5. FICA ENVIANDO ZERO POR ALGUNS SEGUNDOS
        #
        for _ in range(50):   # 50 × 0.1s = 5 segundos
            yield ")0  00000    00\r"
            time.sleep(0.1)

        # E reinicia o ciclo normalmente


def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST, PORT))
        servidor.listen(1)
        print(f"Servidor TCP iniciado em {HOST}:{PORT}")
        print("Aguardando conexão...")

        conn, addr = servidor.accept()
        print(f"Cliente conectado: {addr}")

        with conn:
            for linha in gerar_valores():
                try:
                    conn.sendall(linha.encode("utf-8"))
                except:
                    print("Cliente desconectou.")
                    break


if __name__ == "__main__":
    iniciar_servidor()

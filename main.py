# Importa o módulo asyncio para suporte a programação assíncrona.
import asyncio
import random

# Lista para armazenar os dados dos sensores
dados_sensores = []

async def gerenciar_sensor(reader, writer):
    # Lê os dados enviados pelo sensor em um loop infinito.
    while True:
        data = await reader.read(100)                                                   # Lê até 100 bytes de dados do sensor.
        if not data:
            break
        addr = writer.get_extra_info('peername')                                        # Obtem informação sobre o endereço do peer remoto conectado ao socket
        leitura = data.decode()                                                         # Decodifica os dados recebidos para uma string.
        print(f"Servidor Recebeu: {leitura} de {addr}")
        dados_sensores.append(leitura)                                                  # Armazena a leitura na lista de dados dos sensores.
        writer.close()                                                                  # Fecha a conexão com o sensor.

async def enviar_dados():
    # Envia as leituras simuladas para o servidor
    while True:
        leitura = random.uniform(0, 100)                                                # Gera uma leitura aleatória entre 0 e 100.
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)               # Conecta-se ao servidor.
        leitura_str = f"{leitura:.2f}"                                                  # Formata a leitura como uma string com 2 casas decimais.
        print(f"Sensor Enviou: {leitura_str}")
        writer.write(leitura_str.encode())                                              # Envia os dados ao servidor.
        await writer.drain()                                                            # Espera até que os dados sejam drenados (enviados).
        writer.close()                                                                  # Fecha a conexão com o servidor.
        await writer.wait_closed()                                                      # Aguarda até que a conexão seja totalmente fechada.
        await asyncio.sleep(1)                                                          # Intervalo de envio de dados


async def main():
    # Inicia o servidor central
    server = await asyncio.start_server(gerenciar_sensor, '127.0.0.1', 8888)

    # Inicia vários sensores (clientes) como tarefas assíncronas.
    for _ in range(5):
        asyncio.create_task(enviar_dados())

    # clientes = [enviar_dados() for _ in range(5)]
    # await asyncio.gather(server.serve_forever(), *clientes)

    # Roda o servidor indefinidamente
    async with server:
        await server.serve_forever()

# Executa a função principal
asyncio.run(main())

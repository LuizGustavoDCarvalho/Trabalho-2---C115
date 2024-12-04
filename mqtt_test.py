import paho.mqtt.client as mqtt
import ssl

# Informações do HiveMQ Cloud
BROKER_URL = "ff65ab71b8c44de48fd23233c6813726.s1.eu.hivemq.cloud"  # Substitua pela URL do seu broker
PORT = 8883  # Porta segura MQTT (com TLS)
USERNAME = "Projeto_C115"  # Substitua pelo seu username
PASSWORD = "@Lgdc2000"  # Substitua pela sua senha
TOPIC = "smartcattle/test"  # O tópico que você deseja publicar e se inscrever

# Função de callback para conexão
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao HiveMQ com sucesso!")
        client.subscribe(TOPIC)  # Inscreve-se no tópico
    else:
        print(f"Erro ao conectar. Código de retorno: {rc}")

# Função de callback para mensagens recebidas
def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico '{msg.topic}': {msg.payload.decode()}")

# Função de callback para desconexão
def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Desconectado com sucesso.")
    else:
        print(f"Desconexão com código: {rc}")

# Criando o cliente MQTT com a nova API (corrigindo o uso da versão mais recente)
client = mqtt.Client(client_id="SmartCattleClient", clean_session=True)  # Usando client_id e clean_session

# Registrando as funções de callback
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Configurando o username e password (autenticação)
client.username_pw_set(USERNAME, PASSWORD)

# Configuração do TLS/SSL (para uma conexão segura)
client.tls_set_context(ssl.create_default_context())

# Conectando ao broker MQTT
client.connect(BROKER_URL, PORT, 60)

# Função para publicar uma mensagem no tópico de teste
def publish_test_message():
    client.publish(TOPIC, "Teste de conexão com o HiveMQ!")

# Iniciando o loop do cliente
client.loop_start()

# Publicando uma mensagem de teste
publish_test_message()

import paho.mqtt.client as mqtt

# Definir o broker MQTT
broker = "ff65ab71b8c44de48fd23233c6813726.s1.eu.hivemq.cloud"  # Pode ser o seu broker HiveMQ Cloud
port = 8883  # Porta padrão para MQTT
topic = "smartcattle/sensor"

# Função para callback quando a conexão for estabelecida
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com sucesso: {rc}")
    client.subscribe(topic)

# Função para callback ao receber mensagem
def on_message(client, userdata, msg):
    print(f"Mensagem recebida: {msg.payload.decode()}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectar ao broker
client.connect(broker, port, 60)

# Publicando dados
data = "Temperatura: 25°C, umidade: 60%"
client.publish(topic, data)

# Manter a conexão
client.loop_start()

from blynklib import Blynk
import random
import time

# Token do Blynk (copie do app)
BLYNK_AUTH = "Seu_Auth_Token"

# Inicializando o Blynk
blynk = Blynk(BLYNK_AUTH)

# Enviando dados simulados para o app
@blynk.handle_event("read V1")  # Virtual Pin 1
def read_temperature():
    temp = round(random.uniform(35.0, 40.0), 2)
    blynk.virtual_write(1, temp)

@blynk.handle_event("read V2")  # Virtual Pin 2
def read_heart_rate():
    heart_rate = random.randint(60, 100)
    blynk.virtual_write(2, heart_rate)

while True:
    blynk.run()
    time.sleep(1)

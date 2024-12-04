#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

#define BLYNK_TEMPLATE_ID "TMPL2uDwwofJw"
#define BLYNK_TEMPLATE_NAME "TESTE"

#include <BlynkSimpleEsp32.h>

#define BLYNK_AUTH_TOKEN "cvzfXLrMwv5FoEwYEJ1sEN54zYZedX4O"

char auth[] = BLYNK_AUTH_TOKEN;
const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "c3edf03c24074f1382d7cb030d8af88e.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_user = "projetoC215";
const char* mqtt_password = "projetoC215";

// Pinos dos sensores
const int pinPh = 34;
const int pinUmidade = 35;
const int pinTemperatura = 32;

// Tópicos MQTT
const char* topic_ph = "sensores/ph";
const char* topic_umidade = "sensores/umidade";
const char* topic_temperatura = "sensores/temperatura";

// Intervalo de publicação MQTT
unsigned long lastMsg = 0;
const long intervalo = 2000;

WiFiClientSecure espClient;
PubSubClient client(espClient);

void setup_wifi() {
    Serial.println("Conectando ao WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi conectado!");
}

void reconnect() {
    while (!client.connected()) {
        Serial.println("Conectando ao broker MQTT...");
        if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
            Serial.println("Conectado ao MQTT!");
        } else {
            Serial.print("Falha na conexão. Código de estado: ");
            Serial.println(client.state());
            delay(2000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    espClient.setInsecure();
    setup_wifi();
    client.setServer(mqtt_server, mqtt_port);
    Blynk.begin(auth, ssid, password);
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    Blynk.run();

    unsigned long now = millis();
    if (now - lastMsg > intervalo) {
        lastMsg = now;

        // Leitura simulada dos sensores
        float valorPh = analogRead(pinPh) * (14.0 / 4095.0);         // Simula leitura de pH
        float valorUmidade = analogRead(pinUmidade) * (100.0 / 4095.0); // Simula leitura de umidade
        float valorTemperatura = analogRead(pinTemperatura) * (50.0 / 4095.0); // Simula leitura de temperatura

        // Publica os valores no MQTT
        client.publish(topic_ph, String(valorPh).c_str());
        client.publish(topic_umidade, String(valorUmidade).c_str());
        client.publish(topic_temperatura, String(valorTemperatura).c_str());

        // Envia os valores para o Blynk
        Blynk.virtualWrite(V1, valorPh);
        Blynk.virtualWrite(V2, valorUmidade);
        Blynk.virtualWrite(V3, valorTemperatura);

        // Exibe os valores no Serial
        Serial.printf("pH: %.2f, Umidade: %.2f%%, Temperatura: %.2f°C\n", valorPh, valorUmidade, valorTemperatura);
    }
}

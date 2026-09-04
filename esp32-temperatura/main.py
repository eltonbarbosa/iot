import network
import time
import ujson
import dht
from machine import Pin
from simple import MQTTClient

# --- Configuração ---
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# Cole o seu Token de Acesso do ThingsBoard aqui
ACCESS_TOKEN = "SEU_TOKEN_DE_ACESSO_DO_THINGSBOARD"
THINGSBOARD_SERVER = "thingsboard.cloud"
MQTT_PORT = 1883  # porta padrão MQTT sem TLS

TOPIC = b"v1/devices/me/telemetry"  # tópico padrão de telemetria do ThingsBoard

# --- Inicialização do Sensor Físico ---
sensor = dht.DHT22(Pin(14))

# --- Conectar ao WiFi ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando ao WiFi...", end="")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(0.5)
    print("\nConectado! Configuração de rede:", wlan.ifconfig())

# --- Conectar ao broker MQTT do ThingsBoard ---
def connect_mqtt():
    client = MQTTClient(
        client_id="wokwi_esp32",
        server=THINGSBOARD_SERVER,
        port=MQTT_PORT,
        user=ACCESS_TOKEN,   # o token substitui usuário/senha tradicionais
        password=""
    )
    client.connect()
    print("Conectado ao broker MQTT do ThingsBoard!")
    return client

# --- Programa Principal ---
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        payload = ujson.dumps({
            "temperature": temperature,
            "humidity": humidity
        })

        print(f"Publicando telemetria via MQTT: {payload}")
        mqtt_client.publish(TOPIC, payload)

    except OSError:
        print("Falha ao ler o sensor DHT22! Verifique as conexões.")
    except Exception as e:
        print(f"Erro MQTT: {e}")
        try:
            mqtt_client = connect_mqtt()
        except Exception:
            connect_wifi()
            mqtt_client = connect_mqtt()

    time.sleep(5)
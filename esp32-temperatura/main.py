import network
import time
import urequests
import dht
from machine import Pin

# --- Configuração ---
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# Cole o seu Token de Acesso do ThingsBoard aqui
ACCESS_TOKEN = "SEU_TOKEN_DE_ACESSO_AQUI" 
THINGSBOARD_SERVER = "thingsboard.cloud"

URL = f"http://{THINGSBOARD_SERVER}/api/v1/{ACCESS_TOKEN}/telemetry"

# --- Inicialização do Sensor Físico ---
# O pino D14 foi o configurado no arquivo diagram.json
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

# --- Programa Principal ---
connect_wifi()

while True:
    try:
        # Lendo os dados do sensor DHT22
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        
        # Cria o payload estruturado para o ThingsBoard
        payload = {
            "temperature": temperature,
            "humidity": humidity
        }
        
        print(f"Enviando telemetria real: {payload}")
        
        # Envia a requisição HTTP POST
        response = urequests.post(URL, json=payload)
        print(f"Status do Servidor: {response.status_code}")
        response.close()
        
    except OSError as e:
        print("Falha ao ler o sensor DHT22! Verifique as conexões.")
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")
        connect_wifi()

    # O sensor DHT22 precisa de pelo menos 2 segundos entre as leituras
    time.sleep(5)

import network
import time
import ujson
import dht
from machine import Pin, ADC
from simple import MQTTClient
from secrets import ACCESS_TOKEN, MQTT_CLIENT_ID

# --- Configuração ---
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

THINGSBOARD_SERVER = "thingsboard.cloud"
MQTT_PORT = 1883  # porta padrão MQTT sem TLS

TOPIC = b"v1/devices/me/telemetry"  # tópico padrão de telemetria do ThingsBoard

# --- Regras locais (Edge) ---
# Mesma referência didática da planilha: 4,5 mm/s = alerta, 7,1 mm/s = crítico
VIBRACAO_ALERTA = 4.5
VIBRACAO_PARADA = 7.1
ROTACAO_NOMINAL = 1750
INTERVALO_ENVIO = 5  # segundos

# --- Inicialização dos Sensores e Atuadores ---
sensor = dht.DHT22(Pin(14))           # temperatura da carcaça do motor

pot_vibracao = ADC(Pin(34))           # potenciômetro simula o sensor de vibração
pot_vibracao.atten(ADC.ATTN_11DB)     # faixa completa de 0 a 3,3 V
pot_corrente = ADC(Pin(35))           # potenciômetro simula o sensor de corrente
pot_corrente.atten(ADC.ATTN_11DB)

led_alerta = Pin(2, Pin.OUT)          # LED amarelo: vibração em alerta
led_parada = Pin(15, Pin.OUT)         # LED vermelho: motor parado pela regra local
botao_rearme = Pin(4, Pin.IN, Pin.PULL_UP)  # técnico libera o motor após inspeção

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
        client_id=MQTT_CLIENT_ID,
        server=THINGSBOARD_SERVER,
        port=MQTT_PORT,
        user=ACCESS_TOKEN,   # o token substitui usuário/senha tradicionais
        password=""
    )
    client.connect()
    print("Conectado ao broker MQTT do ThingsBoard!")
    return client

# --- Leitura dos potenciômetros convertida para grandezas do motor ---
def ler_vibracao():
    return round(pot_vibracao.read() / 4095 * 12, 2)   # 0 a 12 mm/s

def ler_corrente():
    return round(pot_corrente.read() / 4095 * 20, 2)   # 0 a 20 A

# --- Programa Principal ---
connect_wifi()
mqtt_client = connect_mqtt()

parado = False
ultimo_envio = 0
ultimo_status = None

while True:
    vibracao = ler_vibracao()

    # Regra local: decide em menos de 1 segundo, mesmo sem internet
    if vibracao > VIBRACAO_PARADA:
        parado = True
    if parado and botao_rearme.value() == 0:
        print("Rearme manual: motor liberado pelo técnico.")
        parado = False

    if parado:
        status = "parado"
    elif vibracao > VIBRACAO_ALERTA:
        status = "alerta"
    else:
        status = "normal"

    led_parada.value(1 if parado else 0)
    led_alerta.value(1 if status == "alerta" else 0)

    agora = time.time()
    if agora - ultimo_envio >= INTERVALO_ENVIO or status != ultimo_status:
        try:
            sensor.measure()
            temperatura = sensor.temperature()
        except OSError:
            print("Falha ao ler o sensor DHT22! Verifique as conexões.")
            temperatura = None

        payload = ujson.dumps({
            "temperatura_c": temperatura,
            "vibracao_mm_s": 0.1 if parado else vibracao,
            # mesma leitura com o nome que o alarme pronto "Motor Vibration Alarm" (IoT Hub) espera
            "vibration": 0.1 if parado else vibracao,
            "corrente_a": 0.0 if parado else ler_corrente(),
            "rotacao_rpm": 0 if parado else ROTACAO_NOMINAL,
            "status": status,
            "parada_local": parado
        })

        try:
            print(f"Publicando telemetria via MQTT: {payload}")
            mqtt_client.publish(TOPIC, payload)
        except Exception as e:
            # Sem internet a regra local continua funcionando; só o envio falha
            print(f"Erro MQTT: {e}")
            try:
                mqtt_client = connect_mqtt()
            except Exception:
                connect_wifi()
                mqtt_client = connect_mqtt()
        ultimo_envio = agora
        ultimo_status = status

    time.sleep(0.2)

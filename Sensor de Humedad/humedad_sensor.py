import machine
import network
import time
import json
import dht  # Importar librería DHT
from ssd1306 import SSD1306_I2C
from umqtt.simple import MQTTClient

# --- CONFIGURACIÓN WIFI ---
ssid = "Wiches"
password = "Luis24050"

# --- CONFIGURACIÓN FLESPI MQTT ---
mqtt_server = "mqtt.flespi.io"
mqtt_port = 1883
# **TU TOKEN** (El que usaste en el script de CO)
mqtt_username = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
mqtt_password = "" 

# --- 🚨 CONFIGURACIÓN DEL DISPOSITIVO ---
client_id = "HUM_Sensor_01" # ID Único para este sensor
mqtt_topic = b"iotzi/escuela/sensor/hum" # Tópico de Humedad

# --- Configuración del Sensor Físico ---
DHT_PIN = 15 # Pin GP15 para el sensor DHT

# --- Configuración de la Pantalla ---
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5))

# --- Variables Globales ---
reading_count = 0
last_publish = 0
publish_interval_ms = 5000 

# --- Objetos Globales ---
wlan = network.WLAN(network.STA_IF)
display = None 
client = MQTTClient(client_id, mqtt_server, port=mqtt_port, user=mqtt_username, password=mqtt_password, keepalive=60)

# Inicializar sensor DHT
try:
    sensor = dht.DHT11(machine.Pin(DHT_PIN))
    print(f"Sensor DHT11 inicializado en GP{DHT_PIN}.")
except Exception as e:
    print(f"Error inicializando DHT: {e}")
    sensor = None 

# --- Funciones (Conexión y Display) ---

def setup_display():
    global display
    try:
        display = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)
        update_display("Display OK", "Iniciando...", "", "", "")
        print("Pantalla SSD1306 inicializada.")
    except OSError as e:
        print(f"Error: No se encontró la pantalla I2C en {i2c.scan()}")
        print("El programa continuará sin pantalla.")

def update_display(line1, line2, line3, line4, line5, line6=""):
    if display:
        display.fill(0) 
        display.text(line1, 0, 0, 1)
        display.text(line2, 0, 10, 1)
        display.text(line3, 0, 20, 1)
        display.text(line4, 0, 30, 1)
        display.text(line5, 0, 44, 1) 
        display.text(line6, 0, 54, 1) 
        display.show()

def setup_wifi():
    print("Conectando a WiFi...")
    update_display("WiFi", "Conectando...", ssid, "", "")
    wlan.active(True)
    wlan.connect(ssid, password)
    max_wait = 15
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3: break
        max_wait -= 1; print("."); time.sleep(1)
    if wlan.status() != 3:
        print("¡Fallo en la conexión WiFi!"); update_display("WiFi", "¡ERROR!", "", "", "Reiniciando..."); time.sleep(5); machine.reset()
    else:
        print(f"✓ Conectado al WiFi. IP: {wlan.ifconfig()[0]}"); update_display("WiFi", "✓ Conectado", wlan.ifconfig()[0], "", "")

def connect_mqtt():
    print("Conectando a MQTT..."); update_display("MQTT", "Conectando...", "", "", "WiFi: OK", "")
    try:
        client.connect()
        print(f"✓ Conectado a MQTT: {mqtt_server}"); update_display("MQTT", "✓ Conectado", "", "", "WiFi: OK", "MQTT: OK"); time.sleep(1) 
    except OSError as e:
        print(f"✗ Error al conectar a MQTT: {e}"); update_display("MQTT", "¡ERROR!", "Revisa Token", "", "WiFi: OK", "MQTT: ERROR"); time.sleep(3); print("Reintentando...")

# --- PROGRAMA PRINCIPAL (SOLO HUMEDAD) ---

setup_display()
setup_wifi()
connect_mqtt()
wdt = machine.WDT(timeout=8000) 

print("\n========================================")
print("💧 Sensor DHT - SOLO HUMEDAD")
print(f"ID: {client_id}")
print(f"Tópico: {mqtt_topic.decode()}")
print("========================================")

while True:
    try:
        wdt.feed() 
        client.check_msg() 
        
        current_time_ms = time.ticks_ms()
        if time.ticks_diff(current_time_ms, last_publish) >= publish_interval_ms:
            last_publish = current_time_ms
            reading_count += 1
            
            hum = 0.0
            
            # 1. LECTURA DEL SENSOR
            try:
                sensor.measure()
                hum = sensor.humidity()
                # No leemos sensor.temperature()
                
            except OSError as e:
                print(f"✗ Error al leer el sensor DHT: {e}")
                update_display(f"ID: {client_id}", "¡ERROR SENSOR!", str(e), "", "WiFi: OK", "MQTT: OK")
                continue 
            
            print(f"✓ LECTURA #{reading_count} | Hum: {hum}%")

            # 2. CREACIÓN DEL JSON (HUMEDAD)
            # Formato {"hum": ...} para tu app.js
            payload_hum = {"val": hum}
            json_hum = json.dumps(payload_hum)
            
            # 3. PUBLICAR
            print(f"  📊 JSON Hum: {json_hum}")
            client.publish(mqtt_topic, json_hum)
            
            # 4. ACTUALIZAR PANTALLA
            update_display(
                f"ID: {client_id}",
                f"Hum:  {hum:.1f} %",
                "", # Línea 3 vacía
                f"Msj #{reading_count} enviado",
                "WiFi: OK",
                "MQTT: OK"
            )

    except OSError as e:
        print(f"Error de red o MQTT: {e}. Reconectando..."); update_display("¡Error!", str(e), "Reconectando...", "", "WiFi: OK", "MQTT: ERROR"); setup_wifi(); connect_mqtt()
    except KeyboardInterrupt:
        print("Programa detenido manualmente."); update_display("Detenido", "Por el usuario", "", "", "", ""); break
        
    time.sleep_ms(100)


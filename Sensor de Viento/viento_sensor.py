import machine
import network
import time
import urandom
import json
from ssd1306 import SSD1306_I2C
from umqtt.simple import MQTTClient

# --- CONFIGURACIÓN WIFI ---
ssid = "Wiches"
password = "Luis24050"

# --- CONFIGURACIÓN FLESPI MQTT ---
mqtt_server = "mqtt.flespi.io"
mqtt_port = 1883
# **TU TOKEN**
mqtt_username = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
mqtt_password = "" 

# --- 🚨 CONFIGURACIÓN DEL DISPOSITIVO ---
# ⚠️ Cambia esta línea para cada uno de tus sensores:
client_id = "Viento_sensor" 

# Tópico para el sensor de viento
mqtt_topic = b"iotzi/escuela/sensor/vien" # 'b' lo convierte a bytes

# --- Configuración de la Pantalla ---
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5))

# --- Variables Globales ---
reading_count = 0
last_publish = 0
publish_interval_ms = 5000 # Publicar cada 5 segundos

# --- Objetos Globales ---
wlan = network.WLAN(network.STA_IF)
display = None # Se inicializará en setup_display
client = MQTTClient(client_id, mqtt_server, port=mqtt_port, user=mqtt_username, password=mqtt_password, keepalive=60)

# --- Funciones ---

def setup_display():
    """Intenta inicializar la pantalla SSD1306."""
    global display
    try:
        display = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)
        update_display("Display OK", "Iniciando...", "", "", "")
        print("Pantalla SSD1306 inicializada.")
    except OSError as e:
        print(f"Error: No se encontró la pantalla I2C en {i2c.scan()}")
        print("El programa continuará sin pantalla.")

def update_display(line1, line2, line3, line4, line5, line6=""):
    """Actualiza la pantalla OLED con 6 líneas de texto."""
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
    """Conecta el Pico W a la red WiFi."""
    print("Conectando a WiFi...")
    update_display("WiFi", "Conectando...", ssid, "", "")
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 15
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print(".")
        update_display("WiFi", "Conectando" + "." * (15 - max_wait), ssid, "", "")
        time.sleep(1)

    if wlan.status() != 3:
        print("¡Fallo en la conexión WiFi!")
        update_display("WiFi", "¡ERROR!", "Revisa SSID/Pass", "", "Reiniciando...", "")
        time.sleep(5)
        machine.reset()
    else:
        print(f"✓ Conectado al WiFi. IP: {wlan.ifconfig()[0]}")
        update_display("WiFi", "✓ Conectado", wlan.ifconfig()[0], "", "")

def connect_mqtt():
    """Conecta (o reconecta) al broker MQTT."""
    print("Conectando a MQTT...")
    update_display("MQTT", "Conectando...", mqtt_server, "", "WiFi: OK", "")
    try:
        client.connect()
        print(f"✓ Conectado a MQTT: {mqtt_server}")
        update_display("MQTT", "✓ Conectado", mqtt_server, "", "WiFi: OK", "MQTT: OK")
        time.sleep(1)
    except OSError as e:
        print(f"✗ Error al conectar a MQTT: {e}")
        update_display("MQTT", "¡ERROR!", str(e), "", "WiFi: OK", "MQTT: ERROR")
        time.sleep(3)
        print("Reintentando...")

def get_wind_direction_cardinal(degrees):
    """Convierte grados en una dirección cardinal (N, NE, E, etc.)."""
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    # Calcula el índice para el array de direcciones
    # Suma 22.5 para centrar la "caja" de cada dirección (cada caja es de 45 grados)
    index = int(((degrees + 22.5) % 360) / 45)
    return dirs[index]

# --- PROGRAMA PRINCIPAL ---

# 1. Inicializar periféricos
setup_display()
setup_wifi()
connect_mqtt()

wdt = machine.WDT(timeout=8000)

print("\n========================================")
print("🍃 SIMULADOR: Sensor de Viento (Pico W)")
print(f"ID del Sensor: {client_id}")
print(f"Tópico: {mqtt_topic.decode()}")
print("========================================")

# 2. Bucle principal
while True:
    try:
        wdt.feed() 
        client.check_msg() 
        
        current_time_ms = time.ticks_ms()
        if time.ticks_diff(current_time_ms, last_publish) >= publish_interval_ms:
            last_publish = current_time_ms
            reading_count += 1
            
            # 1. SIMULACIÓN DE LECTURA
            speed_kmh = 0.0
            is_gust_anomaly = (reading_count % 15 == 0) # Ráfaga 1 de cada 15
            
            if is_gust_anomaly:
                # Simula una ráfaga de viento fuerte: 60 a 80 km/h
                speed_kmh = urandom.uniform(60.0, 80.0)
                print("🌬️  ALERTA: Ráfaga de viento fuerte detectada!")
            else:
                # Simula una brisa normal: 5 a 35 km/h
                speed_kmh = urandom.uniform(5.0, 35.0)
            
            # Simula la dirección del viento
            direction_deg = urandom.uniform(0.0, 360.0)
            direction_cardinal = get_wind_direction_cardinal(direction_deg)
            
            # 2. CREACIÓN DEL JSON
            payload = {
                "wind_speed_kmh": round(speed_kmh, 1),
                "wind_direction_deg": round(direction_deg, 1),
                "wind_direction_cardinal": direction_cardinal
            }
            json_payload = json.dumps(payload)
            
            # 3. PUBLICAR
            print(f"✓ LECTURA #{reading_count} | {speed_kmh:.1f} km/h, {direction_cardinal} ({direction_deg:.1f}°)")
            print(f"  📊 JSON Enviado: {json_payload}")
            
            client.publish(mqtt_topic, json_payload)
            
            # 4. ACTUALIZAR PANTALLA
            update_display(
                f"ID: {client_id}",
                f"Vel: {speed_kmh:.1f} km/h",
                f"Dir: {direction_cardinal} ({direction_deg:.0f}d)",
                f"Msj #{reading_count} enviado",
                "WiFi: OK",
                "MQTT: OK"
            )

    except OSError as e:
        print(f"Error de red o MQTT: {e}. Reconectando...")
        update_display("¡Error!", str(e), "Reconectando...", "", "WiFi: OK", "MQTT: ERROR")
        setup_wifi()
        connect_mqtt()
        
    except KeyboardInterrupt:
        print("Programa detenido manualmente.")
        update_display("Detenido", "Por el usuario", "", "", "", "")
        break
        

    time.sleep_ms(100)

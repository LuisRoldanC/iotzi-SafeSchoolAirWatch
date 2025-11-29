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
mqtt_password = "" # El token de Flespi se usa como Username, la contraseña va vacía

# --- 🚨 CONFIGURACIÓN DEL DISPOSITIVO ---
# ⚠️ Cambia esta línea para cada uno de tus 3 sensores:
# "CO_Sensor_01", "CO_Sensor_02", "CO_Sensor_03"
client_id = "CO_Sensor" 

# Tópico general para los sensores de CO
mqtt_topic = b"iotzi/escuela/sensor/co" # 'b' lo convierte a bytes

# --- Configuración del Sensor CO ---
CO_NORMAL_MAX = 9.0
CO_ELEVATED = 50.0
CO_DANGEROUS = 100.0

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
        display.fill(0) # Limpia la pantalla
        display.text(line1, 0, 0, 1)
        display.text(line2, 0, 10, 1)
        display.text(line3, 0, 20, 1)
        display.text(line4, 0, 30, 1)
        display.text(line5, 0, 44, 1) # Líneas de estado
        display.text(line6, 0, 54, 1) # Líneas de estado
        display.show()

def setup_wifi():
    """Conecta el Pico W a la red WiFi."""
    print("Conectando a WiFi...")
    update_display("WiFi", "Conectando...", ssid, "", "")
    wlan.active(True)
    wlan.connect(ssid, password)

    # Espera por la conexión
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
        time.sleep(1) # Pausa para ver el mensaje
    except OSError as e:
        print(f"✗ Error al conectar a MQTT: {e}")
        update_display("MQTT", "¡ERROR!", str(e), "", "WiFi: OK", "MQTT: ERROR")
        time.sleep(3)
        print("Reintentando...")

def classifyCO(co):
    """Clasifica el nivel de CO (portado de C++)."""
    if co <= CO_NORMAL_MAX: return "NORMAL"
    if co < CO_ELEVATED: return "ELEVATED"
    if co < CO_DANGEROUS: return "DANGEROUS"
    return "HIGHLY_DANGEROUS"

# --- PROGRAMA PRINCIPAL ---

# 1. Inicializar periféricos
setup_display()
setup_wifi()
connect_mqtt()

# Activa el Watchdog Timer (re-inicia el Pico si se cuelga por más de 8s)
wdt = machine.WDT(timeout=8000)

print("\n========================================")
print("🏭 SIMULADOR: Sensor de CO (Pico W)")
print(f"ID del Sensor: {client_id}")
print(f"Tópico: {mqtt_topic.decode()}") # .decode() para imprimirlo bonito
print("========================================")

# 2. Bucle principal
while True:
    try:
        wdt.feed() # Alimenta al perro guardián
        
        # Revisa mensajes MQTT (aunque no nos suscribimos, es buena práctica)
        client.check_msg() 
        
        # Lógica de publicación temporizada (no bloqueante)
        current_time_ms = time.ticks_ms()
        if time.ticks_diff(current_time_ms, last_publish) >= publish_interval_ms:
            last_publish = current_time_ms
            reading_count += 1
            
            # 1. SIMULACIÓN DE LECTURA (portado de C++)
            co_value = 0.0
            is_leak_anomaly = (reading_count % 10 == 0) # Fuga 1 de cada 10
            
            if is_leak_anomaly:
                co_value = urandom.uniform(55.0, 150.0)
                print("🔥 ALERTA: Fuga de CO detectada!")
            else:
                co_value = urandom.uniform(1.0, 9.0)
            
            co_status = classifyCO(co_value)
            
            # 2. CREACIÓN DEL JSON (estilo Python)
            payload = {
                "co_ppm": round(co_value, 1),
                "co_status": co_status
            }
            json_payload = json.dumps(payload)
            
            # 3. PUBLICAR
            print(f"✓ LECTURA #{reading_count} | CO: {co_value:.1f} ppm | {co_status}")
            print(f"  📊 JSON Enviado: {json_payload}")
            
            client.publish(mqtt_topic, json_payload)
            
            # 4. ACTUALIZAR PANTALLA
            update_display(
                f"ID: {client_id}",
                f"CO: {co_value:.1f} ppm",
                f"St: {co_status}",
                f"Msj #{reading_count} enviado",
                "WiFi: OK",
                "MQTT: OK"
            )

    except OSError as e:
        print(f"Error de red o MQTT: {e}. Reconectando...")
        update_display("¡Error!", str(e), "Reconectando...", "", "WiFi: OK", "MQTT: ERROR")
        setup_wifi() # Asegura WiFi primero
        connect_mqtt() # Luego intenta reconectar MQTT
        
    except KeyboardInterrupt:
        print("Programa detenido manualmente.")
        update_display("Detenido", "Por el usuario", "", "", "", "")
        break
        

    time.sleep_ms(100) # Pequeña pausa para no saturar el CPU

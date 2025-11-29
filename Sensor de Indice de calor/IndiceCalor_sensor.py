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
client_id = "IndiceCalor_sensor" 

# Tópico para el sensor de índice de calor
mqtt_topic = b"iotzi/escuela/sensor/IndiceC" # 'b' lo convierte a bytes

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

def calculate_heat_index(T_f, RH_percent):
    """
    Calcula el Índice de Calor (Heat Index) usando la fórmula de regresión 
    de la NWS (National Weather Service) de EE. UU.
    
    :param T_f: Temperatura en Fahrenheit
    :param RH_percent: Humedad Relativa en % (ej. 60.5)
    :return: Índice de Calor en Fahrenheit
    """
    
    # La fórmula solo es válida para T > 80°F y RH > 40%
    if T_f <= 80.0 or RH_percent <= 40.0:
        return T_f # Si no se cumplen las condiciones, el índice es solo la temperatura

    T = T_f
    RH = RH_percent
    
    # Fórmula de regresión de Steadman (usada por NWS)
    HI_f = (-42.379 + 
            2.04901523 * T + 
            10.14333127 * RH - 
            0.22475541 * T * RH - 
            0.00683783 * T * T - 
            0.05481717 * RH * RH + 
            0.00122874 * T * T * RH + 
            0.00085282 * T * RH * RH - 
            0.00000199 * T * T * RH * RH)
    
    return HI_f

# --- PROGRAMA PRINCIPAL ---

# 1. Inicializar periféricos
setup_display()
setup_wifi()
connect_mqtt()

wdt = machine.WDT(timeout=8000)

print("\n========================================")
print("🌡️  SIMULADOR: Indice de Calor (Pico W)")
print(f"ID del Sensor: {client_id}")
print(f"Topico: {mqtt_topic.decode()}")
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
            
            # 1. SIMULACIÓN DE LECTURA (Temp y Humedad)
            # Simulamos un día caluroso y húmedo para que el cálculo sea relevante
            temp_c = urandom.uniform(28.0, 42.0)
            humi_rh = urandom.uniform(45.0, 90.0)
            
            # 2. CÁLCULO
            # La fórmula necesita la temperatura en Fahrenheit
            temp_f = (temp_c * 1.8) + 32
            
            # Calcular el índice de calor en Fahrenheit
            hi_f = calculate_heat_index(temp_f, humi_rh)
            
            # Convertir el resultado de vuelta a Celsius
            hi_c = (hi_f - 32) / 1.8
            
            # 3. CREACIÓN DEL JSON
            payload = {
                "temperature_c": round(temp_c, 1),
                "humidity_rh": round(humi_rh, 1),
                "heat_index_c": round(hi_c, 1) # El valor calculado
            }
            json_payload = json.dumps(payload)
            
            # 4. PUBLICAR
            print(f"✓ LECTURA #{reading_count} | T: {temp_c:.1f}C, H: {humi_rh:.1f}% -> HI: {hi_c:.1f}C")
            print(f"  📊 JSON Enviado: {json_payload}")
            
            client.publish(mqtt_topic, json_payload)
            
            # 5. ACTUALIZAR PANTALLA
            update_display(
                f"ID: {client_id}",
                f"T: {temp_c:.1f}C H: {humi_rh:.1f}%",
                f"SENSACION: {hi_c:.1f} C",
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

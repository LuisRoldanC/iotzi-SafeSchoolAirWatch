# 🌡️ Sensor de Temperatura (DHT11 – Pico W)

Este módulo del sistema **IoTzi SafeSchool AirWatch** permite medir y transmitir en tiempo real la **temperatura ambiental** usando un sensor **DHT11** conectado a un **Raspberry Pi Pico W**.

El dispositivo envía lecturas al broker MQTT de Flespi y muestra los valores en una pantalla OLED I2C.  
Está diseñado para entornos escolares, laboratorios y monitoreo ambiental.

## 1. Librerías Utilizadas

El programa utiliza:

- **dht** – Lectura del sensor DHT11  
- **machine** – Control de pines, I2C, WDT  
- **network** – Conexión WiFi  
- **umqtt.simple** – Cliente MQTT para MicroPython  
- **ssd1306** – Pantalla OLED  
- **json** – Construcción y envío del payload  
- **time** – Timers y control del intervalo de lectura  


## 2. Hardware Requerido

| Componente | Función |
|-----------|---------|
| Raspberry Pi Pico W | WiFi + procesamiento |
| Sensor DHT11 | Medición de temperatura |
| OLED SSD1306 (I2C) | Pantalla de información |
| GP15 | Pin de datos del DHT11 |
| GP4 (SDA) | I2C |
| GP5 (SCL) | I2C |

## 3. Configuración del Sensor

- El DHT11 se conecta al pin **GP15**  
- Solo se utiliza la lectura de **temperatura**  
- La medición de **humedad NO se incluye** en este módulo (solo temperatura)

En caso de falla del sensor, el sistema continúa funcionando y muestra el error en pantalla.

## 4. Conectividad WiFi

El módulo:

- Se conecta automáticamente al SSID configurado  
- Muestra estado de conexión en la pantalla  
- Si falla la conexión, **reinicia el Pico W automáticamente**  
- Muestra la IP obtenida al conectarse con éxito  

## 5. Conexión al Broker MQTT (Flespi)

El programa se conecta a:
`mqtt.flespi.io`


Usando:

- **Client ID único:** `TEMP_Sensor_01`
- **Token Flespi como username**
- **Keepalive de 60 segundos**

### 🟦 Tópico del sensor

`iotzi/escuela/sensor/temp`

Cada lectura se publica en este tópico.

## 6. Lógica de Lectura

El dispositivo envía una lectura de temperatura cada:
`5 segundos (5000 ms)`

Proceso:

1. El DHT11 toma una medición
2. Solo se extrae el valor de temperatura (°C)
3. Se construye un JSON simple para compatibilidad con tu app:

   ```json
   {"val": 25.0}


## 6. Ejecucion

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Sensor%20Temperatura.png)

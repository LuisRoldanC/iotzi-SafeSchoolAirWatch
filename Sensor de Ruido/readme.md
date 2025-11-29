# 🔊 Simulador de Sensor de Ruido (Pico W)

Este módulo forma parte del sistema **IoTzi SafeSchool AirWatch**, encargado de monitorear parámetros ambientales dentro de entornos escolares.  
El **Sensor de Ruido** implementado en un **Raspberry Pi Pico W** simula niveles de sonido en decibeles (dB), incluyendo eventos anómalos como picos de ruido fuertes.

El simulador es ideal para pruebas de:
- Dashboards IoT (Grafana, Flespi, Node-RED, ThingsBoard)
- Integración MQTT
- Monitoreo en tiempo real
- Sistema de alertas

## 1. Librerías Utilizadas

El módulo usa las siguientes librerías en MicroPython:

- **network** – Conexión WiFi.
- **umqtt.simple.MQTTClient** – Envío MQTT al broker Flespi.
- **machine** – Control del hardware (WDT, pines, I2C).
- **ssd1306** – Manejo de la pantalla OLED 128x64.
- **urandom** – Generación aleatoria del nivel de ruido.
- **json** – Construcción del payload publicado.

## 2. Configuración del Hardware

Aunque el ruido se simula, el programa usa:

| Componente | Uso |
|-----------|-----|
| **Raspberry Pi Pico W** | Procesamiento y WiFi |
| **Pantalla OLED SSD1306 (I2C)** | Muestra lecturas y estado del sensor |
| **I2C SDA (GPIO 4)** | Comunicación con OLED |
| **I2C SCL (GPIO 5)** | Comunicación con OLED |

No se requiere sensor físico, ya que los valores son generados internamente.

## 3. Pantalla OLED (128x64)

El sistema muestra en tiempo real:

- ID del sensor  
- Nivel de ruido (dB)  
- Clasificación del ruido  
- Número de mensaje enviado  
- Estado WiFi  
- Estado MQTT  

La pantalla se inicializa automáticamente.  
Si no se detecta, el programa continúa sin detenerse.


## 4. Conectividad WiFi

El módulo:

- Se conecta automáticamente a la red WiFi configurada.
- Reintenta si falla la conexión.
- Reinicia el Pico W si después de varios intentos no logra conectarse.

La pantalla muestra el progreso de conexión y la IP obtenida.


## 5. Conexión al Broker MQTT (Flespi)

El módulo se conecta al broker:

`mqtt.flespi.io`

Usa:

- **Client ID único por sensor**
- **Token Flespi como username**
- **Keepalive de 60 segundos**
- Reconexión automática si hay error

El tópico asignado para este sensor es:

`iotzi/escuela/sensor/ruido`


---

## 6. Lógica de Simulación de Ruido

El sistema simula dos tipos de mediciones:

### ✔️ Ruido Ambiental Normal  
Rango: **40.0 a 60.0 dB**

Se genera en la mayoría de ciclos.

### ✔️ Anomalía / Ruido Fuerte  
Rango: **90.0 a 115.0 dB**

Se genera **1 vez cada 10 lecturas**:

- Simula un grito en salón  
- Golpe fuerte  
- Puerta azotada  
- Evento de riesgo  

En la consola aparece:

`💥 ALERTA: Ruido fuerte detectado!`

Esto permite generar alertas educativas o preventivas.

## 7. Clasificación Automática del Nivel de Ruido

Según el valor obtenido:

| Rango (dB) | Clasificación |
|------------|--------------|
| ≤ 65 | **AMBIENT** |
| 66 – 89 | **LOUD** |
| ≥ 90 | **VERY_LOUD** |

Esta clasificación aparece en pantalla y en el JSON enviado a MQTT.


## 8. Intervalo de Publicación

El sensor envía una lectura cada:
`5 segundos (5000 ms)`

Incluye:

- Número de lectura acumulada
- Nivel actual en decibeles
- Clasificación del ruido
- Estado del sistema


## 9. Formato del Mensaje (JSON)

Cada mensaje publicado tiene esta estructura:

```json
{
  "noise_db": 72.4,
  "noise_level": "LOUD"
}
```

## 9. Ejecucion

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Sensor%20de%20Ruido.png)

# 🍃 **Monitor de Velocidad y Dirección del Viento**

El presente documento forma parte del sistema **IoTzi SafeSchool AirWatch**, una red híbrida destinada al **monitoreo ambiental en escuelas**, con enfoque en salud, seguridad y bienestar.

Este módulo implementa un **simulador de sensor de viento** capaz de generar datos de velocidad y dirección del viento en tiempo real. El sensor está pensado para aplicaciones de monitoreo ambiental, estaciones climáticas escolares y sistemas IoT de alerta temprana.

---

## 1. 🎯 Objetivo del Módulo

Monitorear de manera continua la **velocidad del viento (km/h)** y su **dirección (grados y punto cardinal)**, enviando los valores a la plataforma IoT mediante **MQTT** para análisis, gráficas e integración en el panel de control del sistema IoTzi SafeSchool AirWatch.

El sistema mide:
- **Velocidad del viento** (km/h)
- **Dirección del viento** en grados (0°–360°)
- **Dirección cardinal** (N, NE, E, SE, S, SW, W, NW)

Este nodo es útil para:
- Monitorear condiciones climáticas en espacios escolares abiertos.
- Detectar ráfagas de viento fuertes que puedan representar riesgos.
- Implementar estaciones meteorológicas educativas.
- Generar alertas automáticas ante condiciones de viento peligrosas.
- Análisis histórico de patrones climáticos locales.

---

## 2. 🧩 Librerías Utilizadas (MicroPython)

Este módulo se ejecuta en un **Raspberry Pi Pico W** utilizando MicroPython. Emplea las siguientes librerías:

- **machine** → Control de hardware (pines, watchdog, I2C).
- **network** → Conectividad Wi-Fi para enlace con la red escolar o local.
- **umqtt.simple** → Cliente MQTT para publicar datos al broker.
- **urandom** → Generación de valores simulados (para prototipado).
- **json** → Formato de salida estándar para transmisión.
- **ssd1306** → Mostrar datos en pantalla OLED (opcional).
- **time** → Gestión de intervalos y temporizadores.

---

## 3. 🔌 Configuración del Hardware

| Componente | Pin / Bus | Descripción |
|-----------|-----------|-------------|
| **Pantalla OLED SSD1306** | I2C0 — SDA (GPIO 4), SCL (GPIO 5) | Muestra velocidad, dirección y estado del sistema. |
| **Raspberry Pi Pico W** | WiFi integrado | Publicación MQTT. No se utiliza sensor físico; todo es simulado. |

**Conexión de la Pantalla OLED:**
- **VCC** → 3.3V
- **GND** → GND
- **SDA** → GP4
- **SCL** → GP5

El uso de pantalla OLED es opcional, pero permite verificar en sitio:
- Velocidad del viento
- Dirección cardinal y en grados
- Estado WiFi
- Estado MQTT
- Número de mensajes enviados

---

## 4. 📡 Configuración MQTT del Sistema

Este nodo utiliza el servicio **Flespi MQTT**, compatible con IoTzi.

### 🔹 Servidor MQTT
- **Host:** `mqtt.flespi.io`
- **Puerto:** `1883`
- **User:** Token Flespi
- **Password:** *(vacío)*

### 🔹 Identificador del Nodo

`Viento_sensor`


### 🔹 Tópico MQTT

`iotzi/escuela/sensor/viento`


---

## 5. 🔄 Lógica de Funcionamiento

El nodo trabaja en ciclos repetitivos con las siguientes tareas:

### 🌬️ Lógica de Medición y Simulación

El sistema genera lecturas de viento cada **5 segundos**, simulando condiciones reales ambientales:

#### ✔️ Velocidad del viento
- **Brisa normal:** entre 5 y 35 km/h
- **Ráfaga fuerte (anomalía):** entre 60 y 80 km/h
  - Ocurre automáticamente cada **15 lecturas**, simulando un pico inesperado

#### ✔️ Dirección del viento
- Generada aleatoriamente entre **0° y 360°**
- Convertida automáticamente a dirección cardinal: **N, NE, E, SE, S, SW, W, NW**

**Tabla de conversión direccional:**

| Rango de Grados | Dirección Cardinal | Descripción |
|----------------|-------------------|-------------|
| 337.5° - 22.5° | N | Norte |
| 22.5° - 67.5° | NE | Noreste |
| 67.5° - 112.5° | E | Este |
| 112.5° - 157.5° | SE | Sureste |
| 157.5° - 202.5° | S | Sur |
| 202.5° - 247.5° | SW | Suroeste |
| 247.5° - 292.5° | W | Oeste |
| 292.5° - 337.5° | NW | Noroeste |

### ✔️ Publicación de datos
Cada **5 segundos**, el nodo envía un mensaje MQTT con los valores de velocidad y dirección.

### ✔️ Formato del mensaje (JSON)
```json
{
  "wind_speed_kmh": 27.4,
  "wind_direction_deg": 120.5,
  "wind_direction_cardinal": "SE"
}
```

## 6. Ejecucion

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Sensor%20Viento.png)

# 📡 Sensor de Humedad (DHT11/DHT22)**

El presente documento forma parte del sistema **IoTzi SafeSchool AirWatch**, una red híbrida destinada al **monitoreo ambiental en escuelas**, con enfoque en salud, seguridad y bienestar.  
Este módulo describe el **nodo de humedad relativa**, basado en sensores DHT11/DHT22, utilizado para evaluar condiciones ambientales en aulas, laboratorios y espacios comunes.


## 1. 🎯 Objetivo del Módulo

Monitorear de manera continua la **humedad relativa del aire (%)**, enviando los valores a la plataforma IoT mediante **MQTT** para análisis, gráficas e integración en el panel de control del sistema IoTzi SafeSchool AirWatch.

Este nodo es útil para:

- Asegurar condiciones saludables en salones de clase.
- Detectar riesgos de condensación o proliferación de hongos.
- Controlar microambientes en laboratorios o áreas sensibles.
- Implementar alertas ambientales de manera automática.


## 2. 🧩 Librerías Utilizadas (MicroPython)

Este módulo se ejecuta en un **ESP32** utilizando MicroPython. Emplea las siguientes librerías:

- **machine** → Control de hardware (pines, watchdog, timers).  
- **network** → Conectividad Wi-Fi para enlace con la red escolar o local.  
- **umqtt.simple** → Cliente MQTT para publicar datos al broker.  
- **dht** → Manejo del sensor DHT11/DHT22.  
- **ssd1306** → Mostrar datos en pantalla OLED (opcional).  
- **json** → Formato de salida estándar para transmisión.  


## 3. 🔌 Configuración del Hardware

| Componente | Pin ESP32 | Descripción |
|-----------|-----------|-------------|
| **Sensor DHT11 / DHT22** | GP15 | Lectura de humedad relativa. |
| **OLED SSD1306 (opcional)** | GP4 (SDA) / GP5 (SCL) | Interfaz I2C para visualización.|

**Conexión del Sensor DHT:**  
- **VCC** → 3.3V  
- **GND** → GND  
- **DATA** → GP15  

El uso de pantalla OLED es opcional, pero permite verificar en sitio:

- Humedad actual  
- Estado WiFi  
- Estado MQTT  
- Número de mensajes enviados  


## 4. 📡 Configuración MQTT del Sistema

Este nodo utiliza el servicio **Flespi MQTT**, compatible con IoTzi.

### 🔹 Servidor MQTT
- **Host:** `mqtt.flespi.io`  
- **Puerto:** `1883`  
- **User:** Token Flespi  
- **Password:** *(vacío)*  

### 🔹 Identificador del Nodo

`HUM_Sensor_01 `

# 5. 🔄 Lógica de Funcionamiento

El nodo trabaja en ciclos repetitivos con las siguientes tareas:

### ✔️ Lectura del sensor  
Se obtiene únicamente el valor de **humedad relativa (%)**.

### ✔️ Publicación de datos  
Cada **5 segundos**, el nodo envía un mensaje MQTT con el valor leído.

### ✔️ Formato del mensaje (JSON)
```json
{
  "val": 52.3
}
```
## 6. Ejecucion

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Sensor%20Humedad.png)


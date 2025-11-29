# 🏭 **Módulo: Simulador del Sensor de Monóxido de Carbono (CO)**

El presente documento forma parte del sistema **IoTzi SafeSchool AirWatch**, una red híbrida destinada al **monitoreo ambiental en escuelas**, con enfoque en salud, seguridad y bienestar.

Este módulo implementa un **sensor simulado de Monóxido de Carbono (CO)** utilizando una Raspberry Pi Pico W. El sistema genera lecturas realistas con picos periódicos que representan posibles fugas peligrosas de CO, y transmite dichas mediciones en tiempo real mediante MQTT hacia Flespi.io.

---

## 1. 🎯 Objetivo del Módulo

Monitorear de manera continua los **niveles de Monóxido de Carbono (CO) en ppm**, enviando los valores a la plataforma IoT mediante **MQTT** para análisis, gráficas e integración en el panel de control del sistema IoTzi SafeSchool AirWatch.

El propósito principal es ofrecer un nodo CO totalmente funcional dentro de una red IoT híbrida (sensores reales + simulados), sin exponer a nadie a gases reales y evitando costos elevados de sensores especializados.

Este nodo es útil para:
- Detectar fugas de monóxido de carbono en laboratorios, calderas y áreas de riesgo.
- Implementar sistemas de alerta temprana ante concentraciones peligrosas.
- Monitorear la calidad del aire en espacios cerrados.
- Proteger la salud de estudiantes y personal educativo.
- Generar estadísticas de seguridad ambiental.

---

## 2. 🧩 Librerías Utilizadas (MicroPython)

Este módulo se ejecuta en un **Raspberry Pi Pico W** utilizando MicroPython. Emplea las siguientes librerías:

- **machine** → Control de hardware (pines, I2C, watchdog timer).
- **network** → Conectividad Wi-Fi en modo estación para enlace con la red.
- **umqtt.simple** → Cliente MQTT lightweight para publicar datos al broker.
- **urandom** → Generación de valores simulados de CO (para prototipado).
- **json** → Formato de salida estándar para transmisión.
- **ssd1306** → Controlador para pantallas OLED I2C.
- **time** → Gestión de intervalos y temporizadores con `ticks_ms()`.

---

## 3. 🔌 Configuración del Hardware

| Componente | Pin Pico W | Descripción |
|-----------|-----------|-------------|
| **SSD1306 I2C (Display)** | SDA → GP4, SCL → GP5 | Muestra lecturas de CO, estado WiFi y MQTT. |
| **WiFi interno** | – | Conexión a red y MQTT Flespi. |
| **WDT (Watchdog)** | Interno | Reinicia el equipo si entra en freeze por más de 8 s. |

**Conexión de la Pantalla OLED:**
- **VCC** → 3.3V
- **GND** → GND
- **SDA** → GP4
- **SCL** → GP5

🔎 **Nota importante:** El sensor de CO es simulado, por lo que no requiere pines adicionales.

El uso de pantalla OLED es opcional, pero permite verificar en sitio:
- Nivel de CO actual (ppm)
- Estado de seguridad
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
```
CO_sensor
```

### 🔹 Tópico MQTT
```
iotzi/escuela/sensor/co
```

---

## 5. 🔄 Lógica de Funcionamiento

El nodo trabaja en ciclos repetitivos con las siguientes tareas:

### 🚨 Lógica de Simulación y Alerta

El sistema genera valores de CO en **ppm (partes por millón)** y los clasifica según umbrales estandarizados:

#### **Clasificación de Niveles de CO**

| Rango (ppm) | Estado | Descripción | Acción Recomendada |
|------------|--------|-------------|-------------------|
| 0–9 | `NORMAL` | Condiciones seguras | Operación normal |
| 10–49 | `ELEVATED` | Incremento significativo | Monitoreo continuo |
| 50–99 | `DANGEROUS` | Riesgo moderado | Ventilación inmediata |
| ≥ 100 | `HIGHLY_DANGEROUS` | Peligro crítico | Evacuación y revisión |

#### 🔥 Picos de Fuga

Cada **10 lecturas**, el sistema genera un valor entre **55–150 ppm**, representando una fuga inesperada:

- En **consola** se imprime la alerta con símbolo 🚨
- En **pantalla** se muestra el estado crítico
- Se publica un **JSON inmediato** vía MQTT

**Lecturas normales:** Entre 0 y 30 ppm (ambiente seguro)

### ✔️ Publicación de datos
Cada **5 segundos**, el nodo envía un mensaje MQTT con el valor de CO y su clasificación.

### ✔️ Formato del mensaje (JSON)
```json
{
  "co_ppm": 87.4,
  "co_status": "DANGEROUS"
}
```

## 6. Ejecucion

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Sensor%20Monoxido.png)

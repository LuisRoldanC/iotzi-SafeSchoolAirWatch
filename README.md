<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/67291be1-1acd-4f98-a328-0ffdf79c71e8" />

# IoTzi SafeSchool AirWatch
### Red Híbrida de Monitoreo Ambiental para Entornos Escolares

---

## 1. Resumen del Proyecto

**IoTzi SafeSchool AirWatch** es un sistema avanzado de monitoreo ambiental diseñado para incrementar la seguridad en entornos escolares mediante una red IoT híbrida que combina:

- **Sensores físicos reales**: obtienen medidas confiables del entorno.  
- **Sensores simulados**: permiten modelar escenarios extremos o peligrosos sin necesidad de hardware costoso.

La arquitectura emplea:

- **ESP32 (C++)**  
- **Raspberry Pi Pico W (MicroPython)**  
- **MQTT + Broker Flespi**, con mensajes JSON ligeros y eficientes.

---

## 2. El Problema: De la Alerta de Gas a la Calidad del Aire Total

Los sistemas tradicionales de alerta se enfocan solo en amenazas aisladas (p. ej. fuga de gas). Sin embargo, la seguridad ambiental real en escuelas depende de múltiples variables.

### 🔹 Amenazas Crónicas
- Exposición prolongada a **PM2.5**  
  → Impactos acumulativos en la salud respiratoria.

### 🔹 Amenazas Agudas
- Picos de **CO**, humo o ruido extremo  
  → Requieren respuesta inmediata.

### 🔹 Factores de Contexto
- Viento y calor extremo  
  → Alteran la propagación de contaminantes o provocan riesgos adicionales.

**IoTzi SafeSchool AirWatch** integra:  
**amenazas + contexto ambiental + sensores físicos + simulaciones avanzadas**.

---

## 3. Marco Teórico: Metodología de Red Híbrida

La solución se basa en **fusión híbrida de sensores**, combinando datos físicos con simulaciones.

### 3.1. Sensores Físicos (Ground Truth)
Proveen mediciones reales mediante sensores **DHT11**:

- Temperatura  
- Humedad  

Funcionan como referencia para cálculos derivados como:

- Índice de calor  
- Tendencias ambientales  
- Generación de alarmas  

### 3.2. Sensores Simulados

Permiten recrear escenarios difíciles o peligrosos:

- Picos de CO  
- Fugas de gas (MQ-4)  
- Presencia de humo (MQ-2)  
- Variaciones de PM2.5  
- Ruido extremo  
- Fenómenos ambientales como viento  

Sus ventajas:

- Reducen costos  
- Aceleran pruebas  
- No requieren riesgos reales  

---

## 4. Arquitectura Tecnológica

| Nivel       | Tecnología             | Plataforma   | Propósito |
|-------------|------------------------|--------------|-----------|
| Hardware A  | ESP32                  | C++          | Simulación de sensores industriales (MQx, PM2.5, DO). |
| Hardware B  | Raspberry Pi Pico W    | MicroPython  | Sensores físicos + simulaciones contextuales (viento, ruido, índice de calor). |
| Protocolo   | MQTT                   | –            | Comunicación ligera en tiempo real. |
| Broker      | Flespi.io              | Nube         | Almacenamiento, enrutamiento y monitoreo de mensajes JSON. |

---

## 5. Implementación de Nodos: ESP32 (C++)

La plataforma **ESP32** contiene 4 nodos simulados.  
Cada uno se encuentra en su propia carpeta dentro del repositorio.

### 5.1. Nodo 1 — Sensor de Oxígeno Disuelto (DO)
- **Tópico:** `iotzi/escuela/sensor/do`  
- **Descripción:** Simula un sensor DO para medir mg/L de oxígeno en agua (cisternas o laboratorios).
- [🫧 Simulador de Sensor de Oxígeno Disuelto (DO) — Documentación](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/Sensor_OxigenoDisuelto/readme.md)

### 5.2. Nodo 2 — Sensor de Partículas PM2.5
- **Tópico:** `iotzi/escuela/sensor/pm25`  
- **Descripción:** Emulación basada en pulsos característicos de sensores de polvo fino.
- [💨 Simulador de Sensor de Polvo PM2.5 (PPD42 — Documentación)](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/Sensor%20de%20Polvo/readme.md)

### 5.3. Nodo 3 — Sensor de Gas (MQ-4 Metano)
- **Tópico:** `iotzi/escuela/sensor/gas`  
- **Descripción:** Simula sensor MQ-4. Usa lógica inversa: **valores bajos = peligro**.
- [🧯 Simulador de Sensor de Gas MQ-4 — Documentación](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/Sensor%20Gas/readme.md)

### 5.4. Nodo 4 — Sensor de Humo (MQ-2)
- **Tópico:** `iotzi/escuela/sensor/humo`  
- **Descripción:** Simula sensor MQ-2 donde valores altos indican presencia de humo.
- [🔥 Simulador de Sensor de Humo MQ-2 — Documentación](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/Sensor%20Humo/readme.md)

---

## 6. Implementación de Nodos: Raspberry Pi Pico W (MicroPython)

La plataforma **Pico W** opera 6 nodos adicionales, combinando sensores físicos reales con simulación avanzada.

### 6.1. Nodo 5 — Sensor de Monóxido de Carbono (CO)
- **Tópico:** `iotzi/escuela/sensor/co`  
- **Descripción:** Simula niveles de CO con picos periódicos.
- [🏭 Simulador del Sensor de Monóxido de Carbono (CO) — Documentación](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/Sensor%20de%20Monoxido%20de%20carbono/readme.md)

### 6.2. Nodo 6 — Sensor de Humedad (Físico)
- **Tópico:** `iotzi/escuela/sensor/hum`  
- **Descripción:** Lecturas reales del sensor **DHT11** en el pin GP15.
- [📡 Sensor de Humedad (DHT11/DHT22) — Documentación](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/Sensor%20de%20Humedad/readme.md)

### 6.3. Nodo 7 — Índice de Calor (Derivado)
- **Tópico:** `iotzi/escuela/sensor/IndiceC`  
- **Descripción:** Calculado mediante fórmula Steadman-NWS usando temperatura + humedad reales.
- [🔥 Sensor Simulador de Índice de Calor — Documentación](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/Sensor%20de%20Indice%20de%20calor/readme.md)

### 6.4. Nodo 8 — Sensor de Ruido (Simulado)
- **Tópico:** `iotzi/escuela/sensor/ruido`  
- **Descripción:** Genera niveles acústicos normales y picos simulados.
- [🔊 Simulador de Sensor de Ruido (Pico W) — Documentación](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/Sensor%20de%20Ruido/readme.md)

### 6.5. Nodo 9 — Sensor de Temperatura (Físico)
- **Tópico:** `iotzi/escuela/sensor/temp`  
- **Descripción:** Lectura real desde DHT11 (variable temperatura).
- [🌡️ Sensor de Temperatura (DHT11 – Pico W)— Documentación](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/Sensor%20de%20Temperatura/readme.md)

### 6.6. Nodo 10 — Sensor de Viento (Simulado)
- **Tópico:** `iotzi/escuela/sensor/vien`  
- **Descripción:** Simula velocidad del viento y calcula dirección cardinal.
- [🍃 Monitor de Velocidad y Dirección del Viento — Documentación](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/Sensor%20de%20Viento/readme.md)

---

## Estado General del Sistema

Los **10 nodos** (físicos + simulados) están **100% operativos** y conectados a la red MQTT-Flespi.

El sistema demuestra:

- ✔️ **Fiabilidad de sensores físicos**  
- ✔️ **Flexibilidad de nodos simulados**  
- ✔️ **Comunicación fluida**  
  Microcontrolador → MQTT → Flespi

---

## Resumen General del Proyecto

| Módulo           | Tipo       | Estado | Tópico MQTT                  |
|------------------|------------|--------|-------------------------------|
| Temperatura      | Físico     | ✔️      | `.../sensor/temp`            |
| Humedad          | Físico     | ✔️      | `.../sensor/hum`             |
| PM2.5            | Simulado   | ✔️      | `.../sensor/pm25`            |
| Gas (MQ-4)       | Simulado   | ✔️      | `.../sensor/gas`             |
| Humo (MQ-2)      | Simulado   | ✔️      | `.../sensor/humo`            |
| CO               | Simulado   | ✔️      | `.../sensor/co`              |
| Viento           | Simulado   | ✔️      | `.../sensor/vien`            |
| Ruido            | Simulado   | ✔️      | `.../sensor/ruido`           |
| Índice de Calor  | Derivado   | ✔️      | `.../sensor/IndiceC`         |
| Oxígeno (DO)     | Simulado   | ✔️      | `.../sensor/do`              |

---

## 7. 📊 Dashboard Web IoTzi SafeSchool AirWatch

### Vista General del Sistema

El **Dashboard Web** de IoTzi SafeSchool AirWatch es una interfaz visual en tiempo real que centraliza todos los datos de los 10 sensores ambientales distribuidos en el campus escolar.


### Características Principales

#### 🎯 Funcionalidades
- **Visualización en tiempo real** de todos los sensores simultáneamente
- **Código de colores** para identificación rápida de alertas (🟢 🟡 🔴)
- **Mapa interactivo** con ubicación de sensores en el campus
- **Actualización automática** vía MQTT sin recargar la página
- **Diseño responsive** adaptable a desktop, tablet y móvil

#### 🏗️ Tecnologías Utilizadas
- **Frontend:** HTML5 + CSS3 + JavaScript
- **Comunicación:** MQTT sobre WebSockets (Flespi.io)
- **Mapas:** Leaflet.js + OpenStreetMap
- **Actualización:** Tiempo real event-driven

---

### 📱 Componentes del Dashboard

#### 1. Header
```
🛡️ IoTzi SafeSchool AirWatch
Estado de Conexión: 🟢 Conectado
```

#### 2. Grid de Sensores (10 Tarjetas)

#### Fila Superior
- 🌡️ **Temperatura:** 25.0°C - NORMAL
- 💧 **Humedad:** 63.0% - NORMAL
- 🔥 **Índice de Calor:** 35.7°C / 46.0°C - DANGER
- 🍃 **Viento:** 19.6 km/h (NE) - NORMAL
- 🏭 **PM2.5:** 17014 mg/m³ - SAFE

#### Fila Inferior
- 🏭 **CO:** 4.9 ppm - NORMAL
- 🔥 **Gas (MQ-4):** 882 - SAFE
- ☁️ **Humo (MQ-2):** 329 - SAFE
- 🫧 **Oxígeno Disuelto:** 3.9 mg/L - LOW
- 🔊 **Ruido:** 58.5 dB - AMBIENT

### 3. Mapa Interactivo
- **Ubicación:** Instituto Tecnológico de Tijuana
- **Marcadores coloreados** según estado del sensor
- **Popup informativo** al hacer clic en cada marcador

---

### 🎨 Sistema Visual

### Estados y Colores
| Estado | Color | Significado |
|--------|-------|-------------|
| 🟢 SAFE/NORMAL | Verde | Valores seguros |
| 🟡 WARNING/ELEVATED | Amarillo | Atención requerida |
| 🔴 DANGER/CRITICAL | Rojo | Acción inmediata |

### Animaciones
- Tarjetas en estado **DANGER** pulsan con borde rojo
- Actualización suave al recibir nuevos datos
- Transiciones de color fluidas


### 🔄 Funcionamiento
```
Sensores → MQTT Broker (Flespi) → WebSocket → Dashboard → Actualización UI
```

**Frecuencia de actualización:** Datos en tiempo real cada 5 segundos

---

### 📐 Diseño Responsive

| Pantalla | Layout |
|----------|--------|
| **Desktop (≥1200px)** | Grid 5 columnas |
| **Tablet (768-1199px)** | Grid 3 columnas |
| **Móvil (<768px)** | Grid 1 columna |


### 📊 Vista del Sistema
```
┌─────────────────────────────────────────────────────┐
│         IoTzi SafeSchool AirWatch                   │
│         Estado: 🟢 Conectado                        │
├─────────────────────────────────────────────────────┤
│  [Temp] [Humedad] [Índice] [Viento] [PM2.5]       │
│  [CO]   [Gas]     [Humo]   [DO]     [Ruido]       │
├─────────────────────────────────────────────────────┤
│            [MAPA INTERACTIVO]                       │
│      Instituto Tecnológico de Tijuana               │
│         🟢🟢🟢🔴🟢 (marcadores)                      │
└─────────────────────────────────────────────────────┘

```

## 8. Vista Dashboard

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Dashboard%201.png)

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Mapa%20Dashboard.png)

---

## 9. Videos demostrativos

🎬 **Sistema IoTzi SafeSchool - Parte 1**  
[🔴 Video demostrativo Parte 1](https://www.loom.com/share/422ece5b37d7407cbeabe30264b2a3d6)

🎬 **Sistema IoTzi SafeSchool - Parte 2**  
[🔴 Video demostrativo Parte 2](https://www.loom.com/share/39a581fb6f7b4fe89eaf17bad5ccf1d5)

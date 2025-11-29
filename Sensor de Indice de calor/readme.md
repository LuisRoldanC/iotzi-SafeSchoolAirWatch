# 🔥 Sensor Simulador de Índice de Calor  

Este módulo forma parte del ecosistema **IoTzi SafeSchool AirWatch**, una plataforma diseñada para monitorear variables ambientales en tiempo real dentro de espacios escolares como aulas, patios, laboratorios y auditorios.

El siguiente documento describe el funcionamiento del **Nodo de Índice de Calor (Heat Index)**, implementado en **Raspberry Pi Pico W con MicroPython**, capaz de simular condiciones térmicas críticas y reportarlas vía MQTT.

## 1. 🎯 Objetivo del Módulo

El propósito de este nodo es **estimar el Índice de Calor (Heat Index)**, un parámetro que combina la temperatura del aire y la humedad relativa para determinar la **sensación térmica real** experimentada por estudiantes y personal escolar.

Este nodo permite:

- Detectar situaciones de **riesgo por calor extremo**.
- Emitir alertas tempranas en zonas donde los alumnos realizan actividades físicas.
- Monitorear condiciones térmicas en escuelas sin necesidad de hardware físico inicial.
- Probar dashboards, reglas y flujos de datos antes de desplegar sensores reales.

## 2. 🧩 Librerías Utilizadas (MicroPython)

El script utiliza las siguientes librerías:

- **machine** → Manejo de pines, temporizadores, watchdog.  
- **network** → Conexión Wi-Fi.  
- **urandom** → Generación de valores simulados (temperatura y humedad).  
- **json** → Empaquetado de la telemetría para MQTT.  
- **ssd1306** → Visualización en pantalla OLED (opcional).  
- **umqtt.simple** → Cliente MQTT para enviar telemetría al broker.  


## 3. 🔌 Configuración del Hardware

Aunque se trata de un **sensor totalmente simulado**, el hardware real incluye:

| Componente | Pines | Función |
|-----------|-------|---------|
| **Pico W** | Integrado | Conexión Wi-Fi + ejecución del simulador. |
| **OLED SSD1306** (opcional) | GP4 (SDA), GP5 (SCL) | Visualización local de valores. |

No se requiere ningún sensor físico, ya que las lecturas se generan mediante funciones aleatorias controladas.


## 4. 🧠 Simulación de Datos Ambientales

El nodo genera lecturas realistas para condiciones calurosas:

- **Temperatura simulada:** entre **28°C y 42°C**  
- **Humedad relativa simulada:** entre **45% y 90%**

Esto permite reproducir escenarios comunes en escuelas de zonas cálidas.


## 5. 🔥 Cálculo del Índice de Calor

Se utiliza la fórmula oficial de la  
**National Weather Service (NWS, EE.UU.)**, conocida como **Steadman's Regression Model**.

## ✔ Condiciones de validez de la fórmula:

- Temperatura > **80°F**  
- Humedad > **40%**

Si no se cumplen, el índice de calor se iguala a la temperatura.

El flujo completo del cálculo es:

1. Convertir la temperatura de °C → °F  
2. Aplicar la fórmula del NWS  
3. Resultado del índice (en °F) → convertir a °C  
4. Enviar como **heat_index_c**


## 6. 📡 Configuración MQTT

El nodo envía sus datos mediante **Flespi MQTT**, compatible con IoTzi:

| Parámetro | Valor |
|----------|-------|
| **Broker** | mqtt.flespi.io |
| **Puerto** | 1883 |
| **Usuario** | Token Flespi |
| **Password** | *(vacío)* |

### 🔹 ID del dispositivo

`IndiceCalor_sensor`


### 🔹 Tópico de publicación

`iotzi/escuela/sensor/IndiceC`


## 7. 🔄 Lógica de Funcionamiento

Cada **5 segundos**, el sistema ejecuta la siguiente lógica:

### ✔ Simulación  
- Genera temperatura (°C)  
- Genera humedad relativa (%)  
- Calcula índice de calor (°C)

### ✔ Empaquetado en JSON  
```json
{
  "temperature_c": 34.2,
  "humidity_rh": 68.1,
  "heat_index_c": 44.7
}
```
## 7. Ejecucion

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Sensor%20Indice%20de%20Calor.png)

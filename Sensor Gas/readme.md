# 🧯 Simulador de Sensor de Gas MQ-4

Este proyecto implementa un **simulador del sensor de gas MQ-4**, diseñado para probar sistemas IoT antes de conectar hardware físico.  
El simulador reproduce el comportamiento típico del MQ-4, donde:

- **Valores altos → ambiente seguro**  
- **Valores bajos → fuga o condición peligrosa**

El sistema envía datos periódicos mediante MQTT (Flespi), alternando entre valores normales y valores de fuga cada cierto número de lecturas.

---

## 1. 📚 Librerías Utilizadas

Este simulador utiliza dos librerías fundamentales:

- **WiFi.h** → Manejo de conectividad WiFi  
- **PubSubClient.h** → Cliente MQTT para publicar datos al broker

---

## 2. 🔧 Configuración de Hardware y Pines

Aunque este es un simulador, el ESP32 utiliza un LED como indicador visual de alerta.

| Pin | Componente     | Descripción                                  |
|-----|----------------|----------------------------------------------|
| 2   | LED de alarma  | Se enciende cuando el nivel de gas es crítico |

---

## 3. 🧪 Lógica de Simulación y Clasificación

La simulación reproduce el comportamiento real del MQ-4, donde **valores bajos indican peligro**.

### 🔹 Generación de Datos

- Se generan valores seguros entre **800 y 1000**.
- Cada **10 lecturas** se genera una **anomalía**, usando valores entre **300 y 600**.
- Esto simula una fuga de gas o una lectura peligrosa.

### 🔹 Clasificación del Estado

El sistema clasifica cada lectura según este umbral:

| Lectura (`gasvalue`) | Estado   |
|----------------------|----------|
| **≤ 700**            | ⚠️ DANGER |
| **> 700**            | ✔️ SAFE   |

### 🔹 Indicador LED

- **Encendido:** estado **DANGER**  
- **Apagado:** estado **SAFE**

---

## 4. ⏱️ Temporización

El simulador publica datos cada: `2 segundos`. 
No se utiliza `delay()`, permitiendo que MQTT siga activo sin bloqueos.

---

## 5. 📡 Protocolo y Formato MQTT

### 🔸 Servidor MQTT (Flespi)

| Parámetro    | Valor                      |
|--------------|----------------------------|
| Servidor     | mqtt.flespi.io             |
| Puerto       | 1883                       |
| Usuario      | Token Flespi               |
| Tópico       | iotzi/escuela/sensor/gas   |

---

## 6. 📤 Ejemplo de Mensaje JSON

Cada publicación contiene el valor leído y su estado:

```json
{
  "gas_value": 845,
  "status": "SAFE"
}
```

Ejemplo durante una anomalía simulada:

```json
{
  "gas_value": 455,
  "status": "DANGER"
}
```

## 7. Ejecucion

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Sensor%20Gas.png)

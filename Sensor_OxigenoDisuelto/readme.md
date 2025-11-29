# 🫧 Simulador de Sensor de Oxígeno Disuelto (DO)

Este proyecto simula un sensor de **Oxígeno Disuelto (DO)** para monitorear la calidad del agua.  
El objetivo principal es enviar lecturas periódicas que representen el nivel de oxígeno (en **mg/L**) y un estado de clasificación (como **"OPTIMAL"** o **"CRITICAL_LOW"**).

Es una simulación ideal para probar la **conectividad MQTT**, la recepción de datos y la visualización en dashboards (como Grafana o Flespi) antes de implementar el hardware físico.

---

## 1. 📚 Librerías de Arduino

Se utilizan las siguientes librerías:

- `WiFi.h`: Para la conectividad Wi-Fi.  
- `PubSubClient.h`: Para la comunicación MQTT.

---

## 2. 🔌 Configuración de Hardware y Pines

Este código es **un simulador** y no depende de pines físicos.

| Pin | Componente | Descripción |
|-----|------------|-------------|
| N/A | (Simulador) | No se lee un pin físico. |
| N/A | (Simulador) | Los datos se generan con `random()`. |

---

## 3. 🧪 Lógica de Simulación y Clasificación

El sistema opera enviando datos a intervalos fijos.

### 🔧 Generación de Datos
- En cada ciclo del `loop()`, se genera un valor flotante aleatorio (`oxygenValue`) entre **1.0** y **10.9** para simular el sensor.

### 🏷️ Clasificación
El valor simulado se compara con constantes como:

- `O2_OPTIMAL_MIN`  
- `O2_CRITICAL_LOW`

Según el rango, se asigna un estado textual (**"OPTIMAL"**, **"LOW"**, **"CRITICAL_LOW"**, etc.)

### ⏱️ Temporización
- El sistema publica un mensaje MQTT cada **5 segundos** mediante `delay(5000)`.

---

## 4. 📡 Protocolo y Formato de Datos

Cada 5 segundos se publica un nuevo mensaje MQTT.

### **Tópico de Publicación**

`iotzi/escuela/sensor/do `


### **Formato del Mensaje (JSON de Telemetría)**

El payload contiene:

- Valor actual de oxígeno en mg/L (`oxygen_mg_L`)
- Estado clasificado (`status`)

### **Ejemplo de Payload**
```json
{
  "oxygen_mg_L": 7.3,
  "status": "OPTIMAL"
}
```

## 5. Ejecucion

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Sensor%20Oxigeno%20Disuelto.png)

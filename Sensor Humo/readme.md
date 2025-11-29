# 🔥 Simulador de Sensor de Humo MQ-2

Este proyecto simula un sensor de **humo MQ-2**, generando valores de lectura que representan la presencia de gases combustibles o humo en el ambiente.  
El objetivo es enviar lecturas periódicas por MQTT que incluyen un valor numérico de concentración y un estado de clasificación como **"SAFE"** o **"DANGER"**.

Este simulador resulta ideal para:
- Probar flujos de IoT sin hardware físico  
- Testear dashboards (Grafana, Flespi, Node-RED)  
- Validar alertas, triggers, sistemas de seguridad y monitoreo  
- Realizar demostraciones de sensores ambientales  

---

## 1. 📚 Librerías de Arduino

Se utilizan dos librerías principales:

- `WiFi.h`: Manejo de la conexión inalámbrica.  
- `PubSubClient.h`: Envío de datos y manejo del protocolo MQTT.

---

## 2. 🔌 Configuración de Hardware y Pines

Este simulador **no utiliza un sensor físico MQ-2**, ya que los valores se generan con `random()`.  
Solo se emplea un LED para indicar condiciones de peligro.

| Pin | Componente | Descripción |
|-----|------------|-------------|
| 2 | LED | Se enciende cuando el valor indica peligro (“DANGER”). |
| N/A | Sensor MQ-2 | No se usa hardware físico; la lectura se simula por software. |

---

## 3. 🧪 Lógica de Simulación y Clasificación

El sistema genera valores que imitan el comportamiento del sensor MQ-2.

### 🔧 Generación de valores simulados
Cada lectura se produce mediante la función `random()`, usando dos rangos principales:

| Tipo de Lectura | Rango Simulado | Significado |
|-----------------|----------------|-------------|
| Normal | 200 – 400 | Ambiente seguro |
| Anomalía | 700 – 1000 | Humo intenso / fuga de gas |

Cada **10 lecturas**, el sistema genera una **anomalía simulada**, lo que permite probar sistemas de alerta.

### 🏷️ Clasificación del Estado

El valor se compara con un umbral:

- `>= 600` → **DANGER**  
- `< 600` → **SAFE**

Si el estado es **DANGER**, el LED del pin 2 se enciende.

### ⏱️ Temporización
El sistema publica nuevos valores cada: `2 segundos`

## 4. 📡 Protocolo y Formato de Datos

Las lecturas se envían usando MQTT.

### **Tópico de Publicación**

`iotzi/escuela/sensor/humo`


### **Formato del Mensaje (JSON)**

Cada mensaje contiene:

- `smoke_value`: Valor numérico que representa la intensidad del humo  
- `status`: Estado clasificado del ambiente  

### **Ejemplo de Payload**
```json
{
  "smoke_value": 845,
  "status": "DANGER"
}
```

## 7. Ejecucion

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Sensor%20Humo.png)


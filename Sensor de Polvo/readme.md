# 💨 Simulador de Sensor de Polvo PM2.5 (PPD42)

Este proyecto simula un sensor de **partículas finas PM2.5** basado en el comportamiento del sensor **PPD42**, el cual trabaja midiendo la duración de pulsos eléctricos en microsegundos (µs).  
El objetivo principal es enviar lecturas periódicas que representen el nivel de partículas en el aire y un estado de clasificación (como **"SAFE"** o **"DANGER"**).

Este simulador es ideal para probar:
- Conectividad MQTT  
- Recepción de datos en backends  
- Dashboards como Grafana, Flespi o Node-RED  
- Alarmas, triggers y procesamiento sin usar hardware físico real  

---

## 1. 📚 Librerías de Arduino

Se utilizaron las siguientes librerías:

- `WiFi.h`: Manejo de la red WiFi.  
- `PubSubClient.h`: Comunicación MQTT y envío de telemetría.

---

## 2. 🔌 Configuración de Hardware y Pines

Este simulador **no depende de un sensor físico PPD42 real**.  
En su lugar, genera pulsos simulados basados en rangos típicos del sensor.

| Pin | Componente | Descripción |
|-----|------------|-------------|
| 2 | LED | LED de alarma (encendido = peligro) |
| N/A | Sensor físico PPD42 | *No se utiliza hardware real, se simula por software.* |

---

## 3. 🧪 Lógica de Simulación y Clasificación

El sistema genera lecturas en un intervalo fijo y las envía por MQTT.

### 🔧 Simulación del PPD42
El sensor original mide la duración de pulsos:

- **Pulsos largos** → alta concentración de polvo → **peligro**  
- **Pulsos cortos** → aire limpio → **seguro**

El simulador reproduce ese comportamiento:

- Cada lectura se genera con `random()`.
- Cada **10 lecturas** ocurre una anomalía simulada (polvo elevado).

### 🔢 Rango de Valores Simulados

| Tipo de Lectura | Rango Simulado (µs) | Significado |
|-----------------|---------------------|-------------|
| Normal | 10,000–50,000 µs | Aire limpio |
| Anomalía | 200,000–400,000 µs | Evento de polvo / peligro |

### 🏷️ Clasificación del Estado

El valor simulado se compara con un umbral:

- `>= 150,000 µs` → **DANGER**
- `< 150,000 µs` → **SAFE**

El LED del pin 2 se enciende al detectar estado **DANGER**.

### ⏱️ Temporización
El sistema publica un mensaje MQTT cada 2 segundos mediante delay(2000)

---

## 4. 📡 Protocolo y Formato de Datos

Cada publicación utiliza MQTT.

### **Tópico de Publicación**

`iotzi/escuela/sensor/pm25`


### **Formato del Mensaje (Telemetría JSON)**

El mensaje incluye:

- `pm_valor`: duración del pulso en microsegundos (µs)  
- `status`: clasificación textual del nivel de polvo  

### **Ejemplo de Payload**
```json
{
  "pm_valor": 234000,
  "status": "DANGER"
}
```

## 5. Ejecucion

![](https://github.com/tectijuana/iotzi-LuisRoldanC/blob/main/ImagenesSensores/Sensor%20Polvo.png)

#include <WiFi.h>
#include <PubSubClient.h>

// --- CONFIGURACIÓN WIFI ---
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// --- CONFIGURACIÓN FLESPI MQTT ---
const char* mqtt_server = "mqtt.flespi.io";
const int mqtt_port = 1883;
const char* mqtt_username = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
const char* mqtt_topic = "iotzi/escuela/sensor/gas";

// --- Configuración del Sensor ---
const char* client_id = "SensorGas_MQ4_Simulado"; // ID de cliente actualizado
const int LED_PIN = 2;            // Pin del LED de alarma

// --- ⚠️ CAMBIO 1: Configuración de la SIMULACIÓN ---
// (Lógica invertida del MQ-4: valor BAJO = PELIGRO)
const int DANGER_THRESHOLD = 700;   // Umbral de peligro
const int ANOMALY_INTERVAL = 10;  // Generar anomalía cada 10 lecturas
const int NORMAL_MIN = 800;       // Valor de gas normal (seguro)
const int NORMAL_MAX = 1000;      // Valor de gas normal (seguro)
const int ANOMALY_MIN = 300;      // Valor de gas en anomalía (peligro)
const int ANOMALY_MAX = 600;      // Valor de gas en anomalía (peligro)


// --- Variables para temporizador y conteo ---
unsigned long lastPublish = 0;
const long publishInterval = 2000; // Publicar cada 2 segundos
// ⚠️ CAMBIO 2: Contador de lecturas
int reading_count = 0;

// Clientes
WiFiClient espClient;
PubSubClient client(espClient);

// Prototipo de función
void reconnectMQTT();

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  delay(1000);

  // ⚠️ CAMBIO 3: Inicializar el generador de números aleatorios
  randomSeed(analogRead(0)); 

  Serial.println("\n========================================");
  Serial.println("🔥 SIMULADOR de Sensor de Gas MQ-4");
  Serial.println("========================================");

  // Conectar WiFi (sin cambios)
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✓ Conectado al WiFi");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // Configurar MQTT (sin cambios)
  client.setServer(mqtt_server, mqtt_port);
  client.setBufferSize(128);
  client.setKeepAlive(60);

  Serial.println("========================================\n");
}

void loop() {
  // 1. Mantener conexión MQTT (sin cambios)
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop(); 

  // 2. Lógica de publicación (sin delay)
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastPublish >= publishInterval) {
    lastPublish = currentMillis; // Reinicia el temporizador

    // --- ⚠️ CAMBIO 4: Lógica de simulación ---
    reading_count++;
    
    int gasvalue;
    bool isAnomaly = (reading_count % ANOMALY_INTERVAL == 0);

    if (isAnomaly) {
      // Generar un valor de ANOMALÍA (peligro, valor bajo)
      gasvalue = random(ANOMALY_MIN, ANOMALY_MAX + 1); 
      Serial.println("🔥 ALERTA: Fuga de gas simulada!");
    } else {
      // Generar un valor NORMAL (seguro, valor alto)
      gasvalue = random(NORMAL_MIN, NORMAL_MAX + 1);
    }
    // --- Fin del cambio 4 ---

    Serial.print("Simulated Gas Value: ");
    Serial.print(gasvalue);

    // Determinar estado y controlar LED
    // (La lógica no cambia, sigue siendo correcta para el MQ-4)
    const char* status;
    if (gasvalue <= DANGER_THRESHOLD) {
      digitalWrite(LED_PIN, HIGH);
      Serial.println(" - Danger! Gas leak Detected!");
      status = "DANGER";
    } else {
      digitalWrite(LED_PIN, LOW);
      Serial.println(" - Environment safe");
      status = "SAFE";
    }

    // Crear y enviar JSON a MQTT
    char json_buffer[100];
    sprintf(json_buffer, "{\"gas_value\":%d,\"status\":\"%s\"}", gasvalue, status);

    if (client.publish(mqtt_topic, json_buffer)) {
      Serial.print("📤 Enviado: ");
      Serial.println(json_buffer);
    } else {
      Serial.println("✗ Error MQTT");
    }

    Serial.println();
  }
}

// (Función de reconexión - sin cambios)
void reconnectMQTT() {
  int attempts = 0;
  while (!client.connected() && attempts < 5) {
    Serial.print("Conectando MQTT... ");

    if (client.connect(client_id, mqtt_username, "")) {
      Serial.println("✓ CONECTADO");
      Serial.print("Tópico: ");
      Serial.println(mqtt_topic);
      Serial.println();
    } else {
      Serial.print("✗ Error rc=");
      Serial.println(client.state());
      Serial.println("Reintentando en 3 segundos...");
      attempts++;
      delay(3000);
    }
  }

  if (!client.connected()) {
    Serial.println("⚠️ No se pudo conectar. Reiniciando...");
    delay(2000);
    ESP.restart();
  }
}

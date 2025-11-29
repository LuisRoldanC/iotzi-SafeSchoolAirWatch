#include <WiFi.h>
#include <PubSubClient.h>

// --- CONFIGURACIÓN WIFI ---
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// --- CONFIGURACIÓN FLESPI MQTT ---
const char* mqtt_server = "mqtt.flespi.io";
const int mqtt_port = 1883;
const char* mqtt_username = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
// ⚠️ CAMBIO 1: Tópico actualizado para PM2.5
const char* mqtt_topic = "iotzi/escuela/sensor/pm25"; 

// --- Configuración del Sensor ---
// ⚠️ CAMBIO 2: ID de cliente actualizado
const char* client_id = "SensorPM25_PPD42_Simulado";
const int LED_PIN = 2;              // Pin del LED de alarma

// --- ⚠️ CAMBIO 3: Configuración de la SIMULACIÓN (basada en µs de pulso) ---
// (Lógica del PPD42: valor ALTO = PELIGRO / más polvo)
const long DANGER_THRESHOLD = 150000; // Umbral de peligro (150,000 µs)
const int ANOMALY_INTERVAL = 10;      // Generar anomalía cada 10 lecturas
const long NORMAL_MIN = 10000;        // Duración de pulso normal (aire limpio)
const long NORMAL_MAX = 50000;        // Duración de pulso normal (aire limpio)
const long ANOMALY_MIN = 200000;      // Duración de pulso en anomalía (polvo)
const long ANOMALY_MAX = 400000;      // Duración de pulso en anomalía (polvo)

// --- Variables para temporizador y conteo ---
unsigned long lastPublish = 0;
const long publishInterval = 2000; // Publicar cada 2 segundos
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

  // Inicializar el generador de números aleatorios
  randomSeed(analogRead(0)); 

  Serial.println("\n========================================");
  // ⚠️ CAMBIO 4: Mensajes de inicio actualizados
  Serial.println("💨 SIMULADOR de Sensor de Polvo PM2.5 (PPD42)");
  Serial.println("========================================");

  // Conectar WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✓ Conectado al WiFi");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // Configurar MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setBufferSize(128); // Aumentado para JSON
  client.setKeepAlive(60);

  Serial.println("========================================\n");
}

void loop() {
  // 1. Mantener conexión MQTT
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop(); 

  // 2. Lógica de publicación (sin delay)
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastPublish >= publishInterval) {
    lastPublish = currentMillis; // Reinicia el temporizador

    // --- ⚠️ CAMBIO 5: Lógica de simulación para PM2.5 ---
    reading_count++;
    
    // Usamos 'long' porque los microsegundos son números grandes
    long pulse_duration; 
    bool isAnomaly = (reading_count % ANOMALY_INTERVAL == 0);

    if (isAnomaly) {
      // Generar un valor de ANOMALÍA (peligro, pulso largo)
      pulse_duration = random(ANOMALY_MIN, ANOMALY_MAX + 1); 
      Serial.println("🔥 ALERTA: Anomalía de polvo simulada!");
    } else {
      // Generar un valor NORMAL (seguro, pulso corto)
      pulse_duration = random(NORMAL_MIN, NORMAL_MAX + 1);
    }
    // --- Fin del cambio 5 ---

    Serial.print("Simulated Pulse Duration (µs): ");
    Serial.print(pulse_duration);
    
    // Determinar estado y controlar LED
    const char* status;
    if (pulse_duration >= DANGER_THRESHOLD) {
      digitalWrite(LED_PIN, HIGH);
      Serial.println(" - Danger! High Dust Level!");
      status = "DANGER";
    } else {
      digitalWrite(LED_PIN, LOW);
      Serial.println(" - Environment safe");
      status = "SAFE";
    }

    // --- ⚠️ CAMBIO 6: Crear y enviar JSON para PM2.5 ---
    char json_buffer[128];
    // Usamos %ld para imprimir variables de tipo 'long'
    sprintf(json_buffer, "{\"pm_valor\":%ld,\"status\":\"%s\"}", pulse_duration, status);

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

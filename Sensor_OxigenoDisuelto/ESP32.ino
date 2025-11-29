#include <WiFi.h>
#include <PubSubClient.h>

// --- CONFIGURACIÓN WIFI ---
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// --- CONFIGURACIÓN FLESPI MQTT ---
const char* mqtt_server = "mqtt.flespi.io"; 
const int mqtt_port = 1883;
const char* mqtt_username = "QwWWJaPQ5ptFVTdPpQ3b17e8jIPY7Kv9H7bfCRKiFcNW1ZAqaeC3u0SQhgMODpYs";
const char* mqtt_topic = "iotzi/escuela/sensor/do";

// --- CONFIGURACIÓN DEL SENSOR ---
const char* client_id = "Sensor_Oxygen_01";

// Rangos de Oxígeno Disuelto (mg/L)
const float O2_CRITICAL_LOW = 2.0;   // Crítico: condiciones anaeróbicas
const float O2_OPTIMAL_MIN = 5.0;    // Mínimo aceptable para cultivos y agua tipo II
const float O2_OPTIMAL_MAX = 8.0;    // Ideal para soluciones bien oxigenadas
const float O2_SUPERSATURATION = 10.0; // Exceso (posible burbujeo o interferencia)

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n========================================");
  Serial.println("🫧 Sensor de Oxígeno Disuelto (DO)");
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
  client.setBufferSize(128);
  client.setKeepAlive(60);
  
  Serial.println("========================================\n");
}

void loop() {
  // Reconectar MQTT si es necesario
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  // Simular lectura de oxígeno disuelto (rango: 1.0 a 11.0 mg/L)
  float oxygenValue = (random(10, 110)) / 10.0;

  // Clasificar nivel de oxígeno
  const char* status;
  if (oxygenValue < O2_CRITICAL_LOW) {
    status = "CRITICAL_LOW";
    Serial.println("⚠️ Oxígeno críticamente bajo — riesgo anaeróbico");
  } else if (oxygenValue < O2_OPTIMAL_MIN) {
    status = "LOW";
    Serial.println("⚡ Oxígeno bajo — requiere aireación");
  } else if (oxygenValue <= O2_OPTIMAL_MAX) {
    status = "OPTIMAL";
    Serial.println("✓ Nivel óptimo de oxígeno disuelto");
  } else if (oxygenValue < O2_SUPERSATURATION) {
    status = "HIGH";
    Serial.println("📈 Oxígeno ligeramente alto — posible sobreaireación");
  } else {
    status = "SUPERSATURATION";
    Serial.println("⚠️ Supersaturación detectada — revisar sistema de burbujeo");
  }

  // Mostrar valor
  Serial.print("Oxígeno disuelto: ");
  Serial.print(oxygenValue, 1);
  Serial.println(" mg/L");

  // Crear y enviar JSON a MQTT
  char json_buffer[150];
  sprintf(json_buffer, "{\"oxygen_mg_L\":%.1f,\"status\":\"%s\"}", oxygenValue, status);
  
  if (client.publish(mqtt_topic, json_buffer)) {
    Serial.print("📤 Enviado: ");
    Serial.println(json_buffer);
  } else {
    Serial.println("✗ Error MQTT");
  }
  
  Serial.println();
  delay(5000); // Leer cada 5 segundos
}

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

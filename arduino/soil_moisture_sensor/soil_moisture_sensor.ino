#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

// Entity-wide constants
const char* WIFI_SSID = "...";
const char* WIFI_PASSWORD = "...";
const char* HOME_ASSISTANT_SENSOR_ID = "...";
const char* HOME_ASSISTANT_DOMAIN = "...";
const char* HOME_ASSISTANT_PASSWORD = "...";

// Script-wide constants
const int MAXIMUM_VALUE = 1024;

void setup() {
  Serial.begin(9600);
  Serial.println("Initializing sensor");
  pinMode(BUILTIN_LED, OUTPUT);
  digitalWrite(BUILTIN_LED, HIGH);

  connectToWiFi();
}

void loop() {
  delay(5000);
  digitalWrite(BUILTIN_LED, LOW);

  int sensorValue = MAXIMUM_VALUE - analogRead(A0);
  output(sensorValue);
  sendValueToHomeAssistant(sensorValue);

  digitalWrite(BUILTIN_LED, HIGH);
}

void connectToWiFi() {
  Serial.print("Connecting to Wi-Fi");
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Wi-Fi connected successfully");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Signal strength: ");
  Serial.print(WiFi.RSSI());
  Serial.println(" dBm");
}

void output(int sensorValue) {
  Serial.print("Value: ");
  Serial.print(sensorValue);
  Serial.print("/");
  Serial.println(MAXIMUM_VALUE);
}

void sendValueToHomeAssistant(int sensorValue) {
  WiFiClientSecure client;
  if (!client.connect(HOME_ASSISTANT_DOMAIN, 443)) {
    Serial.print("Could not connect to https://");
    Serial.println(HOME_ASSISTANT_DOMAIN);
    return;
  }

  String body = String("{\"state\":") + sensorValue + "}";

  client.print("POST /api/states/sensor.");
  client.print(HOME_ASSISTANT_SENSOR_ID);
  client.println(" HTTP/1.1");
  client.print("Host: ");
  client.println(HOME_ASSISTANT_DOMAIN);
  client.print("X-HA-Access: ");
  client.println(HOME_ASSISTANT_PASSWORD);
  client.println("Content-Type: application/json");
  client.print("Content-Length: ");
  client.println(body.length());
  client.println();
  client.println(body);

  // Read the first line, to enforce that data is sent
  String line = client.readStringUntil('\n');
  Serial.print("Value sent to Home Assistant, HTTP response: ");
  Serial.println(line);
}


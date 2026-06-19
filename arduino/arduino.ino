#include <ArduinoJson.h>

// 신호등 LED 모듈(4핀): 빨강(R)=13 사용. 노랑(Y)=12·초록(G)=11은 배선만(미사용).
const int ledPin = 13;
const int trigPin = 2;
const int echoPin = 3;

unsigned long lastSentTime = 0;
const int interval = 200;


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(50);

  pinMode(ledPin, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

}

void loop() {
  if (Serial.available() > 0) {
    JsonDocument doc;

    DeserializationError error = deserializeJson(doc, Serial);

    if (!error) {
      if (doc.containsKey("type")) {
        String type = doc["type"];

        if (type == "led") {
          if (doc.containsKey("status")) {
            String status = doc["status"];

            if (status == "on") {
              digitalWrite(ledPin, HIGH);
            }
            else if (status == "off") {
              digitalWrite(ledPin, LOW);
            }
          }
        }
      }
    }
  }

  unsigned long currentTime = millis();
  if (currentTime - lastSentTime >= interval) {

    int distance = calculateDistance();

    JsonDocument doc;

    doc["type"] = "sonar";
    doc["distance"] = distance;

    serializeJson(doc, Serial);
    Serial.println();

    lastSentTime = currentTime;
  }
}

int calculateDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  int distance = duration * 0.034 / 2;

  return distance;
}
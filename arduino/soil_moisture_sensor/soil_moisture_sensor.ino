int MAXIMUM_VALUE = 1024;

void setup() {
  Serial.begin(9600);
  Serial.println("Initializing sensor");
  pinMode(BUILTIN_LED, OUTPUT);
}

void loop() {
  int sensorValue = MAXIMUM_VALUE - analogRead(A0);
  output(sensorValue);
  delay(1000);
  digitalWrite(BUILTIN_LED, HIGH);
  delay(1000);
  digitalWrite(BUILTIN_LED, LOW);
}

void output(int sensorValue) {
  String output = "Value is ";
  output = output + sensorValue;
  output = output + " / ";
  output = output + MAXIMUM_VALUE;
  Serial.println(output);
}


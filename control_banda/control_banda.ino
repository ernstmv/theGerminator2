#define band 10
#define led 13

void setup() {
  Serial.begin(9600);
  pinMode(band,OUTPUT);
  pinMode(led, OUTPUT); 
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    if (command == 'r') {
      digitalWrite(band, HIGH);
      digitalWrite(led, LOW);
    } else if (command = 's'){
      digitalWrite(band, LOW);
      digitalWrite(led, HIGH);
    }
  }
}

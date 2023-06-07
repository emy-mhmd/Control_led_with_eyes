#include <Arduino.h>
define ledLeft 8
define ledRight 4
define ledMid 7
byte byteRead;
char x;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ledLeft, OUTPUT);
  pinMode(ledRight, OUTPUT);
  pinMode(ledMid, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    char signal = Serial.read();
    if (signal == '1') {
      digitalWrite(ledRight, HIGH);  
      digitalWrite(ledLeft, LOW);   
      digitalWrite(ledMid, LOW);   
    } else if (signal == '2') {
      digitalWrite(ledRight, LOW);
      digitalWrite(ledLeft, HIGH);  
      digitalWrite(ledMid, LOW);   
    } else if (signal == '3') {
      digitalWrite(ledRight, LOW);   
      digitalWrite(ledLeft, LOW);  
      digitalWrite(ledMid, HIGH);  
    }
  }
}
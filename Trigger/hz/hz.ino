void setup()
{
  //DDRD = B11111111; // set PORTD (digital 7~0) to outputs
  
  
  
  //DDRD = B00011111; // set digital pins 5-7 as INPUT and digital pins 0-4 in as OUTPUT

  DDRD &= ~bit(DDD5);                       // set digital pin 5 as INPUT
  DDRD |= bit(DDD4);                        // set digital pin 4 as OUTPUT
  PORTD &= ~bit(PORTD4);                    // set digital pin 4 as LOW
}

void loop()
{
  //PORTD = B11110000; // digital 4~7 HIGH, digital 3~0 LOW
  //delay(1);
  //PORTD = B00001111; // digital 4~7 LOW, digital 3~0 HIGH
  //delay(1);

  bitRead(PIND, PIND5);              // read state of digital pin 2 (0 = LOW, 1 = HIGH)
  PORTD ^= bit(PORTD5);              // toggle state of digital pin 5
}

const int inPin = 5;
const int outPin =  4;  

const int fpsDivider = 2;

int lastInState = LOW;

//int inState = LOW;
int counter = 2;

unsigned long previousHigh = 0;


// Variables will change:
int outState = HIGH;         // the current state of the output pin
int inState;   
int lastReading = LOW;   // the previous reading from the input pin

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 1;    // the debounce time; increase if the output flickers


void setup() {
  // put your setup code here, to run once:
  //Serial.begin(9600);

  pinMode(outPin, OUTPUT);
  pinMode(inPin, INPUT);
  digitalWrite(outPin, LOW);
}

void loop() {
  int inState = digitalRead(inPin);

  /*
  if (inState == HIGH && lastInState == LOW) {
    //if (counter == 0) {
    digitalWrite(outPin, HIGH);
      //counter = fpsDivider;
    //}
    //previousHigh = millis();
    lastInState == inState;
    counter--;
  }
  if (inState == LOW && lastInState == HIGH) {
    digitalWrite(outPin, LOW);
    lastInState == inState;
  }
  */

  
  //Serial.println(counter);
  if (inState == HIGH) {
    if (inState != lastInState) {
      if (counter >= 2) {
        digitalWrite(outPin, HIGH);         
        counter = 0;    
      }
      counter = counter+1;
    }
    lastInState == HIGH; 
  }
  
  if(inState == LOW) {
    digitalWrite(outPin, LOW);
    lastInState == LOW;
  }
  

  //if (previousHigh > millis() + 1000) {
  //  counter = 0;
  //}


/*
  // read the state of the switch into a local variable:
  int reading = digitalRead(inPin);

  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (reading != lastReading) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != inState) {
      inState = reading;

      // only toggle the LED if the new button state is HIGH
      if (inState == HIGH) {
        outState = !outState;
      }
    }
  }

  // set the LED:
  digitalWrite(outPin, outState);

  // save the reading. Next time through the loop, it'll be the lastButtonState:
  lastReading = reading;
*/
}

#include <Adafruit_NeoPixel.h>

#define LEDPIN         2
#define NUMPIXELS      2

// Trigger pins (left to right)
const int camOut = 3;
const int optOut = 4;
const int gateIn = 5;
const int modeIn = 6; // button

// Timing
int FPS = 80;   // Opti fps
int divider = 4; // Divider for cam fps (=25)
unsigned long interval = 1000 / FPS;
unsigned long periodTime = interval / 2;
int iter = 0;

// For timing triggers
unsigned long currentTime;
unsigned long previousTime;

// For checking IOs
bool mode; // record/create
bool gate; // recoding gate up/down
bool lastModeState;
bool lastGateState;
unsigned long lastModeTime = 0;
unsigned long lastGateTime = 0;
unsigned long debounceDelay = 50;

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, LEDPIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pinMode(camOut, OUTPUT);
  pinMode(optOut, OUTPUT);
  pinMode(modeIn, INPUT); // Switch record/create
  pinMode(gateIn, INPUT); // Recording gate
 
  mode = digitalRead(modeIn);
  lastModeState = mode;
  gate = digitalRead(gateIn);
  lastGateState = gate;
  
  pixels.begin(); // This initializes the NeoPixel library.

  //Serial.begin(115200);
  
  currentTime = millis();
  previousTime = currentTime;
}

void loop() {

  // Get updates from IO ports 
  updateIOs();
  
  // Time to trigger? ...
  currentTime = millis();
  if (currentTime - previousTime >= interval) 
  {
    previousTime = currentTime;
    //Serial.print( currentTime );
        
    // We are recording... Trigger everything
    if (mode) 
    {
      // Only if recording gate is open
      if (gate || iter != 0)
      {
        // Trigger OptiTrack
        //Serial.print( "  Opti" );
        digitalWrite(optOut, HIGH); 

        // Trigger cameras if it's time to
        if (iter % divider == 0)
        {
          //Serial.print( "  Cam" );
          digitalWrite(camOut, HIGH); 
          iter = 0;
        }
        iter++;
      }
    }
    
    // We are creating... Trigger OptiTracks
    else
    {
      // Trigger OptiTrack
      //Serial.print( "  Opti" );
      digitalWrite(optOut, HIGH); 
    }

    // Keep it up for a moment
    //Serial.println();
    while (millis() - previousTime <= periodTime) {}
    digitalWrite(optOut, LOW); 
    digitalWrite(camOut, LOW);
  }
}




// Use debounce time to determine if inputs have changed
void updateIOs() 
{
  int modeReading = digitalRead(modeIn);
  int gateReading = digitalRead(gateIn);

  // If the switch changed, due to noise or pressing:
  if (modeReading != lastModeState) {
    // reset the debouncing timer
    lastModeTime = millis();
  }
  if (gateReading != lastGateState) {
    // reset the debouncing timer
    lastGateTime = millis();
  }

  lastModeState = modeReading;
  lastGateState = gateReading;

  if ((millis() - lastModeTime) > debounceDelay) {
    if (modeReading != mode) {
      mode = modeReading;
    }
  }
  if ((millis() - lastGateTime) > debounceDelay) {
    if (gateReading != gate) {
      gate = gateReading;
    }
  }
  
  //mode = true;
  //gate = true;

  // Update leds accordingly
  if (mode && gate) 
  {
    // RED Recording
    pixels.setPixelColor(0, pixels.Color(255,0,0));
    pixels.setPixelColor(1, pixels.Color(255,0,0));
  }
  else if(mode)
  {
    // BLUE Ready to record
    pixels.setPixelColor(0, pixels.Color(0,0,255));
    pixels.setPixelColor(1, pixels.Color(0,0,255));
  }
  else
  {
    // GREEN Creating
    pixels.setPixelColor(0, pixels.Color(0,255,0));
    pixels.setPixelColor(1, pixels.Color(0,255,0));
  }
  pixels.show();
}

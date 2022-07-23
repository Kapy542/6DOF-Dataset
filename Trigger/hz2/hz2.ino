/*
void setup() {
  // put your setup code here, to run once:
  //DDRD = 0b11011111; //Pin 5 of PORTD is an input, all others are outputs
  //DDRB = 0b00000000; //All are outputs
  
  DDRD &= ~(1<<PD5);    //Configure PORTD pin 5 as an input
  PORTD |= (1<<PD5);    //Activate pull-ups in PORTD pin 5
  DDRB |= (1<<PB5);    //Configure PORTB pin 5 an output, this is the digital 13 in the Arduino that as the built-in led

}

void loop() {
  // put your main code here, to run repeatedly: 
  //char my_var = 0;        //Create a variable to store the data read from PORTD
  //my_var = (PIND & (1<<PD1));    //Read the PORTD pin 1 value and put it in the variable
  
  if(PIND & (1<<PD5)) {
    //PORTD ^=(1<<PD4); // Toggle pin 4
    PORTB ^=(1<<PB5); // Toggle pin 13 (led)
  } 
}

*/

void setup(void){
  
  DDRD &= ~(1<<PD2);    //Configure PORTD pin 2 as an input
  //PORTD |= (1<<PD2);    //Activate pull-ups in PORTD pin 2
  DDRB |= (1<<PB5);     //Configure PORTB pin 5 an output, this is the digital 13 in the Arduino that as the built-in led
  int prev_state;
  int counter = 0;
  
  while(1){                //Infinite loop (returning back to the start of void loop takes time...)
    int state = (PIND & (1<<PD2));
    if(state and counter == 0){        //Verify the button state
      //PORTB = (1<<PB5);
      PORTB ^=(1<<PB5);    //This is the above mentioned XOR that toggles the led
      counter = 1; // HOXHOXHOX
    }
    else if (state){
      counter--;
    }
    //else {
    //  PORTB = (0<<PB5);
    //}
    _delay_ms(250);            //Delay between consecutive button presses
  }
}
   
uint8_t readButton(void){
  if((PIND & (1<<PD2)) == 0){        //If the button was pressed
  _delay_ms(25); }        //Debounce the read value
  if((PIND & (1<<PD2)) == 0){        //Verify that the value is the same that what was read
    return 1; }            //If it is still 0 its because we had a button press
  else{                    //If the value is different the press is invalid
    return 0; }
}

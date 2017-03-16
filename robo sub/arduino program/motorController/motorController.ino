//read serial data packet from raspberry pi, and apply to motor controller - grant carr 2017

// define pin name

#define pwm_1 3
#define dir_1 2
#define pwm_2 5
#define dir_2 4

#define pwm_3 7
#define dir_3 6
#define pwm_4 9
#define dir_4 8

#define pwm_5 11
#define dir_5 10
#define pwm_6 13
#define dir_6 12

#define vertical_1 1
#define vertical_2 4
#define hori_1 3
#define hori_2 6
#define thrust_1 2
#define thrust_2 5

//int variables
int incomingByte = 0;   // for incoming serial data
int state = 0;
int motorNumber = 0;
int rawInput1 = 0;
int rawInput2 = 0;
int rawInput3 = 0;
int motorPower = 0;

int motor_id_arr[] = {0, 1, 2, 3, 4, 5, 6};
int motor_pwm_pins[] = {0, 3, 5, 7, 9, 11, 13};
int maotor_dir_pin[] = {0, 2, 4, 6, 8, 10, 12};

void setup() {
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  pinMode(pwm_1, OUTPUT);
  pinMode(dir_1, OUTPUT);
  pinMode(pwm_2, OUTPUT);
  pinMode(dir_2, OUTPUT);

  pinMode(pwm_3, OUTPUT);
  pinMode(dir_3, OUTPUT);
  pinMode(pwm_4, OUTPUT);
  pinMode(dir_4, OUTPUT);

  pinMode(pwm_5, OUTPUT);
  pinMode(dir_5, OUTPUT);
  pinMode(pwm_6, OUTPUT);
  pinMode(dir_6, OUTPUT);
}

void loop() {

  readSerialPacket();
  stateMachine();
  delay(2);
    
}

void setMotor(int motor, int value)//motor number 1-6 and value 0-255
{
  digitalWrite(motor_pwm_pins[motor], HIGH);
  analogWrite(maotor_dir_pin[motor], value);
}


//function to read byte from USB serial line
void readSerialPacket()
{
  //receive data:
  if (Serial.available() > 0) 
  {
    // read the incoming byte:
    incomingByte = Serial.read();
  
    // say what you got:
    Serial.println(incomingByte, DEC);
  
  }
}

//state machine for motor control packet format = M#value!= m1127! = m 'motor' 1 'number' 127'value' ! 'end of command'
void stateMachine()
{
  
 if(state==0)//check for 77 'M' or 109 'm' change state to one, default state
 {
   
      //clear input storage variables for next packet
      rawInput1 = 0;
      rawInput2 = 0;
      rawInput3 = 0;
      
     if(incomingByte==77 || incomingByte==109 ){
       
        state = 1;
     }           
     
  }else if (state==1){  //check for motor number, expected char 1, 2, 3, 4, 5, 6 as dec 49, 50, 51, 52, 53, 54
     
    
    if(incomingByte > 48 && incomingByte < 55)
    {
      //convert char incomingByte to ascii value
      motorNumber = incomingByte - 48;
  
      state = 2;
    }else{
      
     //bad data will reset to initial state 0
     state = 0; 
    }
      
  }else if (state==2){
    
    if(incomingByte > 47 && incomingByte < 58)                    //read input 1
    {
      rawInput1 = incomingByte - 48;
      state = 3;
    }else{
      
     //bad data will reset to initial state 0
     state = 0; 
    }
    
  }else if (state==3){
    
    if(incomingByte == 33){ //check for end of packet 33 '!'
      //single digit input from packet
      state = 6;
      
    }else if(incomingByte > 47 && incomingByte < 58){              //read input 2
      
      rawInput2 = incomingByte - 48;
      state = 4;
    }else{
      
     //bad data will reset to initial state 0
     state = 0; 
    }
    
  }else if (state==4){
    
     if(incomingByte == 33){ //check for end of packet 33 '!'
      //double digit input from packet
      state = 7;
      
    }else if(incomingByte > 47 && incomingByte < 58){             //read input 3
      
      rawInput3 = incomingByte - 48;
      state = 5;
      
    }else{
      
     //bad data will reset to initial state 0
     state = 0; 
    }
    
    
  }else if (state==5){
      
     if(incomingByte == 33){ //check for end of packet 33 '!'
      //single digit input from packet
      state = 8;
      
    }else{
      
     //bad data will reset to initial state 0
     state = 0;  
    }
    
    
  }else if (state==6){//input state for single digit motor power 0-9
    
    motorPower = rawInput1;
    
    state = 9;
  }else if (state==7){//input state for double digit motor power 10-99
    
    //convert single digits to double digit number
    rawInput1 = rawInput1 * 10;
    motorPower = rawInput1 + rawInput2;
    state = 9;
  }else if (state==8){//input state for triple digit motor power 100-255
    
    //convert single digits to triple digit number
    rawInput1 = rawInput1 * 100;
    rawInput2 = rawInput2 * 10;
    rawInput1 = rawInput1 + rawInput2;
    motorPower = rawInput1 + rawInput3;
    state = 9;
    
  }else if(state==9){
 
    //call function to set motor speed setMotor(int motorNumber, int motorSpeed);

    //display parsed data
    Serial.print("\nMotor: ");
    Serial.print(motorNumber);
    Serial.print("\tValue: ");
    Serial.print(motorPower);
    setMotor(motorNumber,motorPower);
    state = 0;
  } 
}

//author: mayur talole
//two motors with changed configuration ofpins



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


int motor_id_arr[] = {0, 1, 2, 3, 4, 5, 6};
int motor_pwm_pins[] = {0, 3, 5, 7, 9, 11, 13};
int maotor_dir_pin[] = {0, 2, 4, 6, 8, 10, 12};


void setup() {

  delay(500);
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
  
  Serial.begin(9600);

}

void loop() {

 
int z = 6;
 
 
 motor_fwd(40,vertical_1);
 motor_fwd(40, vertical_2);
 motor_fwd(40,hori_1);
 motor_fwd(25, thrust_1);
  motor_fwd(25, thrust_2);
  delay(9000);
motor_break(vertical_1);
motor_break(vertical_2);

delay(5000);


    

}


//random functions
void motor_fwd(int x, int motor_id) {
  int y;

  
  digitalWrite(motor_pwm_pins[motor_id], HIGH);
   Serial.println(motor_id_arr[motor_id]);
   y = map(x, 0, 100, 125, 0);
    analogWrite(maotor_dir_pin[motor_id], y);
    Serial.print(y);
  

}

void motor_rev(int x, int motor_id) {
  int y;

  digitalWrite(motor_pwm_pins[motor_id], HIGH);
   Serial.println(motor_id_arr[motor_id]);
   y = map(x, 0, 100, 130, 255);
    analogWrite(maotor_dir_pin[motor_id], y);
    Serial.print(y);

    

}

void motor_break(int motor_id) {
 
   digitalWrite(motor_pwm_pins[motor_id], LOW);
   analogWrite(maotor_dir_pin[motor_id], 128);
    Serial.println("break");
    
  
 

}




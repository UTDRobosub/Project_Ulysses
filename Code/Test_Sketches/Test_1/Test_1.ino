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

#define lateral_1 5
#define lateral_2 1

#define vertical_1 3
#define vertical_2 4

#define thruster_1 2
#define thruster_2 6


int motor_id_arr[] = {0, 1, 2, 3, 4, 5, 6};
int motor_pwm_pins[] = {0, 3, 5, 7, 9, 11, 13};
int motor_dir_pins[] = {0, 2, 4, 6, 8, 10, 12};


void setup() {
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
  runMotor(100, vertical_1, 0);
  runMotor(100, vertical_2, 1);
  delay(5000);
  runMotor(100, thruster_1, 1);
  runMotor(100, thruster_2, 1);
  delay(5000);
  runMotor(0, thruster_1, 1);
  runMotor(0, thruster_2, 0);
  delay(5000);
  runMotor(100, thruster_1, 0);
  runMotor(100, thruster_2, 1);
  delay(5000);
  runMotor(0, thruster_1, 1);
  runMotor(0, thruster_2, 0);
  delay(5000);
//  runMotor(100,lateral_1, 1);
//  runMotor(100,lateral_2, 0);
//  delay(5000);
//  runMotor(100,lateral_1, 1);
//  runMotor(100,lateral_2, 1);
//  delay(5000);
//  runMotor(100,lateral_1, 0);
//  runMotor(100,lateral_2, 0);
//  delay(5000);  
}


//random functions
void runMotor(int x, int motor_id, int dir) {
  int y;
  digitalWrite(motor_pwm_pins[motor_id], dir);
  Serial.println(motor_id_arr[motor_id]);
  y = map(x, 100, 0, 255, 0);
  analogWrite(motor_dir_pins[motor_id], y);
  Serial.print(y);
}

//void motor_break(int motor_id) {
// 
//   digitalWrite(motor_dir_pins[motor_id], LOW);
//   analogWrite(motor_pwm_pins[motor_id], 128);
//    Serial.println("break");
//}




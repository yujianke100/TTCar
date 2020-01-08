#define SPEED  250
#define STEP 50 
#define LATTICE_NUM 1
#define TURNSTEP 1700
int flag = 0;
int i = 0;
int head0,head1,tail0,tail1; //0对nano板4口，1对5口。左转时，0高1低，直线置高
int headD1,head,tailD1,tail;  //分别对应两端上的一号传感器

int directionSet = 1;   //前进方向,1为前，-1为后
int digitalSet = 10;    //转弯时监测的传感器，10为前D4,11为后D4
int signalPin = 12;     //前进时数格子的传感器，12为前D1,13为后D1

int tmp = 0;

int speedplus = 0;

int diffirent_time = 0;

int impulse_time = 0;

void setup()
{
   Serial.begin(9600);
   pinMode(2,OUTPUT);
   pinMode(3,OUTPUT);
   pinMode(4,OUTPUT); //左脉冲
   pinMode(5,OUTPUT); //右脉冲
   pinMode(6,INPUT);  //前传感器信号1
   pinMode(7,INPUT);  //前传感器信号2
   pinMode(8,INPUT);  //后传感器信号1
   pinMode(9,INPUT);  //后传感器信号2
   pinMode(10,INPUT); //前D4传感器
   pinMode(11,INPUT); //后D4传感器
   pinMode(12,INPUT); //前D1传感器
   pinMode(13,INPUT); //后D1传感器
   flag = digitalRead(signalPin);
}

 void line_Read()
 {
   head0 = digitalRead(6);
   head1 = digitalRead(7);
   tail0 = digitalRead(8);
   tail1 = digitalRead(9);
   head = digitalRead(10);
   tail = digitalRead(11);
//   headD1 = digitalRead(12);
//   tailD1 = digitalRead(13);
 }

void impulse(int mode, int flag, int pin1, int pin2){
    if(mode == 0){
      digitalWrite(pin1, HIGH);
      digitalWrite(pin2, HIGH);
      delayMicroseconds(10);  
      digitalWrite(pin1, LOW); 
      digitalWrite(pin2, LOW);
      delayMicroseconds(SPEED + speedplus);
      }
     else if(mode == 1){
      digitalWrite(pin1, HIGH);
      if(flag)
        digitalWrite(pin2, HIGH);
      delayMicroseconds(10);  
      digitalWrite(pin1, LOW);
      if(flag) 
        digitalWrite(pin2, LOW);
      delayMicroseconds(SPEED + speedplus);
      }
      else{
      digitalWrite(pin1, HIGH);
      digitalWrite(pin2, HIGH);
      delayMicroseconds(10);  
      digitalWrite(pin1, LOW); 
      digitalWrite(pin2, LOW);
      delayMicroseconds(SPEED + SPEED);
      }
}
//void impulse(int mode, int pin1, int pin2){
//  if(mode == 0){
//    digitalWrite(pin1, HIGH);
//    digitalWrite(pin2, HIGH);
//    delayMicroseconds(10);  
//    digitalWrite(pin1, LOW); 
//    digitalWrite(pin2, LOW);
//    delayMicroseconds(SPEED + speedplus);
//  }
//  else {
//    digitalWrite(pin1, HIGH);
//    if(impulse_time % 2 == 0)
//      digitalWrite(pin2, HIGH);
//    delayMicroseconds(10);  
//    digitalWrite(pin1, LOW); 
//    if(impulse_time % 2 == 0)
//      digitalWrite(pin2, LOW);
//    delayMicroseconds(SPEED + speedplus);
//    if(impulse_time >= 2)
//      impulse_time = 1;
//    else
//      impulse_time ++;
//  }
//  }
  
//void motor(int left_speed, int right_speed){
//    if(left_speed == right_speed){
//        impulse(0, 4, 5);
//      }
//    else if(left_speed > right_speed){
//        impulse(-1, 4, 5);
//      }
//    else {
//        impulse(1, 5, 4);
//      }
//    
//}   

void motor(int t, int l, int r){
  impulse_time ++;
  if(impulse_time >= 101)
    impulse_time = 1;
  if(t == 1 && l == 1 && r == 1){
      impulse(0,0,4,5);
    }
  else if(t == 1 && l == 1 && r == 0){
    if(impulse_time % 3 != 0 || impulse_time % 30 == 0 )
      impulse(1,1,5,4);
    else
      impulse(1,0,5,4);
    }
  else if(t == 1 && l == 0 && r == 1){
    if(impulse_time % 3 != 0 || impulse_time % 30 == 0 )
      impulse(1,1,4,5);
    else
      impulse(1,0,4,5);
    }
  else if(t ==1  && l == 0 && r == 0){
    if(impulse_time % 2 != 0 || impulse_time %10 == 0)
      impulse(1,1,5,4);
    else
      impulse(1,0,5,4);
    }
  else if(t == 0 && l == 1 && r == 1){
    if(impulse_time % 2 != 0 || impulse_time %10 == 0)
      impulse(1,1,4,5);
    else
      impulse(1,0,4,5);
    }
  else if(t == 0 && l == 1 && r == 0){
    if(impulse_time % 5 == 0)
      impulse(1,1,5,4);
    else
      impulse(1,0,5,4);
    }
  else if(t == 0 && l == 0 && r == 1){
    if(impulse_time % 5 == 0)
      impulse(1,1,4,5);
    else
      impulse(1,0,4,5);
    }
  else{
      impulse(-1,0,4,5);
    }
}

void track_zhixian(int Direction)
{
  line_Read();
  if(Direction == 1){
        digitalWrite(2, HIGH);
        digitalWrite(3, LOW);
        motor(head,head1,head0);
    }

  else if(Direction == -1){
        digitalWrite(3, HIGH);
        digitalWrite(2, LOW);
        motor(tail,tail0,tail1);
    }

}
void left(int Digital)
{
  digitalWrite(2, HIGH);
  digitalWrite(3, HIGH);
  for(int tmp = 0;tmp < TURNSTEP; tmp ++)
        impulse(0,0,4,5);
  i = 0;
}
void right(int Digital)
{
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  for(int tmp = 0;tmp < TURNSTEP; tmp ++)
        impulse(0,0,4, 5);
  i = 0;
}
//void left(int Digital)
//{
//  digitalWrite(2, HIGH);
//  digitalWrite(3, HIGH);
//  int flag = digitalRead(Digital);
//  int k = 0;
//  while(1){
//        impulse(4,5);
//        if(flag != digitalRead(Digital)){
//          k ++;
//          flag = digitalRead(Digital);
//        }
//        if(k == 2)
//          break;
//    }
//}
//
//
//void right(int Digital)
//{
//  digitalWrite(2, LOW);
//  digitalWrite(3, LOW);
//  int flag = digitalRead(Digital);
//  int k = 0;
//  while(1){
//        impulse(4,5);
//        if(flag != digitalRead(Digital)){
//          k ++;
//          flag = digitalRead(Digital);
//        }
//        if(k == 2)
//          break;
//    }
//}

int var = 0;

void loop()
{
   if(Serial.available()>0)
        var = Serial.read();
    if(var == 104){         //小写h，进入前进模式
        directionSet = 1;   //前进方向,1为前，-1为后
        digitalSet = 10;    //转弯时监测的传感器，10为前D4,11为后D4
        signalPin = 12;    //前进时数格子的传感器，12为前D1,13为后D1
        var = 0;
      }
    else if(var == 116){    //小写t，进入后退模式
        directionSet = -1;  //前进方向,1为前，-1为后
        digitalSet = 11;    //转弯时监测的传感器，10为前D4,11为后D4
        signalPin = 13;    //前进时数格子的传感器，12为前D1,13为后D1
        var = 0;
      }
    else if(var == 48){    //输入0 前进，后方数格子
        speedplus = 0;
        tmp = signalPin;
        signalPin = 13;
        if(i < (LATTICE_NUM * 1) ){
          track_zhixian(directionSet);
          delay(1);
        }
            
        else{
          for(int tmp = 0;tmp < 100; tmp++){
            track_zhixian(directionSet);
            delay(1);
          }
          i = 0;
          var = 0;
          signalPin = tmp;
          Serial.write(1);
        }
    }
    else if(var == 108){ //输入l little
      //speedplus = 100;
      speedplus = 0;
      for(int tmp = 0;tmp < 175; tmp++){
            track_zhixian(directionSet);
            delay(1);
          }
        i = 0; 
        var = 0;
        speedplus = 0;
        Serial.write(1);
    }
    else if(var == 102){ //输入f fast
      speedplus = -150;
      if(i < (LATTICE_NUM * 2) ){
          track_zhixian(directionSet);
        }
        else{
          i = 0;
          var = 0;
          Serial.write(1);
        }
    }
    if(var == 49){    //输入1 前进
        speedplus = 0;
        if(i < (LATTICE_NUM * 2) ){
          track_zhixian(directionSet);
        }
        else{
            speedplus = 50;
            for(int tmp = 0;tmp < 750; tmp++){
              track_zhixian(directionSet);
            }
          speedplus = 0;
          i = 0;
          var = 0;
          Serial.write(1);
        }
	  }
   
    else if(var == 50){ //输入2 左转
        speedplus = 0;
    	left(digitalSet); 
        i = 0; 
        var = 0;
        Serial.write(1);
    }

    else if(var == 51){ //输入3 右转
        speedplus = 0;
        right(digitalSet); 
        i = 0; 
        var = 0;
        Serial.write(1);
    }
    
    else if(var == 52){ //输入4 半格
      //speedplus = 100;
      speedplus = 0;
      for(int tmp = 0;tmp < 800; tmp++){
            track_zhixian(directionSet);
            delay(1);
          }
        i = 0; 
        var = 0;
        speedplus = 0;
        Serial.write(1);
    }
    
    if(flag != digitalRead(signalPin)){
          flag = digitalRead(signalPin);
          i++;
          Serial.write(2);
        
    } 
//    Serial.println(digitalRead(12));
//    delay(1000);
//    if(flag == digitalRead(signalPin)){
//      diffirent_time ++;
//      if(diffirent_time > 100)
//        diffirent_time = 100;
//        
//    }
}

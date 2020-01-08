int D1,D2,D3,D4,D5,D6,D7;
void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);
   pinMode(2,OUTPUT);
   pinMode(3,OUTPUT);
   pinMode(4,OUTPUT);
   pinMode(5,OUTPUT);
   pinMode(6,INPUT);
   pinMode(7,INPUT);
   pinMode(8,INPUT);
   pinMode(9,INPUT);
   pinMode(10,INPUT);
   pinMode(11,INPUT);
   pinMode(12,INPUT);
}
 
 void line_Read()
 {
   D1 = digitalRead(6);
   D2 = digitalRead(7);
   D3 = digitalRead(8);
   D4 = digitalRead(9);
   D5 = digitalRead(10);
   D6 = digitalRead(11);
   D7 = digitalRead(12);
 }

void motor(int l, int r){
      if(l == 50 && r == 50){ //5050111
        digitalWrite(2, HIGH);
        digitalWrite(4, HIGH);
        digitalWrite(5, HIGH); 
        }
       else if(l == 50 && r == 35){ //5035110
        digitalWrite(2, HIGH);
        digitalWrite(4, HIGH);
        digitalWrite(5, LOW); 
        }
        else if(l == 35 && r == 50){ //3550101
        digitalWrite(2, HIGH);
        digitalWrite(4, LOW);
        digitalWrite(5, HIGH); 
        }
        else if(l == 50 && r == 30){ //5030100
        digitalWrite(2, HIGH);
        digitalWrite(4, LOW);
        digitalWrite(5, LOW); 
        }
        else if(l == 30 && r == 50){ //3050011
        digitalWrite(2, LOW);
        digitalWrite(4, HIGH);
        digitalWrite(5, HIGH); 
        }
        else if(l == 50 && r == 10){ //5010010
        digitalWrite(2, LOW);
        digitalWrite(4, HIGH);
        digitalWrite(5, LOW); 
        }
        else if(l == 10 && r == 50){ //1050001
        digitalWrite(2, LOW);
        digitalWrite(4, LOW);
        digitalWrite(5, HIGH); 
        }
//    if(left_speed == right_speed){
//        digitalWrite(4, HIGH);
//        digitalWrite(5, HIGH); 
//      }
//    else if(left_speed > right_speed){
//        digitalWrite(4, LOW);
//        digitalWrite(5, HIGH); 
//      }
//    else {
//        digitalWrite(4, HIGH);
//        digitalWrite(5, LOW); 
//      }
    
}   

void track_zhixian() //信号口：2，4，5。
{
  line_Read();
  if(D4 == 0)  
  {
    motor(50,50);//5050->111
  }
  else if((D3 == 0)&&(D4 == 0))   
  {
    motor(35,50);//3550->101
  }
  else if((D4 == 0)&&(D5 == 0))  
  {
    motor(50,35);//->110
  }
  else if((D3 == 0)&&(D4 != 0))
  {
    motor(30,50);//->011
  }
  else if((D4 != 0)&&(D5 == 0))   
  {
    motor(50,30);//->100
  }
  else if((D2 == 0)&&(D3 == 0))     
  {
    motor(10,50);//->001
  }
  else if((D5 == 0)&&(D6 == 0))    
  {
    motor(50,10);//->010
  }
  else if((D2 == 0)&&(D3 != 0))   
  {
    motor(10,50);//->001
  }
  else if((D5 != 0)&&(D6 == 0))  
  {
    motor(50,10);//->010
  }
  else if((D1 == 0)&&(D2 == 0)) 
  {
    motor(10,50);
  }
  else if((D6 == 0)&&(D7 == 0))  
  {
    motor(50,10);
  }
  else if((D1 == 0)&&(D2 != 0))    
  {
    motor(10,50);
  }
  else if((D6 != 0)&&(D7 == 0))  
  {
    motor(50,10);
  }
  else   
  {
    //motor(20,20);//->000
    digitalWrite(2, LOW);
    digitalWrite(4, LOW);
    digitalWrite(5, LOW); 
  }
}




void loop() {
  // put your main code here, to run repeatedly:
  while(1){
    track_zhixian();
    digitalWrite(3,!!(digitalRead(6) + digitalRead(12)));
    }
}

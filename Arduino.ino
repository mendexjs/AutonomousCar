int IN1 = 8; //MOTOR1
int IN2 = 9; //MOTOR1
int IN3 = 10;//MOTOR2
int IN4 = 11;//MOTOR2
void setup() {
 Serial.begin(9600);
 pinMode(IN1, OUTPUT); //INICIALIZANDO
 pinMode(IN2, OUTPUT);
 pinMode(IN3, OUTPUT);
 pinMode(IN4, OUTPUT);
}
void loop() {
 while(Serial.available() >0){
 switch(Serial.read()){
 case 't': //virar a direita
 digitalWrite(IN1, LOW);
 digitalWrite(IN2, HIGH);
 digitalWrite(IN3, HIGH);
 digitalWrite(IN4, LOW);
 delay(450);
 //acelerarC(); //APOS VIRAR CONTINUA ANDANDO EM FRENTE
 break;

 case 'p': // Curva a esquerda
 digitalWrite(IN1, HIGH);
 digitalWrite(IN2, LOW);
 digitalWrite(IN3, LOW);
 digitalWrite(IN4, HIGH);
27
 delay(400);
 //acelerarC(); //APOS VIRAR CONTINUA ANDANDO EM FRENTE
 break;

 case 'h': // PARA ATÉ LER OUTRO COMANDO
 pararC();
 break;
 case 'c':
 acelerarC(); // ANDA SOMENTE EM LINHA RETA - volta a andar se tiver parado com
o hexágono.
 break;
 }
 }
}
void pararC(){ //MÉTODO DE FREAR TOTALMENTE
 digitalWrite(IN1, LOW);
 digitalWrite(IN2, LOW);
 digitalWrite(IN3, LOW);
 digitalWrite(IN4, LOW);
}
void acelerarC(){ //MÉTODO DE ACELERAR - para todos os movimentos em ação, e anda
em frente.
 digitalWrite(IN1, LOW);
 digitalWrite(IN2, LOW);
 digitalWrite(IN3, LOW);
 digitalWrite(IN4, LOW);
 delay(500);
 digitalWrite(IN1, LOW);
 digitalWrite(IN2, HIGH);
 digitalWrite(IN3, LOW);
 digitalWrite(IN4, HIGH);
}

uint8_t mux1[5] = {21, 19, 18, 5, 0};
uint8_t CS1 = 2;//CS1,WR1,EN1 다 mux,demux 엮여있음. Chip Selection
uint8_t CS2 = 22;
uint8_t CS3= 23;
uint8_t WR1 = 15;//WR이 write 무엇무엇일듯... 16핀 : UART 2 RX.
uint8_t EN1 = 4;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  analogReadResolution(12);// 분해능 값을 12 비트로 설정합니다 아날로그 값을 2 ^ 12(2의 12승) 즉 0 ~ 4095까지 측정 가능

  //  pinMode(CS1, OUTPUT);//chip select
  //  digitalWrite(CS1, LOW); //Low 됨, HIGH 안됨
  pinMode(CS1, OUTPUT);
  digitalWrite(CS1, HIGH);
  
  pinMode(CS2, OUTPUT);
  digitalWrite(CS2, HIGH);
  
  pinMode(CS3, OUTPUT);
  digitalWrite(CS3, HIGH);

  pinMode(WR1, OUTPUT);
  digitalWrite(WR1, LOW);

  pinMode(EN1, OUTPUT);
  digitalWrite(EN1, HIGH);//

  for (uint8_t i = 0; i < 5; i++) {
    pinMode(mux1[i], OUTPUT); //출력하겠다!! OUTPUT mode : 전력을 보내니깐 OUTPUT. 값을 읽어올땐 INPUT 으로 전환.
    //pinMode(deMux1[i], OUTPUT); //현재 소스에서 값은 5행에 analogRead(A4)에 A4가 alias로 mcu 32번 핀에서 값 갖고 옴
    digitalWrite(mux1[i], LOW); //아직 대기
    //digitalWrite(deMux1[i], LOW);
  }
  /*
  pD = &data[0]; // pD에 data[0]의 주소값을 참조시킴, 처음이니까 헤더 작성
  *pD = header; // header = 0xA8A8;//43176

  pD = &data[1 + NUM_SENSOR];//헤더 랑 32개 센서 추가하여서 data[33]에 푸터 작성
  *pD = footer;
  */
  
}


void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(EN1, HIGH);
  digitalWrite(CS1, HIGH);
  digitalWrite(mux1[0], 1);
  digitalWrite(mux1[1], 1);
  digitalWrite(mux1[2], 1);
  digitalWrite(mux1[3], 1);
  digitalWrite(mux1[4], 0);
 
  digitalWrite(CS1, LOW);
  digitalWrite(WR1, HIGH);
  delay(1);
  digitalWrite(WR1, LOW);
  delay(1000);

  
  digitalWrite(WR1, HIGH);

  
  digitalWrite(EN1, HIGH);
  digitalWrite(CS1, HIGH);
  digitalWrite(mux1[0], 1);
  digitalWrite(mux1[1], 1);
  digitalWrite(mux1[2], 1);
  digitalWrite(mux1[3], 0);
  digitalWrite(mux1[4], 1);
 
  digitalWrite(CS1, LOW);
  digitalWrite(WR1, HIGH);
  delay(1);
  digitalWrite(WR1, LOW);
  delay(1000);


    digitalWrite(WR1, HIGH);







  /*
  digitalWrite(EN1, LOW);
  digitalWrite(CS1, LOW);
  digitalWrite(mux1[0], 1);
  digitalWrite(mux1[1], 1);
  digitalWrite(mux1[2], 1);
  digitalWrite(mux1[3], 1);
  digitalWrite(mux1[4], 0);
 
  digitalWrite(CS1, HIGH);
  digitalWrite(WR1, LOW);
  delay(1);
  digitalWrite(WR1, HIGH);
  delay(1000);

  
  digitalWrite(WR1, LOW);

  
  digitalWrite(EN1, LOW);
  digitalWrite(CS1, LOW);
  digitalWrite(mux1[0], 1);
  digitalWrite(mux1[1], 1);
  digitalWrite(mux1[2], 1);
  digitalWrite(mux1[3], 0);
  digitalWrite(mux1[4], 1);
 
  digitalWrite(CS1, HIGH);
  digitalWrite(WR1, LOW);
  delay(1);
  digitalWrite(WR1, HIGH);
  delay(1000);
  */
}

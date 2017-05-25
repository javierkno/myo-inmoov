
#include <Servo.h>
#include "SimpleSerialProtocol.h"

const unsigned short secThreshold = 5;

const unsigned short SFrontalMin = 20 + secThreshold;
const unsigned short SFrontalMax = 110 - secThreshold;

const unsigned short SLateralMin = 95 + secThreshold;
const unsigned short SLateralMax = 150 - secThreshold;

const unsigned short BRotationMin = 45 + secThreshold;
const unsigned short BRotationMax = 105 - secThreshold;

const unsigned short EFlexMin = 17 + secThreshold;
const unsigned short EFlexMax = 90 - secThreshold;


// Servo 1
const int PinSFrontal = 5;

// Servo 2
const int PinBRotation = 10;

// Servo 3
const int PinSLateral = 6;

// Servo 4
const int PinEFLex = 11;

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

SimpleSerialProtocol p;

byte joint = 0;
int position = 0;
 
void setup() {

  Serial.begin(9600);

  p.CmdReceivedPtr = CmdReceived;
  
  servo1.attach(PinSFrontal);
  servo2.attach(PinBRotation);
  servo3.attach(PinSLateral);
  servo4.attach(PinEFLex);
}
 
void loop() {
  
  p.receive();
  moveJoint();
  delay(500);
}

void moveJoint() {
  switch(joint) {
    case 1:
      if (position > SFrontalMin && position < SFrontalMax) {
        servo1.write(position);
      }
      break;
    case 2:
      if (position > BRotationMin && position < BRotationMax) {
        servo2.write(position);
      }
      break;
    case 3:
      if (position > SLateralMin && position < SLateralMax) {
        servo3.write(position);
      }
      break;
    case 4:
      if (position > EFlexMin && position < EFlexMax) {
        servo4.write(position);
      }
      break;
  }
}

void CmdReceived(byte* cmd, byte cmdLength)
{
    joint = 0;
    position = 0;
    if (cmdLength > 0 && cmdLength < SimpleSerialProtocol::BUF_MAX_LENGTH) {
        int sum = 0;
        for (int i = 0; i < cmdLength - 1; i++) sum +=cmd[i];
         
        if ((sum & 0xFF) == cmd[cmdLength - 1]) { //test if the CRC matches
            joint = cmd[0];
            position = cmd[1] << 8 | cmd[2];

            Serial.print("art: ");
            Serial.print(joint);
            Serial.print(" pos: ");
            Serial.println(position);
        }
    }
}

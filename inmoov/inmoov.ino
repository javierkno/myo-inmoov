#include "SimpleSerialProtocol.h"
 
SimpleSerialProtocol p;
 
void setup()
{
    Serial.begin(9600);
    p.CmdReceivedPtr = CmdReceived;
}
 
void loop()
{
    p.receive();
}
 
void CmdReceived(byte* cmd, byte cmdLength)
{
    if (cmdLength > 0 && cmdLength < SimpleSerialProtocol::BUF_MAX_LENGTH) {
        int sum = 0;
        for (int i = 0; i < cmdLength - 1; i++) sum +=cmd[i];
         
        if ((sum & 0xFF) == cmd[cmdLength - 1]) { //test if the CRC matches
            Serial.print(char(cmd[0])); //A
            Serial.print(char(cmd[1])); //B
            Serial.print(char(cmd[2])); //C
            digitalWrite(13, HIGH);
                delay(100);
                digitalWrite(13, LOW);
                delay(200);
        }
    }
}

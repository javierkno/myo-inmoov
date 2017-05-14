#include "SimpleSerialProtocol.h"
 
SimpleSerialProtocol p;
 
void setup()
{
    Serial.begin(9600);
    p.CmdReceivedPtr = CmdReceived;

    pinMode(LED_BUILTIN, OUTPUT);
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
            byte joint = cmd[0];
            int position = cmd[1] << 8 | cmd[2];

            Serial.print("art: ");
            Serial.print(joint);
            Serial.print(" pos: ");
            Serial.println(position);
        }
    }
}

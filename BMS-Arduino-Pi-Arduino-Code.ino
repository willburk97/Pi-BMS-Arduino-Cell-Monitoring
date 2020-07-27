//#include <SPI.h>

volatile bool received;
volatile byte Slavereceived,Slavesend;

volatile byte lsbVolt, msbVolt;
int battVolt;
int battPin = 2;
float analogConversion = 5.7;

void setup()
{
  Serial.begin(9600);
  analogReference(INTERNAL);
  
  pinMode(MISO, OUTPUT);  // Make MISO an output
  SPCR |= _BV(SPE);  // Turn on spi in slave mode
  SPCR |= _BV(SPIE);  // Turn on interrupts
  
  received = false;
    
}

ISR (SPI_STC_vect)
{
  Slavereceived = SPDR;
  if (Slavereceived == 1) // First byte
  {
    SPDR = lsbVolt;
    return;
  }
  else
  {
    SPDR = msbVolt;
    received = true;
    return;
  }
}

void loop()
{
  battVolt = (analogRead(battPin) / 10.24) * 1.1 * analogConversion;
  lsbVolt = (battVolt & 0x00FF);
  msbVolt = ((battVolt & 0xFF00) >>8);
  Serial.println(msbVolt*256 + lsbVolt);  // The real math
  if (received)
  {
    Serial.print("Received:  ");
    Serial.println(Slavereceived);
    received = false;
  }
  else
  {
//    Serial.println("Nothing Received");
    delay(300);
  }

}

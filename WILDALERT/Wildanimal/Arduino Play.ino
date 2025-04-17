/***************************************************
DFPlayer - A Mini MP3 Player For Arduino
 <https://www.dfrobot.com/index.php?route=product/product&product_id=1121>

 ***************************************************
 This example shows the basic function of library for DFPlayer.

 Created 2016-12-07
 By [Angelo qiao](Angelo.qiao@dfrobot.com)

 GNU Lesser General Public License.
 See <http://www.gnu.org/licenses/> for details.
 All above must be included in any redistribution
 ****************************************************/

/***********Notice and Trouble shooting***************
 1.Connection and Diagram can be found here
 <https://www.dfrobot.com/wiki/index.php/DFPlayer_Mini_SKU:DFR0299#Connection_Diagram>
 2.This code is tested on Arduino Uno, Leonardo, Mega boards.
 ****************************************************/
#include<LiquidCrystal.h>
#include "Arduino.h"
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

SoftwareSerial mySoftwareSerial(10, 11); // RX, TX
DFRobotDFPlayerMini myDFPlayer;
void printDetail(uint8_t type, int value);

LiquidCrystal lcd(2,3,4,5,6,7); // sets the interfacing pins

char i;

String num="9943053398 ";

void setup()
{
  lcd.begin(16, 2);
  lcd.setCursor(0,0);
  lcd.clear();
  mySoftwareSerial.begin(9600);
  Serial.begin(9600);

  Serial.println();
  Serial.println(F("DFRobot DFPlayer Mini Demo"));
  Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));

  if (!myDFPlayer.begin(mySoftwareSerial)) {  //Use softwareSerial to communicate with mp3.
    Serial.println(F("Unable to begin:"));
    Serial.println(F("1.Please recheck the connection!"));
    Serial.println(F("2.Please insert the SD card!"));
    while(true);
  }
  Serial.println(F("DFPlayer Mini online."));

 /* myDFPlayer.volume(30);  //Set volume value. From 0 to 30
  myDFPlayer.play(1);  //Play the first mp3
  delay(5000);
  myDFPlayer.volume(30);  //Set volume value. From 0 to 30
  myDFPlayer.play(2);  //Play the first mp3*/

  
  
}

void loop()
{
  static unsigned long timer = millis();

  while(Serial.available())
  {
     i=Serial.read(); 
     //Serial.println("enter the character");  
     if(i=='A') 
      {
       lcd.clear();
       lcd.setCursor(0,0); 
       lcd.print("Elephant");
       lcd.setCursor(0,1);
       lcd.print("Detected");
        myDFPlayer.volume(10);  //Set volume value. From 0 to 30
        myDFPlayer.play(1);  //Play the first mp3
        delay(5000); 
        Serial.println("AT\r");
       delay(500);
       Serial.println("AT+CMGF=1\r");
       delay(500);
       Serial.print("AT+CMGS=\"");
       Serial.print(num);
       Serial.println("\"\r");
       delay(500);
       Serial.println("ELEPHENT DETECTED");
       Serial.println((char)26);
       delay(2000);
       Serial.println("  message sent");
      }
    if(i=='B')
      {
         lcd.clear();
         lcd.setCursor(0,0); 
         lcd.print("Tiger");
         lcd.setCursor(0,1); 
         lcd.print("Detected");
         myDFPlayer.volume(10);  //Set volume value. From 0 to 30
        myDFPlayer.play(2);  //Play the first mp3
        delay(5000); 
        Serial.println("AT\r");
       delay(500);
       Serial.println("AT+CMGF=1\r");
       delay(500);
       Serial.print("AT+CMGS=\"");
       Serial.print(num);
       Serial.println("\"\r");
       delay(500);
       Serial.println("TIGER Detected");
       Serial.println((char)26);
       delay(2000);
       Serial.println("  message sent");
      }
     if(i=='C')
      {
         lcd.clear();
         lcd.setCursor(0,0); 
         lcd.print("LION");
         lcd.setCursor(0,1); 
         lcd.print("Detected");
         myDFPlayer.volume(10);  //Set volume value. From 0 to 30
        myDFPlayer.play(3);  //Play the first mp3
        delay(5000); 
        Serial.println("AT\r");
       delay(500);
       Serial.println("AT+CMGF=1\r");
       delay(500);
       Serial.print("AT+CMGS=\"");
       Serial.print(num);
       Serial.println("\"\r");
       delay(500);
       Serial.println("LION Detected");
       Serial.println((char)26);
       delay(2000);
       Serial.println("  message sent");
      }
     if(i=='D')
      {
         lcd.clear();
         lcd.setCursor(0,0); 
         lcd.print("Rhinoceros");
         lcd.setCursor(0,1); 
         lcd.print("Detected");
         myDFPlayer.volume(10);  //Set volume value. From 0 to 30
        myDFPlayer.play(4);  //Play the first mp3
        delay(5000); 
        Serial.println("AT\r");
       delay(500);
       Serial.println("AT+CMGF=1\r");
       delay(500);
       Serial.print("AT+CMGS=\"");
       Serial.print(num);
       Serial.println("\"\r");
       delay(500);
       Serial.println("RHINONCEROS Detected");
       Serial.println((char)26);
       delay(2000);
       Serial.println("  message sent");
      }
      if(i=='E')
      {
         lcd.clear();
         lcd.setCursor(0,0); 
         lcd.print("Bear");
         lcd.setCursor(0,1); 
         lcd.print("Detected");
         myDFPlayer.volume(10);  //Set volume value. From 0 to 30
        myDFPlayer.play(5);  //Play the first mp3
        delay(5000); 
        Serial.println("AT\r");
       delay(500);
       Serial.println("AT+CMGF=1\r");
       delay(500);
       Serial.print("AT+CMGS=\"");
       Serial.print(num);
       Serial.println("\"\r");
       delay(500);
       Serial.println("BEAR Detected");
       Serial.println((char)26);
       delay(2000);
       Serial.println("  message sent");
      }
  }

  if (myDFPlayer.available()) {
    printDetail(myDFPlayer.readType(), myDFPlayer.read()); //Print the detail message from DFPlayer to handle different errors and states.
  }

  
}

void printDetail(uint8_t type, int value){
  switch (type) {
    case TimeOut:
      Serial.println(F("Time Out!"));
      break;
    case WrongStack:
      Serial.println(F("Stack Wrong!"));
      break;
    case DFPlayerCardInserted:
      Serial.println(F("Card Inserted!"));
      break;
    case DFPlayerCardRemoved:
      Serial.println(F("Card Removed!"));
      break;
    case DFPlayerCardOnline:
      Serial.println(F("Card Online!"));
      break;
    case DFPlayerPlayFinished:
      Serial.print(F("Number:"));
      Serial.print(value);
      Serial.println(F(" Play Finished!"));
      break;
    case DFPlayerError:
      Serial.print(F("DFPlayerError:"));
      switch (value) {
        case Busy:
          Serial.println(F("Card not found"));
          break;
        case Sleeping:
          Serial.println(F("Sleeping"));
          break;
        case SerialWrongStack:
          Serial.println(F("Get Wrong Stack"));
          break;
        case CheckSumNotMatch:
          Serial.println(F("Check Sum Not Match"));
          break;
        case FileIndexOut:
          Serial.println(F("File Index Out of Bound"));
          break;
        case FileMismatch:
          Serial.println(F("Cannot Find File"));
          break;
        case Advertise:
          Serial.println(F("In Advertise"));
          break;
        default:
          break;
      }
      break;
    default:
      break;
  }
}

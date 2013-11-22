
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"
#include <LiquidCrystal.h>

//Variables

char Incoming = 0;  //Used to store the incoming character from the serial port
String IncDat;  //Used to store the incoming data from the serial port as a string 

byte LeftDirection;
byte RightDirection;

long RightSpeed = 0;
long LeftSpeed = 0;
long leftdir = 0;
long righdir = 0;

String RSpeed =String("");
String LSpeed;
String RDirection;
String LDirection;



//Motor Shield

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *LEFT = AFMS.getMotor(1);  //Left Drive
Adafruit_DCMotor *RIGHT = AFMS.getMotor(4); //Right Drive
Adafruit_DCMotor *DISPENSE = AFMS.getMotor(3);  //Domino Motor


//LCD SETUP//
LiquidCrystal lcd(7,8,9,10,11,12); //Initialize LCD. Give data pin locations
int brightness = 255; //Enables changing the overall backlight brightness
int blRed=3;  //Red backlight pin
int blGrn=5;  //Green backlight pin
int blBlu=6;  //Blue backlight pin

void setup() 
{    
    AFMS.begin();   //Start motor shield
    Serial.begin(9600);  //Open serial port

    IncDat.reserve(200); //Reserve 200 bytes for the incoming serial data


    LEFT->setSpeed(150); //Start both motors
    LEFT->run(FORWARD);
    LEFT->run(RELEASE);

    RIGHT->setSpeed(150);
    RIGHT->run(FORWARD);
    RIGHT->run(RELEASE);

    DISPENSE->setSpeed(150);
    DISPENSE->run(FORWARD);
    DISPENSE->run(RELEASE);

    Serial.println("1500"); //Indicates to python that the Arduino is ready
                            //Windows Only?
    DISPENSE->setSpeed(100);
    DISPENSE->run(FORWARD);


    //LCD SETUP//
    lcd.begin(16, 2);
    lcd.clear();
    pinMode(blRed, OUTPUT);
    pinMode(blGrn, OUTPUT);
    pinMode(blBlu, OUTPUT);
    analogWrite(blRed,0);
    analogWrite(blGrn,100);
    analogWrite(blBlu,100);
    lcd.setCursor(1,0);
    lcd.print("Left:");
    lcd.setCursor(0,1);
    lcd.print("Right:");
}

void loop() 
{
    if (Serial.available())
    {
        while (Serial.available())
        {
            Incoming=Serial.read();

            if (Incoming==char(003))
            {
                RSpeed=IncDat.substring(0,3);
                LSpeed =IncDat.substring(3,6);
                RDirection =IncDat.substring(6,7);
                LDirection = IncDat.substring(7,8);
                IncDat=""; //Clear IncDat for next serial transmission
            }
            else
            {
                IncDat += Incoming; //Append most recent character to IncDat string
            }
        }
    }
    //Convert separated string to long with string.toInt    
     RightSpeed=RSpeed.toInt();
     LeftSpeed= LSpeed.toInt();
     leftdir=LDirection.toInt();
     righdir=RDirection.toInt();

    //Convert leftdir and righdir (Left and Right directional info) to bytes. Req'd for adafruit library

    LeftDirection=leftdir;
    RightDirection=righdir;
    
    RunMotors(RightSpeed,LeftSpeed,RightDirection,LeftDirection);
}



void RunMotors(int rs, int ls, byte rd, byte ld) //Run two drive motors
{
    // LEFT->setSpeed(rs);
    lcd.setCursor(7,1);
    lcd.print(rs);
    // LEFT->run(rd);

    // RIGHT->setSpeed(ls);
    lcd.setCursor(7,0);
    lcd.print(ls);

    // RIGHT->run(ld);

}
//Look into serialEvent
//Would it make more sense to have serial checking in the void_loop 
//or would it make more sense to have it occur at the end of the void loop
//if serial data is detected? Will there be a difference?

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"

//Variables

byte SignalPin = 4; //Pin to connect to indicator LED or buzzer

byte LeftDirection;
byte RightDirection;
byte DispenserDirection;

long RightSpeed = 0;
long LeftSpeed = 0;
long leftdir = 0;
long righdir = 0;
long DispenserSpeed = 0;


//Motor Shield

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *LEFT = AFMS.getMotor(1);  //Left Drive
Adafruit_DCMotor *RIGHT = AFMS.getMotor(4); //Right Drive
Adafruit_DCMotor *DISPENSE = AFMS.getMotor(3);  //Domino Dispenser Motor


void setup() 
{    
    LEFT->setSpeed(150); //Start both motors
    LEFT->run(FORWARD);
    LEFT->run(RELEASE);

    RIGHT->setSpeed(150);
    RIGHT->run(FORWARD);
    RIGHT->run(RELEASE);

    DISPENSE->setSpeed(150);
    DISPENSE->run(FORWARD);
    DISPENSE->run(RELEASE);


///////////////////SET PARAMETERS HERE///////////////////

    RightSpeed = 180;  //0-255
    LeftSpeed =  180;   //0-255

    RightDirection = 1;  // 0 (stop), 1 (forward), 2 (reverse)
    LeftDirection =  1;   // 0 (stop), 1 (forward), 2 (reverse)

    DispenserDirection = 1;

///////////////////END OF PARAMETERS/////////////////////

    DispenserSpeed = map(min(RightSpeed, LeftSpeed), 0, 255, 0, 255); //Change the last two numbers to tune the dispenser motor speed

    RunMotors(RightSpeed, LeftSpeed, DispenserSpeed, RightDirection, LeftDirection, DispenserDirection);
}

void loop() 
{}


void RunMotors(int rs, int ls, int ds, byte rd, byte ld, byte dd) //Run two drive motors
{
    LEFT->setSpeed(rs);
    LEFT->run(rd);
    RIGHT->setSpeed(ls);
    RIGHT->run(ld);
    DISPENSE->setSpeed(ds);
    DISPENSE->run(dd);
}
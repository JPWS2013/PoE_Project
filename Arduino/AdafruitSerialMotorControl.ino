#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"

//Variables

char Incoming = 0; 	//Used to store the incoming character from the serial port
String IncDat;	//Used to store the incoming data from the serial port as a string 

byte DominoCount = 0; //Counts number of dominoes dispensed

byte SignalPin = 11; //Pin to connect to indicator LED or buzzer
byte BreakBeamPin = 8; //Pin to connect to breakbeam data pin.
byte BreakBState = 0; //Variable to store

byte LeftDirection;
byte RightDirection;
byte DispenserDirection;

long RightSpeed = 0;
long LeftSpeed = 0;
long leftdir = 0;
long righdir = 0;
long DispenserSpeed = 0;

float dividingfactor=3.5;

String RSpeed =String("");
String LSpeed;
String RDirection;
String LDirection;



//Motor Shield

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *LEFT = AFMS.getMotor(1); 	//Left Drive
Adafruit_DCMotor *RIGHT = AFMS.getMotor(2);	//Right Drive
Adafruit_DCMotor *DISPENSE = AFMS.getMotor(3); 	//Domino Motor


void setup() 
{	 
	AFMS.begin();	//Start motor shield
	pinMode(SignalPin, OUTPUT);
	Serial.begin(9600);	 //Open serial port

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
	tone(SignalPin, 1800, 1500); //Beep for 1.5 seconds (high pitch)
}

void loop() 
{
	while (DominoCount <40)
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
                 RightSpeed=RightSpeed/dividingfactor;
                 RightSpeed=long(RightSpeed);
		 LeftSpeed= LSpeed.toInt();
                 LeftSpeed=LeftSpeed/dividingfactor;
                 LeftSpeed=long(LeftSpeed);
		 leftdir=LDirection.toInt();
		 righdir=RDirection.toInt();

		//Convert leftdir and righdir (Left and Right directional info) to bytes. Req'd for adafruit library

		LeftDirection=leftdir;
		RightDirection=righdir;		
                
                if (LeftSpeed==0 || RightSpeed==0)
                {
                  DispenserSpeed=0;
                  RightSpeed=0;
                }
                else
                {
                  DispenserSpeed = 125;//map(min(RightSpeed, LeftSpeed), 0, (255/dividingfactor), 100, 150); //Change the last two numbers to tune the dispenser motor speed
                  RightSpeed = 49;
                }
                
                //RightSpeed = 140;
                LeftSpeed = RightSpeed;
                DispenserDirection = 1; //Should always be either one or two, depending on motor mount orientation.
		
                BreakBState = digitalRead(BreakBeamPin);
		if (BreakBState == HIGH)
		{
                        RunMotors(0, 0, 0, 0, 0, 0);
                        
                        delay(250);
//			while (BreakBState == HIGH)
//			{
//				BreakBState = digitalRead(BreakBeamPin); //Makes sure dominoes are not double counted
//			}

			DominoCount += 1;
		}

                RunMotors(RightSpeed, LeftSpeed, DispenserSpeed, RightDirection, LeftDirection, DispenserDirection);
	}
		
}



void RunMotors(int rs, int ls, int ds, byte rd, byte ld, byte dd) //Run two drive motors
{
	LEFT->setSpeed(rs);
	LEFT->run(rd);
	RIGHT->setSpeed(ls);
	RIGHT->run(ld);
	DISPENSE->setSpeed(ds);
	DISPENSE->run(dd);

    if(rs == 0 && ls == 0)
    {
    	tone(SignalPin, 740); //During running, if motors are told not to move, that means that it has lost the laser.Play a low tone.
    }
    else
    {
    	noTone(SignalPin); //As soon as the motors move, do not play the warning low tone.
    }
}

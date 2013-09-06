////////////////////////////////////////////////////////////////////////////////
// Rabbit Parameters
////////////////////////////////////////////////////////////////////////////////
#define EOUTBUFSIZE 127
#define EINBUFSIZE 127
#define FOUTBUFSIZE 1023
#define FINBUFSIZE 1023
#define pi    (3.14159)
#use ES308_SBC.lib
////////////////////////////////////////////////////////////////////////////////
//Function Definitions
float DesRud(float ActHeading)
     {
     float Des;
     //if/else statement accounts for the circular nature of heading this makes
     //sure the boat doesn't drive in a rightward circle to just go left
        if (ActHeading > 180.0)
        {
        	Des = (360.0 - ActHeading)*(pi/180.0);
        }
       else
       	{
         Des = (0.0 - ActHeading)*(pi/180.0);
         }
     //These if statements floor the max through angle to +/- 0.5235 rads to
     //prevent the motor from blowing a fuse
       if (Des > 0.5235)
       	{
         	Des = 0.5235;
         }
       if (Des < -0.5235)
       	{
         	Des = -0.5235;
         }
      //Returns desired rudder angle   
         return Des;
       }
////////////////////////////////////////////////////////////////////////////////
// Begin main
////////////////////////////////////////////////////////////////////////////////
void main(void)
{//Begin Main
//Initialize Variables
   float MotorVolts, MotorVolts_Old;
   float Error, ErrorAct, Error_Old;
   float Rudder_Counts, Rudder_Angle, DesR;
   float DesHeading, ActHeading;
	char MVHex[2], MVStrRoboteQ[4],buf[50],HxSentence[50], Heading[5];
   char *tok, delimiter[2];
   int MVInt, sentInt,i;
   int switchDir;
   char RxSentence[5];
   char RudderAngleStr[5];
   float Kenc, k2, k1;
//Control constants and parameters
   Kenc = 0.0001885;
   k1 = 25;
//Zero out all errors, angles, and counts
   Error = 0.0;
   ErrorAct = 0.0;

   DesHeading = 0.0;
   ActHeading = 0.0;

   MotorVolts = 0.0;

   Rudder_Counts = 0.0;
   Rudder_Angle = 0.0;
   DesR = 0.0;
//Define the delimter for parsing GPS and Header Data
   delimiter[0] = ',';
	delimiter[1] = 0;
//Clear buffer for GPS, Heading, and RudderAngle arrays
   for(i=0;i<5;i++)
  {
    RxSentence[i] = '\0';
  }

  for(i=0;i<5;i++)
  {
    RudderAngleStr[i] = '\0';
  }

  for(i=0;i<50;i++)
  {
    HxSentence[i] = '\0';
  }
////////////////////////////////////////////////////////////////////////////////
// Initialize Rabbit SBC
// Open each serial port
////////////////////////////////////////////////////////////////////////////////
// Laptop communication link
////////////////////////////////////////////////////////////////////////////////
// RoboteQ communication links
  	   serBopen(9600);
 	   serBparity(PARAM_EPARITY);
  	   serBdatabits(PARAM_7BIT);
   	serBwrFlush();
    	serBrdFlush();

      serEopen(9600);
      serEflowcontrolOff();
      serEdatabits(8);
      serEparity(PARAM_NOPARITY);

      serFopen(4800);
      serFflowcontrolOff();
      serFdatabits(8);
      serFparity(PARAM_NOPARITY);

////////////////////////////////////////////////////////////////////////////////
// Main loop
////////////////////////////////////////////////////////////////////////////////
	while(1)
    {
////////////////////////////////////////////////////////////////////////////////
 	 costate // Costatement for determining current rudder angle from the encoder
   	 {
      	serErdFlush();
			// Clear serial strings
        	for(i=0;i<5;i++)
        		{
          	RxSentence[i] = '\0';
        		}

      	wfd cof_serEgets(RxSentence, 5, 10);

       		RudderAngleStr[0] = RxSentence[1];
       		RudderAngleStr[1] = RxSentence[2];
       		RudderAngleStr[2] = RxSentence[3];
       		RudderAngleStr[3] = RxSentence[4];

       	Rudder_Counts = atof(RxSentence);
       	Rudder_Angle = Kenc*Rudder_Counts;

       serErdFlush;
      }
////////////////////////////////////////////////////////////////////////////////
       costate //Costatement for reading in and parsing heading string from
	    {       //AIRMAR sensor

        	for(i=0;i<50;i++)
        		{
          	HxSentence[i] = '\0';
        		}

	      wfd cof_serFgets(HxSentence, 50, 10);

          	if(HxSentence[0] == '$' && HxSentence[1] == 'H')
            {

			     tok=strtok(HxSentence,delimiter);//header
              tok=strtok(NULL,delimiter);	//UTC TIME
              strcpy(Heading, tok);
				  ActHeading = atof(Heading);

             // printf("Heading = %.1f DesRudder = %.1f \r\n", ActHeading, Desired_Rudder_Angle);
            printf("Rudder Angle = %.3f Heading = %.1f MotorVolts = %.1f Desired = %.1f \r", Rudder_Angle, ActHeading, MotorVolts, DesR);
             }
             for(i=0;i<50;i++)
        			{
         			HxSentence[i] = '\0';
        			}
        	 //		serFrdFlush;
          }
////////////////////////////////////////////////////////////////////////////////
//Control Calculations
       DesR = DesRud(ActHeading); //Desired Rudder Angle

       ErrorAct = DesR - Rudder_Angle; //Error between desired and actual rudder

       MotorVolts = k1*ErrorAct; //Calculate triller voltage based on error
////////////////////////////////////////////////////////////////////////////////
// RoboteQ HEX serial commands
// Ex: !b00 - !b7F OR !B00 - !B7F
// A carriage return needs to be sent for execution of command.
////////////////////////////////////////////////////////////////////////////////
//Writes Voltage Signal to the Roboteq motor controller
     if(MotorVolts>0)
       strcpy(MVStrRoboteQ,"!B"); //B is the starter for Roboteq messages
     else
       strcpy(MVStrRoboteQ,"!b");
//Limits MotorVoltage to 10V, this prevents blowing fuses
     if(MotorVolts>10.0)
       MotorVolts = 10.0;
     if(MotorVolts<-10.0)
       MotorVolts = -10.0;
//Converts floating point to Hex number for transport
     MVInt = floor((fabs(MotorVolts)/24.0)*127);
     strcpy(MVHex,0);
     htoa(MVInt,MVHex);

     if(MVHex[1]==0)
     {
       MVHex[1] = MVHex[0];
       MVHex[0] = '0';
     }
// Build string and send to amplifier
    strcat(MVStrRoboteQ,MVHex);
    sentInt = serBputs(MVStrRoboteQ);
    serBputs("\r");
////////////////////////////////////////////////////////////////////////////////
 } //End While Loop
} //End Main

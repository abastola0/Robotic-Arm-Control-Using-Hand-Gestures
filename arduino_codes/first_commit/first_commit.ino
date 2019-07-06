//
//
///* ------------------------------------------------
//* SERIAL COM - HANDELING MULTIPLE BYTES inside ARDUINO - 03_function development
//* by beltran berrocal
//*
//* this prog establishes a connection with the pc and waits for it to send him
//* a long string of characters like "hello Arduino!". 
//* Then Arduino informs the pc that it heard the whole sentence
//*
//* the same as examlpe 02 but it deploys 2 reusable functions.
//* for doing the same job. 
//* readSerialString() and  printSerialString()
//* the only problem is that they use global variables instead of getting them passed 
//* as parameters. this means that in order to reuse this code you should also copy
//* the 4 variables instantiated at the beginning of the code.
//* Another problem is that if you expect more than one string at a time 
//* you will have to duplicate and change names to all variables as well as the functions.
//* Next version should have the possibility to pass the array as a parameter to the function.
//*
//* created 15 Decembre 2005;
//* copyleft 2005 Progetto25zero1  <http://www.progetto25zero1.com>
//*
//* --------------------------------------------------- */
//
//int  serIn;             // var that will hold the bytes-in read from the serialBuffer
//char serInString[100];  // array that will hold the different bytes  100=100characters;
//                        // -> you must state how long the array will be else it won't work.
//int  serInIndx  = 0;    // index of serInString[] in which to insert the next incoming byte
//int  serOutIndx = 0;    // index of the outgoing serInString[] array;
//
//
///*read a string from the serial and store it in an array
////you must supply the array variable and the index count
//void readSerialString (char *strArray, int indx) {
//    int sb;                               //declare local serial byte before anything else
//    Serial.print("reading Serial String: ");   
//    if(serialAvailable()) {     
//       while (serialAvailable()){ 
//          sb = serialRead();             
//          strArray[indx] = sb;
//          indx++;
//          serialWrite(sb);
//       }
//    }  
//    Serial.println();
//}
//*/
//
////read a string from the serial and store it in an array
////this func uses globally set variable so it's not so reusable
////I need to find the right syntax to be able to pass to the function 2 parameters:
//// the stringArray and (eventually) the index count
//void readSerialString () {
//    int sb;   
//    if(Serial.available()) { 
//       //Serial.print("reading Serial String: ");     //optional confirmation
//       while (Serial.available()){ 
//          sb = Serial.read();             
//          serInString[serInIndx] = sb;
//          serInIndx++;
//          //serialWrite(sb);                        //optional confirmation
//       }
//       //Serial.println();
//    }  
//}
//
////print the string all in one time
////this func as well uses global variables
//void printSerialString() {
//   if( serInIndx > 0) {     
//      //loop through all bytes in the array and print them out
//      for(serOutIndx=0; serOutIndx < serInIndx; serOutIndx++) {
//          Serial.print( serInString[serOutIndx] );    //print out the byte at the specified index
//          //serInString[serOutIndx] = "";            //optional: flush out the content
//      }        
//      //reset all the functions to be able to fill the string back with content
//      serOutIndx = 0;
//      serInIndx  = 0;
//      Serial.println();
//   }
//
//}
//
//
//void setup() {
//  Serial.begin(9600);
//  Serial.println("Hello World");   
//}
//
//void loop () {
//  //simple feedback from Arduino
//  
//  //read the serial port and create a string out of what you read
//  //readSerialString(serInString, serInIndx);
//  readSerialString();
//  
//  //do somenthing else perhaps wait for other data or read another Serial string
////  Serial.println ("------------ arduino is doing somenthing else ");
//  
//  //try to print out collected information. it will do it only if there actually is some info.
//  printSerialString();
//  
//  //slows down the visualization in the terminal
////  delay(10);
//}

//zoomkat 11-22-12 simple delimited ',' string parse 
//from serial port input (via serial monitor)
//and print result out serial port
//multi servos added 

String readString;
#include <Servo.h> 
Servo myservoa, myservob, myservoc;  // create servo object to control a servo 

void setup() {
  Serial.begin(9600);

  //myservoa.writeMicroseconds(1500); //set initial servo position if desired

  myservoa.attach(9);  //the pin for the servoa control
  myservob.attach(10);  //the pin for the servob control
  myservoc.attach(11);  //the pin for the servoc control
//  myservod.attach(9);  //the pin for the servod control 
  Serial.println("multi-servo-delimit-test-dual-input-11-22-12"); // so I can keep track of what is loaded
}

void loop() {

  //expect single strings like 700a, or 1500c, or 2000d,
  //or like 30c, or 90a, or 180d,
  //or 30c,180b,70a,120d,

  if (Serial.available())  {
    char b = Serial.read();  //gets one byte from serial buffer
    if (b == ',') {
      if (readString.length() >1) {
//        Serial.println(readString); //prints string to serial port out

        int n = readString.toInt();  //convert readString into a number
//        Serial.println(n);
        // auto select appropriate value, copied from someone elses code.
        if(n >= 500)
        {
//          Serial.print("writing Microseconds: ");
//          Serial.println(n);
//          if(readString.indexOf('a') >0) Serial.println(n);
//          if(readString.indexOf('b') >0) Serial.println(n);
//          if(readString.indexOf('c') >0) Serial.println(n);
//          y = map(x, 1, 50, 50, 1);
//          if(readString.indexOf('a') >0) myservoa.writeMicroseconds(map(n, 0, 1366, 0, 179));
//          if(readString.indexOf('b') >0) myservob.writeMicroseconds(map(n, 0, 768, 0, 90));
//          if(readString.indexOf('c') >0) myservoc.writeMicroseconds(n);
            if(readString.indexOf('a') >0) myservoa.write(n);
            if(readString.indexOf('b') >0) myservob.write(n);
            if(readString.indexOf('c') >0) myservoc.write(n);
//          if(readString.indexOf('d') >0) myservod.writeMicroseconds(n);
        }
        else
        {   
//          Serial.print("writing Angle: ");
//          Serial.println(n);       
//            if(readString.indexOf('a') >0) Serial.println(n);
//            if(readString.indexOf('b') >0) Serial.println(n);
//            if(readString.indexOf('c') >0) Serial.println(n);
//          if(readString.indexOf('a') >0) myservoa.write(map(n, 0, 1366, 0, 179));
//          if(readString.indexOf('b') >0) myservob.write(map(n, 68, 700, 0, 90));
             if(readString.indexOf('a') >0) myservoa.write(n);
            if(readString.indexOf('b') >0) myservob.write(n);
            if(readString.indexOf('c') >0) myservoc.write(n);
//          if(readString.indexOf('d') >0) myservod.write(n);
        }
         readString="\n"; //clears variable for new input
      }
    }  
    else {     
      readString += b; //makes the string readString
    }
  }
}

int redPin = 9;    // Red LED connected to pin 9
int greenPin = 10; // Green LED connected to pin 10
int bluePin = 11;  // Blue LED connected to pin 11
int value = 0;     // Variable to store incoming value

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(redPin, OUTPUT);   // Set RGB pins as outputs
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) { // Check if data is available to read
    value = Serial.parseInt(); // Read the incoming value
    if (value == 4 || value == 5 || value == 7) { // If the value is '1'
      runningLights(); // Perform the running light effect
    } else { // For other values, set the RGB LED immediately
      analogWrite(redPin, getRed(value));     // Set red intensity based on value
      analogWrite(greenPin, getGreen(value)); // Set green intensity based on value
      analogWrite(bluePin, getBlue(value));   // Set blue intensity based on value
    }
  }
}

// Functions to calculate RGB intensities based on input value
int getRed(int value) {

  if (value == 1) return 135;                     //angry
  else if (value == 2) return 230;                  //disgust
  else if (value == 3) return 51;                //fear
 // else if (value == 4) return 255;                   //happy
 // else if (value == 5) return 0;                  //neutral
  else if (value == 6) return 246;                //sad
//else if (value == 7) return 128;                //surprise
  else return 0; // Default case
}

int getGreen(int value) {

  if (value == 1) return 206;                       //angry
  else if (value == 2) return 230;                //disgust
  else if (value == 3) return 255;                //fear  
 // else if (value == 4) return 128;                    //happy
//else if (value == 5) return 255;                //neutral
  else if (value == 6) return 231;                  //sad
//else if (value == 7) return 128;                //surprise
  else return 0; // Default case
}

int getBlue(int value) {

  if (value == 1) return 235;               //angry
  else if (value == 2) return 255;          //disgust
  else if (value == 3) return 51;          //fear
 // else if (value == 4) return 0;                //happy
//else if (value == 5) return 255;        //neutral
  else if (value == 6) return 210;        //sad
//else if (value == 7) return 255;        //surprise
  else return 0; // Default case
}


void runningLights() {
  for (int i = 0; i <= 255; i++) {
    analogWrite(redPin, i);      // Red increasing
    analogWrite(greenPin, 255 - i);  // Green decreasing
    analogWrite(bluePin, 0);     // Blue off
    delay(10); // Adjust delay for speed of transition
  }
  for (int i = 0; i <= 255; i++) {
    analogWrite(redPin, 255);    // Red at full intensity
    analogWrite(greenPin, 0); // Green off
    analogWrite(bluePin, i);     // Blue increasing
    delay(10); // Adjust delay for speed of transition
  }
  for (int i = 0; i <= 255; i++) {
    analogWrite(redPin, 255 - i); // Red decreasing
    analogWrite(greenPin, i);    // Green increasing
    analogWrite(bluePin, 255);   // Blue at full intensity
    delay(10); // Adjust delay for speed of transition
  }
  for (int i = 0; i <= 255; i++) {
    analogWrite(redPin, i);     // Red increasing
    analogWrite(greenPin, 255); // Green at full intensity
    analogWrite(bluePin, 255 - i); // Blue decreasing
    delay(10); // Adjust delay for speed of transition
  }
}

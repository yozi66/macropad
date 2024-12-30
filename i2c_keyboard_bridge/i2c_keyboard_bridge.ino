#include <Wire.h>
#include "HID-Project.h"

void setup() {
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
  Consumer.begin();
  Keyboard.begin();
}

void loop() {
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  Serial.print("receive: ");
  Serial.println(howMany);
  while (Wire.available() > 0) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    Serial.print(c);         // print the character
    switch(c) {
      case 'D':
        Consumer.write(MEDIA_VOLUME_DOWN);
        break;
      case 'L':
        Keyboard.press(KEY_LEFT_GUI); // Windows key (Left GUI key)
        Keyboard.press('l');          // 'L' key
        delay(100);                   // Short delay to simulate holding the keys
        Keyboard.releaseAll();        // Release all keys
        break;
      case 'P':
        Consumer.write(MEDIA_PLAY_PAUSE);
        break;
      case 'U':
        Consumer.write(MEDIA_VOLUME_UP);
        break;
      default:
        Keyboard.write(c);
        break;
    }
  }
  Serial.println();
}

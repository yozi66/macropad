#include <Wire.h>
#include "HID-Project.h"

void setup() {
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Consumer.begin();
  Keyboard.begin();
}

void loop() {
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  while (Wire.available() > 0) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    switch(c) {
      case '0':
        Keyboard.press(HID_KEYBOARD_GRAVE_ACCENT_AND_TILDE); // zero in Hungarian layout
        Keyboard.releaseAll();
        break;
      case 'D':
        Consumer.write(MEDIA_VOLUME_DOWN);
        break;
      case 'E':
        Keyboard.press(HID_KEYBOARD_ENTER);
        Keyboard.releaseAll();
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
}

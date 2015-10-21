# python-duckencode

This program converts Duckyscript code into Arduino code. This arduino code will only work on AVR chips with USB support.

----

**Installation:**

Simply download/clone this repository and run `./compiler.py` or `python3 compiler.py`

---

You may need to change a file on the arduino folder

This may be /usr/share/arduino/hardware/arduino/cores/arduino/USBAPI.h or similar
If you installed the board stuff from the manager then it will be under your sketches directory as hardware/arduino/cores/arduino/USBAPI.h

Open that file and find

private:
    KeyMap* _keyMap;
    void sendReport(KeyReport* keys);
    void setKeyMap(KeyMap* keyMap);
public:
    Keyboard_();
    virtual size_t write(uint8_t);

Then change that to

private:
KeyMap* _keyMap;
void setKeyMap(KeyMap* keyMap);
public:
void sendReport(KeyReport* keys);
Keyboard_();
virtual size_t write(uint8_t);

https://ctrlaltnarwhal.wordpress.com/2012/10/31/installing-usb-rubber-ducky-on-3rd-party-devices/
 /usr/share/arduino/hardware/arduino/cores/arduino/HID.cpp
 http://codereview.stackexchange.com/questions/108174/duckyscript-precompiler-for-arduino-leonardo
 http://arduino.stackexchange.com/questions/17057/keyboard-print-skips-keys

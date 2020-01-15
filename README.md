Description:
------------

This program converts Duckyscript code into Arduino code. This arduino code will only work on AVR chips with USB support. I was inspired by [this project][1]

Installation:
-------------

1. Clone this repository and `cd` into it:

        git clone https://github.com/0x2b3bfa0/python-duckencode.git
        cd python-duckencode

2. Make public the `sendReport()` function:

    You should edit a file called `USBAPI.h`. This file may be on one of the following paths<sup>[1](#footnote_1)</sup>:

        {ARDUINO}/hardware/arduino/cores/arduino/USBAPI.h
        {SKETCHES}/hardware/arduino/cores/arduino/USBAPI.h


    Once you've found this file, open it with your favorite text editor and locate these lines:

        private:
            KeyMap* _keyMap;
            void sendReport(KeyReport* keys);
            void setKeyMap(KeyMap* keyMap);
        public:
            Keyboard_();
            virtual size_t write(uint8_t);

    Simply cut this line from the `private` section and paste it on the `public` section:

        void sendReport(KeyReport* keys);

    Once edited these lines should look like this:

        private:
            KeyMap* _keyMap;
            void setKeyMap(KeyMap* keyMap);
        public:
            void sendReport(KeyReport* keys);
            Keyboard_();
            virtual size_t write(uint8_t);

3. Run the program:

        ./compiler.py

---

<a name="footnote_1">**1**</a>**:** `{ARDUINO}` represents the directory into which the Arduino IDE and supporting files have been installed. This may be `/usr/local/arduino` or `/usr/share/arduino` or one of many other possible choices depending on your operating system.

[1]: https://ctrlaltnarwhal.wordpress.com/2012/10/31/installing-usb-rubber-ducky-on-3rd-party-devices/

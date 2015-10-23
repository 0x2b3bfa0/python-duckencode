#!/usr/bin/env python3


"""
This module contains all the compiler data, including a keycode lookup table
and the arduino program base.
"""


import textwrap


# Here is the base code of the output. Note that the double curl braces escapes
# the format strings. This will avoid later to get confused the format function
code = textwrap.dedent("""
    {includes}

    {defines}

    void sendKey(byte k0, byte k1, byte k2, byte k3,
                 byte k4, byte k5, byte modifiers)
    {{
      KeyReport report = {{0}};

      report.keys[0] = k0;
      report.keys[1] = k1;
      report.keys[2] = k2;
      report.keys[3] = k3;
      report.keys[4] = k4;
      report.keys[5] = k5;
      report.modifiers = modifiers;
      report.reserved = 1;
      Keyboard.sendReport(&report);

      report = {{0}};
      Keyboard.sendReport(&report);
    }}

    void setup() {{
    {setup}
    }}

    void loop() {{
    {loop}
    }}
""").strip()

# Here is the base code for the REPEAT command.
repeat = textwrap.dedent("""
    for(int i=0; i<{}; i++) {{
     {}
     delay({});
    }}
""").strip()

# Dictionary with the keys and their hexadecimal values.
# The structure follows these rules:
#
#    ('KEY_ALIAS_1', 'KEY_ALIAS_2', 'KEY_ALIAS_N'): [0xKeyCode, IsModifier]
#
# If the key is a modifier key (CTRL, ALT, SHIFT or GUI), IsModifier will be 1,
# else it will be 0.
#
# The keycodes were extracted from the arduino defines and slightly modified to
# respect the DuckieScript coding standards.
#
# You can get the base of this dictionary piping the arduino defines to these
# commands (only if you're in a *nix system):
#
#    sed 's/KEY_//' |
#    awk '{ print "(\x27"$2"\x27, \x27KEY_"$2"\x27): ["$3", 0]," }'
keycodes = {
    ('A', 'KEY_A'): [0x04, 0],
    ('B', 'KEY_B'): [0x05, 0],
    ('C', 'KEY_C'): [0x06, 0],
    ('D', 'KEY_D'): [0x07, 0],
    ('E', 'KEY_E'): [0x08, 0],
    ('F', 'KEY_F'): [0x09, 0],
    ('G', 'KEY_G'): [0x0A, 0],
    ('H', 'KEY_H'): [0x0B, 0],
    ('I', 'KEY_I'): [0x0C, 0],
    ('J', 'KEY_J'): [0x0D, 0],
    ('K', 'KEY_K'): [0x0E, 0],
    ('L', 'KEY_L'): [0x0F, 0],
    ('M', 'KEY_M'): [0x10, 0],
    ('N', 'KEY_N'): [0x11, 0],
    ('O', 'KEY_O'): [0x12, 0],
    ('P', 'KEY_P'): [0x13, 0],
    ('Q', 'KEY_Q'): [0x14, 0],
    ('R', 'KEY_R'): [0x15, 0],
    ('S', 'KEY_S'): [0x16, 0],
    ('T', 'KEY_T'): [0x17, 0],
    ('U', 'KEY_U'): [0x18, 0],
    ('V', 'KEY_V'): [0x19, 0],
    ('W', 'KEY_W'): [0x1A, 0],
    ('X', 'KEY_X'): [0x1B, 0],
    ('Y', 'KEY_Y'): [0x1C, 0],
    ('Z', 'KEY_Z'): [0x1D, 0],
    ('1', 'KEY_1'): [0x1E, 0],
    ('2', 'KEY_2'): [0x1F, 0],
    ('3', 'KEY_3'): [0x20, 0],
    ('4', 'KEY_4'): [0x21, 0],
    ('5', 'KEY_5'): [0x22, 0],
    ('6', 'KEY_6'): [0x23, 0],
    ('7', 'KEY_7'): [0x24, 0],
    ('8', 'KEY_8'): [0x25, 0],
    ('9', 'KEY_9'): [0x26, 0],
    ('0', 'KEY_0'): [0x27, 0],
    ('ENTER', 'NEWLINE', 'KEY_ENTER'): [0x28, 0],
    ('ESC', 'ESCAPE', 'KEY_ESC'): [0x29, 0],
    ('BACKSPACE', 'KEY_BACKSPACE'): [0x2A, 0],
    ('TAB', 'KEY_TAB'): [0x2B, 0],
    ('SPACE', 'KEY_SPACE'): [0x2C, 0],
    ('MINUS', 'KEY_MINUS'): [0x2D, 0],
    ('EQUAL', 'KEY_EQUAL'): [0x2E, 0],
    ('LEFTBRACE', 'KEY_LEFTBRACE'): [0x2F, 0],
    ('RIGHTBRACE', 'KEY_RIGHTBRACE'): [0x30, 0],
    ('BACKSLASH', 'KEY_BACKSLASH'): [0x31, 0],
    ('NONUSHASH', 'KEY_NONUSHASH'): [0x32, 0],
    ('SEMICOLON', 'KEY_SEMICOLON'): [0x33, 0],
    ('APOSTROPHE', 'KEY_APOSTROPHE'): [0x34, 0],
    ('GRAVE', 'KEY_GRAVE'): [0x35, 0],
    ('COMMA', 'KEY_COMMA'): [0x36, 0],
    ('DOT', 'KEY_DOT'): [0x37, 0],
    ('SLASH', 'KEY_SLASH'): [0x38, 0],
    ('CAPSLOCK', 'KEY_CAPSLOCK'): [0x39, 0],
    ('F1', 'KEY_F1'): [0x3A, 0],
    ('F2', 'KEY_F2'): [0x3B, 0],
    ('F3', 'KEY_F3'): [0x3C, 0],
    ('F4', 'KEY_F4'): [0x3D, 0],
    ('F5', 'KEY_F5'): [0x3E, 0],
    ('F6', 'KEY_F6'): [0x3F, 0],
    ('F7', 'KEY_F7'): [0x40, 0],
    ('F8', 'KEY_F8'): [0x41, 0],
    ('F9', 'KEY_F9'): [0x42, 0],
    ('F10', 'KEY_F10'): [0x43, 0],
    ('F11', 'KEY_F11'): [0x44, 0],
    ('F12', 'KEY_F12'): [0x45, 0],
    ('SYSRQ', 'KEY_SYSRQ'): [0x46, 0],
    ('SCROLLLOCK', 'KEY_SCROLLLOCK'): [0x47, 0],
    ('PAUSE', 'KEY_PAUSE'): [0x48, 0],
    ('INSERT', 'KEY_INSERT'): [0x49, 0],
    ('HOME', 'KEY_HOME'): [0x4A, 0],
    ('PAGEUP', 'KEY_PAGEUP'): [0x4B, 0],
    ('DELETE', 'KEY_DELETE'): [0x4C, 0],
    ('END', 'KEY_END'): [0x4D, 0],
    ('PAGEDOWN', 'KEY_PAGEDOWN'): [0x4E, 0],
    ('RIGHT', 'RIGHTARROW', 'KEY_RIGHT'): [0x4F, 0],
    ('LEFT', 'LEFTARROW', 'KEY_LEFT'): [0x50, 0],
    ('DOWN', 'DOWNARROW', 'KEY_DOWN'): [0x51, 0],
    ('UP', 'UPARROW', 'KEY_UP'): [0x52, 0],
    ('NUMLOCK', 'KEY_NUMLOCK'): [0x53, 0],
    ('KPSLASH', 'KEY_KPSLASH'): [0x54, 0],
    ('KPASTERISK', 'KEY_KPASTERISK'): [0x55, 0],
    ('KPMINUS', 'KEY_KPMINUS'): [0x56, 0],
    ('KPPLUS', 'KEY_KPPLUS'): [0x57, 0],
    ('KPENTER', 'KEY_KPENTER'): [0x58, 0],
    ('KP1', 'KEY_KP1'): [0x59, 0],
    ('KP2', 'KEY_KP2'): [0x5A, 0],
    ('KP3', 'KEY_KP3'): [0x5B, 0],
    ('KP4', 'KEY_KP4'): [0x5C, 0],
    ('KP5', 'KEY_KP5'): [0x5D, 0],
    ('KP6', 'KEY_KP6'): [0x5E, 0],
    ('KP7', 'KEY_KP7'): [0x5F, 0],
    ('KP8', 'KEY_KP8'): [0x60, 0],
    ('KP9', 'KEY_KP9'): [0x61, 0],
    ('KP0', 'KEY_KP0'): [0x62, 0],
    ('KPDOT', 'KEY_KPDOT'): [0x63, 0],
    ('102ND', 'KEY_102ND'): [0x64, 0],
    ('COMPOSE', 'KEY_COMPOSE'): [0x65, 0],
    ('POWER', 'KEY_POWER'): [0x66, 0],
    ('KPEQUAL', 'KEY_KPEQUAL'): [0x67, 0],
    ('F13', 'KEY_F13'): [0x68, 0],
    ('F14', 'KEY_F14'): [0x69, 0],
    ('F15', 'KEY_F15'): [0x6A, 0],
    ('F16', 'KEY_F16'): [0x6B, 0],
    ('F17', 'KEY_F17'): [0x6C, 0],
    ('F18', 'KEY_F18'): [0x6D, 0],
    ('F19', 'KEY_F19'): [0x6E, 0],
    ('F20', 'KEY_F20'): [0x6F, 0],
    ('F21', 'KEY_F21'): [0x70, 0],
    ('F22', 'KEY_F22'): [0x71, 0],
    ('F23', 'KEY_F23'): [0x72, 0],
    ('F24', 'KEY_F24'): [0x73, 0],
    ('OPEN', 'KEY_OPEN'): [0x74, 0],
    ('HELP', 'KEY_HELP'): [0x75, 0],
    ('PROPS', 'MENU', 'APP', 'CONTEXTMENU', 'KEY_PROPS'): [0x76, 0],
    ('FRONT', 'KEY_FRONT'): [0x77, 0],
    ('STOP', 'KEY_STOP'): [0x78, 0],
    ('AGAIN', 'KEY_AGAIN'): [0x79, 0],
    ('UNDO', 'KEY_UNDO'): [0x7A, 0],
    ('CUT', 'KEY_CUT'): [0x7B, 0],
    ('COPY', 'KEY_COPY'): [0x7C, 0],
    ('PASTE', 'KEY_PASTE'): [0x7D, 0],
    ('FIND', 'KEY_FIND'): [0x7E, 0],
    ('MUTE', 'KEY_MUTE'): [0x7F, 0],
    ('VOLUMEUP', 'KEY_VOLUMEUP'): [0x80, 0],
    ('VOLUMEDOWN', 'KEY_VOLUMEDOWN'): [0x81, 0],
    ('RETURN', 'KEY_RETURN'): [0x9E, 0],
    # ('LEFTCTRL', 'KEY_LEFTCTRL'): [0xE0, 0],
    # ('LEFTSHIFT', 'KEY_LEFTSHIFT'): [0xE1, 0],
    # ('LEFTALT', KEY_LEFTALT'): [0xE2, 0],
    # ('LEFTGUI', 'KEY_LEFTGUI'): [0xE3, 0],
    # ('RIGHTCTRL', 'KEY_RIGHTCTRL'): [0xE4, 0],
    # ('RIGHTSHIFT', 'KEY_RIGHTSHIFT'): [0xE5, 0],
    # ('RIGHTALT', 'KEY_RIGHTALT'): [0xE6, 0],
    # ('RIGHTGUI', 'KEY_RIGHTGUI'): [0xE7, 0],
    ('KEY_MODIFIER_LEFT_CTRL',
     'KEY_LEFTCONTROL',
     'KEY_LEFTCTRL',
     'KEY_CONTROL'
     'KEY_CTRL',
     'LEFTCONTROL',
     'LEFTCTRL',
     'CONTROL',
     'CTRL',): [0x01, 1],
    ('KEY_MODIFIER_LEFT_SHIFT',
     'KEY_LEFTSHIFT',
     'KEY_SHIFT',
     'LEFTSHIFT',
     'SHIFT'): [0x02, 1],
    ('KEY_MODIFIER_LEFT_ALT',
     'KEY_LEFTOPTION',
     'KEY_LEFTALT',
     'KEY_OPTION',
     'KEY_ALT',
     'LEFTOPTION',
     'LEFTALT',
     'OPTION',
     'ALT'): [0x04, 1],
    ('KEY_MODIFIER_LEFT_GUI',
     'KEY_COMMAND',
     'KEY_WINDOWS',
     'KEY_SUPER',
     'KEY_META',
     'KEY_GUI',
     'KEY_LEFTCOMMAND',
     'KEY_LEFTWINDOWS',
     'KEY_LEFTSUPER',
     'KEY_LEFTMETA',
     'KEY_LEFTGUI',
     'LEFTCOMMAND',
     'LEFTWINDOWS',
     'LEFTSUPER',
     'LEFTMETA',
     'LEFTGUI'
     'COMMAND',
     'WINDOWS',
     'SUPER',
     'META',
     'GUI'): [0x08, 1],
    ('KEY_MODIFIER_RIGHT_CTRL',
     'KEY_RIGHTCONTROL',
     'KEY_RIGHTCTRL',
     'RIGHTCONTROL',
     'RIGHTCTRL'): [0x10, 1],
    ('KEY_MODIFIER_RIGHT_SHIFT',
     'KEY_RIGHTSHIFT',
     'RIGHTSHIFT'): [0x20, 1],
    ('KEY_MODIFIER_RIGHT_ALT',
     'KEY_RIGHTOPTION',
     'KEY_RIGHTALT',
     'RIGHTOPTION',
     'RIGHTALT'): [0x40, 1],
    ('KEY_MODIFIER_RIGHT_GUI',
     'KEY_RIGHTCOMMAND',
     'KEY_RIGHTWINDOWS',
     'KEY_RIGHTSUPER',
     'KEY_RIGHTMETA',
     'KEY_RIGHTGUI',
     'RIGHTCOMMAND',
     'RIGHTWINDOWS',
     'RIGHTSUPER',
     'RIGHTMETA',
     'RIGHTGUI'): [0x80, 1],
    ('PLAYPAUSE', 'KEY_PLAYPAUSE'): [0xE8, 0],
    ('STOPCD', 'KEY_STOPCD'): [0xE9, 0],
    ('PREVIOUSSONG', 'KEY_PREVIOUSSONG'): [0xEA, 0],
    ('NEXTSONG', 'KEY_NEXTSONG'): [0xEB, 0],
    ('EJECTCD', 'KEY_EJECTCD'): [0xEC, 0],
    ('WWW', 'KEY_WWW'): [0xF0, 0],
    ('BACK', 'KEY_BACK'): [0xF1, 0],
    ('FORWARD', 'KEY_FORWARD'): [0xF2, 0],
    ('SCROLLUP', 'KEY_SCROLLUP'): [0xF5, 0],
    ('SCROLLDOWN', 'KEY_SCROLLDOWN'): [0xF6, 0],
    ('EDIT', 'KEY_EDIT'): [0xF7, 0]
}

#!/usr/bin/env python3


"""
Usage: {} <input> <output>

<input> should be a DuckieScript file and <output> will be an Arduino sketch
"""


import os
import sys
import fileinput
import textwrap
from data import keycodes
from data import repeat
from data import code


delay = 0
cmdtype = 0
commands = []
includes = []
defines = []
loop = []


def info(type, msg, **kwargs):
    lineno = fileinput.lineno()
    exit = kwargs.get('exit', None)
    path = os.path.basename(input_file)
    types = ['error', 'warning', 'info', 'screw up risk']
    message = '{}:{}: {}: {}'.format(path, lineno, types[type], msg)
    print(message)
    if exit:
        print('{}: compilation aborted.'.format(path))
        sys.exit(exit)


def getkey(keys):
    global commands
    keys = keys.split()
    modifier_keys = 0
    normal_keys = []
    arguments = []

    for key in keys:
        if not key.isupper() and len(key) is not 1:
            info(1, 'you should type all the special keys in uppercase')
        key = key.upper()

        try:
            key = [keycodes.get(code) for code in keycodes if key in code][0]
        except IndexError:
            info(0, 'unrecognized key: {}'.format(key), exit=5)

        if key[1]:
            modifier_keys |= key[0]
        else:
            normal_keys.append(key[0])

    if len(normal_keys) > 6:
        info(0, 'maximum number of non-modifier keys per line is 6', exit=4)

    for index in range(0, 6):
        try:
            arguments.append(normal_keys[index])
        except:
            arguments.append(0)

    arguments.append(modifier_keys)
    arguments = [format(byte, '#04x') for byte in arguments]

    commands.append('sendKey({},{},{},{},{},{},{});'.format(*arguments))

    return True


if len(sys.argv) is not 3:
    print(__doc__.format(sys.argv[0]))
    sys.exit(1)
elif not os.path.isfile(sys.argv[1]):
    print()
    print('Error: You must specify a valid input file')
    print(__doc__.format(sys.argv[0]))
    sys.exit(2)
else:
    output_file = sys.argv[2]
    input_file = sys.argv[1]

for line in fileinput.input([input_file]):
    base = line.split(maxsplit=1)
    base = map(str.strip, base)
    base = list(base)

    if len(base) is 2:
        command, options = base
    elif len(base) is 1:
        command = base[0]
        options = None
    else:
        continue

    if not command.isupper() and command not in ('#', '//', ';', '@', '%'):
        info(1, 'commands should be typed in uppercase')
        command = command.upper()

    if command in ('REM', 'COMMENT', '#', '//', ';'):
        commands.append('// {}'.format(options))
        needs_delay = False
        cmdtype = -1

    elif command in ('INCLUDE'):
        info(3, 'don\'t use {} unless you really need it'.format(command))
        if cmdtype > 0:
            info(0, 'you shouldn\'t mix {} in the code'.format(command), exit=1)
        includes.append('#include {}'.format(options))
        needs_delay = False
        cmdtype = 0

    elif command in ('DEFINE'):
        info(3, 'don\'t use {} unless you really need it'.format(command))
        if cmdtype > 1:
            info(0, 'you shouldn\'t mix {} in the code'.format(command), exit=1)
        defines.append('#define {}'.format(options))
        needs_delay = False
        cmdtype = 1

    elif command in ('LOOP', '@'):
        info(3, "don't use {} unless you really need it".format(command))
        if cmdtype > 2:
            info(0, 'you should put {} in the top of the program'.format(command), exit=1)
        loop.append(options)
        needs_delay = False
        cmdtype = 2

    elif command in ('ARDUINO', 'CODE', '%'):
        info(3, "don't use {} unless you really need it".format(command))
        commands.append(options)
        needs_delay = False
        cmdtype = 3

    elif command in ('DEFAULT_DELAY', 'DEFAULTDELAY'):
        if not options.isdigit():
            info(0, '{} only accepts integers'.format(command), exit=3)
        delay = int(options)
        needs_delay = False
        cmdtype = -1

    elif command in ('SLEEP', 'DELAY', 'WAIT'):
        if not options.isdigit():
            info(0, '{} only accepts integers'.format(command), exit=3)
        commands.append('delay({});'.format(options))
        needs_delay = False
        cmdtype = 3

    elif command in ('REPEAT'):
        if not options.isdigit():
            info(0, '{} only accepts integers'.format(command), exit=3)
        last_command = commands.splitlines()[-1]
        commands.append(repeat.format(options, last_command, delay))
        needs_delay = False
        cmdtype = 3

    elif command in ('STRING', 'TEXT', 'PRINT'):
        commands.append('Keyboard.print("{}");'.format(options.replace('"', '\\"')))
        needs_delay = True
        cmdtype = 3

    else:
        cmdtype = 3
        if not getkey(line):
            info(0, 'unrecognized command: {}'.format(command), exit=2)

    if delay > 0 and needs_delay:
        commands.append('delay({});'.format(delay))

commands = ['  ' + line for line in commands]
loop = ['  ' + line for line in loop]

code = code.format(includes='\n'.join(defines),
                   defines='\n'.join(defines),
                   setup='\n'.join(commands),
                   loop='\n'.join(loop))
code = code.strip()

try:
    with open(output_file, 'w') as output:
        output.write(code)
except Exception as e:
    info(0, '{}'.format(e), exit=6)

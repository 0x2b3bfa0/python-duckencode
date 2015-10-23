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
from data import code


delay = 0
cmdtype = 0
commands = ""
includes = ""
defines = ""
loop = ""


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
    normal_keys = []
    arguments = []
    modifiers = 0

    for key in keys:
        if not key.isupper() and len(key) is not 1:
            info(1, 'you should type all the special keys in uppercase')
        key = key.upper()

        try:
            key = [keycodes.get(code) for code in keycodes if key in code][0]
        except IndexError:
            info(0, 'unrecognized key: {}'.format(key), exit=127)

        if key[1]:
            modifiers |= key[0]
        else:
            normal_keys.append(key[0])

    if len(normal_keys) > 6:
        info(0, 'maximum number of non-modifier keys per line is 6', exit=126)

    for index in range(0,6):
        arguments.append(normal_keys.get(index, 0))
    arguments.append(modifiers)
    arguments = [format(byte, '#04x') for byte in arguments]
    commands += 'sendKey({},{},{},{},{},{},{});'.format(*arguments)
    commands += '\n'

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
    base = list(map(str.strip, line.split(maxsplit=1)))
    if len(base) is 2:
        command, options = base
    elif len(base) is 1:
        command = base[0]
        options = None
    else:
        continue

    if not command.isupper() and command not in ('#', '//', ';', '@', '%'):
        command = command.upper()
        info(1, 'commands should be typed in uppercase')

    if command in ('REM', 'COMMENT', '#', '//', ';'):
        commands += '// {}'.format(options)
        commands += '\n'
        needs_delay = False
        cmdtype = -1

    elif command in ('INCLUDE'):
        info(3, 'don\'t use {} unless you really need it'.format(command))
        if cmdtype > 0:
            info(0, 'you shouldn\'t mix {} in the code'.format(command), exit=5)
        includes += '#include {}'.format(options)
        includes += '\n'
        needs_delay = False
        cmdtype = 0

    elif command in ('DEFINE'):
        info(3, 'don\'t use {} unless you really need it'.format(command))
        if cmdtype > 1:
            info(0, 'you shouldn\'t mix {} in the code'.format(command), exit=5)
        includes += '#define {}'.format(options)
        includes += '\n'
        needs_delay = False
        cmdtype = 1

    elif command in ('LOOP', '@'):
        info(3, "don't use {} unless you really need it".format(command))
        if cmdtype > 2:
            info(0, 'you should put {} in the top of the program'.format(command), exit=5)
        loop += options
        loop += '\n'
        needs_delay = False
        cmdtype = 2

    elif command in ('ARDUINO', 'CODE', '%'):
        info(3, "don't use {} unless you really need it".format(command))
        commands += options
        commands += '\n'
        needs_delay = False
        cmdtype = 3

    elif command in ('DEFAULT_DELAY', 'DEFAULTDELAY'):
        if not options.isdigit():
            info(0, '{} only accepts integers'.format(command), exit=11)
        delay = int(options)
        needs_delay = False
        cmdtype = -1

    elif command in ('SLEEP', 'DELAY', 'WAIT'):
        if not options.isdigit():
            info(0, '{} only accepts integers'.format(command), exit=11)
        commands += 'delay({});'.format(options)
        commands += '\n'
        needs_delay = False
        cmdtype = 3

    elif command in ('REPEAT'):
        if not options.isdigit():
            info(0, '{} only accepts integers'.format(command), exit=11)
        last_command = commands.splitlines()[-1]
        commands += 'int i=0;'
        commands += '\n'
        commands += 'for(i; i<={}; i++) {{'.format(options)
        commands += '\n'
        commands += '  {}'.format(last_command)
        commands += '\n'
        commands += '  delay({});'.format(delay)
        commands += '\n'
        commands += '}'
        commands += '\n'
        needs_delay = False
        cmdtype = 3

    elif command in ('STRING', 'TEXT', 'PRINT'):
        commands += 'Keyboard.print("{}");'.format(options.replace('"', '\\"'))
        commands += '\n'
        needs_delay = True
        cmdtype = 3

    else:
        cmdtype = 3
        if not getkey(line):
            info(0, 'unrecognized command: {}'.format(command), exit=10)

    if delay > 0 and needs_delay:
        commands += 'delay({});'.format(delay)
        commands += '\n'

commands = "\n".join(["  " + i for i in commands.splitlines()])
loop = "\n".join(["  " + i for i in loop.splitlines()])

code = code.format(includes=includes,
                   defines=defines,
                   setup=commands,
                   loop=loop)
code = code.strip()

with open(output_file, 'w') as output:
    output.write(code)

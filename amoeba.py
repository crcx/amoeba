#!/usr/bin/env python

# Amoeba
# Copyright (c) 2013, 2015, 2016  Charles Childers
#
# This is an attempt to implement traditional something closer to a traditional
# Forth as an interface layer over Parable.
#
# TODO  (+ is done, - is remaining)
#
# + stack display
# + word listing
# + allow ending a session
# + forth style defintions
# + forth style comments
# + forth style conditionals
# + pep8 compliant source
# + don't import the entire parable namespace
#
# - multiline parsing
# - forth style loops
# - file i/o (port from ika?)
# - load stdlib extensions from a separate file?
#   (~/.parable/amoeba.p or amoeba.p in the cwd)
#

import os
import sys
import parable


def display_item(prefix, value):
    sys.stdout.write('\t' + prefix + str(value))


def dump_stack():
    """display the stack"""
    i = 0
    while i < len(parable.stack):
        tos = parable.stack_value_for(i)
        type = parable.stack_type_for(i)
        sys.stdout.write("\t" + str(i))
        if type == parable.TYPE_NUMBER:
            display_item('#', tos)
        elif type == parable.TYPE_CHARACTER:
            display_item('$', chr(tos))
        elif type == parable.TYPE_STRING:
            display_item('\'', parable.slice_to_string(tos) + '\'')
        elif type == parable.TYPE_POINTER:
            display_item('&', tos)
        elif type == parable.TYPE_REMARK:
            display_item('"', parable.slice_to_string(tos) + '"')
        elif type == parable.TYPE_FLAG:
            if tos == -1:
                display_item("", "true")
            elif tos == 0:
                display_item("", "false")
            else:
                display_item("", "malformed flag")
        else:
            display_item("", "unmatched type on the stack")
        sys.stdout.write("\n")
        i += 1


def dump_dict():
    """display named items"""
    l = ''
    for w in parable.dictionary_names():
        l = l + w + ' '
    sys.stdout.write(l)
    sys.stdout.write("\n")


def display_value():
    i = len(parable.stack) - 1
    if parable.types[i] == parable.TYPE_NUMBER:
        sys.stdout.write(str(parable.stack[i]))
    elif parable.types[i] == parable.TYPE_CHARACTER:
        sys.stdout.write(str(chr(parable.stack[i])))
    elif parable.types[i] == parable.TYPE_STRING:
        sys.stdout.write(parable.slice_to_string(parable.stack[i]))
    elif parable.types[i] == parable.TYPE_POINTER:
        sys.stdout.write('&' + str(parable.stack[i]))
    elif parable.types[i] == parable.TYPE_FLAG:
        if parable.stack[i] == -1:
            sys.stdout.write("true")
        elif parable.stack[i] == 0:
            sys.stdout.write("false")
        else:
            sys.stdout.write("malformed flag")


def opcodes(slice, offset, opcode):
    if opcode == 9000:
        display_value()
        parable.stack_pop()
    elif opcode == 9010:
        dump_stack()
    elif opcode == 9020:
        exit()
    elif opcode == 9030:
        dump_dict()
    elif opcode == 9040:
        s = parable.request_slice()
        i = 0
        for word in parable.dictionary_names():
            value = parable.string_to_slice(word)
            parable.store(value, s, i, parable.TYPE_STRING)
            i = i + 1
        parable.stack_push(s, parable.TYPE_POINTER)
    elif opcode == 3000:
        slot = 0
        i = 1
        while i < 8:
            if files[i] == 0:
                slot = i
            i = i + 1
        mode = parable.slice_to_string(parable.stack_pop())
        name = parable.slice_to_string(parable.stack_pop())
        if slot != 0:
            files[int(slot)] = open(name, mode)
        stack_push(slot, TYPE_NUMBER)
    elif opcode == 3001:
        slot = int(parable.stack_pop())
        files[slot].close()
        files[slot] = 0
    elif opcode == 3002:
        slot = int(parable.stack_pop())
        stack_push(ord(files[slot].read(1)), TYPE_NUMBER)
    elif opcode == 3003:
        slot = int(parable.stack_pop())
        files[slot].write(unichr(int(parable.stack_pop())))
    elif opcode == 3004:
        slot = int(parable.stack_pop())
        parable.stack_push(files[slot].tell(), TYPE_NUMBER)
    elif opcode == 3005:
        slot = int(parable.stack_pop())
        pos = int(parable.stack_pop())
        parable.stack_push(files[slot].seek(pos, 0), TYPE_NUMBER)
    elif opcode == 3006:
        slot = int(parable.stack_pop())
        at = files[slot].tell()
        files[slot].seek(0, 2) # SEEK_END
        parable.stack_push(files[slot].tell(), TYPE_NUMBER)
        files[slot].seek(at, 0) # SEEK_SET
    elif opcode == 3007:
        name = parable.slice_to_string(parable.stack_pop())
        if os.path.exists(name):
            os.remove(name)
    elif opcode == 3008:
        name = parable.slice_to_string(parable.stack_pop())
        if os.path.exists(name):
            stack_push(-1, TYPE_FLAG)
        else:
            stack_push(0, TYPE_FLAG)
    elif opcode == 4000:
        name = parable.slice_to_string(parable.stack_pop())
        print name
        if os.path.exists(name):
            lines = parable.condense_lines(open(name).readlines())
            for l in lines:
                s = rewrite(l)
                print s
                slice = parable.request_slice()
                parable.interpret(parable.compile(s, slice), opcodes)
    return offset


def rewrite(str):
    new = ""
    names = []
    cleaned = ' '.join(str.split())
    tokens = cleaned.split(' ')
    count = len(tokens)
    i = 0
    condc = 0
    conds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    while i < count:
        token = tokens[i]
        if token == ":":
            new = new + " ["
            i += 1
            names.append(tokens[i])
        elif token == ";":
            new = new + " ] '" + names.pop() + "' :"
        elif token == "if":
            new = new + " ["
            condc = condc + 1
            conds[condc] = 1
        elif token == "else":
            new = new + " ] ["
            conds[condc] = 2
        elif token == "then":
            if conds[condc] == 2:
                new = new + " ] if"
            else:
                new = new + " ] if-true"
            conds[condc] = 0
            condc = condc - 1
        elif token == "[']":
            new = new + " &"
            i += 1
            new = new + tokens[i]
        elif token == "(":
            new = new + ' "'
        elif token == ")":
            new = new + '"'
        elif parable.is_number(token):
            new = new + " #" + token
        elif token == "\\":
            new = new + ' "'
            i += 1
            while i < count:
                new = new + " " + tokens[i]
                i += 1
            new = new + '"'
        else:
            new = new + " " + token
        i += 1
    return new


def evaluate(s):
    parable.interpret(parable.compile(s, parable.request_slice()))

if __name__ == '__main__':
    print 'Amoeba, Copyright (c) 2013-2016 Charles Childers\n'
    parable.prepare_slices()
    parable.prepare_dictionary()
    parable.parse_bootstrap(open('stdlib.p').readlines())
    parable.parse_bootstrap(open('amoeba.p').readlines())

    while 1 == 1:
        sys.stdout.write("\nok ")
        sys.stdout.flush()

        src = sys.stdin.readline()

        if len(src) > 1:
            t = rewrite(src)
            print 'translate>> ' + t
            slice = parable.request_slice()
            parable.interpret(parable.compile(t, slice), opcodes)

        for e in parable.errors:
            sys.stdout.write(e)

        parable.clear_errors()
        sys.stdout.flush()

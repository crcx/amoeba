#!/usr/bin/env python

# Amoeba
# Copyright (c) 2013, 2015  Charles Childers
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
#
# - multiline parsing
# - forth style loops
# - don't import the entire parable namespace
# - file i/o (port from ika?)
# - load stdlib extensions from a separate file?
#   (~/.parable/amoeba.p or amoeba.p in the cwd)
#

import sys
from parable import *


def display_item(prefix, value):
    sys.stdout.write('\t' + prefix + str(value))


def dump_stack():
    """display the stack"""
    global stack
    i = 0
    while i < len(stack):
        tos = stack[i]
        type = types[i]
        sys.stdout.write("\t" + str(i))
        if type == TYPE_NUMBER:
            display_item('#', tos)
        elif type == TYPE_CHARACTER:
            display_item('$', chr(tos))
        elif type == TYPE_STRING:
            display_item('\'', slice_to_string(tos) + '\'')
        elif type == TYPE_POINTER:
            display_item('&', tos)
        elif type == TYPE_COMMENT:
            display_item('"', slice_to_string(tos) + '"')
        elif type == TYPE_FLAG:
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
    for w in dictionary_names:
        l = l + w + ' '
    sys.stdout.write(l)
    sys.stdout.write("\n")


def display_value():
    global stack, types
    i = len(stack) - 1
    if types[i] == TYPE_NUMBER:
        sys.stdout.write(str(stack[i]))
    elif types[i] == TYPE_CHARACTER:
        sys.stdout.write(str(chr(stack[i])))
    elif types[i] == TYPE_STRING:
        sys.stdout.write(slice_to_string(stack[i]))
    elif types[i] == TYPE_POINTER:
        sys.stdout.write('&' + str(stack[i]))
    elif types[i] == TYPE_FLAG:
        if stack[i] == -1:
            sys.stdout.write("true")
        elif stack[i] == 0:
            sys.stdout.write("false")
        else:
            sys.stdout.write("malformed flag")


def opcodes(slice, offset, opcode):
    if opcode == 9000:
        display_value()
        stack_pop()
    elif opcode == 9010:
        dump_stack()
    elif opcode == 9020:
        exit()
    elif opcode == 9030:
        dump_dict()
    elif opcode == 9040:
        s = request_slice()
        i = 0
        for word in dictionary_names:
            store(string_to_slice(word), s, i, TYPE_STRING)
            i = i + 1
        stack_push(s, TYPE_POINTER)

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
            new = new + " ] '" + names.pop() + "' define"
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
        elif is_number(token):
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


if __name__ == '__main__':
    print 'Amoeba, Copyright (c) 2015 Charles Childers\n'
    prepare_slices()
    prepare_dictionary()
    parse_bootstrap(open('stdlib.p').readlines())

    interpret(compile("[ \"v-\"  `9000 ] '?' define", request_slice()))
    interpret(compile("[ \"-\"   `9010 ] '.s' define", request_slice()))
    interpret(compile("[ \"-\"   `9020 ] 'bye' define", request_slice()))
    interpret(compile("[ \"-\"   `9030 ] 'words' define", request_slice()))

    while 1 == 1:
        sys.stdout.write("\nok ")
        sys.stdout.flush()

        src = sys.stdin.readline()

        if len(src) > 1:
            t = rewrite(src)
            print 'translate>> ' + t
            interpret(compile(rewrite(src), request_slice()), opcodes)

        for e in errors:
            sys.stdout.write(e)

        clear_errors()
        sys.stdout.flush()

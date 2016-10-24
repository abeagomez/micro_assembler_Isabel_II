#!/usr/bin/env python3

from __future__ import print_function

__author__ = 'Amalia Gómez Marcheco'

import sys
import re
import os

code = '00000000000000000000000000000000'

labels = {}

def nop(inst):
    return '0' * 32

def mov(inst):
    inst = inst.lower()
    if inst[3] == 'r':
        i = 3
        while i < len(inst):
            if inst[i] == '[':
                exp = removeRS(inst)
                return regRegOrRegConst('000100', '000011', exp)
            i += 1
        return regRegOrRegConst('000010', '000001', inst)
    elif inst[3] == '[':
        if inst[4] == 'r':
            exp = removeRS(inst)
            return CmpLikeRegRegOrRegConst('000110', '000101', exp)
        else:
            exp = removeRS(inst)
            cons = constant(exp,False)
            return '000111' + '0'*4 + registersManager(1,exp)[0] + '00' + cons


def removeRS(inst):
    i = 0
    while(i<len(inst)):
        if inst[i] in ('[', ']'):
            inst = inst[:i]+inst[i+1:]
        i += 1
    return inst


def push(inst):
    opcode = '001000'
    l = oneRegisterInstruction(opcode, inst)
    return opcode + '0'*4 + l[6:10] + '0'*18

def pop(inst):
    opcode = '001001'
    return oneRegisterInstruction(opcode, inst)


def call(inst):
    return regOrConst('001011', '001010', inst)


def ret(inst):
    opcode = '001100'
    return opcode + code[6:]


def jmp(inst):
    return regOrConst('001110', '001101', inst)


def jz(inst):
    return CondJump('010000', inst)


def jn(inst):
    return CondJump('010001', inst)


def je(inst):
    return CondJump('010010', inst)


def jne(inst):
    return CondJump('010011', inst)


def jgt(inst):
    return CondJump('010100', inst)


def jge(inst):
    return CondJump('010101', inst)


def jlt(inst):
    return CondJump('010110', inst)


def jle(inst):
    return CondJump('010111', inst)


def tty(inst):
    return regOrConst('011000', '011001', inst)


def kbd(inst):
    opcode = '011010'
    l = oneRegisterInstruction(opcode, inst)
    return opcode + l[0] + code[10:]


def add(inst):
    return threeRegOrTwoRegConst('100001', '100000', inst)


def sub(inst):
    return threeRegOrTwoRegConst('100011', '100010', inst)


def mult(inst):
    return threeRegOrTwoRegConst('100101', '100100', inst)


def div(inst):
    return threeRegOrTwoRegConst('100111', '100110', inst)


def mod(inst):
    return threeRegOrTwoRegConst('101001', '101000', inst)


def And(inst):
    return threeRegOrTwoRegConst('101011', '101010', inst)


def Or(inst):
    return threeRegOrTwoRegConst('101101', '101100', inst)


def Xor(inst):
    return threeRegOrTwoRegConst('101111', '101110', inst)


def shl(inst):
    return regRegOrRegConst('110001', '110000', inst)


def rol(inst):
    return regRegOrRegConst('110011', '110010', inst)


def cmp(inst):
    return CmpLikeRegRegOrRegConst('110101', '110100', inst)


def CmpLikeRegRegOrRegConst(opcodeA, opcodeB, inst):
    const = constant(inst, True)
    if const is None:
        a = twoRegistersInstructions(opcodeA, inst)
        return a[:6] + '0'*4 + a[6:14] + '0'*14
    else:
        a = oneRegisterInstruction(opcodeB, inst)
        return a[:6] + '0'*4 + a[6:10] + '0'*2 + const


def neg(inst):
    opcode = '110110'
    return twoRegistersInstructions(opcode, inst)


def Not(inst):
    opcode = '110111'
    return twoRegistersInstructions(opcode, inst)


def rnd(inst):
    opcode = '111000'
    return oneRegisterInstruction(opcode, inst[3:])


def halt(inst):
    opcode = '111100'
    return opcode + code[len(opcode):]

def data(inst):
    reo = re.compile(r'^data(?:(?P<dk>-?\d+)|(?P<hk>-?0x[0-9a-f]+))$', re.IGNORECASE)
    mo = reo.match(inst)
    if mo is None:
        return None
    
    if mo.group('dk') is not None:
        d = int(mo.group('dk'))
    elif mo.group('hk') is not None:
        d = int(mo.group('hk'), 16)
    else:
        return None
        
    if d < 0:
        return bin(2 ** 32 + d)[-32:]
    else:
        return bin(d)[2:].rjust(32, '0')

def twoRegistersInstructions(opcode, inst):
    l = registersManager(2, inst)
    return opcode + l[0] + l[1] + code[14:]


def oneRegisterInstruction(opcode, inst):
    l = registersManager(1, inst)
    return opcode + l[0] + '0'*22


def threeRegistersInstructions(opcode, inst):
    l = registersManager(3, inst)
    return opcode + l[0] + l[1] + l[2] + code[18:]


def regOrConst(opcodeR, opcodeC, inst):
    const = constant(inst, False)
    if const is None:
        a = oneRegisterInstruction(opcodeR, inst)
        return a[:6] + '0' * 4 + a[6:10] + '0' * 18
    else:
        return opcodeC + '0' * 10 + const


def regRegOrRegConst(opcodeA, opcodeB, inst):
    const = constant(inst, True)
    if const is None:
        return twoRegistersInstructions(opcodeA, inst)
    else:
        a = oneRegisterInstruction(opcodeB, inst)
        return a[:16] + const


def threeRegOrTwoRegConst(opcodeA, opcodeB, inst):
    const = constant(inst, True)
    if const is None:
        return threeRegistersInstructions(opcodeA, inst)
    else:
        a = twoRegistersInstructions(opcodeB, inst)
        return a[:16] + const


def constant(inst, wreg):
    if not wreg and re.match(r'\D+r\d+', inst, re.IGNORECASE):
        return None
    c = inst.find('-')
    exp = r'[\D]+([-]*([0-9]+))'
    if wreg:
        exp = r'[\S]+,(-*[0-9]+)'
    p = re.compile(exp, re.IGNORECASE)
    m = p.match(inst)
    if m:
        x = int(m.group(1))
        if c > -1:
            if wreg == False:
                x = 0 - int(m.group(1))
        a = bin(2**16+x)[-16:]
        return a
    return None


def regToBinary(m, i):
    l = []
    if m:
        for index in range(1, i + 1):
            a = bin(int(m.group(index)))[2:]
            if len(a) > 4:
                raise Exception("Valor de registro no valido")
            l.append('0' * (4 - len(a)) + a)
        return l

    else:
        raise Exception("Comando no valido")


def reg(ins, exp):
    p = re.compile(exp, re.IGNORECASE)
    m = p.match(ins)
    return m


def registersManager(regNum, inst):
    oneReg = '[\S]*r([0-9]+)[\S]*'
    twoReg = '[\S]*r([0-9]+)[\S]*r([0-9]+)[\S]*'
    threeReg = '[\S]*r([0-9]+)[\S]*r([0-9]+)[\S]*r([0-9]+)[/S]*'
    if (regNum == 1):
        a = regToBinary(reg(inst, oneReg), 1)
        return a
    elif (regNum == 2):
        a = regToBinary(reg(inst, twoReg), 2)
        return a
    elif (regNum == 3):
        a = regToBinary(reg(inst, threeReg), 3)
        return a
    else:
        return 0


def instructionSelector(inst):
    """

    :param inst:assembler instruction
    :return: {str} binary instruction
    """
    for i, k in dic.items():
        p = re.compile(i, re.IGNORECASE)
        inst = spfilter(inst.lower())
        m = p.match(inst)
        if m:
            return k(inst.replace(' ', ''))

    return None 

def CondJump(opcode, inst):
    return opcode + '0' * 10 + constant(inst, False)


def spfilter(inst):
    return inst.replace('sp', 'r15')


def assembler(opath):
    global bank0, bank1, bank2, bank3
    f = open(opath)
    i = 0
    addr = 0
    for linen, line in enumerate(f, 1):
        comment = line.find('#')
        if comment > -1:
            line = line[:comment]
        line = line.strip()
        if len(line) == 0:
            continue

        if line.endswith(':'):
            label = line[:-1]
            if label in labels:
                raise Exception('Duplicate label: {}'.format(label))
            labels[label] = addr
            continue
        addr += 4

    f.seek(0)
    # print(labels)

    addr = 0
    for linen, line in enumerate(f, 1):
        original_line = line
        comment = line.find('#')
        if comment > -1:
            line = line[:comment]
        line = line.strip()
        if len(line) == 0:
            continue
        
        if line.endswith(':'):
            continue

        if ':' in line:
            op,rest = line.split(None, 1)
            if op.lower() == 'call':
                a = labels[rest[1:]]
            if op.lower() in {'jmp','jz','je','jne','jn','jgt','jge','jlt','jle'}:
                a = labels[rest[1:]] - addr 
            line = '{} {}'.format(op,a)

        # print(line)

        binStr = instructionSelector(line)
        if binStr is None:
            print('Syntax error at line', linen, ':', line)
            exit(1)
        
        a = hex(int(binStr[:16], 2))[2:]
        b = hex(int(binStr[16:], 2))[2:]

        if len(sys.argv) > 3 and sys.argv[3] == '-d':
            print(original_line.strip())
            print(line)
            print(binStr)
            print('{:04x}{:04x}'.format(int(a,16),int(b,16)))
            print()

        if i == 0:
            bank0.append(b)
            bank1.append(a)
            i = 2
        else:
            bank2.append(b)
            bank3.append(a)
            i = 0

        addr += 4
    f.close()

    for bank_name, bank in zip([ 'Bank0', 'Bank1', 'Bank2', 'Bank3' ],
                               [  bank0 ,  bank1 ,  bank2 ,  bank3  ]):
        # print(bank)
        try:
            outputdir = sys.argv[2]
        except:
            outputdir = '.'
        bf = open(os.path.join(outputdir,bank_name), 'w')
        bf.write('v2.0 raw\n')
        bf.write(' '.join(bank))
        bf.close()

bank0 = []
bank1 = []
bank2 = []
bank3 = []

dic = {'nop': nop,
       'mov': mov,
       'push': push,
       'pop': pop,
       'call': call,
       'ret': ret,
       'jmp': jmp,
       'jz': jz,
       'je': je,
       'jne': jne,
       'jn[^e]': jn,
       'jgt': jgt,
       'jge': jge,
       'jlt': jlt,
       'jle': jle,
       'tty': tty,
       'kbd': kbd,
       'add': add,
       'sub': sub,
       'mul': mult,
       'div': div,
       'mod': mod,
       'and': And,
       'or' : Or,
       'xor': Xor,
       'shl': shl,
       'rol': rol,
       'cmp': cmp,
       'neg': neg,
       'not': Not,
       'rnd': rnd,
       'halt': halt,
       'data' : data }

assembler(sys.argv[1])


#tester = {'CALL 1026':  '001010 0000 0000 000000010000000010',
#           "POP R9":     '001001 1001 0000 000000000000000000',
#'PUSH R9':    '001000 0000 1001 000000000000000000',
#'MOV [R1], R2':  '000110 0000 0001 001000000000000000',
#'MOV [R9], SP'  :  '000110 0000 1001 111100000000000000',
#'MOV [R1],  4'  : '000101 0000 0001 000000000000000100',
#'MOV [R1], -1'  :  '000101 0000 0001 001111111111111111',
#'MOV R3,[R4]'   :  '000100 0011 0100 000000000000000000',
#'MOV R9,[R10]'  :  '000100 1001 1010 000000000000000000',
#'MOV R3,[6]'  :  '000011 0011 0000 000000000000000110',
#'MOV R9,[0]'  :  '000011 1001 0000 000000000000000000'}



#for i in range(0, len(tester)):
#    a = tester.keys()[i]
#    b = tester.values()[i]
#    print a
#    print instructionSelector(a)
#    print b.replace(' ', '')
#    if instructionSelector(a) == b.replace(' ', ''):
#        print 'true'
#    print i

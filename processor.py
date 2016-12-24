import sys


class Processor:

    def __init__(self):
        self._maxMemory = 2**15
        self._get = {0: self.halt, 21: self.noop, 19: self.out, 6: self.jmp,
                     7: self.jt, 8: self.jf, 1: self.set, 9: self.add,
                     4: self.eq, 2: self.push, 3: self.pop, 5: self.gt,
                     12: self.bit_and, 13: self.bit_or, 14: self.bit_not,
                     17: self.call, 18: self.ret, 10: self.mult,
                     11: self.mod, 15: self.rmem, 16: self.wmem,
                     20: self.readIn}
        self._nArg = {0: 0, 21: 0, 19: 1, 6: 1, 7: 2, 8: 2, 1: 2, 9: 3,
                      4: 3, 2: 1, 3: 1, 5: 3, 12: 3, 13: 3, 14: 2, 17: 1,
                      18: 0, 10: 3, 11: 3, 15: 2, 16: 2, 20: 1}

        self._main = []
        self._registers = {}
        self._stack = []
        self._pc = 0
        self._inputString = []
        self.initRegisters()
        self.initMemory()

    def writeToRegister(self, reg, val):
        if 32768 <= reg <= 32775:
            self._registers[reg % self._maxMemory] = val
        else:
            print("Invalid register", reg, val)

    def readIn(self, args):
        if len(self._inputString) == 0:
            self._inputString = list(input() + "\n")
        self.writeToRegister(args[0], ord(self._inputString.pop(0)))
        self._pc += 2

    def set(self, args):
        self.writeToRegister(args[0], self.getValue(args[1]))
        self._pc += 3

    def bit_and(self, args):
        self.writeToRegister(args[0], self.getValue(args[1]) &
                             self.getValue(args[2]))
        self._pc += 4

    def bit_or(self, args):
        self.writeToRegister(args[0], self.getValue(args[1]) |
                             self.getValue(args[2]))
        self._pc += 4

    def bit_not(self, args):
        self.writeToRegister(args[0], ~self.getValue(args[1]) & 0x7FFF)
        self._pc += 3

    def gt(self, args):
        if self.getValue(args[1]) > self.getValue(args[2]):
            self.writeToRegister(args[0], 1)
        else:
            self.writeToRegister(args[0], 0)
        self._pc += 4

    def push(self, args):
        self._stack.append(self.getValue(args[0]))
        self._pc += 2

    def pop(self, args):
        if len(self._stack) > 0:
            self.writeToRegister(args[0], self._stack.pop())
        else:
            self.halt(None)
        self._pc += 2

    def add(self, args):
        self.writeToRegister(args[0], (self.getValue(args[1]) +
                                       self.getValue(args[2])) %
                             self._maxMemory)
        self._pc += 4

    def mult(self, args):
        self.writeToRegister(args[0], (self.getValue(args[1]) *
                                       self.getValue(args[2])) %
                             self._maxMemory)
        self._pc += 4

    def mod(self, args):
        self.writeToRegister(args[0], self.getValue(args[1]) %
                             self.getValue(args[2]))
        self._pc += 4

    def eq(self, args):
        if self.getValue(args[1]) == self.getValue(args[2]):
            self.writeToRegister(args[0], 1)
        else:
            self.writeToRegister(args[0], 0)
        self._pc += 4

    def call(self, args):
        self._stack.append(self._pc + 2)
        self._pc = self.getValue(args[0])

    def ret(self, args):
        if len(self._stack) > 0:
            self._pc = self._stack.pop()
        else:
            self.halt(None)

    def halt(self, args):
        sys.exit(0)

    def noop(self, args):
        self._pc += 1

    def out(self, args):
        print(chr(self.getValue(args[0])), end="")
        self._pc += 2

    def jmp(self, args):
        self._pc = self.getValue(args[0])

    def jt(self, args):
        if self.getValue(args[0]) != 0:
            self._pc = self.getValue(args[1])
        else:
            self._pc += 3

    def jf(self, args):
        if self.getValue(args[0]) == 0:
            self._pc = self.getValue(args[1])
        else:
            self._pc += 3

    def rmem(self, args):
        self.writeToRegister(args[0], self._main[self.getValue(args[1])])
        self._pc += 3

    def wmem(self, args):
        self._main[self.getValue(args[0])] = self.getValue(args[1])
        self._pc += 3

    def loadProgram(self, i, hword):
        self._main[self.getValue(i)] = hword

    def initRegisters(self):
        for i in range(8):
            self._registers[i] = 0

    def initMemory(self):
        self._main = [0 for i in range(self._maxMemory)]

    def doOperation(self):
        op = self._main[self._pc]

        if op not in self._get:
            print("{}: Opcode {} not implemented yet!".format(self._pc, op))
            self.halt(None)
        n = self._nArg[op]
        a = [self._main[self._pc + i] for i in range(1, self._nArg[op] + 1)]
        self._get[op](a)

    def getValue(self, a):
        if a < self._maxMemory:
            return a
        elif a < self._maxMemory + 8:
            return self._registers[a % self._maxMemory]
        else:
            print("Invalid value/register")
            self.halt(None)

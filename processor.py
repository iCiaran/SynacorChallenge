import sys


class Processor:

    def __init__(self):
        self._maxMemory = 2**15
        self._get = {0: self.halt, 21: self.noop, 19: self.out, 6: self.jmp,         7: self.jt, 8: self.jf, 1: self.set}
        self._nArg = {0: 0, 21: 0, 19: 1, 6: 1, 7: 2, 8:2, 1:2}
        self._main = []
        self._registers = {}
        self._pc = 0
        self.initRegisters()
        self.initMemory()

    def set(self, args):
        self._registers[args[0] % self._maxMemory] = self.getValue(args[1])
        print(self._registers)
        self._pc += 3

    def halt(self, args):
        sys.exit(0)

    def noop(self, args):
        self._pc += 1

    def out(self, args):
        print(chr(args[0]), end="")
        self._pc += 2

    def jmp(self, args):
        #print("jmp,", args)
        self._pc = self.getValue(args[0])

    def jt(self, args):
        #print(self.getValue(args[0]))
        if self.getValue(args[0]) != 0:
            self._pc = self.getValue(args[1])
        else:
            self._pc += 3

    def jf(self, args):
        if self.getValue(args[0]) == 0:
            self._pc = self.getValue(args[1])
        else:
            self._pc += 3

    def wmem(self, args):
        self._main[self.getValue(args[0])] = self.getValue(
                                                                    args[1])
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
            self._pc += 1
            sys.exit(0)
        n = self._nArg[op]
        a = [self._main[self._pc + i] for i in range(1, self._nArg[op] + 1)]
        #print(self._pc, op, n, a)
        self._get[op](a)

    def getValue(self, a):
        if a < self._maxMemory:
            return a
        elif a < self._maxMemory + 8:
            #print("Accessed Register", self._pc, a % self._maxMemory)
            return self._registers[a % self._maxMemory]
        else:
            print("Invalid value/register")
            system.exit(0)

    

from dataclasses import dataclass
from collections import OrderedDict
from collections.abc import Callable

@dataclass
class INSTRUCTION:
    name: str
    operate: Callable
    addrmode: Callable
    cycles: int = 0


C = 0
Z = 1
I = 2
D = 3
B = 4
U = 5
V = 6
N = 7

# TODO: Overflow detect all sets !IMPORTANT!

class olc6502:    
    def __init__(self):
        self.bus = None
        self.a      = 0x00
        self.x      = 0x00
        self.y      = 0x00
        self.stkp   = 0x00
        self.pc     = 0x0000
        self.status = 0x00

        self.fetched  = 0x00
        self.addr_abs = 0x0000
        self.addr_rel = 0x0000
        self.opcode   = 0x00
        self.cycles   = 0
        self.temp     = 0

        self.lookup = [
            INSTRUCTION("BRK", self.BRK, self.IMM, 7), INSTRUCTION("ORA", self.ORA, self.IZX, 6), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("???", self.NOP, self.IMP, 3), INSTRUCTION("ORA", self.ORA, self.ZP0, 3), INSTRUCTION("ASL", self.ASL, self.ZP0, 5), INSTRUCTION("???", self.XXX, self.IMP, 5), INSTRUCTION("PHP", self.PHP, self.IMP, 3), INSTRUCTION("ORA", self.ORA, self.IMM, 2), INSTRUCTION("ASL", self.ASL, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("ORA", self.ORA, self.ABS, 4), INSTRUCTION("ASL", self.ASL, self.ABS, 6), INSTRUCTION("???", self.XXX, self.IMP, 6),
            INSTRUCTION("BPL", self.BPL, self.REL, 2), INSTRUCTION("ORA", self.ORA, self.IZY, 5), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("ORA", self.ORA, self.ZPX, 4), INSTRUCTION("ASL", self.ASL, self.ZPX, 6), INSTRUCTION("???", self.XXX, self.IMP, 6), INSTRUCTION("CLC", self.CLC, self.IMP, 2), INSTRUCTION("ORA", self.ORA, self.ABY, 4), INSTRUCTION("???", self.NOP, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 7), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("ORA", self.ORA, self.ABX, 4), INSTRUCTION("ASL", self.ASL, self.ABX, 7), INSTRUCTION("???", self.XXX, self.IMP, 7),
            INSTRUCTION("JSR", self.JSR, self.ABS, 6), INSTRUCTION("AND", self.AND, self.IZX, 6), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("BIT", self.BIT, self.ZP0, 3), INSTRUCTION("AND", self.AND, self.ZP0, 3), INSTRUCTION("ROL", self.ROL, self.ZP0, 5), INSTRUCTION("???", self.XXX, self.IMP, 5), INSTRUCTION("PLP", self.PLP, self.IMP, 4), INSTRUCTION("AND", self.AND, self.IMM, 2), INSTRUCTION("ROL", self.ROL, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("BIT", self.BIT, self.ABS, 4), INSTRUCTION("AND", self.AND, self.ABS, 4), INSTRUCTION("ROL", self.ROL, self.ABS, 6), INSTRUCTION("???", self.XXX, self.IMP, 6),
            INSTRUCTION("BMI", self.BMI, self.REL, 2), INSTRUCTION("AND", self.AND, self.IZY, 5), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("AND", self.AND, self.ZPX, 4), INSTRUCTION("ROL", self.ROL, self.ZPX, 6), INSTRUCTION("???", self.XXX, self.IMP, 6), INSTRUCTION("SEC", self.SEC, self.IMP, 2), INSTRUCTION("AND", self.AND, self.ABY, 4), INSTRUCTION("???", self.NOP, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 7), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("AND", self.AND, self.ABX, 4), INSTRUCTION("ROL", self.ROL, self.ABX, 7), INSTRUCTION("???", self.XXX, self.IMP, 7),
            
            INSTRUCTION("RTI", self.RTI, self.IMP, 6), INSTRUCTION("EOR", self.EOR, self.IZX, 6), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("???", self.NOP, self.IMP, 3), INSTRUCTION("EOR", self.EOR, self.ZP0, 3), INSTRUCTION("LSR", self.LSR, self.ZP0, 5), INSTRUCTION("???", self.XXX, self.IMP, 5), INSTRUCTION("PHA", self.PHA, self.IMP, 3), INSTRUCTION("EOR", self.EOR, self.IMM, 2), INSTRUCTION("LSR", self.LSR, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("JMP", self.JMP, self.ABS, 3), INSTRUCTION("EOR", self.EOR, self.ABS, 4), INSTRUCTION("LSR", self.LSR, self.ABS, 6), INSTRUCTION("???", self.XXX, self.IMP, 6),
            INSTRUCTION("BVC", self.BVC, self.REL, 2), INSTRUCTION("EOR", self.EOR, self.IZY, 5), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("EOR", self.EOR, self.ZPX, 4), INSTRUCTION("LSR", self.LSR, self.ZPX, 6), INSTRUCTION("???", self.XXX, self.IMP, 6), INSTRUCTION("CLI", self.CLI, self.IMP, 2), INSTRUCTION("EOR", self.EOR, self.ABY, 4), INSTRUCTION("???", self.NOP, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 7), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("EOR", self.EOR, self.ABX, 4), INSTRUCTION("LSR", self.LSR, self.ABX, 7), INSTRUCTION("???", self.XXX, self.IMP, 7),
            INSTRUCTION("RTS", self.RTS, self.IMP, 6), INSTRUCTION("ADC", self.ADC, self.IZX, 6), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("???", self.NOP, self.IMP, 3), INSTRUCTION("ADC", self.ADC, self.ZP0, 3), INSTRUCTION("ROR", self.ROR, self.ZP0, 5), INSTRUCTION("???", self.XXX, self.IMP, 5), INSTRUCTION("PLA", self.PLA, self.IMP, 4), INSTRUCTION("ADC", self.ADC, self.IMM, 2), INSTRUCTION("ROR", self.ROR, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("JMP", self.JMP, self.IND, 5), INSTRUCTION("ADC", self.ADC, self.ABS, 4), INSTRUCTION("ROR", self.ROR, self.ABS, 6), INSTRUCTION("???", self.XXX, self.IMP, 6),
            INSTRUCTION("BVS", self.BVS, self.REL, 2), INSTRUCTION("ADC", self.ADC, self.IZY, 5), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("ADC", self.ADC, self.ZPX, 4), INSTRUCTION("ROR", self.ROR, self.ZPX, 6), INSTRUCTION("???", self.XXX, self.IMP, 6), INSTRUCTION("SEI", self.SEI, self.IMP, 2), INSTRUCTION("ADC", self.ADC, self.ABY, 4), INSTRUCTION("???", self.NOP, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 7), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("ADC", self.ADC, self.ABX, 4), INSTRUCTION("ROR", self.ROR, self.ABX, 7), INSTRUCTION("???", self.XXX, self.IMP, 7),
            
            INSTRUCTION("???", self.NOP, self.IMP, 2), INSTRUCTION("STA", self.STA, self.IZX, 6), INSTRUCTION("???", self.NOP, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 6), INSTRUCTION("STY", self.STY, self.ZP0, 3), INSTRUCTION("STA", self.STA, self.ZP0, 3), INSTRUCTION("STX", self.STX, self.ZP0, 3), INSTRUCTION("???", self.XXX, self.IMP, 3), INSTRUCTION("DEY", self.DEY, self.IMP, 2), INSTRUCTION("???", self.NOP, self.IMP, 2), INSTRUCTION("TXA", self.TXA, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("STY", self.STY, self.ABS, 4), INSTRUCTION("STA", self.STA, self.ABS, 4), INSTRUCTION("STX", self.STX, self.ABS, 4), INSTRUCTION("???", self.XXX, self.IMP, 4),
            INSTRUCTION("BCC", self.BCC, self.REL, 2), INSTRUCTION("STA", self.STA, self.IZY, 6), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 6), INSTRUCTION("STY", self.STY, self.ZPX, 4), INSTRUCTION("STA", self.STA, self.ZPX, 4), INSTRUCTION("STX", self.STX, self.ZPY, 4), INSTRUCTION("???", self.XXX, self.IMP, 4), INSTRUCTION("TYA", self.TYA, self.IMP, 2), INSTRUCTION("STA", self.STA, self.ABY, 5), INSTRUCTION("TXS", self.TXS, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 5), INSTRUCTION("???", self.NOP, self.IMP, 5), INSTRUCTION("STA", self.STA, self.ABX, 5), INSTRUCTION("???", self.XXX, self.IMP, 5), INSTRUCTION("???", self.XXX, self.IMP, 5),
            INSTRUCTION("LDY", self.LDY, self.IMM, 2), INSTRUCTION("LDA", self.LDA, self.IZX, 6), INSTRUCTION("LDX", self.LDX, self.IMM, 2), INSTRUCTION("???", self.XXX, self.IMP, 6), INSTRUCTION("LDY", self.LDY, self.ZP0, 3), INSTRUCTION("LDA", self.LDA, self.ZP0, 3), INSTRUCTION("LDX", self.LDX, self.ZP0, 3), INSTRUCTION("???", self.XXX, self.IMP, 3), INSTRUCTION("TAY", self.TAY, self.IMP, 2), INSTRUCTION("LDA", self.LDA, self.IMM, 2), INSTRUCTION("TAX", self.TAX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("LDY", self.LDY, self.ABS, 4), INSTRUCTION("LDA", self.LDA, self.ABS, 4), INSTRUCTION("LDX", self.LDX, self.ABS, 4), INSTRUCTION("???", self.XXX, self.IMP, 4), 
		    INSTRUCTION("BCS", self.BCS, self.REL, 2), INSTRUCTION("LDA", self.LDA, self.IZY, 5), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 5), INSTRUCTION("LDY", self.LDY, self.ZPX, 4), INSTRUCTION("LDA", self.LDA, self.ZPX, 4), INSTRUCTION("LDX", self.LDX, self.ZPY, 4), INSTRUCTION("???", self.XXX, self.IMP, 4), INSTRUCTION("CLV", self.CLV, self.IMP, 2), INSTRUCTION("LDA", self.LDA, self.ABY, 4), INSTRUCTION("TSX", self.TSX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 4), INSTRUCTION("LDY", self.LDY, self.ABX, 4), INSTRUCTION("LDA", self.LDA, self.ABX, 4), INSTRUCTION("LDX", self.LDX, self.ABY, 4), INSTRUCTION("???", self.XXX, self.IMP, 4), 
    		
            INSTRUCTION("CPY", self.CPY, self.IMM, 2), INSTRUCTION("CMP", self.CMP, self.IZX, 6), INSTRUCTION("???", self.NOP, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("CPY", self.CPY, self.ZP0, 3), INSTRUCTION("CMP", self.CMP, self.ZP0, 3), INSTRUCTION("DEC", self.DEC, self.ZP0, 5), INSTRUCTION("???", self.XXX, self.IMP, 5), INSTRUCTION("INY", self.INY, self.IMP, 2), INSTRUCTION("CMP", self.CMP, self.IMM, 2), INSTRUCTION("DEX", self.DEX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("CPY", self.CPY, self.ABS, 4), INSTRUCTION("CMP", self.CMP, self.ABS, 4), INSTRUCTION("DEC", self.DEC, self.ABS, 6), INSTRUCTION("???", self.XXX, self.IMP, 6), 
    		INSTRUCTION("BNE", self.BNE, self.REL, 2), INSTRUCTION("CMP", self.CMP, self.IZY, 5), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("CMP", self.CMP, self.ZPX, 4), INSTRUCTION("DEC", self.DEC, self.ZPX, 6), INSTRUCTION("???", self.XXX, self.IMP, 6), INSTRUCTION("CLD", self.CLD, self.IMP, 2), INSTRUCTION("CMP", self.CMP, self.ABY, 4), INSTRUCTION("NOP", self.NOP, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 7), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("CMP", self.CMP, self.ABX, 4), INSTRUCTION("DEC", self.DEC, self.ABX, 7), INSTRUCTION("???", self.XXX, self.IMP, 7), 
    		INSTRUCTION("CPX", self.CPX, self.IMM, 2), INSTRUCTION("SBC", self.SBC, self.IZX, 6), INSTRUCTION("???", self.NOP, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("CPX", self.CPX, self.ZP0, 3), INSTRUCTION("SBC", self.SBC, self.ZP0, 3), INSTRUCTION("INC", self.INC, self.ZP0, 5), INSTRUCTION("???", self.XXX, self.IMP, 5), INSTRUCTION("INX", self.INX, self.IMP, 2), INSTRUCTION("SBC", self.SBC, self.IMM, 2), INSTRUCTION("NOP", self.NOP, self.IMP, 2), INSTRUCTION("???", self.SBC, self.IMP, 2), INSTRUCTION("CPX", self.CPX, self.ABS, 4), INSTRUCTION("SBC", self.SBC, self.ABS, 4), INSTRUCTION("INC", self.INC, self.ABS, 6), INSTRUCTION("???", self.XXX, self.IMP, 6), 
    		INSTRUCTION("BEQ", self.BEQ, self.REL, 2), INSTRUCTION("SBC", self.SBC, self.IZY, 5), INSTRUCTION("???", self.XXX, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 8), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("SBC", self.SBC, self.ZPX, 4), INSTRUCTION("INC", self.INC, self.ZPX, 6), INSTRUCTION("???", self.XXX, self.IMP, 6), INSTRUCTION("SED", self.SED, self.IMP, 2), INSTRUCTION("SBC", self.SBC, self.ABY, 4), INSTRUCTION("NOP", self.NOP, self.IMP, 2), INSTRUCTION("???", self.XXX, self.IMP, 7), INSTRUCTION("???", self.NOP, self.IMP, 4), INSTRUCTION("SBC", self.SBC, self.ABX, 4), INSTRUCTION("INC", self.INC, self.ABX, 7), INSTRUCTION("???", self.XXX, self.IMP, 7), 
        ]

    def connectBus(self, bus):
        self.bus = bus

    def read(self, a):
        return self.bus.cpuRead(a, False)

    def write(self, a, d):
        self.bus.cpuWrite(a, d)

    def fetch(self):
        if self.lookup[self.opcode].addrmode != self.IMP:
            self.fetched = self.read(self.addr_abs)
        return self.fetched

    def getFlag(self, flagNo: int):
        return (self.status >> flagNo) & 1

    def setFlag(self, flagNo: int, value: bool):
        if value:
            self.status |= (1 << flagNo)
        else:
            self.status &= ~(1 << flagNo)

    def reset(self):
        self.addr_abs = 0xFFFC
        lo = self.read(self.addr_abs + 0)
        hi = self.read(self.addr_abs + 1)

        self.pc = (hi << 8) | lo

        self.a = 0
        self.x = 0
        self.y = 0
        self.stkp = 0xFD
        self.status = 0x00 | (1 << U)

        self.addr_abs = 0x0000
        self.addr_rel = 0x0000
        self.fetched = 0x00

        self.cycles = 8
        
    def irq(self):
        if (self.getFlag(I) == 0):
            self.write(0x0100 + self.stkp, (self.pc >> 8) & 0x00FF)
            self.stkp -= 1
            self.write(0x0100 + self.stkp, self.pc & 0x00FF)
            self.stkp -= 1

            self.setFlag(B, 0)
            self.setFlag(U, 1)
            self.setFlag(I, 1)
            self.write(0x0100 + self.stkp, self.status)
            self.stkp -= 1

            self.addr_abs = 0xFFFE
            lo = self.read(self.addr_abs + 0)
            hi = self.read(self.addr_abs + 1)
            self.pc = (hi << 8) | lo

            self.cycles = 7
        
    def nmi(self):
        self.write(0x0100 + self.stkp, (self.pc >> 8) & 0x00FF)
        self.stkp -= 1
        self.write(0x0100 + self.stkp, self.pc & 0x00FF)
        self.stkp -= 1
        
        self.setFlag(B, 0)
        self.setFlag(U, 1)
        self.setFlag(I, 1)
        self.write(0x0100 + self.stkp, self.status)
        self.stkp -= 1

        self.addr_abs = 0xFFFA
        lo = self.read(self.addr_abs + 0)
        hi = self.read(self.addr_abs + 1)
        self.pc = (hi << 8) | lo

        self.cycles = 8
        
    def clock(self):
        print('cpu clock', self.cycles)
        if self.cycles == 0:
            self.opcode = self.read(self.pc)
            self.setFlag(U, True)
            self.pc += 1
            
            self.cycles = self.lookup[self.opcode].cycles
            
            additional_cycle_1 = (self.lookup[self.opcode].addrmode)()
            
            additional_cycle_2 = (self.lookup[self.opcode].operate)()

            self.cycles += (additional_cycle_1 & additional_cycle_2)

            print(self.cycles)

            self.setFlag(U, True)
            

        self.cycles -= 1

    def complete(self):
        return self.cycles == 0

    def disassemble(self, nStart, nStop):
        addr = nStart
        value, lo, hi = 0x00, 0x00, 0x00
        mapLines = OrderedDict()
        line_addr = 0

        def hex(n, d):
            s = ['0' for i in range(d)]
            for i in range(d-1, -1, -1):
                s[i] = "0123456789ABCDEF"[n & 0xF]
                n >>= 4
            return ''.join(s)

        while addr <= nStop:
            line_addr = addr
            sInst = "$" + hex(addr, 4) + ': '
            opcode = self.bus.cpuRead(addr, True)
            addr += 1
            sInst += self.lookup[opcode].name + ' '

            if self.lookup[opcode].addrmode == self.IMP:
                sInst += ' {IMP}'
                
            elif self.lookup[opcode].addrmode == self.IMM:
                value = self.bus.cpuRead(addr, True)
                addr += 1
                sInst += "#$" + hex(value, 2) + " {IMM}"
                
            elif self.lookup[opcode].addrmode == self.ZP0:
                lo = self.bus.cpuRead(addr, True)
                addr += 1
                hi = 0x00
                sInst += "$" + hex(lo, 2) + " {ZP0}"
                
            elif self.lookup[opcode].addrmode == self.ZPX:
                lo = self.bus.cpuRead(addr, True)
                addr += 1
                hi = 0x00
                sInst += "$" + hex(lo, 2) + ", X {ZPX}"
                
            elif self.lookup[opcode].addrmode == self.ZPY:
                lo = self.bus.cpuRead(addr, True)
                addr += 1
                hi = 0x00
                sInst += "$" + hex(lo, 2) + ", Y {ZPY}"
                
            elif self.lookup[opcode].addrmode == self.IZX:
                lo = self.bus.cpuRead(addr, True)
                addr += 1
                hi = 0x00
                sInst += "($" + hex(lo, 2) + ", X) {IZX}"
                
            elif self.lookup[opcode].addrmode == self.IZY:
                lo = self.bus.cpuRead(addr, True)
                addr += 1
                hi = 0x00
                sInst += "($" + hex(lo, 2) + ", Y) {IZY}"
                
            elif self.lookup[opcode].addrmode == self.ABS:
                lo = self.bus.cpuRead(addr, True)
                addr += 1
                hi = self.bus.cpuRead(addr, True)
                addr += 1
                sInst += "$" + hex((hi << 8) | lo, 4) + " {ABS}"
                
            elif self.lookup[opcode].addrmode == self.ABX:
                lo = self.bus.cpuRead(addr, True)
                addr += 1
                hi = self.bus.cpuRead(addr, True)
                addr += 1
                sInst += "$" + hex((hi << 8) | lo, 4) + ", X {ABX}"
                
            elif self.lookup[opcode].addrmode == self.ABY:
                lo = self.bus.cpuRead(addr, True)
                addr += 1
                hi = self.bus.cpuRead(addr, True)
                addr += 1
                sInst += "$" + hex((hi << 8) | lo, 4) + ", Y {ABY}"
                
            elif self.lookup[opcode].addrmode == self.IND:
                lo = self.bus.cpuRead(addr, True)
                addr += 1
                hi = self.bus.cpuRead(addr, True)
                addr += 1
                sInst += "($" + hex((hi << 8) | lo, 4) + ") {IND}"
                
            elif self.lookup[opcode].addrmode == self.REL:
                value = self.bus.cpuRead(addr, True)
                addr += 1
                sInst += "$" + hex(value, 2) + " [$" + hex(addr + value, 4) + "] {REL}"

            mapLines[line_addr] = sInst

        return mapLines

    ''''''
    #######################
    #  ADDRESSING MODES  #
    #######################
    
    def IMP(self):
        self.fetched = self.a
        return 0
        
    def ZP0(self):
        self.addr_abs = self.read(self.pc)
        self.pc += 1
        self.addr_abs &= 0x00FF
        return 0
        
    def ZPY(self):
        self.addr_abs = self.read(self.pc) + self.y
        self.pc += 1
        self.addr_abs &= 0x00FF
        return 0
        
    def ABS(self):
        lo = self.read(self.pc)
        self.pc += 1
        hi = self.read(self.pc)
        self.pc += 1

        self.addr_abs = (hi << 8) | lo

        return 0
        
    def ABY(self):
        lo = self.read(self.pc)
        self.pc += 1
        hi = self.read(self.pc)
        self.pc += 1

        self.addr_abs = (hi << 8) | lo
        self.addr_abs += self.y
        
        if (self.addr_abs & 0xFF00) != (hi << 8):
            return 1
        else:
            return 0
        
    def IZX(self):
        t = self.read(self.pc)
        self.pc += 1

        lo = self.read((t + self.x) & 0x00FF)
        hi = self.read((t + self.x + 1) & 0x00FF)

        self.addr_abs = (hi << 8) | lo
        
        return 0
        
    def IMM(self):
        self.addr_abs = self.pc
        self.pc += 1
        return 0
        
    def ZPX(self):
        self.addr_abs = self.read(self.pc) + self.x
        self.pc += 1
        self.addr_abs &= 0x00FF
        return 0
        
    def ABX(self):
        lo = self.read(self.pc)
        self.pc += 1
        hi = self.read(self.pc)
        self.pc += 1

        self.addr_abs = (hi << 8) | lo
        self.addr_abs += self.x

        if (self.addr_abs & 0xFF00) != (hi << 8):
            return 1
        else:
            return 0
        
    def IND(self):
        ptr_lo = self.read(self.pc)
        self.pc += 1
        ptr_hi = self.read(self.pc)
        self.pc += 1

        ptr = (ptr_hi << 8) | ptr_lo

        if ptr_lo  == 0x00FF:
            self.addr_abs = (self.read(ptr & 0xFF00) << 8) | self.read(ptr + 0)
        else:
            self.addr_abs = (self.read(ptr + 1) << 8) | self.read(ptr + 0)

        return 0
        
    def IZY(self):
        t = self.read(self.pc)
        self.pc += 1

        lo = self.read(t & 0x00FF)
        hi = self.read((t + 1) & 0x00FF)

        self.addr_abs = (hi << 8) | lo
        self.addr_abs += self.y

        if (self.addr_abs & 0xFF00) != (hi << 8):
            return 1
        else:
            return 0

    def REL(self):
        self.addr_rel = self.read(self.pc)
        self.pc += 1

        if self.addr_rel & 0x80:
            self.addr_rel |= 0xFF00

        return 0
        
    ''''''
    ##############
    #  OP CODES  #
    ##############

    def ADC(self):
        self.fetch()

        self.temp = self.a + self.fetched + self.getFlag(C)

        self.setFlag(C, self.temp > 255)
        self.setFlag(Z, (self.temp & 0x00FF) == 0)
        self.setFlag(V, (~(self.a ^ self.fetched) & (self.a ^ self.temp)) & 0x0080)
        self.setFlag(N, self.temp & 0x80)

        self.a = self.temp & 0x00FF

        return 1
        
    def AND(self):
        self.fetch()
        
        self.a = self.a & self.fetched
        
        self.setFlag(Z, self.a == 0x00)
        self.setFlag(N, self.a & 0x80)
        
        return 1
        
    def ASL(self):
        self.fetch()
        self.temp = self.fetched << 1

        self.setFlag(C, (self.temp & 0xFF00) > 0)
        self.setFlag(Z, (self.temp & 0x00FF) == 0x00)
        self.setFlag(N, self.temp & 0x80)

        if self.lookup[self.opcode].addrmode == self.IMP:
            self.a = self.temp & 0x00FF
        else:
            self.write(self.addr_abs, self.temp & 0x00FF)

        return 0
        
    def BCC(self):
        if self.getFlag(C) == 0:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00):
                self.cycles += 1

            self.pc = self.addr_abs

        return 0
            
    def BCS(self):
        if self.getFlag(C) == 1:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00):
                self.cycles += 1

            self.pc = self.addr_abs

        return 0
        
    def BEQ(self):
        if self.getFlag(Z) == 1:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00):
                self.cycles += 1

            self.pc = self.addr_abs

        return 0
        
    def BIT(self):
        self.fetch()
        self.temp = self.a & self.fetched

        self.setFlag(Z, (self.temp & 0x00FF) == 0x00)
        self.setFlag(N, self.fetched & (1 << 7))
        self.setFlag(V, self.fetched & (1 << 6))

        return 0
        
    def BMI(self):
        if self.getFlag(N) == 1:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00):
                self.cycles += 1

            self.pc = self.addr_abs

        return 0
        
    def BNE(self):
        if self.getFlag(Z) == 0:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00):
                self.cycles += 1

            self.pc = self.addr_abs & 0xFFFF

        return 0
        
    def BPL(self):
        if self.getFlag(N) == 0:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00):
                self.cycles += 1

            self.pc = self.addr_abs

        return 0
        
    def BRK(self):
        self.pc += 1
	    
        self.setFlag(I, 1)
        self.write(0x0100 + self.stkp, (self.pc >> 8) & 0x00FF)
        self.stkp -= 1
        self.write(0x0100 + self.stkp, self.pc & 0x00FF)
        self.stkp -= 1
    
        self.setFlag(B, 1)
        self.write(0x0100 + self.stkp, self.status)
        self.stkp -= 1
        self.setFlag(B, 0)
    
        self.pc = self.read(0xFFFE) | (self.read(0xFFFF) << 8)
        
        return 0
        
    def BVC(self):
        if self.getFlag(V) == 0:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00):
                self.cycles += 1

            self.pc = self.addr_abs

        return 0
        
    def BVS(self):
        if self.getFlag(V) == 1:
            self.cycles += 1
            self.addr_abs = self.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.pc & 0xFF00):
                self.cycles += 1

            self.pc = self.addr_abs

        return 0
        
    def CLC(self):
        self.setFlag(C, False)
        return 0
        
    def CLD(self):
        self.setFlag(D, False)
        return 0
        
    def CLI(self):
        self.setFlag(I, False)
        return 0
        
    def CLV(self):
        self.setFlag(V, False)
        return 0
        
    def CMP(self):
        self.fetch()
        self.temp = self.a - self.fetched

        self.setFlag(C, self.a >= self.fetched)
        self.setFlag(Z, (self.temp & 0x00FF) == 0x0000)
        self.setFlag(N, self.temp & 0x0080)

        return 1
        
    def CPX(self):
        self.fetch()
        self.temp = self.x - self.fetched

        self.setFlag(C, self.x >= self.fetched)
        self.setFlag(Z, (self.temp & 0x00FF) == 0x0000)
        self.setFlag(N, self.temp & 0x0080)

        return 0
        
    def CPY(self):
        self.fetch()
        self.temp = self.y - self.fetched

        self.setFlag(C, self.y >= self.fetched)
        self.setFlag(Z, (self.temp & 0x00FF) == 0x0000)
        self.setFlag(N, self.temp & 0x0080)

        return 0
        
    def DEC(self):
        self.fetch()
        self.temp = self.fetched - 1
        self.write(self.addr_abs, self.temp & 0x00FF)
        
        self.setFlag(Z, (self.temp & 0x00FF) == 0x0000)
        self.setFlag(N, self.temp & 0x0080)
        
        return 0
        
    def DEX(self):
        self.x -= 1

        self.setFlag(Z, self.x == 0x00)
        self.setFlag(N, self.x & 0x80)

        return 0
        
    def DEY(self):
        self.y -= 1

        self.setFlag(Z, self.y == 0x00)
        self.setFlag(N, self.y & 0x80)

        return 0
        
    def EOR(self):
        self.fetch()
        self.a = self.a ^ self.fetched
        
        self.setFlag(Z, self.a == 0x00)
        self.setFlag(N, self.a & 0x80)
        
        return 1
        
    def INC(self):
        self.fetch()
        self.temp = self.fetched + 1
        self.write(self.addr_abs, self.temp & 0x00FF)
        
        self.setFlag(Z, (self.temp & 0x00FF) == 0x0000)
        self.setFlag(N, self.temp & 0x0080)
        
        return 0
        
    def INX(self):
        self.x += 1

        self.setFlag(Z, self.x == 0x00)
        self.setFlag(N, self.x & 0x80)

        return 0
        
    def INY(self):
        self.y += 1

        self.setFlag(Z, self.y == 0x00)
        self.setFlag(N, self.y & 0x80)

        return 0
        
    def JMP(self):
        self.pc = self.addr_abs
        return 0
        
    def JSR(self):
        self.pc -= 1

        self.write(0x0100 + self.stkp, (self.pc >> 8) & 0x00FF)
        self.stkp -= 1
        self.write(0x0100 + self.stkp, self.pc & 0x00FF)
        self.stkp -= 1
    
        self.pc = self.addr_abs
        return 0
        
    def LDA(self):
        self.fetch()
        self.a = self.fetched
        
        self.setFlag(Z, self.a == 0x00)
        self.setFlag(N, self.a & 0x80)
        
        return 1
        
    def LDX(self):
        self.fetch()
        self.x = self.fetched
        
        self.setFlag(Z, self.x == 0x00)
        self.setFlag(N, self.x & 0x80)
        
        return 1
        
    def LDY(self):
        self.fetch()
        self.y = self.fetched
        
        self.setFlag(Z, self.y == 0x00)
        self.setFlag(N, self.y & 0x80)
        
        return 1
        
    def LSR(self):
        self.fetch()
        
        self.setFlag(C, self.fetched & 0x0001)
        self.temp = self.fetched >> 1
        self.setFlag(Z, (self.temp & 0x00FF) == 0x0000)
        self.setFlag(N, self.temp & 0x0080)

        if self.loopup[self.opcode].addrmode == self.IMP:
            self.a = self.temp & 0x00FF
        else:
            self.write(self.addr_abs, self.temp & 0x00FF)

        return 0
        
    def NOP(self):
        # Just a big switch statement
        if (self.opcode == 0x1C):
            pass
        elif (self.opcode == 0x3C):
            pass
        elif (self.opcode == 0x5C):
            pass
        elif (self.opcode == 0x7C):
            pass
        elif (self.opcode == 0xDC):
            pass
        elif (self.opcode == 0xFC):
            return 1
        else:
            pass

        return 0
        
    def ORA(self):
        self.fetch()
        self.a = self.a | self.fetched
        
        self.setFlag(Z, self.a == 0x00)
        self.setFlag(N, self.a & 0x80)
        
        return 1
        
    def PHA(self):
        self.write(0x0100 + self.stkp, self.a)
        self.stkp -= 1
        return 0
        
    def PHP(self):
        self.write(0x0100 + self.stkp, self.status | (1 << B) | (1 << U))
        
        self.setFlag(B, 0)
        self.setFlag(U, 0)
        
        self.stkp -= 1
        return 0
        
    def PLA(self):
        self.stkp += 1
        self.a = self.read(0x0100 + self.stkp)
        
        self.setFlag(Z, self.a == 0x00)
        self.setFlag(N, self.a & 0x80)

        return 0
        
    def PLP(self):
        self.stkp += 1
        self.status = self.read(0x0100 + self.stkp)
        
        self.setFlag(U, True)

        return 0
        
    def ROL(self):
        self.fetch()
        self.temp = self.fetched << 1 | self.getFlag(C)
        
        self.setFlag(C, self.fetched & 0xFF00)
        self.setFlag(Z, (self.temp & 0x00FF) == 0x0000)
        self.setFlag(N, self.temp & 0x0080)

        if self.loopup[self.opcode].addrmode == self.IMP:
            self.a = self.temp & 0x00FF
        else:
            self.write(self.addr_abs, self.temp & 0x00FF)

        return 0
        
    def ROR(self):
        self.fetch()
        self.temp = (self.getFlag(C) << 7) | (self.fetched >> 1)
        
        self.setFlag(C, self.fetched & 0x01)
        self.setFlag(Z, (self.temp & 0x00FF) == 0x00)
        self.setFlag(N, self.temp & 0x0080)

        if self.loopup[self.opcode].addrmode == self.IMP:
            self.a = self.temp & 0x00FF
        else:
            self.write(self.addr_abs, self.temp & 0x00FF)

        return 0
        
    def RTI(self):
        self.stkp += 1
        self.read(0x0100 + self.stkp)
        self.status &= ~(1 << B)
        self.status &= ~(1 << U)

        self.stkp += 1
        self.pc = self.read(0x0100 + self.stkp)
        self.stkp += 1
        self.pc |= self.read(0x0100 + self.stkp) << 8

        return 0
        
    def RTS(self):
        self.stkp += 1
        self.pc = self.read(0x0100 + self.stkp)
        self.stkp += 1
        self.pc |= self.read(0x0100 + self.stkp) << 8

        self.pc += 1

        return 0
        
    def SBC(self):
        self.fetch()

        value = self.fetched ^ 0x00FF

        self.temp = self.a + value + self.getFlag(C)
        
        self.setFlag(C, self.temp > 255)
        self.setFlag(Z, (self.temp & 0x00FF) == 0)
        self.setFlag(V, (self.temp ^ self.a) & (self.temp ^ value) & 0x0080)
        self.setFlag(N, self.temp & 0x80)

        self.a = self.temp & 0x00FF

        return 1
        
    def SEC(self):
        self.setFlag(C, True)
        return 0
        
    def SED(self):
        self.setFlag(D, True)
        return 0
        
    def SEI(self):
        self.setFlag(I, True)
        return 0
        
    def STA(self):
        self.write(self.addr_abs, self.a)
        return 0
        
    def STX(self):
        self.write(self.addr_abs, self.x)
        return 0
        
    def STY(self):
        self.write(self.addr_abs, self.y)
        return 0
        
    def TAX(self):
        self.x = self.a

        self.setFlag(Z, self.x == 0x00)
        self.setFlag(N, self.x & 0x80)

        return 0
        
    def TAY(self):
        self.y = self.a

        self.setFlag(Z, self.y == 0x00)
        self.setFlag(N, self.y & 0x80)

        return 0
        
    def TSX(self):
        self.x = self.stkp

        self.setFlag(Z, self.x == 0x00)
        self.setFlag(N, self.x & 0x80)

        return 0
        
    def TXA(self):
        self.a = self.x

        self.setFlag(Z, self.a == 0x00)
        self.setFlag(N, self.a & 0x80)

        return 0
        
    def TXS(self):
        self.stkp = self.x
        return 0
        
    def TYA(self):
        self.a = self.y

        self.setFlag(Z, self.a == 0x00)
        self.setFlag(N, self.a & 0x80)

        return 0
        
    def XXX(self):
        return 0


###################
#   End Of File   #
###################

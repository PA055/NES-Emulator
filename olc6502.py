from Bus import Bus
from dataclasses import dataclass
from collections.abc import Callable

@dataclass
class INSTRUCTION:
    name: str
    operate: Callable
    addrmode: Callable
    cycles: int = 0

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
        return self.bus.read(a, False)

    def write(self, a, d):
        self.bus.write(a, d)

    def fetch():
        pass

    def getFlag(self, flagNo: int):
        return (self.status & (1 << flagNo)) >> flagNo

    def setFlag(self, flagNo: int, value: bool):
        if value:
            self.status |= (1 << flagNo)
        else:
            self.status &= ~(1 << flagNo)

    #######################
    #  ADDERESSING MODES  #
    #######################

    def IMP(self):
        pass
    def ZP0(self):
        pass
    def ZPY(self):
        pass
    def ABS(self):
        pass
    def ABY(self):
        pass
    def IZX(self):
        pass
    def IMM(self):
        pass
    def ZPX(self):
        pass
    def REL(self):
        pass
    def ABX(self):
        pass
    def IND(self):
        pass
    def IZY(self):
        pass


    ##############
    #  OP CODES  #
    ##############

    def ADC(self):
        pass
    def AND(self):
        pass
    def ASL(self):
        pass
    def BCC(self):
        pass
    def BCS(self):
        pass
    def BEQ(self):
        pass
    def BIT(self):
        pass
    def BMI(self):
        pass
    def BNE(self):
        pass
    def BPL(self):
        pass
    def BRK(self):
        pass
    def BVC(self):
        pass
    def BVS(self):
        pass
    def CLC(self):
        pass
    def CLD(self):
        pass
    def CLI(self):
        pass
    def CLV(self):
        pass
    def CMP(self):
        pass
    def CPX(self):
        pass
    def CPY(self):
        pass
    def DEC(self):
        pass
    def DEX(self):
        pass
    def DEY(self):
        pass
    def EOR(self):
        pass
    def INC(self):
        pass
    def INX(self):
        pass
    def INY(self):
        pass
    def JMP(self):
        pass
    def JSR(self):
        pass
    def LDA(self):
        pass
    def LDX(self):
        pass
    def LDY(self):
        pass
    def LSR(self):
        pass
    def NOP(self):
        pass
    def ORA(self):
        pass
    def PHA(self):
        pass
    def PHP(self):
        pass
    def PLA(self):
        pass
    def PLP(self):
        pass
    def ROL(self):
        pass
    def ROR(self):
        pass
    def RTI(self):
        pass
    def RTS(self):
        pass
    def SBC(self):
        pass
    def SEC(self):
        pass
    def SED(self):
        pass
    def SEI(self):
        pass
    def STA(self):
        pass
    def STX(self):
        pass
    def STY(self):
        pass
    def TAX(self):
        pass
    def TAY(self):
        pass
    def TSX(self):
        pass
    def TXA(self):
        pass
    def TXS(self):
        pass
    def TYA(self):
        pass
    def XXX(self):
        pass

    def reset(self):
        pass
        
    def irq(self):
        pass
        
    def nmi(self):
        pass
        
    def clock(self):
        if self.cycles == 0:
            self.opcode = read(self.pc)
            self.pc += 1
            
            self.cycles = self.lookup[self.opcode].cycles
            
            additional_cycle_1 = (self.lookup[self.opcode].addrmode)()
            
            additional_cycle_2 = (self.lookup[self.opcode].operate)()

            self.cycles += (additional_cycle_1 & additional_cycle_2)

        self.cycles -= 1

    def complete(self):
        pass

    def disassemble(self, nStart, nStop):
        pass
    
class Bus:
    def __init__(self, cpu, ppu):
        self.cpu = cpu
        self.ppu = ppu
        self.cpuRam = [0 for i in range(2*1024)]
        self.cart = None
        self.cpu.connectBus(self)

        self.nSystemClockCounter = 0
        self.nInstructionCounter = 0
        
    def cpuWrite(self, addr, data):
        toMapper = self.cart.cpuWrite(addr, data)
        if toMapper:
            pass

        elif (addr >= 0x0000 and addr <= 0x1FFF):
            self.cpuRam[addr & 0x07FF] = data

        elif (addr >= 0x2000 and addr <= 0x3FFF):
            self.ppu.cpuWrite(addr & 0x0007, data)
        
    def cpuRead(self, addr, bReadOnly=False):
        data = 0x00
        
        data, toMapper = self.cart.cpuRead(addr, data)
        if toMapper:
            pass

        elif (addr >= 0x0000 and addr <= 0x1FFF):
            data = self.cpuRam[addr & 0x07FF]

        elif (addr >= 0x2000 and addr <= 0x3FFF):
            data = self.ppu.cpuRead(addr & 0x0007, bReadOnly)

        return data

    def insertCartridge(self, cartridge):
        self.cart = cartridge
        self.ppu.connectCartridge(cartridge)

    def reset(self):
        self.cpu.reset()
        self.nSystemClockCounter = 0

    def clock(self):
        self.ppu.clock()

        if self.nSystemClockCounter % 3 == 0:
            self.cpu.clock()
            if self.cpu.complete():
                self.nInstructionCounter += 1
                #print('CPU Instruction Counter:', self.nInstructionCounter)

        if (self.ppu.nmi):
            self.ppu.nmi = False
            self.cpu.nmi()

        self.nSystemClockCounter += 1
        #print("PPU Instruction Counter:", self.nSystemClockCounter)
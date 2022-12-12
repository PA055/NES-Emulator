class Bus:
    def __init__(self, cpu):
        self.cpu = cpu
        self.ram = [0 for i in range(64*1024)]
        self.cpu.connectBus(self)
        
    def write(self, addr, data):
        if (addr >= 0x0000 and addr <= 0xFFFF):
            self.ram[addr] = data
        
    def read(self, addr, bReadOnly=False):
        if (addr >= 0x0000 and addr <= 0xFFFF):
            return self.ram[addr]
        return 0x00


class olc2C02:
    def __init__(self):
        self.cart = None
        self.tblName = [[0 for i in range(1024)] for j in range(2)]
        self.tblPalette = [0 for i in range(32)]
        self.tblPattern = [[0 for i in range(4096)] for j in range(2)]
        

    def connectCartridge(self, cartridge):
        self.cart = cartridge

    def clock(self):
        pass

    def cpuWrite(self, addr, data):
        if (addr == 0x0000): # Control
            pass
        elif (addr == 0x0001): # Mask
            pass
        elif (addr == 0x0002): # Status
            pass
        elif (addr == 0x0003): # OAM Address
            pass
        elif (addr == 0x0004): # OAM Data
            pass
        elif (addr == 0x0005): # Scroll
            pass
        elif (addr == 0x0006): # PPU Address
            pass
        elif (addr == 0x0007): # PPU Data
            pass
        

    def cpuRead(self, addr, rdonly=False):
        data = 0x00

        if (addr == 0x0000): # Control
            pass
        elif (addr == 0x0001): # Mask
            pass
        elif (addr == 0x0002): # Status
            pass
        elif (addr == 0x0003): # OAM Address
            pass
        elif (addr == 0x0004): # OAM Data
            pass
        elif (addr == 0x0005): # Scroll
            pass
        elif (addr == 0x0006): # PPU Address
            pass
        elif (addr == 0x0007): # PPU Data
            pass
        
        return data

    def ppuRead(self, addr, rdonly=False):
        data = 0x00
        addr &= 0x3FFF

        return data

    def ppuWrite(self, addr, data):
        addr &= 0x3FFF
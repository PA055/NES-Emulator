from PixelGameEngine import Sprite
import random as rand

class olc2C02:
    def __init__(self):
        self.cart = None
        self.tblName = [[0 for i in range(1024)] for j in range(2)]
        self.tblPalette = [0 for i in range(32)]
        self.tblPattern = [[0 for i in range(4096)] for j in range(2)]

        self.palScreen = [(0, 0, 0) for i in range(0x40)]
        self.sprScreen = Sprite(256, 240)
        self.sprNameTable = [Sprite(256, 240) for i in range(2)]
        self.sprPatternTable = [Sprite(128, 128) for i in range(2)]

        self.frame_complete = False
        self.scanline = 0
        self.cycle = 0

        if True:
            self.palScreen[0x00] = (84, 84, 84)
            self.palScreen[0x01] = (0, 30, 116)
            self.palScreen[0x02] = (8, 16, 144)
            self.palScreen[0x03] = (48, 0, 136)
            self.palScreen[0x04] = (68, 0, 100)
            self.palScreen[0x05] = (92, 0, 48)
            self.palScreen[0x06] = (84, 4, 0)
            self.palScreen[0x07] = (60, 24, 0)
            self.palScreen[0x08] = (32, 42, 0)
            self.palScreen[0x09] = (8, 58, 0)
            self.palScreen[0x0A] = (0, 64, 0)
            self.palScreen[0x0B] = (0, 60, 0)
            self.palScreen[0x0C] = (0, 50, 60)
            self.palScreen[0x0D] = (0, 0, 0)
            self.palScreen[0x0E] = (0, 0, 0)
            self.palScreen[0x0F] = (0, 0, 0)
            self.palScreen[0x10] = (152, 150, 152)
            self.palScreen[0x11] = (8, 76, 196)
            self.palScreen[0x12] = (48, 50, 236)
            self.palScreen[0x13] = (92, 30, 228)
            self.palScreen[0x14] = (136, 20, 176)
            self.palScreen[0x15] = (160, 20, 100)
            self.palScreen[0x16] = (152, 34, 32)
            self.palScreen[0x17] = (120, 60, 0)
            self.palScreen[0x18] = (84, 90, 0)
            self.palScreen[0x19] = (40, 114, 0)
            self.palScreen[0x1A] = (8, 124, 0)
            self.palScreen[0x1B] = (0, 118, 40)
            self.palScreen[0x1C] = (0, 102, 120)
            self.palScreen[0x1D] = (0, 0, 0)
            self.palScreen[0x1E] = (0, 0, 0)
            self.palScreen[0x1F] = (0, 0, 0)
            self.palScreen[0x20] = (236, 238, 236)
            self.palScreen[0x21] = (76, 154, 236)
            self.palScreen[0x22] = (120, 124, 236)
            self.palScreen[0x23] = (176, 98, 236)
            self.palScreen[0x24] = (228, 84, 236)
            self.palScreen[0x25] = (236, 88, 180)
            self.palScreen[0x26] = (236, 106, 100)
            self.palScreen[0x27] = (212, 136, 32)
            self.palScreen[0x28] = (160, 170, 0)
            self.palScreen[0x29] = (116, 196, 0)
            self.palScreen[0x2A] = (76, 208, 32)
            self.palScreen[0x2B] = (56, 204, 108)
            self.palScreen[0x2C] = (56, 180, 204)
            self.palScreen[0x2D] = (60, 60, 60)
            self.palScreen[0x2E] = (0, 0, 0)
            self.palScreen[0x2F] = (0, 0, 0)
            self.palScreen[0x30] = (236, 238, 236)
            self.palScreen[0x31] = (168, 204, 236)
            self.palScreen[0x32] = (188, 188, 236)
            self.palScreen[0x33] = (212, 178, 236)
            self.palScreen[0x34] = (236, 174, 236)
            self.palScreen[0x35] = (236, 174, 212)
            self.palScreen[0x36] = (236, 180, 176)
            self.palScreen[0x37] = (228, 196, 144)
            self.palScreen[0x38] = (204, 210, 120)
            self.palScreen[0x39] = (180, 222, 120)
            self.palScreen[0x3A] = (168, 226, 144)
            self.palScreen[0x3B] = (152, 226, 180)
            self.palScreen[0x3C] = (160, 214, 228)
            self.palScreen[0x3D] = (160, 162, 160)
            self.palScreen[0x3E] = (0, 0, 0)
            self.palScreen[0x3F] = (0, 0, 0)
        

    def connectCartridge(self, cartridge):
        self.cart = cartridge

    def clock(self):
        self.sprScreen.setPixel((self.cycle - 1, self.scanline), self.palScreen[0x3F if rand.randint(0, 1) else 0x30])

        self.cycle += 1
        if self.cycle >= 341:
            self.cycle = 0
            self.scanline += 1
            if self.scanline >= 261:
                self.scanline = -1
                self.frame_complete = True

    def getScreen(self):
        return self.sprScreen

    def getNameTable(self, i):
        return self.sprNameTable[i]

    def getPatternTable(self, i):
        return self.sprPatternTable[i]

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

        data, toMapper = self.cart.ppuRead(addr, data)
        if toMapper:
            pass

        return data

    def ppuWrite(self, addr, data):
        addr &= 0x3FFF

        data, toMapper = self.cart.ppuWrite(addr, data)
        if toMapper:
            pass
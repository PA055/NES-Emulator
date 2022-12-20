from dataclasses import dataclass
from PixelGameEngine import Sprite
import random as rand

def toFile(filename, data, type='list', mode = 'w+'):
    with open(filename, mode) as f:
        if type == 'list':
            f.writelines(['\n' + str(datap) for datap in data])
        elif type == 'dict':
            f.writelines(['\n' + str(item) + ': ' + str(value) for item, value in data])
        elif type == 'raw':
            f.write(str(data))


@dataclass
class StatusReg:
    unused: int = 0
    sprite_overflow: bool = False
    sprite_zero_hit: bool = False
    vertical_blank: bool = False

    def __init__(self):
        self.reg = 0x00

    @property
    def reg(self):
        reg = 0x00
        reg |= ((self.unused & 0x10) << 0)
        reg |= (int(self.sprite_overflow) << 5)
        reg |= (int(self.sprite_zero_hit) << 6)
        reg |= (int(self.vertical_blank) << 7)

        return reg

    @reg.setter
    def reg(self, value):
        self.unused = int((value >> 0) & 0x10)
        self.sprite_overflow = bool((value >> 5) & 0x01)
        self.sprite_zero_hit = bool((value >> 6) & 0x01)
        self.vertical_blank = bool((value >> 7) & 0x01)

@dataclass
class MaskReg:
    grayscale: bool = False
    render_background_left: bool = False
    render_sprites_left: bool = False
    render_background: bool = False
    render_sprites: bool = False
    enhance_red: bool = False
    enhance_green: bool = False
    enhance_blue: bool = False

    def __init__(self):
        self.reg = 0x00

    @property
    def reg(self):
        reg = 0x00
        reg |= (int(self.grayscale) << 0)
        reg |= (int(self.render_background_left) << 1)
        reg |= (int(self.render_sprites_left) << 1)
        reg |= (int(self.render_background) << 3)
        reg |= (int(self.render_sprites) << 4)
        reg |= (int(self.enhance_red) << 5)
        reg |= (int(self.enhance_green) << 6)
        reg |= (int(self.enhance_blue) << 7)

        return reg

    @reg.setter
    def reg(self, value):
        self.grayscale = bool((value >> 0) & 0x01)
        self.render_background_left = bool((value >> 1) & 0x01)
        self.render_sprites_left = bool((value >> 1) & 0x01)
        self.render_background = bool((value >> 3) & 0x01)
        self.render_sprites = bool((value >> 4) & 0x01)
        self.enhance_red = bool((value >> 5) & 0x01)
        self.enhance_green = bool((value >> 6) & 0x01)
        self.enhance_blue = bool((value >> 7) & 0x01)

@dataclass
class ControlReg:
    nametable_x: bool = False
    nametable_y: bool = False
    increment_mode: bool = False
    pattern_sprite: bool = False
    pattern_background: bool = False
    sprite_size: bool = False
    slave_mode: bool = False # unused
    enable_nmi: bool = False

    def __init__(self):
        self.reg = 0x00

    @property
    def reg(self):
        reg = 0x00
        reg |= (int(self.nametable_x) << 0)
        reg |= (int(self.nametable_y) << 1)
        reg |= (int(self.increment_mode) << 2)
        reg |= (int(self.pattern_sprite) << 3)
        reg |= (int(self.pattern_background) << 4)
        reg |= (int(self.sprite_size) << 5)
        reg |= (int(self.slave_mode) << 6)
        reg |= (int(self.enable_nmi) << 7)

        return reg

    @reg.setter
    def reg(self, value):
        self.nametable_x = bool((value >> 0) & 0x01)
        self.nametable_y = bool((value >> 1) & 0x01)
        self.increment_mode = bool((value >> 2) & 0x01)
        self.pattern_sprite = bool((value >> 3) & 0x01)
        self.pattern_background = bool((value >> 4) & 0x01)
        self.sprite_size = bool((value >> 5) & 0x01)
        self.slave_mode = bool((value >> 6) & 0x01)
        self.enable_nmi = bool((value >> 7) & 0x01)


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

        self.status = StatusReg()
        self.mask = MaskReg()
        self.control = ControlReg()

        self.address_latch = 0x00
        self.ppu_data_buffer = 0x00
        self.ppu_address = 0x0000

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

    def getColorFromPaletteRam(self, palette, pixel):
        return self.palScreen[self.ppuRead(0x3F00 + (palette << 2) + pixel) & 0x3F]

    def getPalette(self, palette):
        pal = []
        for i in range(4):
            pal.append(self.getColorFromPaletteRam(palette, i))
        
        return pal


    def getPatternTable(self, i, palette):
        for nTileY in range(16):
            for nTileX in range(16):
                nOffset = nTileY * 256 + nTileX * 16

                for row in range(8):
                    tile_lsb = self.ppuRead(i * 0x1000 + nOffset + row + 0x0000)
                    tile_msb = self.ppuRead(i * 0x1000 + nOffset + row + 0x0008)

                    for col in range(8):
                        pixel = (tile_lsb & 0x01) + (tile_msb & 0x01)
                        tile_lsb >>= 1
                        tile_msb >>= 1

                        self.sprPatternTable[i].setPixel((
                                nTileX * 8 + (7 - col),
                                nTileY * 8 + row
                            ), 
                            self.getColorFromPaletteRam(palette, pixel)
                        )
        
        toFile(f'sprPatternTable{i}.txt', self.sprPatternTable[i].imageArray)
        return self.sprPatternTable[i]

    def cpuWrite(self, addr, data):
        if (addr == 0x0000): # Control
            self.control.reg = data
        elif (addr == 0x0001): # Mask
            self.mask.reg = data
        elif (addr == 0x0002): # Status
            pass
        elif (addr == 0x0003): # OAM Address
            pass
        elif (addr == 0x0004): # OAM Data
            pass
        elif (addr == 0x0005): # Scroll
            pass
        elif (addr == 0x0006): # PPU Address
            if self.address_latch == 0:
                self.ppu_address = (self.ppu_address & 0x00FF) | data
                self.address_latch = 1
            else:
                self.ppu_address = (self.ppu_address & 0xFF00) | (data << 8)
                self.address_latch = 0
        elif (addr == 0x0007): # PPU Data
            self.ppuWrite(self.ppu_address, data)
            self.ppu_address += 1
            pass
        

    def cpuRead(self, addr, rdonly=False):
        data = 0x00

        if (addr == 0x0000): # Control
            pass
        elif (addr == 0x0001): # Mask
            pass
        elif (addr == 0x0002): # Status
            self.status.vertical_blank = True
            data = (self.status.reg & 0xE0) | (self.ppu_data_buffer & 0x1F)
            self.status.vertical_blank = False
            self.address_latch = 0
        elif (addr == 0x0003): # OAM Address
            pass
        elif (addr == 0x0004): # OAM Data
            pass
        elif (addr == 0x0005): # Scroll
            pass
        elif (addr == 0x0006): # PPU Address
            pass
        elif (addr == 0x0007): # PPU Data
            data = self.ppu_data_buffer
            self.ppu_data_buffer = self.ppuRead(self.ppu_address)

            if self.ppu_address > 0x3F00:
                data = self.ppu_data_buffer

            self.ppu_address += 1
        
        return data

    def ppuRead(self, addr, rdonly=False):
        data = 0x00
        addr &= 0x3FFF

        data, toMapper = self.cart.ppuRead(addr, data)
        if toMapper:
            pass

        elif addr >= 0x0000 and addr <= 0x1FFF:
            data = self.tblPattern[(addr & 0x1000) >> 12][addr & 0x0FFF]

        elif addr >= 0x2000 and addr <= 0x3EFF:
            pass

        elif addr >= 0x3F00 and addr <= 0x3FFF:
            addr &= 0x001F
            addr = 0x0000 if addr == 0x0010 else addr
            addr = 0x0004 if addr == 0x0014 else addr
            addr = 0x0008 if addr == 0x0018 else addr
            addr = 0x000C if addr == 0x001C else addr
            data = self.tblPalette[addr]

        return data

    def ppuWrite(self, addr, data):
        addr &= 0x3FFF

        toMapper = self.cart.ppuWrite(addr, data)
        if toMapper:
            pass

        elif addr >= 0x0000 and addr <= 0x1FFF:
            self.tblPattern[(addr & 0x1000) >> 12][addr & 0x0FFF] = data

        elif addr >= 0x2000 and addr <= 0x3EFF:
            pass

        elif addr >= 0x3F00 and addr <= 0x3FFF:
            addr &= 0x001F
            addr = 0x0000 if addr == 0x0010 else addr
            addr = 0x0004 if addr == 0x0014 else addr
            addr = 0x0008 if addr == 0x0018 else addr
            addr = 0x000C if addr == 0x001C else addr
            self.tblPalette[addr] = data
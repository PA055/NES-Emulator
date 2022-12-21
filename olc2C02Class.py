from dataclasses import dataclass
from PixelGameEngine import Sprite
import CartridgeClass
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

@dataclass
class LoopyReg:
    coarse_x: int = 0x00
    coarse_y: int = 0x00
    nametable_x: bool = False
    nametable_y: bool = False
    fine_y: int = 0x0
    unused: bool = False

    def __init__(self):
        self.reg = 0x0000

    @property
    def reg(self):
        reg = 0x00
        reg |= (int(self.coarse_x & 0x001F) << 0)
        reg |= (int(self.coarse_y & 0x001F) << 4)
        reg |= (int(self.nametable_x) << 9)
        reg |= (int(self.nametable_y) << 10)
        reg |= (int(self.fine_y & 0x7) << 11)
        reg |= (int(self.unused) << 15)

        return reg

    @reg.setter
    def reg(self, value):
        self.coarse_x = int((value >> 0) & 0x001F)
        self.coarse_y = int((value >> 4) & 0x001F)
        self.nametable_x = bool((value >> 9) & 0x0001)
        self.nametable_y = bool((value >> 10) & 0x0001)
        self.coarse_y = int((value >> 11) & 0x0007)
        self.unused = bool((value >> 15) & 0x0001)




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

        self.nmi = False
        self.frame_complete = False
        self.scanline = 0
        self.cycle = 0

        self.status = StatusReg()
        self.mask = MaskReg()
        self.control = ControlReg()
        self.vram_addr = LoopyReg()
        self.tram_addr = LoopyReg()

        self.fine_x = 0x00

        self.address_latch = 0x00
        self.ppu_data_buffer = 0x00

        self.bg_next_tile_id = 0x00
        self.bg_next_tile_attrib = 0x00
        self.bg_next_tile_lsb = 0x00
        self.bg_next_tile_msb = 0x00

        self.bg_shifter_pattern_lo = 0x0000
        self.bg_shifter_pattern_hi = 0x0000
        self.bg_shifter_attrib_lo = 0x0000
        self.bg_shifter_attrib_hi = 0x0000


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

        def IncrementScrollX():
            if self.mask.render_background or self.mask.render_sprites:
                if self.vram_addr.coarse_x == 31:
                    self.vram_addr.coarse_x = 0

                    self.vram_addr.nametable_x = not self.vram_addr.nametable_x
                else:
                    self.vram_addr.coarse_x += 1

        def IncrementScrollY():
            if self.mask.render_background or self.mask.render_sprites:
                if self.vram_addr.fine_y < 7:
                    self.vram_addr.fine_y += 1
                else:
                    self.vram_addr.fine_y = 0
                    if self.vram_addr.coarse_y == 29:
                        self.vram_addr.coarse_y = 0
                        self.vram_addr.nametable_y = not self.vram_addr.nametable_y
                    elif self.vram_addr.coarse_y == 31:
                        self.vram_addr.coarse_y = 0
                    else:
                        self.vram_addr.coarse_y += 1

        def TransferAddressX():
            if self.mask.render_background or self.mask.render_sprites:
                self.vram_addr.nametable_x = self.tram_addr.nametable_x
                self.vram_addr.coarse_x = self.tram_addr.coarse_x

        def TransferAddressY():
            if self.mask.render_background or self.mask.render_sprites:
                self.vram_addr.nametable_y = self.tram_addr.nametable_y
                self.vram_addr.coarse_y = self.tram_addr.coarse_y
                self.vram_addr.fine_y = self.tram_addr.fine_y

        def LoadBackgroundShifters():
            self.bg_shifter_pattern_lo = (self.bg_shifter_pattern_lo & 0xFF00) | self.bg_next_tile_lsb
            self.bg_shifter_pattern_hi = (self.bg_shifter_pattern_hi & 0xFF00) | self.bg_next_tile_msb
            
            self.bg_shifter_attrib_lo = (self.bg_shifter_attrib_lo & 0xFF00) | (0xFF if (self.bg_next_tile_attrib & 0b01) else 0x00)
            self.bg_shifter_attrib_hi = (self.bg_shifter_attrib_hi & 0xFF00) | (0xFF if (self.bg_next_tile_attrib & 0b10) else 0x00)
            

        def UpdateShifters():
            if self.mask.render_background:
                self.bg_shifter_pattern_lo <<= 1
                self.bg_shifter_pattern_hi <<= 1

                self.bg_shifter_attrib_lo <<= 1
                self.bg_shifter_attrib_hi <<= 1


                

        if self.scanline >= -1 and self.scanline < 240:

            if self.scanline == -1 and self.cycle == 1:
                self.status.vertical_blank = False

            if (self.cycle >= 2 and self.cycle < 258) or (self.cycle >= 321 and self.cycle < 338):
                UpdateShifters()

                if ((self.cycle - 1) % 8) == 0:
                    LoadBackgroundShifters()
                    self.bg_next_tile_id = self.ppuRead(0x2000 | (self.vram_addr.reg & 0x0FFF))

                elif ((self.cycle - 1) % 8) == 2:
                    self.bg_next_tile_attrib = self.ppuRead(0x23C0 | (self.vram_addr.nametable_y << 11) | (self.vram_addr.nametable_x << 10) | ((self.vram_addr.coarse_y >> 2) << 3) | (self.vram_addr.coarse_x >> 2))
                    if self.vram_addr.coarse_y & 0x02:
                        self.bg_next_tile_attrib >>= 4
                    if self.vram_addr.coarse_x & 0x02:
                        self.bg_next_tile_attrib >>= 2
                    self.bg_next_tile_attrib &= 0x03
                    
                elif ((self.cycle - 1) % 8) == 4:
                    self.bg_next_tile_lsb = self.ppuRead((self.control.pattern_background << 12) + self.bg_next_tile_id << 4 + self.vram_addr.fine_y + 0)
                
                elif ((self.cycle - 1) % 8) == 6:
                    self.bg_next_tile_msb = self.ppuRead((self.control.pattern_background << 12) + self.bg_next_tile_id << 4 + self.vram_addr.fine_y + 8)
                
                elif ((self.cycle - 1) % 8) == 7:
                    IncrementScrollX()

            if self.cycle == 256:
                IncrementScrollY()

            if self.cycle == 257:
                TransferAddressX()

            if self.scanline == -1 and self.cycle >= 280 and self.cycle < 305:
                TransferAddressY()

        if self.scanline == 240:
            pass # nothing happens

            

        if self.scanline == 241 and self.cycle == 1:
            self.status.vertical_blank = True
            if self.control.enable_nmi:
                self.nmi = True

        bg_pixel = 0x00
        bg_palette = 0x00

        if self.mask.render_background:
            bit_mask = 0x8000 >> self.fine_x

            p0_pixel = (self.bg_shifter_pattern_lo & bit_mask) > 0
            p1_pixel = (self.bg_shifter_pattern_hi & bit_mask) > 0
            bg_pixel = (p1_pixel << 1) | p0_pixel

            p0_palette = (self.bg_shifter_attrib_lo & bit_mask) > 0
            p1_palette = (self.bg_shifter_attrib_hi & bit_mask) > 0
            bg_palette = (p1_palette << 1) | p0_palette
            

        self.sprScreen.setPixel((self.cycle - 1, self.scanline), self.getColorFromPaletteRam(bg_palette, bg_pixel))

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
        
        return self.sprPatternTable[i]

    def cpuWrite(self, addr, data):
        if (addr == 0x0000): # Control
            self.control.reg = data
            self.tram_addr.nametable_x = self.control.nametable_x
            self.tram_addr.nametable_y = self.control.nametable_y
        elif (addr == 0x0001): # Mask
            self.mask.reg = data
        elif (addr == 0x0002): # Status
            pass
        elif (addr == 0x0003): # OAM Address
            pass
        elif (addr == 0x0004): # OAM Data
            pass
        elif (addr == 0x0005): # Scroll
            if self.address_latch == 0:
                self.fine_x = data & 0x07
                self.tram_addr.coarse_x = data >> 3
                self.address_latch = 1
            else:
                self.fine_y = data & 0x07
                self.tram_addr.coarse_y = data >> 3
                self.address_latch = 0

        elif (addr == 0x0006): # PPU Address
            if self.address_latch == 0:
                self.tram_addr.reg = (self.tram_addr.reg & 0x00FF) | data
                self.address_latch = 1
            else:
                self.tram_addr.reg = (self.tram_addr.reg & 0xFF00) | (data << 8)
                self.vram_addr = self.tram_addr
                self.address_latch = 0
        elif (addr == 0x0007): # PPU Data
            self.ppuWrite(self.vram_addr.reg, data)
            self.vram_addr.reg += 32 if self.control.increment_mode else 1
            pass
        

    def cpuRead(self, addr, rdonly=False):
        data = 0x00

        if (addr == 0x0000): # Control
            pass
        elif (addr == 0x0001): # Mask
            pass
        elif (addr == 0x0002): # Status
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
            self.ppu_data_buffer = self.ppuRead(self.vram_addr.reg)

            if self.vram_addr.reg > 0x3F00:
                data = self.ppu_data_buffer

            self.vram_addr.reg += 32 if self.control.increment_mode else 1
        
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
            if self.cart.mirror == CartridgeClass.VERTICAL:
                if addr >= 0x0000 and addr <= 0x03FF:
                    data = self.tblName[0][addr & 0x03FF]
                if addr >= 0x0400 and addr <= 0x07FF:
                    data = self.tblName[1][addr & 0x03FF]
                if addr >= 0x0800 and addr <= 0x0BFF:
                    data = self.tblName[0][addr & 0x03FF]
                if addr >= 0x0C00 and addr <= 0x0FFF:
                    data = self.tblName[1][addr & 0x03FF]
                
            elif self.cart.mirror == CartridgeClass.HORIZONTAL:
                if addr >= 0x0000 and addr <= 0x03FF:
                    data = self.tblName[0][addr & 0x03FF]
                if addr >= 0x0400 and addr <= 0x07FF:
                    data = self.tblName[0][addr & 0x03FF]
                if addr >= 0x0800 and addr <= 0x0BFF:
                    data = self.tblName[1][addr & 0x03FF]
                if addr >= 0x0C00 and addr <= 0x0FFF:
                    data = self.tblName[1][addr & 0x03FF]
                
            

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
            if self.cart.mirror == CartridgeClass.VERTICAL:
                if addr >= 0x0000 and addr <= 0x03FF:
                    self.tblName[0][addr & 0x03FF] = data
                if addr >= 0x0400 and addr <= 0x07FF:
                    self.tblName[1][addr & 0x03FF] = data
                if addr >= 0x0800 and addr <= 0x0BFF:
                    self.tblName[0][addr & 0x03FF] = data
                if addr >= 0x0C00 and addr <= 0x0FFF:
                    self.tblName[1][addr & 0x03FF] = data
                
            elif self.cart.mirror == CartridgeClass.HORIZONTAL:
                if addr >= 0x0000 and addr <= 0x03FF:
                    self.tblName[0][addr & 0x03FF] = data
                if addr >= 0x0400 and addr <= 0x07FF:
                    self.tblName[0][addr & 0x03FF] = data
                if addr >= 0x0800 and addr <= 0x0BFF:
                    self.tblName[1][addr & 0x03FF] = data
                if addr >= 0x0C00 and addr <= 0x0FFF:
                    self.tblName[1][addr & 0x03FF] = data
                
            

        elif addr >= 0x3F00 and addr <= 0x3FFF:
            addr &= 0x001F
            addr = 0x0000 if addr == 0x0010 else addr
            addr = 0x0004 if addr == 0x0014 else addr
            addr = 0x0008 if addr == 0x0018 else addr
            addr = 0x000C if addr == 0x001C else addr
            self.tblPalette[addr] = data
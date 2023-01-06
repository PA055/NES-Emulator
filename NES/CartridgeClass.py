from dataclasses import dataclass
from Mapper_000Class import Mapper_000


@dataclass
class sHeader:
    name: str
    prg_rom_chunks: int
    chr_rom_chunks: int
    mapper1: int
    mapper2: int
    prg_ram_size: int
    tv_system1: int
    tv_system2: int
    unused: str

def toFile(filename, data, type='list', mode = 'w+'):
    with open(filename, mode) as f:
        if type == 'list':
            f.writelines(['\n' + str(datap) for datap in data])
        elif type == 'dict':
            f.writelines(['\n' + str(item) + ': ' + str(value) for item, value in data])
        elif type == 'raw':
            f.write(str(data))

HORIZONTAL = 1
VERTICAL = 2
ONESCREEN_LO = 3
ONESCREEN_HI = 4

class Cartridge:
    def __init__(self, filename):
        self.vPRGMemory = []
        self.vCHRMemory = []

        self.nMapperID = 0
        self.mirror = HORIZONTAL
        self.nPRGBanks = 0
        self.nCHRBanks = 0

        self.header = sHeader('    ', 0, 0, 0, 0, 0, 0, 0, '     ')

        self.bImageValid = False

        with open(filename, 'rb') as ifs:
            # read header
            if True:
                data = ifs.read(4)
                self.header.name = data.decode('ascii')
                data = ifs.read(1)
                self.header.prg_rom_chunks = ord(data)
                data = ifs.read(1)
                self.header.chr_rom_chunks = ord(data)
                data = ifs.read(1)
                self.header.mapper1 = ord(data)
                data = ifs.read(1)
                self.header.mapper2 = ord(data)
                data = ifs.read(1)
                self.header.prg_ram_size = ord(data)
                data = ifs.read(1)
                self.header.tv_system1 = ord(data)
                data = ifs.read(1)
                self.header.tv_system2 = ord(data)
                data = ifs.read(5)
                self.header.unused = data.decode('ascii')
            
            if self.header.mapper1 & 0x04:
                ifs.read(512)
            
            self.nMapperID = ((self.header.mapper2 >> 4) << 4) | (self.header.mapper1 >> 4)
            self.mirror = VERTICAL if (self.header.mapper1 & 0x01) else HORIZONTAL

            nFileType = 1

            if nFileType == 0:
                pass

            elif nFileType == 1:
                self.nPRGBanks = self.header.prg_rom_chunks
                for i in range(self.nPRGBanks * 16384):
                    data = ifs.read(1)
                    self.vPRGMemory.append(ord(data))

                self.nCHRBanks = self.header.chr_rom_chunks
                for i in range(self.nCHRBanks * 8192):
                    data = ifs.read(1)
                    self.vCHRMemory.append(ord(data))

            elif nFileType == 2:
                pass

            if self.nMapperID == 0:
                self.pMapper = Mapper_000(self.nPRGBanks, self.nCHRBanks)
            elif self.nMapperID == 1:
                self.pMapper = None

            self.bImageValid = True


    def imageValid(self):
        return self.bImageValid

    def cpuRead(self, addr, data):
        mapped_addr, mapperMod = self.pMapper.cpuMapRead(addr, 0)
        if mapperMod:
            data = self.vPRGMemory[mapped_addr]
            return data, True
        else:
            return data, False

    def cpuWrite(self, addr, data):
        mapped_addr, mapperMod = self.pMapper.cpuMapWrite(addr, 0)
        if mapperMod:
            self.vPRGMemory[mapped_addr] = data
            return True
        else:
            return False

    def ppuRead(self, addr, data):
        mapped_addr, mapperMod = self.pMapper.ppuMapRead(addr, 0)
        if mapperMod:
            data = self.vCHRMemory[mapped_addr]
            return data, True
        else:
            return data, False

    def ppuWrite(self, addr, data):
        mapped_addr, mapperMod = self.pMapper.ppuMapWrite(addr, 0)
        if mapperMod:
            self.vCHRMemory[mapped_addr] = data
            return True
        else:
            return False
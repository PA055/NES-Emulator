from MapperBase import Mapper

class Mapper_000(Mapper):
    def __init__(self, prgBanks, chrBanks):
        super().__init__(prgBanks, chrBanks)

    def cpuMapRead(self, addr, mapped_addr):
        if (addr >= 0x8000 and addr <= 0xFFFF):
            mapped_addr = addr & (0x7FFF if self.nPRGBanks > 1 else 0x3FFF)
            return mapped_addr, True

        return mapped_addr, False

    def cpuMapWrite(self, addr, mapped_addr):
        if (addr >= 0x8000 and addr <= 0xFFFF):
            mapped_addr = addr & (0x7FFF if self.nPRGBanks > 1 else 0x3FFF)
            return mapped_addr, True
        
        return mapped_addr, False

    def ppuMapRead(self, addr, mapped_addr):
        if (addr >= 0x0000 and addr <= 0x1FFF):
            mapped_addr = addr
            return mapped_addr, True
        
        return mapped_addr, False

    def ppuMapWrite(self, addr, mapped_addr):
        if (addr >= 0x0000 and addr <= 0x1FFF):
            if self.nCHRBanks == 0:
                mapped_addr = addr
                return mapped_addr, True

        return mapped_addr, False
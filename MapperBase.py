

class Mapper:
    def __init__(self, prgBanks, chrBanks):
        self.nPRGBanks = prgBanks
        self.nCHRBanks = chrBanks

    def cpuMapRead(self, addr, mapped_addr):
        return mapped_addr, False

    def cpuMapWrite(self, addr, mapped_addr):
        return mapped_addr, False

    def ppuMapRead(self, addr, mapped_addr):
        return mapped_addr, False

    def ppuMapWrite(self, addr, mapped_addr):
        return mapped_addr, False


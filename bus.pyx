from cpu import CPU

cdef class Bus:
    cdef public object cpu
    cdef public unsigned char ram[65536] # 64 kilobytes

    def __init__(self, cpu=None):
        if cpu:
            self.cpu = cpu
        else:
            self.cpu = CPU()
        self.cpu.ConnectBus(self)

        self.ram = [0x00 for i in self.ram]

    cdef public unsigned char read(self, unsigned short addr, bint bReadOnly):
        if (addr >= 0x0000 and addr <= 0xFFFF):
            return self.ram[addr]
        return 0x00

    cdef public void write(self, unsigned short addr, unsigned char data):
        if (addr >= 0x0000 and addr <= 0xFFFF):
            self.ram[addr] = data
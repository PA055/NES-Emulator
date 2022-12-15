from pygame.locals import *
from PixelGameEngine import *
import olc6502Class
from BusClass import Bus
from collections import OrderedDict

cpu = olc6502Class.olc6502()
nes = Bus(cpu)

mapAsm = OrderedDict()

def hex(n, d):
    s = ['0' for i in range(d)]
    for i in range(d-1, -1, -1):
        s[i] = "0123456789ABCDEF"[n & 0xF]
        n >>= 4
    return ''.join(s)

def DrawRam(game, x, y, nAddr, nRows, nColumns):
    nRamX = x
    nRamY = y
    for row in range(nRows):
        sOffset = '$' + hex(nAddr, 4) + ':'
        for col in range(nColumns):
            sOffset += ' ' + hex(nes.read(nAddr, True), 2)
            nAddr += 1

        game.drawString(sOffset, (nRamX, nRamY), Color.WHITE)
        nRamY += 10


def DrawCPU(game, x, y):
    game.drawString('STATUS:', (x, y), Color.WHITE)
    game.drawString('N', (x + 64, y), Color.GREEN if (nes.cpu.status & (1 << olc6502Class.N)) else Color.RED)
    game.drawString('V', (x + 80, y), Color.GREEN if (nes.cpu.status & (1 << olc6502Class.V)) else Color.RED)
    game.drawString('-', (x + 96, y), Color.GREEN if (nes.cpu.status & (1 << olc6502Class.U)) else Color.RED)
    game.drawString('B', (x + 112, y), Color.GREEN if (nes.cpu.status & (1 << olc6502Class.B)) else Color.RED)
    game.drawString('D', (x + 128, y), Color.GREEN if (nes.cpu.status & (1 << olc6502Class.D)) else Color.RED)
    game.drawString('I', (x + 144, y), Color.GREEN if (nes.cpu.status & (1 << olc6502Class.I)) else Color.RED)
    game.drawString('Z', (x + 160, y), Color.GREEN if (nes.cpu.status & (1 << olc6502Class.Z)) else Color.RED)
    game.drawString('C', (x + 178, y), Color.GREEN if (nes.cpu.status & (1 << olc6502Class.C)) else Color.RED)
    game.drawString('PC: $' + hex(nes.cpu.pc, 4), (x, y + 10), Color.WHITE)
    game.drawString('A: $' + hex(nes.cpu.a, 2) + "  [" + str(nes.cpu.a) + ']', (x, y + 20), Color.WHITE)
    game.drawString('X: $' + hex(nes.cpu.x, 2) + "  [" + str(nes.cpu.x) + ']', (x, y + 30), Color.WHITE)
    game.drawString('Y: $' + hex(nes.cpu.y, 2) + "  [" + str(nes.cpu.y) + ']', (x, y + 40), Color.WHITE)
    game.drawString('Stack Ptr: $' + hex(nes.cpu.stkp, 4), (x, y + 50), Color.WHITE)

# TODO: Fix This
def DrawCode(game, x, y, nLines):
    pcOffset = 0
    nLineY = (nLines >> 1) * 10 + y
    if (mapAsm.get(nes.cpu.pc + pcOffset)): # check if item exists
        game.drawString(mapAsm[nes.cpu.pc + pcOffset], (x, nLineY), Color.CYAN)
        while nLineY < (nLines * 10) + y:
            nLineY += 10
            if (mapAsm.get(nes.cpu.pc + pcOffset)): # check if item exists
                pcOffset += 1
                game.drawString(mapAsm[nes.cpu.pc + pcOffset], (x, nLineY))

    pcOffset = 0
    nLineY = (nLines >> 1) * 10 + y
    if (mapAsm.get(nes.cpu.pc + pcOffset)): # check if item exists
        while nLineY > y:
            nLineY -= 10
            if (mapAsm.get(nes.cpu.pc + pcOffset)): # check if item exists
                pcOffset -= 1
                game.drawString(mapAsm[nes.cpu.pc + pcOffset], (x, nLineY))

def Start(game):
    '''
        Program (assembled at https://www.masswerk.at/6502/assembler.html)
            *=$8000
			LDX #10
			STX $0000
			LDX #3
			STX $0001
			LDY $0000
			LDA #0
			CLC
			loop
			ADC $0001
			DEY
			BNE loop
			STA $0002
			NOP
			NOP
			NOP
    '''
    
    ss = list("A2 0A 8E 00 00 A2 03 8E 01 00 AC 00 00 A9 00 18 6D 01 00 88 D0 FA 8D 02 00 EA EA EA".split())
    nOffset = 0x8000
    while len(ss) > 0:
        b = ss.pop(0)
        nes.ram[nOffset] = int(b, 16)
        nOffset += 1

    nes.ram[0xFFFC] = 0x00
    nes.ram[0xFFFD] = 0x00

    mapAsm = nes.cpu.disassemble(0x0000, 0xFFFF)

    nes.cpu.reset()
    return True

def Update(game):
    game.clearScreen()
    
    key = game.getKeyDown()

    if (key == K_SPACE):
        nes.cpu.clock()
        while not nes.cpu.complete():
            nes.cpu.clock()

    if key == K_r:
        nes.cpu.reset()

    if key == K_i:
        nes.cpu.irq()

    if key == K_n:
        nes.cpu.nmi()


    DrawRam(game, 2, 2, 0x0000, 16, 16)
    DrawRam(game, 2, 2, 0x8000, 16, 16)

    DrawCPU(game, 448, 2)
    DrawCode(game, 448, 72, 26)

    game.drawString("SPACE = Step Instruction    R = RESET    I = IRQ    N = NMI", (10, 370), Color.WHITE)

    return True

    
gameEngine = PixelEngine('NES Demo', 480, 680, 2, 2, 0.75)
gameEngine.setBackground(Color.DARK_BLUE)
keys = gameEngine.getKeyDown()

gameEngine.Start(Start, Update)


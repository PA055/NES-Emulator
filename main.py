from PixelGameEngine import *
import olc6502Class
from BusClass import Bus

cpu = olc6502Class.olc6502()
nes = Bus(cpu)


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
    game.drawString('N', (x + 64, y), Color.GREEN if (nes.cpu.status & (1 << olc6502.N)) else Color.RED)
    game.drawString('V', (x + 80, y), Color.GREEN if (nes.cpu.status & (1 << olc6502.V)) else Color.RED)
    game.drawString('-', (x + 96, y), Color.GREEN if (nes.cpu.status & (1 << olc6502.U)) else Color.RED)
    game.drawString('B', (x + 112, y), Color.GREEN if (nes.cpu.status & (1 << olc6502.B)) else Color.RED)
    game.drawString('D', (x + 128, y), Color.GREEN if (nes.cpu.status & (1 << olc6502.D)) else Color.RED)
    game.drawString('I', (x + 144, y), Color.GREEN if (nes.cpu.status & (1 << olc6502.I)) else Color.RED)
    game.drawString('Z', (x + 160, y), Color.GREEN if (nes.cpu.status & (1 << olc6502.Z)) else Color.RED)
    game.drawString('C', (x + 178, y), Color.GREEN if (nes.cpu.status & (1 << olc6502.C)) else Color.RED)
    game.drawString('PC: $' + hex(nes.cpu.pc, 4), (x, y + 10), Color.WHITE)
    game.drawString('A: $' + hex(nes.cpu.a, 2) + "  [" + str(nes.cpu.a) + ']', (x, y + 20), Color.WHITE)
    game.drawString('X: $' + hex(nes.cpu.x, 2) + "  [" + str(nes.cpu.x) + ']', (x, y + 30), Color.WHITE)
    game.drawString('Y: $' + hex(nes.cpu.y, 2) + "  [" + str(nes.cpu.y) + ']', (x, y + 40), Color.WHITE)
    game.drawString('Stack Ptr: $' + hex(nes.cpu.stkp, 4), (x, y + 50), Color.WHITE)

def DrawCode(game, x, y, nLines):
    pass

def Start(game):
    return True

def Update(game):
    return True

gameEngine = PixelEngine('NES Demo', 480, 680, 2, 2, 0.5)
gameEngine.setBackground(Color.DARK_BLUE)

gameEngine.Start(Start, Update)


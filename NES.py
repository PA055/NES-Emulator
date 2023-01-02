import pygame, sys, time
from pygame.locals import *
from PixelGameEngine import Color, Sprite
import olc6502Class
import olc2C02Class
from BusClass import Bus
from CartridgeClass import Cartridge
from collections import OrderedDict



pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = (780, 480)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('kongtext.ttf', 8)

cart = None
ppu = olc2C02Class.olc2C02()
cpu = olc6502Class.olc6502()
nes = Bus(cpu, ppu)

mapAsm = OrderedDict()


bEmulationRun = False
fResidualTime = 0.0

nSelectedPalette = 0x00


def toFile(filename, data, type='list', mode = 'w+'):
    with open(filename, mode) as f:
        if type == 'list':
            f.writelines(['\n' + str(datap) for datap in data])
        elif type == 'dict':
            f.writelines(['\n' + str(item) + ': ' + str(value) for item, value in data])
        elif type == 'raw':
            f.write(str(data))

def hex(n, d):
    s = ['0' for i in range(d)]
    for i in range(d-1, -1, -1):
        s[i] = "0123456789ABCDEF"[n & 0xF]
        n >>= 4
    return ''.join(s)

def drawCPU(x, y):
    surf = font.render('STATUS:', False, Color.WHITE)
    screen.blit(surf, (x, y))

    surf = font.render('N', False, Color.GREEN if (nes.cpu.status & (1 << olc6502Class.N)) else Color.RED)
    screen.blit(surf, (x + 74, y))

    surf = font.render('V', False, Color.GREEN if (nes.cpu.status & (1 << olc6502Class.V)) else Color.RED)
    screen.blit(surf, (x + 88, y))
    
    surf = font.render('-', False, Color.GREEN if (nes.cpu.status & (1 << olc6502Class.U)) else Color.RED)
    screen.blit(surf, (x + 106, y))
    
    surf = font.render('B', False, Color.GREEN if (nes.cpu.status & (1 << olc6502Class.B)) else Color.RED)
    screen.blit(surf, (x + 120, y))
    
    surf = font.render('D', False, Color.GREEN if (nes.cpu.status & (1 << olc6502Class.D)) else Color.RED)
    screen.blit(surf, (x + 138, y))
    
    surf = font.render('I', False, Color.GREEN if (nes.cpu.status & (1 << olc6502Class.I)) else Color.RED)
    screen.blit(surf, (x + 154, y))
    
    surf = font.render('Z', False, Color.GREEN if (nes.cpu.status & (1 << olc6502Class.Z)) else Color.RED)
    screen.blit(surf, (x + 170, y))
    
    surf = font.render('C', False, Color.GREEN if (nes.cpu.status & (1 << olc6502Class.C)) else Color.RED)
    screen.blit(surf, (x + 188, y))

    surf = font.render('PC: $' + hex(nes.cpu.pc, 4), False, Color.WHITE)
    screen.blit(surf, (x, y + 10))

    surf = font.render('A: $' + hex(nes.cpu.a, 2) + "  [" + str(nes.cpu.a) + ']', False, Color.WHITE)
    screen.blit(surf, (x, y + 20))
    
    surf = font.render('X: $' + hex(nes.cpu.x, 2) + "  [" + str(nes.cpu.x) + ']', False, Color.WHITE)
    screen.blit(surf, (x, y + 30))
    
    surf = font.render('Y: $' + hex(nes.cpu.y, 2) + "  [" + str(nes.cpu.y) + ']', False, Color.WHITE)
    screen.blit(surf, (x, y + 40))
    
    surf = font.render('Stack Ptr: $' + hex(nes.cpu.stkp, 4), False, Color.WHITE)
    screen.blit(surf, (x, y + 50))
    

def drawCode(x, y, nLines):
    pcOffset = 0
    nLineY = (nLines >> 1) * 10 + y
    if ((nes.cpu.pc + pcOffset) in list(mapAsm.keys())): # check if item exists
        pcOffset += 1
        while nLineY < (nLines * 10) + y:
            if ((nes.cpu.pc + pcOffset) in list(mapAsm.keys())): # check if item exists
                nLineY += 10
                surf = font.render(mapAsm[nes.cpu.pc + pcOffset], False, Color.WHITE)
                screen.blit(surf, (x, nLineY))
            pcOffset += 1

    pcOffset = 0
    nLineY = (nLines >> 1) * 10 + y
    if ((nes.cpu.pc + pcOffset) in list(mapAsm.keys())): # check if item exists
        surf = font.render(mapAsm[nes.cpu.pc + pcOffset], False, Color.CYAN)
        screen.blit(surf, (x, nLineY))
        pcOffset -= 1
        while nLineY > y:
            if ((nes.cpu.pc + pcOffset) in list(mapAsm.keys())): # check if item exists
                nLineY -= 10
                surf = font.render(mapAsm[nes.cpu.pc + pcOffset], False, Color.WHITE)
                screen.blit(surf, (x, nLineY))
            pcOffset -= 1

def Start():
    global mapAsm

    cart = Cartridge('ROMs/nestest.nes')
    if not cart.imageValid():
        pygame.quit()
        sys.exit()

    nes.insertCartridge(cart)

    mapAsm = nes.cpu.disassemble(0x0000, 0xFFFF)

    toFile('Dissasembled.txt', [instr for addr, instr in mapAsm.items()])

    nes.cpu.reset()

def Update(dt):
    global bEmulationRun, fResidualTime, nSelectedPalette

    screen.fill(Color.DARK_BLUE)

    if bEmulationRun:
        if fResidualTime > 0:
            fResidualTime -= dt
        else:
            fResidualTime += (1/60) - dt

            nes.clock()
            while not nes.ppu.frame_complete:
                nes.clock()

            nes.ppu.frame_complete = False

    drawCode(520, 80, 25)
    drawCPU(520, 2)

    start = time.perf_counter()
    nSwatchSize = 6
    for p in range(8):
        for s in range(4):
            rect = pygame.Rect((516 + p * (nSwatchSize * 5) + s * nSwatchSize, 340), (nSwatchSize, nSwatchSize))
            pygame.draw.rect(screen, nes.ppu.getColorFromPaletteRam(p, s), rect)

    rect = pygame.Rect(516 + nSelectedPalette * (nSwatchSize * 5) - 1, 339, (nSwatchSize * 4), nSwatchSize)
    pygame.draw.rect(screen, Color.WHITE, rect, width=1)
    end = time.perf_counter()
    # print(f'Palette: { (end - start) } sec')


    start = time.perf_counter()
    screen.blit( nes.ppu.getPatternTable(0, nSelectedPalette).surf, (648, 348))
    end = time.perf_counter()
    # print(f'Pattern Table 0: { (end - start) } sec')

    start = time.perf_counter()
    screen.blit( nes.ppu.getPatternTable(1, nSelectedPalette).surf, (516, 348))
    end = time.perf_counter()
    # print(f'Pattern Table 1: { (end - start) } sec')

    start = time.perf_counter()
    screen.blit(pygame.transform.scale2x(nes.ppu.getScreen().surf), (0, 0))
    end = time.perf_counter()
    # print(f'Screen: { (end - start) } sec')

    return



Start()

while True:
    dt = clock.tick(100) / 1000

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if not bEmulationRun:
                if event.key == K_c:
                    start = time.perf_counter()
                    nes.clock()
                    while not nes.cpu.complete():
                        nes.clock()
                    end = time.perf_counter()
                    print(f'Instruction: { (end - start) } sec')

                if event.key == K_f:
                    start = time.perf_counter()
                    nes.clock()
                    while not nes.ppu.frame_complete:
                        nes.clock()
                    
                    nes.clock()
                    while not nes.cpu.complete():
                        nes.clock()

                    nes.ppu.frame_complete = False
                    end = time.perf_counter()
                    print(f'Frame: { (end - start) } sec')

            if event.key == K_SPACE:
                bEmulationRun = not bEmulationRun

            if event.key == K_r:
                nes.reset()

            if event.key == K_p:
                nSelectedPalette = (nSelectedPalette + 1) & 0x07        

    Update(dt)

    pygame.display.set_caption(f'NES Emulator         FPS: {clock.get_fps():.2f}')
    pygame.display.update()

import pygame, sys
from collections import OrderedDict

import cpu, bus

if True: # profiling setup
    import cProfile, pstats # profiling (below)
    '''
    with cProfile.Profile() as pr:
        pass

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats('profile_file.prof')
    '''
if True: # logging setup
    import logging

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('nes.log')

    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.WARNING)

    console_handler.setFormatter(logging.Formatter('[%(levelname)s] - %(name)s - %(asctime)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S'))
    file_handler.setFormatter(logging.Formatter('[%(levelname)s] - %(name)s - %(asctime)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S'))

    log.addHandler(console_handler)
    log.addHandler(file_handler)

    log.info('msg')


cpu6502 = cpu.CPU()
nes = bus.Bus(cpu6502)

C = 0
Z = 1
I = 2
D = 3
B = 4
U = 5
V = 6
N = 7

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = (780, 480)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('kongtext.ttf', 8)


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

    surf = font.render('N', False, Color.GREEN if (nes.cpu.status & (1 << N)) else Color.RED)
    screen.blit(surf, (x + 74, y))

    surf = font.render('V', False, Color.GREEN if (nes.cpu.status & (1 << V)) else Color.RED)
    screen.blit(surf, (x + 88, y))
    
    surf = font.render('-', False, Color.GREEN if (nes.cpu.status & (1 << U)) else Color.RED)
    screen.blit(surf, (x + 106, y))
    
    surf = font.render('B', False, Color.GREEN if (nes.cpu.status & (1 << B)) else Color.RED)
    screen.blit(surf, (x + 120, y))
    
    surf = font.render('D', False, Color.GREEN if (nes.cpu.status & (1 << D)) else Color.RED)
    screen.blit(surf, (x + 138, y))
    
    surf = font.render('I', False, Color.GREEN if (nes.cpu.status & (1 << I)) else Color.RED)
    screen.blit(surf, (x + 154, y))
    
    surf = font.render('Z', False, Color.GREEN if (nes.cpu.status & (1 << Z)) else Color.RED)
    screen.blit(surf, (x + 170, y))
    
    surf = font.render('C', False, Color.GREEN if (nes.cpu.status & (1 << C)) else Color.RED)
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


while True:
    dt = clock.tick(100) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.set_caption(f'NES Emulator         FPS: {clock.get_fps():.2f}')
    pygame.display.update()
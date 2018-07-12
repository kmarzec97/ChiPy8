from ctypes import *
from tkinter import *
import random
import time
import sys
def canvasClear(c):
    i = 0
    while i < 2048:
        c.itemconfig(s[i], fill='black')
        i += 1
def keyPress(event):
    if event.char == 'v':
        chip8.keypad[0] = 1
    elif event.char == 'q':
        chip8.keypad[1] = 1
    elif event.char == 'w':
        chip8.keypad[2] = 1
    elif event.char == 'e':
        chip8.keypad[3] = 1
    elif event.char == 'a':
        chip8.keypad[4] = 1
    elif event.char == 'x':
        chip8.keypad[5] = 1
    elif event.char == 'd':
        chip8.keypad[6] = 1
    elif event.char == 'z':
        chip8.keypad[7] = 1
    elif event.char == 's':
        chip8.keypad[8] = 1
    elif event.char == 'c':
        chip8.keypad[9] = 1
    elif event.char == '1':
        chip8.keypad[10] = 1
    elif event.char == '2':
        chip8.keypad[11] = 1
    elif event.char == '3':
        chip8.keypad[12] = 1
    elif event.char == '4':
        chip8.keypad[13] = 1
    elif event.char == '5':
        chip8.keypad[14] = 1
    elif event.char == '6':
        chip8.keypad[15] = 1
    elif event.keysym == 'Escape':
        root.destroy()

def keyRelease(event):
    if event.char == 'v':
        chip8.keypad[9] = 0
    elif event.char == 'q':
        chip8.keypad[1] = 0
    elif event.char == 'w':
        chip8.keypad[2] = 0
    elif event.char == 'e':
        chip8.keypad[3] = 0
    elif event.char == 'a':
        chip8.keypad[4] = 0
    elif event.char == 'x':
        chip8.keypad[5] = 0
    elif event.char == 'd':
        chip8.keypad[6] = 0
    elif event.char == 'z':
        chip8.keypad[7] = 0
    elif event.char == 's':
        chip8.keypad[8] = 0
    elif event.char == 'c':
        chip8.keypad[9] = 0
    elif event.char == '1':
        chip8.keypad[10] = 0
    elif event.char == '2':
        chip8.keypad[11] = 0
    elif event.char == '3':
        chip8.keypad[12] = 0
    elif event.char == '4':
        chip8.keypad[13] = 0
    elif event.char == '5':
        chip8.keypad[14] = 0
    elif event.char == '6':
        chip8.keypad[15] = 0
#==========================================================

class CPU:
    memory: c_uint8 = [0]*0x1000
    regs: c_uint8 = [0]*0x10
    keypad: c_uint8 = [0]*0x10
    picture: c_uint8 = [0]*0x800
    stack: c_uint16 = [0]*0x10
    font: c_uint8 = [ 0xF0, 0x90, 0x90, 0x90, 0xF0, 0x20, 0x60, 0x20, 0x20, 0x70, 0xF0, 0x10, 0xF0, 0x80, 0xF0, 0xF0, 0x10, 0xF0, 0x10, 0xF0, 0x90, 0x90, 0xF0, 0x10, 0x10, 0xF0, 0x80, 0xF0, 0x10, 0xF0, 0xF0, 0x80, 0xF0, 0x90, 0xF0, 0xF0, 0x10, 0x20, 0x40, 0x40, 0xF0, 0x90, 0xF0, 0x90, 0xF0, 0xF0, 0x90, 0xF0, 0x10, 0xF0, 0xF0, 0x90, 0xF0, 0x90, 0x90, 0xE0, 0x90, 0xE0, 0x90, 0xE0, 0xF0, 0x80, 0x80, 0x80, 0xF0, 0xE0, 0x90, 0x90, 0x90, 0xE0, 0xF0, 0x80, 0xF0, 0x80, 0xF0, 0xF0, 0x80, 0xF0, 0x80, 0x80]
    def __init__(self):
        self.iteration = -1
        self.canvasReset = False
        print("Setting up things for you!")
        self.resetInternals()
        self.resetMemory()
        self.resetScreen()
        self.injectFont()
        self.programCounter = 0x200
        self.index = 0
        self.stackPointer = 0
        self.opcode = 0
        self.delayTicker = 0
        self.loadROM()
        print("Reading and executing ROM")
    def dumpPicture(self):
        print(self.picture)
    def codeDiag(self):
        self.iteration += 1
        print("CODE:", self.opcode, "programCounter:", self.programCounter, "iteration:", self.iteration)
        print("INDEX:",self.index, "stackPointer:", self.stackPointer)
    def memoryDump(self):
        i = 0
        while i < 1000:
            print("INDEX:",i,self.memory[i])
            i += 1
    def loadROM(self):
        try:
            rom = open(game, 'rb').read()
        except IOError:
            print('Rom not found.')
            exit()
        for index, val in enumerate(rom):
            self.memory[index + 0x200] = val
    def resetInternals(self):
        i = 0
        while i < 0x10:
            self.stack[i] = 0
            self.keypad[i] = 0
            self.regs[i] = 0
            i += 1
    def resetScreen(self):
        i = 0
        while i < 0x800:
            self.picture[i] = 0
            i += 1
        self.canvasReset = True
    def resetMemory(self):
        i = 0
        while i < 0x1000:
            self.memory[i] = 0
            i += 1
    def injectFont(self):
        i = 0
        while i < 80:
            self.memory[i] = self.font[i]
            i += 1
    def CPUCycle(self):
        self.opcode = (self.memory[self.programCounter] << 8) | self.memory[self.programCounter+1]
        self.opcode %= 65536
        #============= DEBUG OPTIONS
        #self.memoryDump()
        #self.codeDiag()
        #===========================
    #0NNN
        if(self.opcode >> 12) == 0x0:
            if(self.opcode & 0x000F) == 0x0000:
                self.resetScreen()
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x000E:
                self.stackPointer -= 1
                self.programCounter = self.stack[self.stackPointer]
                self.programCounter += 2
    #1NNN
        elif(self.opcode >> 12) == 0x1:
            self.programCounter = self.opcode & 0x0FFF
    #2NNN
        elif(self.opcode >> 12) == 0x2:
            self.stack[self.stackPointer] = self.programCounter
            self.stack[self.stackPointer] %= 65536
            self.stackPointer += 1
            self.programCounter = self.opcode & 0x0FFF
    #3NNN
        elif(self.opcode >> 12) == 0x3:
            if(self.regs[(self.opcode & 0x0F00) >> 8] == (self.opcode & 0x00FF)):
                self.programCounter += 4
            else:
                self.programCounter += 2
    #4NNN
        elif(self.opcode >> 12) == 0x4:
            if(self.regs[(self.opcode & 0x0F00) >> 8] != (self.opcode & 0x00FF)):
               self.programCounter += 4
            else:
                self.programCounter += 2
    #5NNN
        elif(self.opcode >> 12) == 0x5:
            if(self.regs[(self.opcode & 0x0F00) >> 8] == self.regs[(self.opcode & 0x00F0) >> 4]):
                self.programCounter += 4
            else:
                self.programCounter += 2
    #6NNN
        elif(self.opcode >> 12) == 0x6:
            self.regs[(self.opcode & 0x0F00)>>8] = (self.opcode & 0x00FF)%256
            self.programCounter += 2
    #7NNN
        elif(self.opcode >> 12) == 0x7:
            self.regs[(self.opcode & 0x0F00)>>8] += (self.opcode & 0x00FF)
            self.regs[(self.opcode & 0x0F00)>>8] %=256
            self.programCounter += 2
    #8NNN
        elif(self.opcode >> 12) == 0x8:
            if(self.opcode & 0x000F) == 0x0000:
                self.regs[(self.opcode & 0x0F00)>>8] = self.regs[(self.opcode & 0x00F0) >> 4]%256
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0001:
                self.regs[(self.opcode & 0x0F00) >> 8] |= self.regs[(self.opcode & 0x00F0) >> 4]%256
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0002:
                self.regs[(self.opcode & 0x0F00) >> 8] &= self.regs[(self.opcode & 0x00F0) >> 4]%256
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0003:
                self.regs[(self.opcode & 0x0F00) >> 8] ^= self.regs[(self.opcode & 0x00F0) >> 4]%256
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0004:
                self.regs[(self.opcode & 0x0F00) >> 8] += self.regs[(self.opcode & 0x00F0) >> 4]%256
                if self.regs[(self.opcode & 0x00F0) >> 4] > (0xFF - self.regs[(self.opcode & 0x0F00) >> 8]):
                    self.regs[0xF] = 1
                else:
                    self.regs[0xF] = 0
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0005:
                if self.regs[(self.opcode & 0x00F0) >> 4] > self.regs[(self.opcode & 0x0F00) >> 8]:
                    self.regs[0xF] = 0
                else:
                    self.regs[0xF] = 1
                self.regs[(self.opcode & 0x0F00) >> 8] -= self.regs[(self.opcode & 0x00F0) >> 4]
                if self.regs[(self.opcode & 0x0F00) >> 8] < 0:
                    self.regs[(self.opcode & 0x0F00) >> 8] += 256
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0006:
                self.regs[0xF] = self.regs[(self.opcode & 0x0F00) >> 8] >> 1
                self.regs[(self.opcode & 0x0F00) >> 8] >>= 1
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0007:
                if self.regs[(self.opcode * 0x0F00) >> 8] > self.regs[(self.opcode & 0x00F0) >> 4]:
                    self.regs[0xF] = 0
                else:
                    self.regs[0xF] = 1
                self.regs[(self.opcode & 0x0F00) >> 8] = self.regs[(self.opcode & 0x00F0) >> 4] - self.regs[(self.opcode & 0x0F00) >> 8]
                if self.regs[(self.opcode & 0x0F00) >> 8] < 0:
                    self.regs[(self.opcode & 0x0F00) >> 8] += 256
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x000E:
                self.regs[0xF] = self.regs[(self.opcode & 0x0F00) >> 8] >> 7
                self.regs[(self.opcode & 0x0F00) >> 8] <<= 1
                self.programCounter += 2
    #9NNN
        elif(self.opcode >> 12) == 0x9:
            if self.regs[(self.opcode & 0x0F00) >> 8] != self.regs[(self.opcode & 0x00F0) >> 4]:
                self.programCounter += 4
            else:
                self.programCounter += 2
    #ANNN
        elif(self.opcode >> 12) == 0xA:
            self.index = (self.opcode & 0x0FFF)%65536
            self.programCounter += 2
    #BNNN
        elif(self.opcode >> 12) == 0xB:
            self.programCounter = ((self.opcode & 0x0FFF) + self.regs(0x0))%65536
    #CNNN
        elif(self.opcode >> 12) == 0xC:
            self.regs[(self.opcode & 0x0F00) >> 8] = ((random.randint(0,0x100)) & (self.opcode & 0x00FF))%256
            self.programCounter += 2
    #DNNN
#=======================================RENDERING==============================================
        elif(self.opcode >> 12) == 0xD:
            self.coordX = self.regs[(self.opcode & 0x0F00) >> 8]
            self.coordY = self.regs[(self.opcode & 0x00F0) >> 4]
            self.height = self.opcode & 0x000F
            self.regs[0xF] = 0
            i = 0
            while i < self.height:
                self.pixel = self.memory[self.index + i]
                j = 0
                while j < 8:
                    if (self.pixel & (0x80 >> j)) != 0:
                        if self.picture[(self.coordX + j + (self.coordY + i)*64)%2048] == 1:
                            self.regs[0xF] = 1
                        if (self.coordX + j + ((self.coordY + i)*64)) <= 2047:
                            self.picture[(self.coordX + j + (self.coordY + i) * 64)] = not(self.picture[(self.coordX + j + (self.coordY + i) * 64)])
                            if (self.coordX + j + (self.coordY + i) * 64) <= 2047 and self.picture[(self.coordX + j + (self.coordY + i) * 64)] == 1:
                                c.itemconfig(s[(self.coordX + j + (self.coordY + i) * 64) % 2048], fill=color)
                            else:
                                c.itemconfig(s[(self.coordX + j + (self.coordY + i) * 64) % 2048], fill='black')
                    j += 1
                i += 1
            self.programCounter += 2
#===============================================================================================
    #ENNN
        elif(self.opcode >> 12) == 0xE:
            if(self.opcode & 0x00FF) == 0x009E:
                if self.keypad[self.regs[(self.opcode & 0x0F00) >> 8]] != 0:
                    self.programCounter += 4
                else:
                    self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x00A1:
                if self.keypad[self.regs[(self.opcode & 0x0F00) >> 8]] == 0:
                    self.programCounter += 4
                else:
                    self.programCounter += 2
    #FNNN
        elif(self.opcode >> 12) == 0xF:
            if(self.opcode & 0x00FF) == 0x0007:
                self.regs[(self.opcode & 0x0F00) >> 8] = self.delayTicker%256
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x000A:
                self.isPressed = 0
                for i in range (0, 16):
                    if self.keypad[i] != 0:
                        self.regs[(self.opcode & 0x0F00) >> 8] = i%256
                        self.isPressed = 1
                if self.isPressed == 0:
                    return
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0015:
                self.delayTicker = (self.regs[(self.opcode & 0x0F00) >> 8])%256
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0018:
                self.soundTicker = (self.regs[(self.opcode & 0x0F00) >> 8])%256
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x001E:
                if self.index + self.regs[(self.opcode & 0x0F00) >> 8] > 0xFFF:
                    self.regs[0xF] = 1
                else:
                    self.regs[0xF] = 0
                self.index += self.regs[(self.opcode & 0x0F00)>>8]
                self.index %= 65536
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0029:
                self.index = (self.regs[(self.opcode & 0x0F00) >> 8] * 0x5)%65536
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0033:
                self.memory[self.index] = int(self.regs[(self.opcode & 0x0F00) >> 8] / 0x64)
                self.memory[self.index + 1] = int((self.regs[(self.opcode & 0x0F00) >> 8] / 0xA) % 0xA)
                self.memory[self.index + 2] = int((self.regs[(self.opcode & 0x0F00) >> 8] % 0x64) % 0xA)
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0055:
                for i in range (0 , (self.opcode & 0x0F00) >> 8):
                    self.memory[self.index + i] = self.regs[i]
                self.index += (((self.opcode & 0x0F00) >> 8) + 1)%65536
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0065:
                i = 0
                while i <= ((self.opcode & 0x0F00) >> 8):
                    self.regs[i] = (self.memory[self.index + i])%256
                    i += 1
                self.index += (((self.opcode & 0x0F00) >> 8) + 1)%65536
                self.programCounter += 2
        if self.delayTicker > 0:
                self.delayTicker -= 1
        self.programCounter %= 65536

if len(sys.argv) > 1:
    resolution = sys.argv[1]
else:
    resolution = '1280x640'  #2:1 ratio only
if len(sys.argv) > 2:
    speed = float(sys.argv[2])
else:
    speed = 0.002
if len(sys.argv) > 3:
    game = sys.argv[3]
else:
    game = "brix.ch8"
if len(sys.argv) > 4:
    color = sys.argv[4]
else:
    color = 'white'
chip8 = CPU()
root = Tk()
root.geometry(resolution)
root.title('ChiPy8 - '+ game)
root.resizable(False,False)
root.update()
resMultip = int(root.winfo_height()/32)
frame = Frame(root)
frame.bind("<KeyPress>", keyPress)
frame.bind("<KeyRelease>", keyRelease)
frame.pack()
frame.focus_set()
c = Canvas(root,width=root.winfo_width(),height=root.winfo_height(),bg='black')
s = []
i = 0
while i < int(root.winfo_height()):
    j = 0
    while j < int(root.winfo_width()):
        s.append(c.create_rectangle(j,i,j+resMultip,i+resMultip, fill='black'))
        c.pack()
        j+=resMultip
    i+=resMultip
while True:
    chip8.CPUCycle()
    if chip8.canvasReset == True:
        canvasClear(c)
        chip8.canvasReset = False
    time.sleep(speed)
    root.update()
#TO DO LIST:
#* SOUND IMPLEMENTATION
#* KEYBOARD SUPPORT
#* REPAIR SOME OPDECODERS
from ctypes import *
from tkinter import *
import random

def cykDwojeczka():
    print('You just pressed button')

class CPU:
    drawPicture: c_int
    memory: c_uint8 = [0]*0x1000
    regs: c_uint8 = [0]*0x10
    keypad: c_uint8 = [0]*0x10
    picture: c_uint8 = [0]*0x800
    soundTicker: c_uint8
    delayTicker: c_uint8

    opcode: c_uint16
    stack: c_uint16 = [0]*0x10
    stackPointer: c_uint16
    programCounter: c_uint16
    index: c_uint16
    isPressed: c_int
    height: c_short
    coordX: c_short
    coordY: c_short
    pixel: c_short
    font: c_uint8 = [ 0xF0, 0x90, 0x90, 0x90, 0xF0, 0x20, 0x60, 0x20, 0x20, 0x70, 0xF0, 0x10, 0xF0, 0x80, 0xF0, 0xF0, 0x10, 0xF0, 0x10, 0xF0, 0x90, 0x90, 0xF0, 0x10, 0x10, 0xF0, 0x80, 0xF0, 0x10, 0xF0, 0xF0, 0x80, 0xF0, 0x90, 0xF0, 0xF0, 0x10, 0x20, 0x40, 0x40, 0xF0, 0x90, 0xF0, 0x90, 0xF0, 0xF0, 0x90, 0xF0, 0x10, 0xF0, 0xF0, 0x90, 0xF0, 0x90, 0x90, 0xE0, 0x90, 0xE0, 0x90, 0xE0, 0xF0, 0x80, 0x80, 0x80, 0xF0, 0xE0, 0x90, 0x90, 0x90, 0xE0, 0xF0, 0x80, 0xF0, 0x80, 0xF0, 0xF0, 0x80, 0xF0, 0x80, 0x80]
    def __init__(self):
        print("Setting up things for you!")
        self.resetInternals()
        self.resetMemory()
        self.resetScreen()
        self.injectFont()
        self.programCounter = 0x200
        self.drawPicture = 0
        self.index = 0
        self.stackPointer = 0
        self.opcode = 0
        self.delayTicker = 0
        self.soundTicker = 10
        self.loadROM()
        print("Reading and executing ROM")
    def getDrawPicture(self):
        return self.drawPicture
    def memoryDump(self):
        print(self.memory)
    def loadROM(self):
        try:
            rom = open("Pong2.ch8", 'rb').read()
        except IOError:
            print('Rom not found.')
            exit()
        for index, val in enumerate(rom):
            self.memory[index + 512] = val
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
        if(self.opcode & 0xF000) == 0x0000:
            if(self.opcode & 0x000F) == 0x0000:
                self.resetScreen()
                self.drawPicture = 1
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x000E:
                self.stackPointer -= 1
                self.programCounter = self.stack[self.stackPointer]
                self.programCounter += 2
        elif(self.opcode & 0xF000) == 0x1000:
            self.programCounter = self.opcode & 0x0FFF
        elif(self.opcode & 0xF000) == 0x2000:
            self.stack[self.stackPointer] = self.programCounter
            self.stackPointer += 1
            self.programCounter = self.opcode & 0x0FFF
        elif(self.opcode & 0xF000) == 0x3000:
            if(self.regs[(self.opcode & 0x0F00) >> 8] == (self.opcode & 0x00FF)):
                self.programCounter += 4
            else:
                self.programCounter += 2
        elif(self.opcode & 0xF000) == 0x4000:
            if(self.regs[(self.opcode & 0x0F00) >> 8] != (self.opcode & 0x00FF)):
               self.programCounter += 4
            else:
                self.programCounter += 2
        elif(self.opcode & 0xF000) == 0x5000:
            if(self.regs[(self.opcode & 0x0F00) >> 8] == self.regs[(self.opcode & 0x00F0) >> 4]):
                self.programCounter += 4
            else:
                self.programCounter += 2
        elif(self.opcode & 0xF000) == 0x6000:
            self.regs[(self.opcode & 0x0F00)>>8] = self.opcode & 0x00FF
            self.programCounter += 2
        elif(self.opcode & 0xF000) == 0x7000:
            self.regs[(self.opcode & 0x0F00)>>8] += self.opcode & 0x00FF
            self.programCounter += 2
        elif(self.opcode & 0xF000) == 0x8000:
            if(self.opcode & 0x000F) == 0x0000:
                self.regs[(self.opcode & 0x0F00)>>8] = self.regs[(self.opcode & 0x00F0) >> 4]
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0001:
                self.regs[(self.opcode & 0x0F00) >> 8] |= self.regs[(self.opcode & 0x00F0) >> 4]
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0002:
                self.regs[(self.opcode & 0x0F00) >> 8] &= self.regs[(self.opcode & 0x00F0) >> 4]
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0003:
                self.regs[(self.opcode & 0x0F00) >> 8] ^= self.regs[(self.opcode & 0x00F0) >> 4]
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x0004:
                self.regs[(self.opcode & 0x0F00) >> 8] += self.regs[(self.opcode & 0x00F0) >> 4]
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
                self.programCounter += 2
            elif(self.opcode & 0x000F) == 0x000E:
                self.regs[0xF] = self.regs[(self.opcode & 0x0F00) >> 8] >> 7
                self.regs[(self.opcode & 0x0F00) >> 8] <<= 1
                self.programCounter += 2
        elif(self.opcode & 0xF000) == 0x9000:
            if self.regs[(self.opcode & 0x0F00) >> 8] != self.regs[(self.opcode & 0x00F0) >> 4]:
                self.programCounter += 4
            else:
                self.programCounter += 2
        elif(self.opcode & 0xF000) == 0xA000:
            self.index = self.opcode & 0x0FFF
            self.programCounter += 2
        elif(self.opcode & 0xF000) == 0xB000:
            self.programCounter = (self.opcode & 0x0FFF) + self.regs(0x0)
        elif(self.opcode & 0xF000) == 0xC000:
            self.regs[(self.opcode & 0x0F00) >> 8] = (random.randint(0,0xFF)+1) & (self.opcode & 0x00FF)
            self.programCounter += 2
        elif(self.opcode & 0xF000) == 0xD000:
            self.coordX = self.regs[(self.opcode & 0x0F00) >> 8]
            self.coordY = self.regs[(self.opcode & 0x00F0) >> 4]
            self.height = self.opcode & 0x000F
            self.regs[0xF] = 0
            for i in range (0, self.height):
                self.pixel = self.memory[self.index + i]
                for j in range (0, 8):
                    if (self.pixel & (0x80 >> j)) != 0:
                        if self.picture[self.coordX + j + ((self.coordY + i)*64)] == 1:
                            self.regs[0xF] = 1
                        self.picture[self.coordX + j + (self.coordY + i)*64] ^= 1
            self.drawPicture = 1
            self.programCounter += 2
        elif(self.opcode & 0xF000) == 0xE000:
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
        elif(self.opcode & 0xF000) == 0xF000:
            if(self.opcode & 0x00FF) == 0x0007:
                self.regs[(self.opcode & 0x0F00) >> 8] = self.delayTicker
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x000A:
                self.isPressed = 0
                for i in range (0, 16):
                    if self.keypad[i] != 0:
                        self.regs[(self.opcode & 0x0F00) >> 8] = i
                        self.isPressed = 1
                if self.isPressed == 0:
                    return
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0015:
                self.delayTicker = self.regs[(self.opcode & 0x0F00) >> 8]
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0018:
                self.soundTicker = self.regs[(self.opcode & 0x0F00) >> 8]
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x001E:
                if self.index + self.regs[(self.opcode & 0x0F00) >> 8] > 0xFFF:
                    self.regs[0xF] = 1
                else:
                    self.regs[0xF] = 0
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0029:
                self.index = self.regs[(self.opcode & 0x0F00) >> 8] * 0x5
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0033:
                self.memory[self.index] = int(self.regs[(self.opcode & 0x0F00) >> 8] / 0x64)
                self.memory[self.index + 1] = int((self.regs[(self.opcode & 0x0F00) >> 8] / 0xA) % 0xA)
                self.memory[self.index + 2] = int((self.regs[(self.opcode & 0x0F00) >> 8] / 0x64) % 0xA)
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0055:
                for i in range (0 , (self.opcode & 0x0F00) >> 8):
                    self.memory[self.index + i] = self.regs[i]
                self.index += ((self.opcode & 0x0F00) >> 8) + 1
                self.programCounter += 2
            elif(self.opcode & 0x00FF) == 0x0065:
                for i in range  (0 , (self.opcode & 0x0F00) >> 8):
                    self.regs[i] = self.memory[self.index + i]
                self.index += ((self.opcode & 0x0F00) >> 8) + 1
                self.programCounter += 2
        if self.delayTicker > 0:
                self.delayTicker -= 1
        if self.soundTicker > 0:
            if self.soundTicker == 1:
                print("BEEP")
            self.soundTicker -= 1

chip8 = CPU()
root = Tk()
root.geometry('640x320')
root.title('ChiPy8')
root.resizable(False,False)
root.update()
frame = Frame(root, width=100, height=100)
resMultip = int(root.winfo_height()/32)
c = Canvas(root,width=root.winfo_width(),height=root.winfo_height(),bg='black')
s = []
i = 0
while i < int(root.winfo_height()):
    j = 0
    while j < int(root.winfo_width()):
        s.append(c.create_rectangle(j,i,j+resMultip,i+resMultip, fill='white'))
        c.pack()
        j+=resMultip
    i+=resMultip
while True:
    frame.bind("<Key>",cykDwojeczka)
    frame.pack()
    #chip8.keypad[1] = 1 KEYBOARD LISTENING TEST
    chip8.CPUCycle()
    #print(chip8.programCounter,chip8.opcode)
#screen rendering POOR PERFORMANCE (SOFTWARE RENDERING)!!
    if chip8.drawPicture == 1:
        i = 0
        while i < 0x800:
            if chip8.picture[i] == 1:
                c.itemconfig(s[i],fill='white')
            else:
                c.itemconfig(s[i],fill='black')
            i+=1
        chip8.drawPicture = 0
#===================================
    root.update()

import pygame

from keyboard import Keyboard
from plugboard import Plugboard
from rotor import Rotor
from reflector import Reflector
from enigma import Enigma
from draw import draw

#set up pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("The Enigma")

#create fonts
BOLD = pygame.font.SysFont("FreeMono", 25, bold = True)
MONO = pygame.font.SysFont("FreeMono", 25, bold = True)

#global variables
width = 1600
height = 900
SCREEN = pygame.display.set_mode((width,height),True,32)
MARGINS = {"top" : 200, "bottom" : 100, "left" : 100, "right" : 100}
GAP = 100

##input and output variable
INPUT = ""
OUTPUT = ""
PATH = []

#*******order of rotors********
#Enigma Rotors and Reflectors creds -> Wikipedia    
I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
IV = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
V = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z")
A = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
C = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")

#Keyboard and Plugboard
KB = Keyboard()
PB = Plugboard(["AB", "CD", "EF"])

#Defining Enigma Machine
ENIGMA = Enigma(B,I,II,III,PB,KB)

#set the rings
ENIGMA.set_rings((1,1,1))

#set the message key
ENIGMA.set_key("CAT")

""""
#encipher MESSAGE
message = "TESTINGTESTINGTESTINGTESTING"
cipher_text = ""
for letter in message:
    cipher_text = cipher_text + ENIGMA.encipher(letter)
print(cipher_text)
"""

animating = True
while animating:

    #background screen
    SCREEN.fill("#333333")
    SCREEN.set_alpha(100)

    #text input
    text = BOLD.render(INPUT, True, "#80BDBD")
    text_box =  text.get_rect(center = (width/2,MARGINS["top"]/3))
    SCREEN.blit(text, text_box)

    #text output
    text = MONO.render(OUTPUT, True, "#B03151")
    text_box =  text.get_rect(center = (width/2,MARGINS["top"]/3+25))
    SCREEN.blit(text, text_box)

    #draw enigma machine
    draw(ENIGMA, PATH, SCREEN, width, height, MARGINS, GAP, BOLD)
    
    #update screen
    pygame.display.flip()

    #track user input
    hit = pygame.mixer.Sound("type.ogg")
    turn = pygame.mixer.Sound("gear.ogg")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            animating = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                turn.play()
                I.rotate()
            elif event.key == pygame.K_DOWN:
                turn.play()
                II.rotate()
            elif event.key == pygame.K_RIGHT:
                turn.play()
                III.rotate()
            elif event.key == pygame.K_SPACE:
                hit.play()
                INPUT = INPUT + " "
                OUTPUT = OUTPUT + " "
            else:
                hit.play()
                key = event.unicode;
                if key in "abcdefghijklmnopqrstuvwxyz":
                    letter = key.upper()
                    INPUT = INPUT + letter

                    PATH, cipher = ENIGMA.encipher(letter)
                    print(PATH)
                    OUTPUT = OUTPUT + cipher
                    #print(INPUT)
                elif key in "0123456789":
                    INPUT = INPUT + key
                    OUTPUT = OUTPUT + key


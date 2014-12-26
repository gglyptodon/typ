# -*- coding: utf-8 -*-

import pygame
import sys
import helpers
import random

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.font.init()
pygame.init()
FONT = pygame.font.Font("kochi-gothic-subst.ttf",20)
def main():

    pass


class Word():
    def __init__(self,x=random.randint(10,WIDTH-10),y=random.randint(20,HEIGHT-20),text="DUMMY",color=(0,250,120),painted=False):
        self.x = x
        self.y = y
        self.color = color
        self.painted = False
        self.score = 100
        self.text = text

class Main():
    def __init__(self, screen, name):
        self.screen = screen
        self.name = name
        pygame.display.set_caption(self.name)
        self.words = [Word(text=w) for w in self.read_txt()[0:40]] #["ab","nasld", "asldsld","bla","na;"]]
        self.painted = []
    def run(self):
        typed = ""
        time_passed = 0.0
        clk = pygame.time.Clock()
        self.reset_screen()
        while True:
            helpers.draw_permanent(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    typed = typed[:-1]
                    self.reset_screen()
                    helpers.set_string(self.screen, typed,FONT)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: #(event.key == pygame.K_SPACE or :
                    typed = ""
                    self.reset_screen()
                elif event.type == pygame.KEYDOWN and event.key : #<=127: #text entered
                    print(event.key)
                    if event.key < 128:
                        typed +=chr(event.key)
                        print("typed:", typed)
                        helpers.set_string(self.screen, typed,FONT)
                        if typed in [x.text for x in self.words if x.painted == True]:
                            print("woot")
                            self.words.remove([x for x in self.words if x.text == typed][0])
                            typed = ""
                            self.reset_screen()
                else:
                    pass

            helpers.draw_clock(self.screen,FONT,time_passed+clk.get_time(),time_passed )
            time_passed +=clk.get_time()
            clk.tick(100)
            pygame.display.flip()
    def reset_screen(self):
        self.screen.fill([0x00,0x00,0x00]) #dummy
        self.draw_words()

    def draw_words(self):
        for w in self.words:
                print(w.text)
                helpers.draw_words(self.screen,w.text,self.painted,FONT)
                w.painted = True

    def read_txt(self, txtfile = "res.txt"):
        with open(txtfile,'r') as infile:
            res = [r.strip() for r in infile.read().split(" ")]
        return res


if __name__ == '__main__':
    clk = pygame.time.Clock()
    main = Main(screen, 'typ')
    main.run()


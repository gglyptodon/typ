# -*- coding: utf-8 -*-

import pygame
import sys
import helpers
import random

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
pygame.init()
FONT = pygame.font.Font("kochi-gothic-subst.ttf",20)


def main():
    pass


class Word():
    def __init__(self, x=random.randint(10, WIDTH-10), y=random.randint(20,HEIGHT-20),text="DUMMY", text_alt = None, text_alt2 = None, color=(0,250,120),painted=False, score=None):
        self.x = x
        self.y = y
        self.color = color
        self.painted = False
        self.score = self.calc_score()
        self.text = text
        self.text_alt = text_alt #eg kana
        self.text_alt2 = text_alt2 #eg romaji

    def setRomajiAsAlt(self):
        print("setting romaji",self.text, Kana.toRomaji(self.text))
        self.text_alt = Kana.toRomaji(self.text)

    @staticmethod
    def calc_score():
        score = 100
        return score


class Kana():
    #table
    hiragana = list(u"あいうえおかきくけこさしすせそざじずぜぞ" \
           u"たちつてとだぢづでどなにぬねのはひふへほ" \
           u"ばびぶべぼぱぴぷぺぽ" \
           u"まみむめもやゆよらりるれろわゐゑをん")
           #todo gyagyugyo...

    katakana = list(u"アイウエオカキクケコサシスセソザジズセゾ" \
               u"タチツテトダヂヅデドナニヌネノハヒフヘホ" \
               u"バビブベボパピプペポ" \
               u"マミムメモヤユヨラリルレロワヰヱヲン")

    romaji = "a,i,u,e,o," \
             "ka,ki,ku,ke,ko," \
             "sa,shi,su,se,so," \
             "za,ji,zu,ze,zo," \
         "ta,chi,tsu,te,to," \
         "da,di,du,de,do," \
         "na,ni,nu,ne,no," \
         "ha,hi,fu,he,ho," \
         "ba,bi,bu,be,bo," \
         "pa,pi,pu,pe,po," \
         "ma,mi,mu,me,mo," \
         "ya,yu,yo," \
         "ra,ri,ru,re,ro," \
         "wa,wi,we,wo,n".split(",")

    hiragana2romaji = {}
    katakana2romaji = {}
    print(len(romaji),len(hiragana),len(katakana))

    for i, h in enumerate(hiragana):
        print(i, h, romaji[i])
        hiragana2romaji[h] = romaji[i]
    for i, k in enumerate(katakana):
        katakana2romaji[k] = romaji[i]

    @staticmethod
    def toRomaji(txt):
        res = ""
        for c in txt:
            #print(c, "C")
            #print(c in Kana.katakana2romaji, res)
            if c in Kana.katakana2romaji:
                res += Kana.katakana2romaji[c]
            elif c in Kana.hiragana2romaji:
                res += Kana.hiragana2romaji[c]
        return res



class Main():
    def __init__(self, screen, name):
        self.screen = screen
        self.name = name
        pygame.display.set_caption(self.name)
        self.words = [Word(text=w) for w in self.read_txt()[0:12]] #["ab","nasld", "asldsld","bla","na;"]]
        self.painted = []

    def get_key(self, event):
        if event.type == pygame.KEYDOWN:
            return (event.key, event.unicode)

    def run(self):
        typed = ""
        score = 0
        score_txt = ""
        time_passed = 0.0
        clk = pygame.time.Clock()
        self.reset_screen()
        for w in self.words:
            w.setRomajiAsAlt()
        while True:
            helpers.draw_permanent(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    typed = typed[:-1]
                    self.reset_screen()
                    helpers.set_string(self.screen, typed, FONT)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: #(event.key == pygame.K_SPACE or :
                    typed = ""
                    self.reset_screen()
                elif event.type == pygame.KEYDOWN and event.key : #<=127: #text entered
                    code, unicode = self.get_key(event)
                    if event.key:
                        typed += unicode
                        helpers.set_string(self.screen, typed, FONT)
                        if typed in [x.text for x in self.words if x.painted] or [x.text_alt for x in self.words if x.painted]:
                            torm = [x for x in self.words if x.text == typed or x.text_alt == typed]
                            if len(torm) > 0:
                                self.words.remove(torm[0])
                                typed = ""
                                self.reset_screen()
                                score+=torm[0].score
                                score_txt = str(score)
                                self.draw_score(score_txt)

                else:
                    pass

            helpers.draw_clock(self.screen,FONT,time_passed+clk.get_time(),time_passed )
            time_passed +=clk.get_time()
            clk.tick(100)
            pygame.display.flip()


    def reset_screen(self):
        self.screen.fill([0x00, 0x00, 0x00]) #dummy
        self.draw_words()
        #self.draw_score(score)

    def draw_score(self, score):
        print("draw score", score)
        textFieldPos = (screen.get_width()) - 120, (screen.get_height()-80)
        screen.blit(FONT.render(str(score), 1, (255,255,255)), textFieldPos)
        #pygame.display.flip()

    def draw_words(self):
        for w in self.words:
                print(w.text)
                helpers.draw_words(self.screen, w.text, self.painted, FONT)
                w.painted = True

    def read_txt(self, txtfile="res.txt"):
        with open(txtfile, 'r') as infile:
            res = [r.strip() for r in infile.read().split(" ")]
        return res


if __name__ == '__main__':
    clk = pygame.time.Clock()
    main = Main(screen, 'typ')
    main.run()


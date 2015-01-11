# -*- coding: utf-8 -*-

import pygame
import sys
import helpers
import random
from jphelpers import Kana, JapaneseText, JapaneseSentence, testJP, KanjiVocab, KanjiImporter


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
pygame.init()
FONT = pygame.font.Font("kochi-gothic-subst.ttf", 20)
INFILE = "renshuu_export2.txt"


def main():
    pass


class JapaneseWord():
    def __init__(self, x=random.randint(10, WIDTH-10),
                 y=random.randint(20, HEIGHT-20),
                 kanji="漢字", kana=None,
                 romaji=None, color=(0, 250, 120),
                 painted=False, score=None):

        self.x = x
        self.y = y
        self.color = color
        self.painted = False
        self.score = self.calc_score()
        self.kanji = kanji
        self.kana = kana
        self.romaji = romaji

    @staticmethod
    def calc_score():
        score = 100
        return score


class Main():
    def __init__(self, screen, name):
        self.screen = screen
        self.name = name
        pygame.display.set_caption(self.name)

        kanjilist = []
        for kanji in KanjiImporter.parseInfile(INFILE):
            kanjilist.append(KanjiVocab(kanji[0], kanji[1], kanji[2]))

        self.words = [JapaneseWord(kanji=k.kanji, kana=k.kana, romaji=k.romaji) for k in kanjilist[0:20]]
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
        while True:
            self.checkGameOver()
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
                        if typed in [x.romaji for x in self.words if x.painted] or [x.kana for x in self.words if x.painted]:
                            torm = [x for x in self.words if x.romaji == typed or x.kana == typed]
                            if len(torm) > 0:
                                self.words.remove(torm[0])
                                typed = ""
                                self.reset_screen()
                                score += torm[0].score
                                score_txt = str(score)
                                self.draw_score(score_txt)

                else:
                    pass

            helpers.draw_clock(self.screen, FONT, time_passed+clk.get_time(), time_passed )
            time_passed += clk.get_time()
            clk.tick(100)
            pygame.display.flip()

    def checkGameOver(self):
        pass

    def reset_screen(self):
        self.screen.fill([0x00, 0x00, 0x00]) #dummy
        self.draw_words()

    def draw_score(self, score):
        print("draw score", score)
        textFieldPos = (screen.get_width()) - 120, (screen.get_height()-80)
        screen.blit(FONT.render(str(score), 1, (255, 255, 255)), textFieldPos)

    def draw_words(self):
        for w in self.words:
                print(w.romaji)
                helpers.draw_words(self.screen, w.kanji, self.painted, FONT)
                #helpers.draw_words(self.screen, w.kana, self.painted, FONT)
                w.painted = True

    def read_txt(self, txtfile="res.txt"):
        with open(txtfile, 'r') as infile:
            res = [r.strip() for r in infile.read().split(" ")]
        return res


if __name__ == '__main__':
    clk = pygame.time.Clock()
    main = Main(screen, 'typ')
    main.run()

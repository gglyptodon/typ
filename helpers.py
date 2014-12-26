# -*- coding: utf-8 -*-
import pygame, pygame.font, pygame.event, pygame.draw, string
import random

def set_string(screen, str, font):
    textFieldPos = (screen.get_width() / 2) - 100, (screen.get_height()-80)
    if len(str) != 0:
        screen.blit(font.render(str, 1, (255,255,255)),
                    textFieldPos)
    pygame.display.flip()



def draw_words(screen,word,painted, font):
    if not word in painted:
        screen.blit(font.render(word, 1, (255,0,100)), (random.randint(30,screen.get_width()-20), random.randint(20,screen.get_height()-100)) )

def rm_words(screen,word,painted, font):
    if not word in painted:
        screen.blit(font.render(word, 1, (0,0,0)), (random.randint(300,screen.get_width()-200), random.randint(200,screen.get_height()-290)) )

def draw_permanent(screen):
    textFieldPos = (screen.get_width() / 2) - 100, (screen.get_height()-80)
    pygame.draw.lines(screen, (244,244,244), False, [textFieldPos, (textFieldPos[0]+200, textFieldPos[1])], 1)

def draw_clock(screen, font, time_in_mill, old_time):
    time_to_show = str(time_in_mill/1000)
    old_time = str(old_time/1000)
    screen.blit(font.render(old_time, 1, (0,0,0)), (screen.get_width() -200, screen.get_height()-80) )
    screen.blit(font.render(time_to_show, 1, (100,0,255)), (screen.get_width() -200, screen.get_height()-80) )



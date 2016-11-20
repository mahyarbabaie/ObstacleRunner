#!/usr/bin/python

import random
import os
import json
import pygame
from MainMenu import *
from Player import *
from Platform import *
from Settings import *
from HighScores import *



class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(title)
        pygame.font.init()
        self.font = pygame.font.Font(FONTNAME, 20)
        self.fileName = "HighScore.json"
        # if there is no file then make one
        if not os.path.isfile(self.fileName):
            empty_score_file = open(self.fileName, "w")
            empty_score_file.write("[]")
            empty_score_file.close()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        from Player import Player
        self.player = Player(self)
        self.running = True
        self.playerDead = False
        self.highscore = HighScores()

    def new(self):
        # start a new game, reset everything
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        from Player import Player
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.highscore.score = 0
        self.highscore = HighScores()
        self.playerDead = False
        # creates a platform
        for platform in PLATFORM_LIST:
            plat = Platform(*platform)
            self.all_sprites.add(plat)
            self.platforms.add(plat)

        self.gameLoop()

    def gameLoop(self):
        self.running = True
        while self.running:
            clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            pygame.display.update()
        pygame.quit()

    def update(self):
        self.all_sprites.update()
        if self.player.velocity.y > 0:
            player_collision = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if player_collision:
                # if the player comes in contact with platform, put him at the top of the platform hitbox
                self.player.position.y = player_collision[0].rect.top
                self.player.velocity.y = 0
        # if player reaches top of the screen move the camera
        if self.player.rect.top <= display_height / 4:
            self.player.position.y += abs(self.player.velocity.y)
            # move platforms down based on player speed
            for plat in self.platforms:
                plat.rect.y += abs(self.player.velocity.y)
                if plat.rect.top >= display_height:
                    plat.kill()
                    self.highscore.score += 10
        # player death
        if self.player.rect.bottom > display_height:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.velocity.y, 7)
                if sprite.rect.bottom < 0:
                    sprite.kill()
                    self.playerDead = True


        # spawn new platforms
        while len(self.platforms) < 10:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, display_width - width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def draw(self):
        screen.fill(teal)
        self.all_sprites.draw(screen)
        screen.blit(self.font.render("Score: {}".format(self.highscore.score), -1, white), (500, 10))
        if self.playerDead:
            highscore = 1
            screen.blit(pygame.font.Font(FONTNAME, 100).render("Game Over", -1, red), (100, 70))
            if highscore == 1:
                screen.blit(
                    pygame.font.Font(FONTNAME, 30).render("Enter your name for the HighScore List", -1,
                                                          white), (10, 450))
                self.highscore.getUserName(self.highscore.score)
                self.highscore.addHighScores()
                highscore = 0
            if highscore == 0:
                MainMenu().game_intro()
        pygame.display.flip()


if __name__ == "__main__":
    Game()
    MainMenu().game_intro()
    quit()




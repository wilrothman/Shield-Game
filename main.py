"""
    "Shield" by Wil Rothman
    1/17/17 - 1/23/17
"""

import pygame
import random


class App:
    def __init__(self):
        global display, width, height, maxSpeed

        pygame.init()

        width = 675
        height = 675

        display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Shield")

        self.clock = pygame.time.Clock()
        self.watch = 0
        self.printer = 0

        self.form = 'default'
        self.keys_down = 0

        maxSpeed = 200
        self.speed = 5

        self.classes()

        self.loop()

    def classes(self):
        global player, bullet

        player = Player()
        bullet = Bullet()

    def loop(self):
        global maxSpeed

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.keys_down += 1

                        print("top")
                        self.form = 'top'

                    if event.key == pygame.K_d:
                        self.keys_down += 1

                        print("right")
                        self.form = 'right'

                    if event.key == pygame.K_s:
                        self.keys_down += 1

                        print("bottom")
                        self.form = 'bottom'

                    if event.key == pygame.K_a:
                        self.keys_down += 1

                        print("left")
                        self.form = 'left'

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_d or event.key == pygame.K_s or event.key == pygame.K_a:
                        print("refrain")
                        self.keys_down -= 1

                    if self.keys_down == 0:
                        self.form = 'default'

            display.fill((255, 255, 255))
            display.blit(player.spr[self.form], (height/2 - 115/2, width/2 - 115/2))

            self.watch = bullet.check(self.watch)
            bullet.movBullets(self.speed, self.form, self.clock)

            self.watch += 1
            pygame.display.update()
            self.clock.tick(60)


class Player:
    def __init__(self):
        self.spr = {
            'default': pygame.image.load("/Users/Wil/PycharmProjects/MyGames/Imgs/Shield/Player.gif"),
            'top': pygame.image.load("/Users/Wil/PycharmProjects/MyGames/Imgs/Shield/Top.gif"),
            'right': pygame.image.load("/Users/Wil/PycharmProjects/MyGames/Imgs/Shield/Right.gif"),
            'bottom': pygame.image.load("/Users/Wil/PycharmProjects/MyGames/Imgs/Shield/Bottom.gif"),
            'left': pygame.image.load("/Users/Wil/PycharmProjects/MyGames/Imgs/Shield/Left.gif")
        }

        for i in self.spr.keys():
            self.spr[i] = pygame.transform.scale(self.spr[i], (115, 115))


class Bullet:
    def __init__(self):
        global bullets

        self.bullets = []
        self.directions = []
        self.chords = []
        self.activation = []

        self.spr = pygame.image.load("/Users/Wil/PycharmProjects/MyGames/Imgs/Shield/Bullet.gif")
        self.spr = pygame.transform.scale(self.spr, (20, 20))

        self.nothing = pygame.image.load("/Users/Wil/PycharmProjects/MyGames/Imgs/Solid Colors/Nothingness.gif")

    def new(self):
        self.bullets.append(self.spr)
        self.activation.append(True)

        """
            Up: 0
            Right: 1
            Down: 2
            Left: 3
        """
        self.direc = random.randrange(4)

        print("direc:", self.direc)

        self.directions.append(self.direc)

        if self.direc == 0:
            display.blit(self.bullets[-1], [675/2, 0])
            self.chords.append([675/2, 0])

        elif self.direc == 1:
            display.blit(self.bullets[-1], [675 - 20, 675/2])
            self.chords.append([675 - 20, 675/2])

        elif self.direc == 2:
            display.blit(self.bullets[-1], [675/2, 675 - 20])
            self.chords.append([675/2, 675 - 20])

        elif self.direc == 3:
            display.blit(self.bullets[-1], [0, 675/2])
            self.chords.append([0, 675/2])

        else:
            print("\n\nRANDOM LASER ERROR\n\n")

    def check(self, watch) -> int:
        global maxSpeed

        if watch >= maxSpeed:
            self.new()

            print("Max Speed:", maxSpeed)

            if maxSpeed > 25:
                maxSpeed *= 0.9

            else:
                maxSpeed *= 0.99
                print("speed increase: 99%")

            return 0

        return watch

    def movBullets(self, speed, form, clock):
        for i in range(len(self.bullets)):
            if self.directions[i] == 0:
                self.chords[i][1] = self.chords[i][1] + speed

                if self.chords[i][1] >= 675/2 - 115/2 and not form == 'top' and self.activation[i]:
                    self.death(clock)

                elif self.chords[i][1] >= 675/2 - 115/2 and form == 'top' and self.activation[i]:
                    self.bullets[i] = self.nothing
                    self.activation[i] = False

            elif self.directions[i] == 1:
                self.chords[i][0] = self.chords[i][0] - speed

                if self.chords[i][0] <= 675/2 + 115/2 - 20 and not form == 'right' and self.activation[i]:
                    self.death(clock)

                elif self.chords[i][0] <= 675/2 + 115/2 - 20 and form == 'right' and self.activation[i]:
                    self.bullets[i] = self.nothing
                    self.activation[i] = False

            elif self.directions[i] == 2:
                self.chords[i][1] = self.chords[i][1] - speed

                if self.chords[i][1] <= 675 / 2 + 115 / 2 - 20and not form == 'bottom' and self.activation[i]:
                    self.death(clock)

                elif self.chords[i][1] <= 675 / 2 + 115 / 2 - 20 and form == 'bottom' and self.activation[i]:
                    self.bullets[i] = self.nothing
                    self.activation[i] = False

            elif self.directions[i] == 3:
                self.chords[i][0] = self.chords[i][0] + speed

                if self.chords[i][0] >= 675/2 - 115/2 and not form == 'left' and self.activation[i]:
                    self.death(clock)

                elif self.chords[i][0] >= 675/2 - 115/2 and form == 'left' and self.activation[i]:
                    self.bullets[i] = self.nothing
                    self.activation[i] = False

            display.blit(self.bullets[i], self.chords[i])

        speed += 1

    def death(self, clock):
        gameOver = pygame.image.load("/Users/Wil/PycharmProjects/MyGames/Imgs/Shield/Game Over.gif")
        gameOver = pygame.transform.scale(gameOver, (675, 675))

        waitingTime = 0

        while True:
            print("DEATH")
            display.fill((0, 0, 0))
            display.blit(gameOver, (20, 50))

            waitingTime += 1

            if waitingTime >= 100:
                pygame.quit()
                quit()
                exit()

            pygame.display.update()
            clock.tick(60)


# Main Function:
def main():
    app = App()


main()

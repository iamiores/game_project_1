import sys
import pygame
pygame.init()

'''SETTINGS'''
W, H = 700, 500

window = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

pygame.display.set_caption('Get Donut!')
icon = pygame.image.load('images/donut.png')
pygame.display.set_icon(icon)

bg = pygame.image.load('images/bgg1.jpg')
bg1 = pygame.transform.scale(bg, (800, 500))

#LISTS
walk_left = [
    pygame.image.load('images/walk left/walk_left1.png'),
    pygame.image.load('images/walk left/walk_left2.png'),
    pygame.image.load('images/walk left/walk_left3.png')
]
walk_right = [
    pygame.image.load('images/walk right/walk_right2.png'),
    pygame.image.load('images/walk right/walk_right1.png'),
    pygame.image.load('images/walk right/walk_right3.png')
]

run_left = [
    pygame.image.load('images/walk left/run_left1.png'),
    pygame.image.load('images/walk left/run_left2.png')
]
run_right = [
    pygame.image.load('images/walk right/run_right1.png'),
    pygame.image.load('images/walk right/run_right2.png')
]

'''CLASSES'''


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inact = (255, 255, 255)
        self.act = (206, 232, 255)

    def draw(self, x, y, text, action=None, fsize=35):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(window, self.inact, (x, y, self.width, self.height))

            if click[0]:
                if action is not None:
                    button.play()
                    action()
        else:
            pygame.draw.rect(window, self.act, (x, y, self.width, self.height))

        set_text(text, x=x+10, y=y+10, fsize=fsize)

    def reset(self, x, y, text, fsize=35):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(window, self.inact, (x, y, self.width, self.height))
            if click[0]:
                button.play()
                return True
        else:
            pygame.draw.rect(window, self.act, (x, y, self.width, self.height))
        set_text(text, x=x + 10, y=y + 10, fsize=fsize)


class Sprite:
    def __init__(self, file, x, y, width, height):
        self.image = pygame.image.load(file)
        self.rect = pygame.Rect(x, y, width, height)
        self.dx = 3

    def reset(self):
        window.blit(self.image, self.rect)

    def movement(self, a1, a2):
        self.reset()
        if self.rect.x >= a1 or self.rect.x <= a2:
            self.dx *= -1
        self.rect.x += self.dx


'''GAME CYCLES'''


def menu():
    finished = False
    menu_back = pygame.image.load('images/bgg1.jpg')
    menu_back2 = pygame.transform.scale(menu_back, (800,500))
    show = True
    play = Button(220, 40)
    settings = Button(220, 40)
    state = 'menu'

    level1 = Button(220, 40)
    level2 = Button(220, 40)
    level3 = Button(220, 40)
    level4 = Button(220, 40)

    volume = Button(220, 40)
    volume_plus = Button(50, 50)
    volume_minus = Button(50, 50)
    back = Button(220, 40)
    sound_volume = 1

    keys = pygame.key.get_pressed()
    while show:
        if not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    show = False
                    exit()
                elif keys[pygame.K_ESCAPE]:
                    show = False
            window.blit(menu_back2, (0, 0))
            if state == 'menu':
                if play.reset(280, 200, 'PLAY', 30):
                    state = 'decide'
                elif settings.reset(280, 270, 'SETTINGS', 30):
                    state = 'settings'
            if state == 'decide':
                level1.draw(100, 200, 'LEVEL 1', game_level1, 30)
                level2.draw(100, 270, 'LEVEL 2', game_level2, 30)
                level3.draw(400, 200, 'LEVEL 3', game_level3, 30)
                level4.draw(400, 270, 'LEVEL 4', game_level4, 30)
                if back.reset(270, 350, 'BACK', 30):
                    state = 'menu'
            if state == 'settings':
                bg_sound.set_volume(sound_volume)
                volume.draw(270, 100, 'VOLUME', None, 30)
                if volume_minus.reset(250, 170, '-', 30):
                    sound_volume -= 0.1
                elif volume_plus.reset(450, 170, '+', 30):
                    sound_volume += 0.1
                if back.reset(270, 350, 'BACK', 30):
                    state = 'menu'

            pygame.display.update()
            clock.tick(60)


#LEVELS

def game_level1():
    walk_anim = 0
    walk_speed = 8
    run_anim = 0

    player_x = -200
    player_y = 220

    is_jump = False
    jump = 9

    gravity = 20

    sum = 0

    state = 'game'
    game = True
    finished = False
    coins = create_coin(160, 15, 580, 215, 200, 125)
    while game:
        if not finished:
            window.blit(bg1, (0, 0))
            for heart in hearts:
                heart.reset()
            platform1.reset()
            platform2.reset()
            platform3.reset()
            platform4.movement(200, 0)
            player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))
            player_rect = player_rect.inflate(-430, -430)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                window.blit(walk_left[walk_anim], (player_x, player_y))
                player_x -= walk_speed
                if keys[pygame.K_w]:
                    walk_speed = 16
                    window.blit(bg1, (0, 0))
                    window.blit(run_left[run_anim], (player_x, player_y))
                else:
                    walk_speed = 8

                if run_anim == 1:
                    run_anim = 0
                else:
                    run_anim += 1

            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                window.blit(walk_right[walk_anim], (player_x, player_y))
                player_x += walk_speed
                if keys[pygame.K_w]:
                    walk_speed = 16
                    window.blit(bg1, (0, 0))
                    window.blit(run_right[run_anim], (player_x, player_y))
                else:
                    walk_speed = 8

                if run_anim == 1:
                    run_anim = 0
                else:
                    run_anim += 1

            else:
                window.blit(walk_right[1], (player_x, player_y))

            if walk_anim == 2:
                walk_anim = 0
            else:
                walk_anim += 1

            if not is_jump:
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    gravity = 0
            else:
                if jump >= -9:
                    if jump > 0:
                        player_y -= (jump **2) / 2
                    else:
                        player_y += (jump ** 2) / 2
                    jump -= 1
                else:
                    is_jump = False
                    jump = 9
                    gravity = 8
            player_y += gravity

            if player_y >= 220:
                player_y -= gravity

            if player_rect.colliderect(platform2.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform2.rect.x, platform2.rect.y, platform2.rect.width, platform2.rect.height):
                    jump = -9
                    player_y = 10
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform4.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform4.rect.x, platform4.rect.y, platform4.rect.width, platform4.rect.height):
                    jump = -9
                    player_y = 90
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform1.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform1.rect.x, platform1.rect.y, platform1.rect.width, platform1.rect.height):
                    jump = -9
                    player_y = -190
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform3.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform3.rect.x, platform3.rect.y, platform3.rect.width, platform3.rect.height):
                    jump = -9
                    player_y = -80
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            for coin in coins:
                coin.reset()
                if player_rect.colliderect(coin.rect):
                    collect_coin.play()
                    coins.remove(coin)
                    sum += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

            if sum == 3:
                next_button = Button(200, 40)
                retry_button = Button(200, 40)
                menu_button = Button(200, 40)
                window.blit(black_screen, (0,0))
                main_coin.reset()
                set_text(':' + str(sum), 370, 110, (255, 255, 255), 50)

                next_button.draw(170, 200, 'NEXT', game_level2, 35)
                menu_button.draw(270, 270, 'MENU', menu, 35)

                if retry_button.draw(400, 200, 'RETRY', game_level1, 35):
                    sum = 0

                    player_x = -200
                    player_y = 220
                    if sum == 0:
                        for coin in coins:
                            coin.reset()
                            coins.append(coin)
                            if player_rect.colliderect(coin.rect):
                                collect_coin.play()
                                coins.remove(coin)
                                sum += 1

            pygame.display.update()
            clock.tick(15)

def game_level2():

    walk_anim = 0
    walk_speed = 8
    run_anim = 0

    player_x = -200
    player_y = 220

    is_jump = False
    jump = 9

    gravity = 20

    sum_coin = 0
    sum_donut = 0
    wounds = 0

    state = 'lobby'
    game = True
    finished = False
    coins = create_coin(80, 15, 620, 230, 30, 295)
    donuts = create_donuts(610, -15)
    poops = create_poops(2, 560, 15, 270, 445)
    hearts = create_hearts()
    while game:
        if not finished:
            window.blit(bg1, (0, 0))
            platform5.reset()
            platform6.movement(420, 250)
            platform7.reset()
            platform8.reset()

            player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))
            player_rect = player_rect.inflate(-430, -430)
            for heart in hearts:
                heart.reset()
                for poop in poops:
                    poop.reset()
                    if player_rect.colliderect(poop.rect):
                        hearts.remove(heart)
                        poops.remove(poop)
                        wounds += 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                window.blit(walk_left[walk_anim], (player_x, player_y))
                player_x -= walk_speed
                if keys[pygame.K_w]:
                    walk_speed = 16
                    window.blit(run_left[run_anim], (player_x, player_y))
                else:
                    walk_speed = 8

                if run_anim == 1:
                    run_anim = 0
                else:
                    run_anim += 1

            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                window.blit(walk_right[walk_anim], (player_x, player_y))
                player_x += walk_speed
                if keys[pygame.K_w]:
                    walk_speed = 16
                    window.blit(run_right[run_anim], (player_x, player_y))
                else:
                    walk_speed = 8

                if run_anim == 1:
                    run_anim = 0
                else:
                    run_anim += 1

            else:
                window.blit(walk_right[1], (player_x, player_y))

            if walk_anim == 2:
                walk_anim = 0
            else:
                walk_anim += 1

            if not is_jump:
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    gravity = 0
            else:
                if jump >= -9:
                    if jump > 0:
                        player_y -= (jump ** 2) / 2
                    else:
                        player_y += (jump ** 2) / 2
                    jump -= 1
                else:
                    is_jump = False
                    jump = 9
                    gravity = 8
            player_y += gravity

            if player_y >= 220:
                player_y -= gravity

            if player_rect.colliderect(platform5.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform5.rect.x, platform5.rect.y, platform5.rect.width, platform5.rect.height):
                    jump = -9
                    player_y = -190
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform7.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform7.rect.x, platform7.rect.y, platform7.rect.width, platform7.rect.height):
                    jump = -9
                    player_y = -210
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform8.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform8.rect.x, platform8.rect.y, platform8.rect.width, platform8.rect.height):
                    jump = -9
                    player_y = 90
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform6.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform6.rect.x, platform6.rect.y, platform6.rect.width, platform6.rect.height):
                    jump = -9
                    player_y = -70
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

            for coin in coins:
                coin.reset()
                if player_rect.colliderect(coin.rect):
                    collect_coin.play()
                    coins.remove(coin)
                    sum_coin += 1
            for donut in donuts:
                donut.reset()
                if player_rect.colliderect(donut.rect):
                    collect_coin.play()
                    donuts.remove(donut)
                    sum_donut += 1

            if sum_coin >= 3 and sum_donut >= 1:
                next_button = Button(200, 40)
                retry_button = Button(200, 40)
                menu_button = Button(200, 40)
                window.blit(black_screen, (0,0))
                main_coin.reset()
                set_text(':' + str(sum_coin), 370, 110, (255, 255, 255), 50)

                main_donut.reset()
                set_text(':' + str(sum_donut), 370, 40, (255, 255, 255), 50)

                next_button.draw(170, 200, 'NEXT', game_level3, 35)
                menu_button.draw(270, 270, 'MENU', menu, 35)

                if state == 'lobby':
                    if retry_button.draw(400, 200, 'RETRY', game_level2, 35):
                        state = 'game1'
                        sum_coin = 0
                        sum_donut = 0

                        player_x = -200
                        player_y = 220
                        if sum_coin == 0 and sum_donut == 0:
                            for coin in coins:
                                coin.reset()
                                coins.append(coin)
                                if player_rect.colliderect(coin.rect):
                                    collect_coin.play()
                                    coins.remove(coin)
                                    sum_coin += 1
                            for donut in donuts:
                                donut.reset()
                                if player_rect.colliderect(donut.rect):
                                    collect_coin.play()
                                    donuts.remove(donut)
                                    sum_donut += 1


            pygame.display.update()
            clock.tick(15)

def game_level3():
    walk_anim = 0
    walk_speed = 8
    run_anim = 0

    player_x = -200
    player_y = 220

    is_jump = False
    jump = 9

    gravity = 20

    sum_coin = 0
    sum_donut = 0
    wounds = 0
    state = 'game'

    game = True
    finished = False
    coins = create_coin(350, 420, 620, 155, 610, 5)
    donuts = create_donuts(0, 140)
    poops = create_poops(3, 480, 25, 670, 175, 350, 325)
    hearts = create_hearts()
    while game:
        if not finished:
            window.blit(bg1, (0, 0))
            platform9.reset()
            platform10.reset()
            platform11.reset()
            platform12.reset()
            platform13.movement(200, -10)
            player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))
            player_rect = player_rect.inflate(-430, -430)
            keys = pygame.key.get_pressed()
            for heart in hearts:
                heart.reset()
                for poop in poops:
                    poop.reset()
                    if player_rect.colliderect(poop.rect):
                        hearts.remove(heart)
                        poops.remove(poop)
                        wounds += 1

            # if wounds != 3: # or sum_coin != 3 and sum_donut != 1
            if state == 'game':
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    window.blit(walk_left[walk_anim], (player_x, player_y))
                    player_x -= walk_speed
                    if keys[pygame.K_w]:
                        walk_speed = 16
                        window.blit(run_left[run_anim], (player_x, player_y))
                    else:
                        walk_speed = 8

                    if run_anim == 1:
                        run_anim = 0
                    else:
                        run_anim += 1

                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    window.blit(walk_right[walk_anim], (player_x, player_y))
                    player_x += walk_speed
                    if keys[pygame.K_w]:
                        walk_speed = 16
                        window.blit(run_right[run_anim], (player_x, player_y))
                    else:
                        walk_speed = 8

                    if run_anim == 1:
                        run_anim = 0
                    else:
                        run_anim += 1

                else:
                    window.blit(walk_right[1], (player_x, player_y))

                if walk_anim == 2:
                    walk_anim = 0
                else:
                    walk_anim += 1

                if not is_jump:
                    if keys[pygame.K_SPACE]:
                        is_jump = True
                        gravity = 0
                else:
                    if jump >= -9:
                        if jump > 0:
                            player_y -= (jump ** 2) / 2
                        else:
                            player_y += (jump ** 2) / 2
                        jump -= 1
                    else:
                        is_jump = False
                        jump = 9
                        gravity = 8
                player_y += gravity
                if wounds == 3:
                    state = 'gameover'
                if sum_coin == 3 and sum_donut == 1:
                    state = 'finish'

            if player_y >= 220:
                player_y -= gravity

            if player_rect.colliderect(platform9.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform9.rect.x, platform9.rect.y, platform9.rect.width, platform9.rect.height):
                    jump = -9
                    player_y = -50
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform11.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform11.rect.x, platform11.rect.y, platform11.rect.width, platform11.rect.height):
                    jump = -9
                    player_y = -200
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform12.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform12.rect.x, platform12.rect.y, platform12.rect.width, platform12.rect.height):
                    jump = -9
                    player_y = 100
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform13.rect):
                player_y -= gravity
                jump = -9

            if player_rect.colliderect(platform10.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform10.rect.x, platform10.rect.y, platform10.rect.width, platform10.rect.height):
                    jump = -9
                    player_y = -50
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

            for coin in coins:
                coin.reset()
                if player_rect.colliderect(coin.rect):
                    collect_coin.play()
                    coins.remove(coin)
                    sum_coin += 1
            for donut in donuts:
                donut.reset()
                if player_rect.colliderect(donut.rect):
                    collect_coin.play()
                    donuts.remove(donut)
                    sum_donut += 1

            if state == 'finish':
            # if sum_coin >= 3 and sum_donut >= 1:
                next_button = Button(200, 40)
                retry_button = Button(200, 40)
                menu_button = Button(200, 40)
                window.blit(black_screen, (0,0))

                main_coin.reset()
                set_text(':' + str(sum_coin), 370, 110, (255, 255, 255), 50)

                main_donut.reset()
                set_text(':' + str(sum_donut), 370, 40, (255, 255, 255), 50)

                next_button.draw(170, 200, 'NEXT', game_level4, 35)
                menu_button.draw(270, 270, 'MENU', menu, 35)

                if retry_button.draw(400, 200, 'RETRY', game_level3, 35):
                    sum_coin = 0
                    sum_donut = 0

                    player_x = -200
                    player_y = 220
                    if sum_coin == 0 and sum_donut == 0:
                        for coin in coins:
                            coin.reset()
                            coins.append(coin)
                            if player_rect.colliderect(coin.rect):
                                collect_coin.play()
                                coins.remove(coin)
                                sum_coin += 1
                        for donut in donuts:
                            donut.reset()
                            if player_rect.colliderect(donut.rect):
                                collect_coin.play()
                                donuts.remove(donut)
                                sum_donut += 1
            if state == 'gameover':
            # if wounds >= 3:
                retry_button = Button(200, 40)
                menu_button = Button(200, 40)
                window.blit(black_screen, (0, 0))
                main_coin.reset()
                set_text(':' + str(sum_coin), 370, 110, (255, 255, 255), 50)

                main_donut.reset()
                set_text(':' + str(sum_donut), 370, 40, (255, 255, 255), 50)

                menu_button.draw(270, 270, 'MENU', menu, 35)

                if retry_button.draw(270, 200, 'RETRY', game_level3, 35):
                    sum_coin = 0
                    sum_donut = 0

                    player_x = -200
                    player_y = 220
                    if sum_coin == 0 and sum_donut == 0:
                        for coin in coins:
                            coin.reset()
                            coins.append(coin)
                            if player_rect.colliderect(coin.rect):
                                collect_coin.play()
                                coins.remove(coin)
                                sum_coin += 1
                        for donut in donuts:
                            donut.reset()
                            if player_rect.colliderect(donut.rect):
                                collect_coin.play()
                                donuts.remove(donut)
                                sum_donut += 1

            pygame.display.update()
            clock.tick(15)
def game_level4():

    walk_anim = 0
    walk_speed = 8
    run_anim = 0

    player_x = -200
    player_y = 220

    is_jump = False
    jump = 9

    gravity = 20

    sum_coin = 0
    sum_donut = 0
    wounds = 0
    state = 'game'

    game = True
    finished = False
    coins = create_coin(580, 380, 40, 290, 380, 100)
    donuts = create_donuts(600, -10)
    poops = create_poops(3, 540, 25, 630, 275, 500, 445)
    hearts = create_hearts()
    while game:
        if not finished:
            window.blit(bg1, (0, 0))
            platform14.reset()
            platform15.reset()
            platform16.reset()
            platform17.movement(270, 50)
            trampoline.reset()
            player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))
            player_rect = player_rect.inflate(-430, -430)
            keys = pygame.key.get_pressed()
            for heart in hearts:
                heart.reset()
                for poop in poops:
                    poop.reset()
                    if player_rect.colliderect(poop.rect):
                        hearts.remove(heart)
                        poops.remove(poop)
                        wounds += 1

            if state == 'game':
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    window.blit(walk_left[walk_anim], (player_x, player_y))
                    player_x -= walk_speed
                    if keys[pygame.K_w]:
                        walk_speed = 16
                        window.blit(run_left[run_anim], (player_x, player_y))
                    else:
                        walk_speed = 8

                    if run_anim == 1:
                        run_anim = 0
                    else:
                        run_anim += 1

                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    window.blit(walk_right[walk_anim], (player_x, player_y))
                    player_x += walk_speed
                    if keys[pygame.K_w]:
                        walk_speed = 16
                        window.blit(run_right[run_anim], (player_x, player_y))
                    else:
                        walk_speed = 8

                    if run_anim == 1:
                        run_anim = 0
                    else:
                        run_anim += 1

                else:
                    window.blit(walk_right[1], (player_x, player_y))

                if walk_anim == 2:
                    walk_anim = 0
                else:
                    walk_anim += 1

                if not is_jump:
                    if player_rect.colliderect(trampoline.rect):
                        is_jump = True
                        gravity = 0
                        jump = 14
                    if keys[pygame.K_SPACE]:
                        is_jump = True
                        gravity = 0
                else:
                    if jump >= -9:
                        if jump > 0:
                            player_y -= (jump ** 2) / 2
                        else:
                            player_y += (jump ** 2) / 2
                        jump -= 1
                    else:
                        is_jump = False
                        jump = 9
                        gravity = 8
                player_y += gravity

                if wounds == 3:
                    state = 'gameover'
                if sum_coin == 3 and sum_donut == 1:
                    state = 'finish'

            if player_y >= 220:
                player_y -= gravity

            if player_rect.colliderect(platform14.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform14.rect.x, platform14.rect.y, platform14.rect.width, platform14.rect.height):
                    jump = -9
                    player_y = -20
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform15.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform15.rect.x, platform15.rect.y, platform15.rect.width, platform15.rect.height):
                    jump = -9
                    player_y = -200
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform17.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform17.rect.x, platform17.rect.y, platform17.rect.width, platform17.rect.height):
                    jump = -9
                    player_y = 90
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            if player_rect.colliderect(platform16.rect):
                player_y -= gravity
                jump = 9
                if player_rect.colliderect(platform16.rect.x, platform16.rect.y, platform16.rect.width, platform16.rect.height):
                    jump = -9
                    player_y = 50
                if keys[pygame.K_SPACE]:
                    is_jump = True
                    jump = 9

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

            for coin in coins:
                coin.reset()
                if player_rect.colliderect(coin.rect):
                    collect_coin.play()
                    coins.remove(coin)
                    sum_coin += 1
            for donut in donuts:
                donut.reset()
                if player_rect.colliderect(donut.rect):
                    collect_coin.play()
                    donuts.remove(donut)
                    sum_donut += 1

            if state == 'finish':
            # if sum_coin >= 3 and sum_donut >= 1:
                next_button = Button(200, 40)
                retry_button = Button(200, 40)
                menu_button = Button(200, 40)
                window.blit(black_screen, (0, 0))

                main_coin.reset()
                set_text(':' + str(sum_coin), 370, 110, (255, 255, 255), 50)

                main_donut.reset()
                set_text(':' + str(sum_donut), 370, 40, (255, 255, 255), 50)

                next_button.draw(170, 200, 'NEXT', None, 35)
                menu_button.draw(270, 270, 'MENU', menu, 35)

                if retry_button.draw(400, 200, 'RETRY', game_level4, 35):
                    sum_coin = 0
                    sum_donut = 0

                    player_x = -200
                    player_y = 220
                    if sum_coin == 0 and sum_donut == 0:
                        for coin in coins:
                            coin.reset()
                            coins.append(coin)
                            if player_rect.colliderect(coin.rect):
                                collect_coin.play()
                                coins.remove(coin)
                                sum_coin += 1
                        for donut in donuts:
                            donut.reset()
                            if player_rect.colliderect(donut.rect):
                                collect_coin.play()
                                donuts.remove(donut)
                                sum_donut += 1
            if state == 'gameover':
            # if wounds >= 3:
                retry_button = Button(200, 40)
                menu_button = Button(200, 40)
                window.blit(black_screen, (0, 0))
                main_coin.reset()
                set_text(':' + str(sum_coin), 370, 110, (255, 255, 255), 50)

                main_donut.reset()
                set_text(':' + str(sum_donut), 370, 40, (255, 255, 255), 50)

                menu_button.draw(270, 270, 'MENU', menu, 35)

                if retry_button.draw(270, 200, 'RETRY', game_level4, 35):
                    sum_coin = 0
                    sum_donut = 0

                    player_x = -200
                    player_y = 220
                    if sum_coin == 0 and sum_donut == 0:
                        for coin in coins:
                            coin.reset()
                            coins.append(coin)
                            if player_rect.colliderect(coin.rect):
                                collect_coin.play()
                                coins.remove(coin)
                                sum_coin += 1
                        for donut in donuts:
                            donut.reset()
                            if player_rect.colliderect(donut.rect):
                                collect_coin.play()
                                donuts.remove(donut)
                                sum_donut += 1

            pygame.display.update()
            clock.tick(15)

'''FUNCTIONS'''

#TEXT
def set_text(message, x, y, fcolor=(0,0,0), fsize=60):
    text = pygame.font.Font('font/slkscreb.ttf', fsize).render(message, True, fcolor)
    window.blit(text, (x, y))

#COINS
def create_coin(x1, y1, x2, y2, x3, y3):
    coins = []
    coin = Sprite('images/coin.png', x1, y1, 50, 50)
    coin1 = Sprite('images/coin.png', x2, y2, 50, 50)
    coin2 = Sprite('images/coin.png', x3, y3, 50, 50)
    coins.append(coin)
    coins.append(coin1)
    coins.append(coin2)
    return coins

#DONUTS
def create_donuts(x1, y1):
    donuts = []
    donut1 = Sprite('images/donut.png', x1, y1, 65, 66)
    donuts.append(donut1)
    return donuts

#ENEMYS
def create_poops(amount, x1, y1, x2=None, y2=None, x3=None, y3=None):
    poops = []
    if amount == 1:
        poop1 = Sprite('images/poop.png', x1, y1, 34, 34)
        poops.append(poop1)
        return poops
    if amount == 2:
        poop1 = Sprite('images/poop.png', x1, y1, 34, 34)
        poop2 = Sprite('images/poop.png', x2, y2, 34, 34)
        poops.append(poop1)
        poops.append(poop2)
        return poops
    if amount == 3:
        poop1 = Sprite('images/poop.png', x1, y1, 34, 34)
        poop2 = Sprite('images/poop.png', x2, y2, 34, 34)
        poop3 = Sprite('images/poop.png', x3, y3, 34, 34)
        poops.append(poop1)
        poops.append(poop2)
        poops.append(poop3)
        return poops

#HEARTS
def create_hearts():
    hearts = []
    amount_heart = 3
    x = 400
    y = -5
    for i in range(amount_heart):
        heart = Sprite('images/heartt.png',  x, y, 76, 76)
        hearts.append(heart)
        x -= 80
    return hearts

'''OTHER STUFF'''
coins = create_coin(0, 0, 0, 0, 0, 0)
poops = create_poops(0, 0, 0)
donuts = create_donuts(0, 0)
hearts = create_hearts()

#IMAGES
platform1 = Sprite('images/platform0.png', 80, 60, 260, 44)
platform2 = Sprite('images/platform0.png', 450, 260, 260, 44)
platform3 = Sprite('images/platform0.png', 80, 170, 260, 44)
platform4 = Sprite('images/platform1.png', 200, 340, 190, 70)

platform5 = Sprite('images/platform0.png', -20, 60, 260, 44)
platform6 = Sprite('images/platform1.png', 420, 180, 190, 70)
platform7 = Sprite('images/platform0.png', 480, 40, 260, 44)
platform8 = Sprite('images/platform0.png', 10, 340, 260, 44)

platform9 = Sprite('images/platform0.png', -20, 200, 260, 44)
platform10 = Sprite('images/platform0.png', 480, 200, 260, 44)
platform11 = Sprite('images/platform0.png', 450, 50, 260, 44)
platform12 = Sprite('images/platform0.png', 250, 350, 260, 44)
platform13 = Sprite('images/platform1.png', 0, 50, 190, 70)

platform14 = Sprite('images/platform0.png', -40, 230, 260, 44)
platform15 = Sprite('images/platform0.png', 530, 50, 260, 44)
platform16 = Sprite('images/platform0.png', 480, 300, 260, 44)
platform17 = Sprite('images/platform1.png', 220, 340, 190, 70)
trampoline = Sprite('images/donuttt.png', 320, 440, 80, 46)

black_screen = pygame.image.load('images/black_screen.jpg')
black_screen.set_alpha(200)

main_coin = Sprite('images/coin.png', 300, 110, 50, 50)
main_donut = Sprite('images/donut.png', 300, 40, 65, 66)

#SOUNDS
button = pygame.mixer.Sound('sounds/button_click.wav')
button.set_volume(0.2)
collect_coin = pygame.mixer.Sound('sounds/collect_coin.mp3')
bg_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')
bg_sound.play(-1)

#OTHER
menu()
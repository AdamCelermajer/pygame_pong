import pygame
import os
import math
pygame.font.init()
pygame.mixer.init()


HEALTH_FONT = pygame.font.SysFont("comic Sans", 40)
WINNER_FONT = pygame.font.SysFont("comic Sans", 110)
FPS = 60
WIDTH, HEIGHT = 900, 600
WIDTHRECT, HEIGHTRECT = 10, 100
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VEL = 5
VEL_BALL = 6
ANGLE_FORCE = math.pi/4
LEFT_IN = pygame.USEREVENT+1
RIGHT_IN = pygame.USEREVENT+2


def draw(left, right, bullets):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, BORDER)
    pygame.draw.rect(WIN, WHITE, left)
    pygame.draw.rect(WIN, WHITE, right)
    for bullet in bullets:
        pygame.draw.rect(WIN, WHITE, bullet)
    pygame.display.update()


def ai_mouv(right, bullets):

    for bullet in bullets:

        if bullet.y > HEIGHT-(10+right.height):
            print("bad")
        else:
            right.y = bullet.y


def handle_mouv(left, keys_pressed):

    if keys_pressed[pygame.K_UP] and left.y-VEL > 0:
        left.y -= VEL
    if keys_pressed[pygame.K_DOWN] and left.y+left.height+VEL < HEIGHT:
        left.y += VEL


def handle_bullet(bullets, left_rect, right_rect, bullet_angle):

    for bullet in bullets:
        xup = VEL_BALL*math.cos(bullet_angle)
        yup = VEL_BALL*math.sin(bullet_angle)

        bullet.x += xup

        bullet.y += yup

        if bullet.x + xup < 0:
            pygame.event.post(pygame.event.Event(LEFT_IN))
            bullets.remove(bullet)

        if bullet.x + xup > WIDTH:
            pygame.event.post(pygame.event.Event(RIGHT_IN))
            bullets.remove(bullet)


################################################################
            # collision with walls

        if bullet.y + yup >= HEIGHT:

            bullet_angle = math.atan2(-yup/VEL_BALL, xup/VEL_BALL)
        if bullet.y + yup <= 0:

            bullet_angle = math.atan2(-yup/VEL_BALL, xup/VEL_BALL)

####################################################################


####################################################################
         # TODO: collision with stick not working properly

        if left_rect.colliderect(bullet):

            if bullet.y > left_rect.y+(left_rect.height//2):
                bullet_angle += math.pi - \
                    (bullet.y/(left_rect.y+left_rect.height))*ANGLE_FORCE
            else:
                bullet_angle += math.pi + \
                    ((left_rect.y+left_rect.height)/bullet.y)*ANGLE_FORCE

        if right_rect.colliderect(bullet):

            if bullet.y > right_rect.y+(right_rect.height//2):
                bullet_angle -= math.pi - \
                    (bullet.y/(right_rect.y+right_rect.height))*ANGLE_FORCE
            else:
                bullet_angle -= math.pi + \
                    ((right_rect.y+right_rect.height)/bullet.y)*ANGLE_FORCE

####################################################################

    return bullet_angle


def main():

    run = True
    clock = pygame.time.Clock()
    right_rect = pygame.Rect(875, 300, WIDTHRECT, HEIGHTRECT)
    left_rect = pygame.Rect(25, 300, WIDTHRECT, HEIGHTRECT)
    bullet_angle = 2*math.pi
    bullets = []
    left_lives = 10
    right_lives = 10
    bullet_exist = False
    winner_text = ""
    while run:
        if bullet_exist == False:
            bullet = pygame.Rect((WIDTH//2)-5, HEIGHT//2, 15, 15)
            bullet_exist = True
            bullet_angle = 2*math.pi
            bullets.append(bullet)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == LEFT_IN:
                left_lives -= 1
                bullet_exist = False
            if event.type == RIGHT_IN:
                right_lives -= 1
                bullet_exist = False
        keys_pressed = pygame.key.get_pressed()
        bullet_angle = handle_bullet(
            bullets, left_rect, right_rect, bullet_angle)
        ai_mouv(right_rect, bullets)
        handle_mouv(left_rect, keys_pressed)
        draw(left_rect, right_rect, bullets)


if __name__ == "__main__":
    main()

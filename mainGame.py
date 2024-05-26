# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random


# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('지구를 지켜라!')


# 게임 음악 로드
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 배경 이미지 로드
background = pygame.image.load('resources/image/background.png').convert()

# 게임 오버 이미지 로드
game_over_image = pygame.image.load('resources/image/gameover.png')

# 재시작 버튼 이미지 로드
restart_button_image = pygame.image.load('resources/image/restart_button.png')
restart_button_rect = restart_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
restart_button_rect.center = (250, 150)  # 버튼 위치 조정
restart_button_rect.width = 200
restart_button_rect.height = 100

# 종료 버튼 이미지 로드
exit_button_image = pygame.image.load('resources/image/exit_button.png')
exit_button_rect = exit_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
exit_button_rect.center = (270, 550)  # 버튼 위치 조정
exit_button_rect.width = 200
exit_button_rect.height = 100

# 게임 오버 상태를 나타내는 변수 추가
is_game_over = False

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

# 플레이어 관련 매개변수 설정
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 플레이어 스프라이트 이미지 영역
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 플레이어 폭발 스프라이트 이미지 영역
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# 총알 객체에 사용할 surface 관련 매개변수 정의
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 적 객체에 사용할 surface 관련 매개변수 정의
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()

# 격추된 비행기를 저장하여 격추된 스프라이트 애니메이션을 렌더링
enemies_down = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0

player_down_index = 16

score = 0

clock = pygame.time.Clock()

# 게임 오버 화면 함수 정의
def show_game_over():
    screen.blit(game_over_image, (0, 0))
    screen.blit(restart_button_image, restart_button_rect)
    screen.blit(exit_button_image, exit_button_rect)

    # 점수 표시
    font = pygame.font.Font(None, 48)
    text = font.render('Score: ' + str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(text, text_rect)

    pygame.display.update()

def reset_game():
    global is_game_over, player, player_down_index, score, enemies1, running
    is_game_over = False
    player.is_hit = False
    player_down_index = 16
    score = 0
    enemies1.empty()
    player.bullets.empty()
    running = True

running = True

while running:
    # 게임의 최대 프레임 속도를 45으로 제어
    clock.tick(45)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and is_game_over:
            mouse_pos = pygame.mouse.get_pos()
            print(f"Mouse Clicked at: {mouse_pos}")  # 클릭 위치 출력
            if restart_button_rect.collidepoint(mouse_pos):
                print("Restart button clicked")  # 디버깅 메시지
                reset_game()  # 게임 재시작
            elif exit_button_rect.collidepoint(mouse_pos):
                print("Exit button clicked")  # 디버깅 메시지
                pygame.quit()
                exit()

    if is_game_over:
        show_game_over()
        continue  # 게임 오버 상태에서는 아래 코드를 실행하지 않음
            
            
    # 총알 발사 빈도 제어 및 발사
    if not player.is_hit:
        if shoot_frequency % 15 == 0:
            bullet_sound.play()
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    # 적 생성
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    # 총알 이동, 창 범위를 벗어나면 삭제
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # 적 이동, 창 범위를 벗어나면 삭제
    for enemy in enemies1:
        enemy.move()
        # 플레이어가 맞았는지 확인
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)

    # 격추된 적 객체를 격추된 적 Group에 추가하여 격추 애니메이션 렌더링
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # 배경 그리기
    screen.fill(0)
    screen.blit(background, (0, 0))

    # 플레이어 비행기 그리기
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # 이미지 인덱스를 변경하여 비행기에 애니메이션 효과 주기
        player.img_index = shoot_frequency // 8
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            is_game_over = True

    # 격추 애니메이션 그리기
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # 총알과 적 그리기
    player.bullets.draw(screen)
    enemies1.draw(screen)

    # 점수 그리기
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    # 화면 업데이트
    pygame.display.update()

    #for event in pygame.event.get():
     #   if event.type == pygame.QUIT:
      #      pygame.quit()
       #     exit()
            
    # 키보드 이벤트 감지
    key_pressed = pygame.key.get_pressed()
    # 플레이어가 맞았을 경우 무효화
    if not player.is_hit:
        # 쉬프트 키가 눌렸을 때 이동 속도 증가
        if key_pressed[K_LSHIFT] or key_pressed[K_RSHIFT]:
            player.speed = 12  # 예시로 이동 속도를 12로 증가시킵니다. 필요에 따라 조절 가능합니다.
        else:
            player.speed = 8   # 쉬프트 키를 뗐을 때 이동 속도를 다시 기본값으로 설정합니다.

    
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()

# 게임 오버 상태에서 마우스 클릭 이벤트를 계속 처리하기 위해 루프 추가
while is_game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 마우스 클릭 이벤트 처리
            mouse_pos = pygame.mouse.get_pos()
            print(f"Mouse Clicked at: {mouse_pos}")  # 클릭 위치 출력
            if restart_button_rect.collidepoint(mouse_pos):
                print("Restart button clicked")  # 디버깅 메시지
                reset_game()  # 게임 재시작
            elif exit_button_rect.collidepoint(mouse_pos):
                print("Exit button clicked")  # 디버깅 메시지
                pygame.quit()
                exit()

    # 배경 화면 그리기
    screen.fill((255, 255, 255))
    screen.blit(game_over_image, (0, 0))
    screen.blit(restart_button_image, restart_button_rect)
    screen.blit(exit_button_image, exit_button_rect)

    # 점수 표시
    font = pygame.font.Font(None, 48)
    text = font.render('Score: ' + str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(text, text_rect)

    pygame.display.update()

font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24

screen.blit(game_over_image, (0, 0))
screen.blit(restart_button_image, restart_button_rect)
screen.blit(exit_button_image, exit_button_rect)
screen.blit(text, text_rect)
pygame.display.update()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()

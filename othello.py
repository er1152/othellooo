# https://niwakomablog.com/othello44-python-application/
import pygame
from pygame.locals import *
import sys
import random
SCR_RECT = Rect(0, 0, 850, 800)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCR_RECT.size)
pygame.display.set_caption("Othllo")
sprite = pygame.sprite.RenderUpdates()
pygame.init()


def drow_line():
    sprite.update()
    sprite.draw(screen)
    pygame.display.update()

    screen.fill((255, 255, 255))

    for xpos in range(X_ST, (8*DIS+X_ST+1), DIS):
        pygame.draw.line(screen, 0x000000, (xpos, Y_ST),
                         (xpos, 8*DIS+Y_ST+1), WEIGHT)
    for ypos in range(Y_ST, 8*DIS+Y_ST+1, DIS):
        pygame.draw.line(screen, 0x000000, (X_ST, ypos),
                         (8*DIS+X_ST+1, ypos), WEIGHT)


def draw_stone():
    for y in range(10):
        for x in range(10):
            color = field[y][x]
            wr_xpos = (x-1) * DIS + X_ST + DIS/2
            wr_ypos = (y-1) * DIS + Y_ST + DIS/2
            if color == 2:
                pygame.draw.circle(
                    screen, 0x000000, (wr_xpos, wr_ypos),  DIS*0.4)
            elif color == 1:
                pygame.draw.circle(
                    screen, 0x000000, (wr_xpos, wr_ypos),  DIS*0.4, 3)
            else:
                continue


def check(xpos, ypos, color):
    reverse_list = []
   # reverseする側（my_color）とされる側（opponet_color）/ 2(black) or 1(white)
    enemy_color = 2 if color == 1 else 1

    if field[ypos][xpos] != 0:
        return False

    for dy, dx in check_list:
        ny, nx = ypos+dy, xpos+dx
        if field[ny][nx] == enemy_color:  # 置けそうだったら
            tmp = [(xpos, ypos)]
            while field[ny][nx] == enemy_color:  # 連鎖スタート
                tmp.append((nx, ny))
                nx += dx
                ny += dy

            if field[ny][nx] == color:  # 連鎖の先に自分と同じ色があるなら
                return True
    return False


def reverse_stone(xpos, ypos, color):  # ひっくり返す(fieldを書き換える)
    reverse_list = []
    # 相手の色　2(black) or 1(white)
    enemy_color = 2 if color == 1 else 1

    for dy, dx in check_list:
        nx, ny = xpos+dx, ypos+dy
        if field[ny][nx] == enemy_color:  # 置けそうだったら
            tmp = [(xpos, ypos)]
            while field[ny][nx] == enemy_color:  # 連鎖スタート
                tmp.append((nx, ny))
                nx += dx
                ny += dy

            if field[ny][nx] == color:  # 連鎖の先に自分と同じ色があるなら
                while tmp:
                    reverse_list.append(tmp.pop())  # rewrite_listにつっこむ
            else:
                tmp.clear()
    for x, y in reverse_list:  # reverse_listから取り出しひっくり返す
        field[y][x] = color
    draw_stone()
    return


def is_pass():
    return


def player_turn():
    print("player turn!!")
    while True:
        clock.tick(3)
        drow_line()
        draw_stone()
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == MOUSEBUTTONDOWN and event.button == 1 and (event.pos[0] >= 100 and event.pos[0] < 740)):
                xpos, ypos = (event.pos[0]-100)//80+1, event.pos[1]//80+1
                if not check(xpos, ypos, player_color):
                    continue
                else:
                    reverse_stone(xpos, ypos, player_color)

                    return


def cpu_turn():
    print("cpu turn!!")
    is_pass = False
    is_placeable_list = []
    for y in range(10):
        for x in range(10):
            if check(x, y, cpu_color):
                is_placeable_list.append((x, y))
    if not is_placeable_list:
        print("cpu:pass")
        return
    else:
        x, y = is_placeable_list[random.randrange(len(is_placeable_list))]
        reverse_stone(x, y, cpu_color)
        clock.tick(10)
        draw_stone()
        return


def main():
    global X_ST
    X_ST = 100
    global Y_ST
    Y_ST = 0
    global DIS
    DIS = 80
    global WEIGHT
    WEIGHT = 10

    global field  # 0:empty 1:white 2:black -1:wall
    field = [[-1 if i == 0 or j == 0 or i == 9 or j ==
              9 else 0 for j in range(10)] for i in range(10)]
    field[4][4], field[5][5] = 2, 2
    field[5][4], field[4][5] = 1, 1
    global player_color
    player_color = 2
    global cpu_color
    cpu_color = 1
    global check_list
    check_list = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                  (1, 0), (-1, 1), (0, 1), (1, 1)]

    for i in range(100):  # 最大100ターン

        is_finish = True  # ターン変わるたびにゲーム終了かの判定
        for y in range(10):
            for x in range(10):
                if field[y][x] == 0:
                    is_finish = False
                    break
            else:
                continue
            break

        if is_finish:
            print("finish!!")

        else:  # ゲームが続いているなら
            if i % 2 == 0:
                player_turn()
            else:
                cpu_turn()

        drow_line()
        draw_stone()


'''    while True:
        clock.tick(60)
        drow_line()
        draw_stone()
        print("131")

        for event in pygame.event.get():        # 閉じるボタンが押されたとき
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit
'''

if __name__ == "__main__":
    main()

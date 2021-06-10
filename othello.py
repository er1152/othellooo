# https://niwakomablog.com/othello44-python-application-code/
import pygame
from pygame.locals import *
import sys
import copy
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


def reverse_stone(rewrite_list, is_playr):
    for x, y in rewrite_list:
        if is_playr:
            field[y][x] = player_color
        else:
            field[y][x] = 1 if player_color == 2 else 2

        wr_xpos = (x-1) * DIS + X_ST + DIS/2
        wr_ypos = (y-1) * DIS + Y_ST + DIS/2
        if is_playr and player_color == 2 or not is_playr and player_color == 1:
            pygame.draw.circle(
                screen, 0x000000, (wr_xpos, wr_ypos),  DIS*0.4)
        elif is_playr and player_color == 1 or not is_playr and player_color == 2:
            pygame.draw.circle(
                screen, 0x000000, (wr_xpos, wr_ypos), DIS*0.4, 3)
        else:
            print("error")
            sys.exti()


def check(ypos, xpos, is_playr):  # 与えられた座標が置ける場所かチェック、置ければひっくり返す座標のリストを返す
    global check_list
    check_list = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                  (1, 0), (-1, 1), (0, 1), (1, 1)]
    rewrite_list = []
    # 相手の色　2(black) or 1(white)
    if is_playr:
        my_color = player_color
        opponet_color = 2 if player_color == 1 else 1
    else:
        my_color = 1 if player_color == 2 else 2
        opponet_color = player_color

    if field[ypos][xpos] != 0:
        return []

    for dy, dx in check_list:
        ny, nx = ypos+dy, xpos+dx
        if field[ny][nx] == opponet_color:  # 置けそうだったら
            tmp = [(xpos, ypos)]
            while field[ny][nx] == opponet_color:  # 連鎖スタート
                tmp.append((nx, ny))
                nx += dx
                ny += dy

            if field[ny][nx] == my_color:  # 連鎖の先に自分と同じ色があるなら
                while tmp:
                    rewrite_list.append(tmp.pop())  # rewrite_listにつっこむ
            else:
                tmp.clear()
    return rewrite_list


def is_pass():


def player_turn():
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
                rewite_list = check(ypos, xpos, True)
                if not rewite_list:
                    continue
                else:
                    reverse_stone(rewite_list, True)
                    return


def cpu_turn():
    is_pass = False
    for y in range(10):
        for x in range(10):
            rewite_list = check(y, x, False)
            if not rewite_list:
                continue
            else:
                is_pass = True
                reverse_stone(rewite_list, False)
                return
    if not is_pass:
        print("cpu:pass")
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

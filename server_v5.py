import socket
import random
import threading
import time
import sys


class Player:
    conn = 0,
    id = 0,
    nickname = 0,
    position = 0,
    direction = 0,
    claimed_dots = 0,
    temp_dots = 0,
    live = 0

    def __init__(self, conn, id, nickname, position, direction, claimed_dots, temp_dots, live):
        self.conn = conn
        self.id = id
        self.nickname = nickname
        self.position = position
        self.direction = direction
        self.claimed_dots = claimed_dots
        self.temp_dots = temp_dots
        self.live = live

    def __str__(self):
        return "conn={0}, id={1}, pos={3}, dir={4}, cd_dots={5}, tp_dots{6}".format(self.conn, self.id, self.nickname,
                                                                                    self.position, self.direction,
                                                                                    self.claimed_dots,
                                                                                    self.temp_dots, self.live)


sizeMap = 20  # размер карты X*X
free_space = '_'  # символ для обозначения пустоты
arrMap = [[free_space for _ in range(0, sizeMap)] for _ in range(0, sizeMap)]  # сама карта
players = []  # массив игроков

HOST = "0.0.0.0"
PORT = 50007

temp_player = Player(0, 1, "nickname", [5, 5], int(random.uniform(-1.4, 2.4)), [[5, 5],[6, 5],[5, 6],[6, 6],[4, 5],[5, 4],[4, 4]], [], 1)
players.append(temp_player)
temp_player = Player(0, 2, "nickname", [2, 2], int(random.uniform(-1.4, 2.4)), [], [], 1)
players.append(temp_player)
temp_player = Player(0, 3, "nickname", [8, 7], int(random.uniform(-1.4, 2.4)), [], [], 1)
players.append(temp_player)
temp_player = Player(0, 4, "nickname", [8, 5], int(random.uniform(-1.4, 2.4)), [], [], 1)
players.append(temp_player)
temp_player = Player(0, 5, "nickname", [10, 1], int(random.uniform(-1.4, 2.4)), [], [], 1)
players.append(temp_player)


def map_to_json():
    return {"map": arrMap, "players_positions": [players[i].position for i in range(0, len(players))]}


def show_map():  # delete in release
    str_arr = ""
    claimed_dots = []
    for z in range(0, len(players)):
        for j in range(0, len(players[z].claimed_dots)):
            claimed_dots.append(players[z].claimed_dots[j])
    print("cm",claimed_dots)
    for i in range(sizeMap):
        for j in range(sizeMap):
            if [i,j] in claimed_dots:
                str_arr+=('{' + str(arrMap[i][j]) + '}')
            else:
                if [i, j] in [players[i].position for i in range(0, len(players))]:
                    str_arr += ('(' + str(arrMap[i][j]) + ')')
                else:
                    str_arr += ('[' + str(arrMap[i][j]) + ']')
        str_arr += "\n"
    return str_arr


'''
player must be alive
'''


def move_player(i):

    # claimed_dots = [[players[z].claimed_dots[j] for j in range(0, len(players[z].claimed_dots))] for z in
    #                 range(0, len(players))]
    temp_dots = []
    for z in range(0, len(players)):
        for j in range(0, len(players[z].temp_dots)):
            temp_dots.append(players[z].temp_dots[j])

    x = players[i].position[0]
    y = players[i].position[1]
    dir = players[i].direction
    print(temp_dots)
    if dir == 1:
        if x > 0 and [x - 1, y] not in temp_dots:
            players[i].temp_dots.append([x - 1, y])
            players[i].position[0] -= 1
            print("up")
            arrMap[players[i].position[0]][players[i].position[1]] = players[i].id
        else:
            players[i].live = 0
            print("die")
    if dir == -1:
        if x < (sizeMap - 1) and [x + 1, y] not in temp_dots:
            players[i].temp_dots.append([x + 1, y])
            players[i].position[0] += 1
            print("down")
            arrMap[players[i].position[0]][players[i].position[1]] = players[i].id
        else:
            players[i].live = 0
            print("die")
    if dir == 0:
        if y > 0 and [x, y - 1] not in temp_dots:
            players[i].temp_dots.append([x, y - 1])
            players[i].position[1] -= 1
            print("left")
            arrMap[players[i].position[0]][players[i].position[1]] = players[i].id
        else:
            players[i].live = 0
            print("die")
    if dir == 2:
        if y < (sizeMap - 1) and [x, y + 1] not in temp_dots:
            players[i].temp_dots.append([x, y + 1])
            players[i].position[1] += 1
            print("right")
            arrMap[players[i].position[0]][players[i].position[1]] = players[i].id

        else:
            players[i].live = 0
            print("die")




def update_map():
    while True:
        if players:
            for i in range(len(players)):
                if players[i].live == 1:
                    move_player(i)
            print(show_map())
            time.sleep(0.7)
            # print(map_to_json())


update_map()

import socket
import random
import threading
import time
import sys
from collections import Counter

''' две рекурсии только '''


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


sizeMap = 30  # размер карты X*X
free_space = '_'  # символ для обозначения пустоты
arrMap = [[free_space for _ in range(0, sizeMap)] for _ in range(0, sizeMap)]  # сама карта
players = []  # массив игроков

HOST = "0.0.0.0"
PORT = 50010


def map_to_json():
    # all_dots = []
    # for z in range(0, len(players)):
    #     for j in range(0, len(players[z].claimed_dots)):
    #         all_dots.append(players[z].claimed_dots[j])
    #         all_dots.append(players[z].id)
    # return {"map": arrMap, "players_positions": [players[i].position for i in range(0, len(players))],
    #         "all_dots": all_dots}
    return {"map": arrMap, "players_positions": [players[i].position for i in range(0, len(players))],
            "all_dots": [players[z].claimed_dots[j] for z in range(0, len(players)) for j in
                         range(0, len(players[z].claimed_dots))]}


def show_map():  # delete in release
    str_arr = ""
    claimed_dots = []
    for z in range(0, len(players)):
        for j in range(0, len(players[z].claimed_dots)):
            claimed_dots.append(players[z].claimed_dots[j])
            # claimed_dots.append(players[z].id)

    print("cm", claimed_dots)
    for i in range(sizeMap):
        for j in range(sizeMap):
            if [i, j] in [players[i].position for i in range(0, len(players))]:
                str_arr += ('(' + str(arrMap[i][j]) + ')')
            else:
                if [i, j] in claimed_dots:
                    str_arr += ('{' + str(arrMap[i][j]) + '}')
                else:
                    str_arr += ('[' + str(arrMap[i][j]) + ']')
        str_arr += "\n"
        # print("WOWOWOWOW\n",str_arr)
    return str_arr


'''
player must be alive
'''


def delete_player(z):
    print("P{0} ! Player #{0} died!".format(players[z].id))
    for i in range(len(players[z].claimed_dots)):
        arrMap[players[z].claimed_dots[i][0]][players[z].claimed_dots[i][1]] = free_space

    for i in range(len(players[z].temp_dots)):
        arrMap[players[z].temp_dots[i][0]][players[z].temp_dots[i][1]] = free_space

    # arrMap[players[z].position[0]][players[z].position[1]] = free_space

    players[z].claimed_dots = []
    players[z].temp_dots = []
    players[z].position = 0
    players[z].live = 0
    players[z].id = -1
    time.sleep(1)
    # players[z].conn.close()


def move_player(i):
    # claimed_dots = [[players[z].claimed_dots[j] for j in range(0, len(players[z].claimed_dots))] for z in
    #                 range(0, len(players))]
    all_temp_dots = []
    for z in range(0, len(players)):
        for j in range(0, len(players[z].temp_dots)):
            all_temp_dots.append([players[z].temp_dots[j], z])

    claimed_dots = []
    # print("len(cd)", len(players[i].claimed_dots))
    for z in range(len(players[i].claimed_dots)):
        # print(z, i, players[i].claimed_dots[z])
        claimed_dots.append([players[i].claimed_dots[z][0], players[i].claimed_dots[z][1]])
    temp_dots = []
    # print("len(td)", len(players[i].temp_dots))
    for z in range(len(players[i].temp_dots)):
        temp_dots.append([players[i].temp_dots[z][0], players[i].temp_dots[z][1]])

    x = players[i].position[0]
    y = players[i].position[1]
    dir = players[i].direction
    live = 1
    # print("all_td", all_temp_dots)

    if dir == 1:
        if x > 0:
            for k in range(len(all_temp_dots)):
                if all_temp_dots and [x - 1, y] in all_temp_dots[k]:
                    delete_player(all_temp_dots[k][1])
                    # print("die", k)
                    live = 0
            if live != 0:
                players[i].temp_dots.append([x - 1, y])
                if [x - 1, y] in claimed_dots:
                    players[i].claimed_dots += temp_dots
                    players[i].temp_dots = []
                players[i].position[0] -= 1
                # print("up")
                arrMap[players[i].position[0]][players[i].position[1]] = players[i].id
        else:
            players[i].live = 0
            delete_player(i)
            # print("die", i)
    if dir == -1:
        if x < (sizeMap - 1):
            for k in range(len(all_temp_dots)):
                if all_temp_dots and [x + 1, y] in all_temp_dots[k]:
                    delete_player(all_temp_dots[k][1])
                    # print("die", k)
                    live = 0
            if live != 0:
                players[i].temp_dots.append([x + 1, y])
                if [x + 1, y] in claimed_dots:
                    players[i].claimed_dots += temp_dots
                    players[i].temp_dots = []
                players[i].position[0] += 1
                # print("up")
                arrMap[players[i].position[0]][players[i].position[1]] = players[i].id
        else:
            players[i].live = 0
            delete_player(i)
            # print("die", i)
    if dir == 0:
        if y > 0:
            for k in range(len(all_temp_dots)):
                if all_temp_dots and [x, y - 1] in all_temp_dots[k]:
                    delete_player(all_temp_dots[k][1])
                    # print("die", k)
                    live = 0
            if live != 0:
                players[i].temp_dots.append([x, y - 1])
                if [x, y - 1] in claimed_dots:
                    players[i].claimed_dots += temp_dots
                    players[i].temp_dots = []
                players[i].position[1] -= 1
                # print("up")
                arrMap[players[i].position[0]][players[i].position[1]] = players[i].id
        else:
            players[i].live = 0
            delete_player(i)
            # print("die", i)
    if dir == 2:
        if y < (sizeMap - 1):
            for k in range(len(all_temp_dots)):
                if all_temp_dots and [x, y + 1] in all_temp_dots[k]:
                    delete_player(all_temp_dots[k][1])
                    # print("die", k)
                    live = 0
            if live != 0:
                players[i].temp_dots.append([x, y + 1])
                if [x, y + 1] in claimed_dots:
                    players[i].claimed_dots += temp_dots
                    players[i].temp_dots = []
                players[i].position[1] += 1
                # print("up")
                arrMap[players[i].position[0]][players[i].position[1]] = players[i].id
        else:
            players[i].live = 0
            delete_player(i)
            # print("die", i)


def update_map():
    while True:
        alive_players = 0
        if players:
            for p in players:
                alive_players += p.live
                # print("id: {0}, live: {1}".format(p.id, p.live))
        if alive_players > 0:
            for i in range(len(players)):
                if players[i].live == 1:
                    move_player(i)
            # print(show_map())
            # print(arrMap)
            time.sleep(0.6)
            # print(map_to_json())


threading.Thread(target=update_map).start()


def get_notfree_dots():
    all_temp_dots = []
    for z in range(0, len(players)):
        for j in range(0, len(players[z].temp_dots)):
            all_temp_dots.append([players[z].temp_dots[j], z])
    all_claimed_dots = []
    for z in range(0, len(players)):
        for j in range(0, len(players[z].claimed_dots)):
            all_claimed_dots.append([players[z].claimed_dots[j], z])
    return all_claimed_dots + all_temp_dots


def give_init_player_position():
    x = -1
    y = -1

    while not (0 < x < (len(arrMap) - 1) > y > 0) and not ([x, y] in get_notfree_dots()):
        x = int(random.uniform(1, (len(arrMap) - 2)))
        y = int(random.uniform(1, (len(arrMap) - 2)))
        print("   init pos: [", x, y, "]")

    return [x, y]


# @TODO сделать отключение игрока и удаление players

def manipulation_with_connected_player(i):
    # print("tt")
    while True:
        try:
            data = ((players[i].conn.recv(1024)).decode()).split()
            data1 = data[1:]
            res = map_to_json()
            if len(data) > 0:
                try:
                    if data[0] == "getId":
                        res = players[i].id
                        players[i].conn.send(str(res).encode())
                    if data[0] == "getData":
                        # print("getData")
                        res = map_to_json()
                        players[i].conn.send(str(res).encode())
                        # if data[0] == "getplayerspos":
                        #     res = get_players_pos(players)
                        # print("show map for", players[i].id)
                    if data[0] == "move":
                        # print("move")

                        if not (players[i].direction == 0 and int(data[1]) == 2 or players[
                            i].direction == 2 and int(data[1]) == 0 or players[i].direction == -1 and int(
                            data[1]) == 1 or players[i].direction == 1 and int(data[1]) == -1) and players[
                            i].live == 1 and players[i].direction != int(data[1]):
                            players[i].direction = int(data[1])
                            print("P{0} | Change dir to {1}".format(players[i].id, players[i].direction))

                            # move(arr, players[0])
                except Exception as e:
                    res = e
                    # move_all(arr)
                    # res = show_map(arr)
                    # players[i].conn.send(str(res).encode())
                    # time.sleep(0.5)
                    # time.sleep(0.1)
                    # print(arr)
        except Exception as e:
            players[i].conn.close()
            delete_player(i)
            # or crush this thread
            break


def generate_id():
    # print("   GENERATE NEW ID")
    while True:
        try:
            ex_ids = []
            if players:
                for i in range(len(players)):
                    ex_ids.append(players[i].id)
            # print(ex_ids)
            a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for x in ex_ids:
                if x in a:
                    a.remove(x)
            # print(a)
            z = a[int(random.uniform(0, len(a)))]
            print("   NEW ID is: ", z)
            return z
        except Exception as e:
            print(">> EXCEPTION: ",e)



def getIndex(id):
    for i in range(len(players)):
        if id == players[i].id:
            return i


def generate_init_base(temp_coords, z):
    arrMap[temp_coords[0]][temp_coords[1]] = z
    arrMap[temp_coords[0] + 1][temp_coords[1] + 1] = z
    arrMap[temp_coords[0]][temp_coords[1] + 1] = z
    arrMap[temp_coords[0] + 1][temp_coords[1]] = z
    arrMap[temp_coords[0] - 1][temp_coords[1] - 1] = z
    arrMap[temp_coords[0]][temp_coords[1] - 1] = z
    arrMap[temp_coords[0] - 1][temp_coords[1]] = z
    arrMap[temp_coords[0] + 1][temp_coords[1] - 1] = z
    arrMap[temp_coords[0] - 1][temp_coords[1] + 1] = z

    return [
        [temp_coords[0], temp_coords[1]],
        [(temp_coords[0] + 1), (temp_coords[1] + 1)],
        [(temp_coords[0]), (temp_coords[1] + 1)],
        [(temp_coords[0] + 1), (temp_coords[1])],
        [(temp_coords[0] - 1), (temp_coords[1] - 1)],
        [(temp_coords[0]), (temp_coords[1]) - 1],
        [(temp_coords[0]) - 1, (temp_coords[1])],
        [(temp_coords[0] + 1), (temp_coords[1] - 1)],
        [(temp_coords[0] - 1), (temp_coords[1] + 1)]
    ]


def get_connections():
    while True:
        s = None
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                      socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except socket.error as msg:
                s = None
                continue
            try:
                s.bind(sa)
                s.listen(1)
            except socket.error as msg:
                s.close()
                s = None
                continue
            break
        if s is None:
            print('could not open socket')
            sys.exit(1)
        conn, addr = s.accept()
        conn.settimeout(3)
        print("[  \n=> Generate a new player:", '\n   Connected by', addr, )
        print("   players: ", players)

        temp_coords = give_init_player_position()
        temp_id = generate_id()
        temp_player = Player(conn, temp_id, "nickname",
                             [temp_coords[0], temp_coords[1]], int(random.uniform(-1.4, 2.4)),
                             generate_init_base(temp_coords, temp_id),
                             [],
                             1)
        print("   NEW PLAYER is: ", str(temp_player))
        players.append(temp_player)
        threading.Thread(target=manipulation_with_connected_player, args=[getIndex(temp_player.id)]).start()
        # players.append(conn)
        # move(arr, players[len(players)-1])

        print("  ", players, "\n]")


threading.Thread(target=get_connections).start()

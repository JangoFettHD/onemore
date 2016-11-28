import socket
import random
import threading
import time
import sys

# from shapely.geometry import Point, Polygon

sizemap = 20
arr = []
free_space='_'


class player():
    conn = ""
    id = ""
    nickname = ""
    positiony = 0
    positionx = 0
    direction = 1
    claimed_dots = []
    live = 1  # 1-жив

    def __init__(self, conn, id, nickname, positionx, positiony, direction, claimed_dots, live):
        self.conn = conn
        self.id = id
        self.nickname = nickname
        self.positiony = positionx
        self.positionx = positiony
        self.direction = direction
        self.claimed_dots = claimed_dots
        self.live = live

    def __str__(self):
        return "conn: {4}, id: {0}, x: {1}, y: {2}, dir: {3}, cm {5}, live {6}".format(self.id, self.positiony,
                                                                                       self.positionx,
                                                                                       self.direction, self.conn,
                                                                                       self.claimed_dots, self.live)


def init(size_map):
    global arr
    n = size_map
    arr = [[free_space for _ in range(0, n)] for _ in range(0, n)]


init(sizemap)
print(arr, len(arr))

HOST = "0.0.0.0"  # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port

players = []


def getIndex(id):
    for i in range(len(players)):
        if id == players[i].id:
            return i


def show_map(arr):
    str_arr = ""
    for i in range(len(arr)):
        for j in range(len(arr)):
            if [i, j] in get_players_pos(players):
                str_arr += ('(' + str(arr[i][j]) + ')')
            else:
                str_arr += ('[' + str(arr[i][j]) + ']')
        str_arr += "\n"
    return str_arr


def get_players_pos(players):
    pl = []
    for i in range(len(players)):
        pl.append([players[i].positionx, players[i].positiony])
    return pl


# def flood_fill(arr, player_id, i, j):
#     if arr[i][j] != player_id:
#         arr[i][j] = player_id
#         if i != 0: flood_fill(arr, player_id, i - 1, j)
#         if j != 0: flood_fill(arr, player_id, i, j - 1)
#         if i != (len(arr) - 1): flood_fill(arr, player_id, i + 1, j)
#         if j != (len(arr[0]) - 1): flood_fill(arr, player_id, i, j + 1)


def flood_fill(arr, player, i, j):
    player_id=player.id
    if arr[i][j] != player_id:
        arr[i][j] = player_id
        if i != 0:
            flood_fill(arr, player, i - 1, j)
        if j != 0:
            flood_fill(arr, player, i, j - 1)
        if i != (len(arr) - 1):
            flood_fill(arr, player, i + 1, j)
        if j != (len(arr[0]) - 1):
            flood_fill(arr, player, i, j + 1)
        player.claimed_dots.append([i,j])


# def inPolygon(x, y, xp, yp):
#     c = 0
#     for i in range(len(xp)):
#         if (((yp[i] <= y < yp[i - 1]) or (yp[i - 1] <= y < yp[i])) and (
#                     x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
#             c = 1 - c
#
#     if c != 0:
#         print("C is", c)
#     return c

#
# def inPolygon(x,y, Exy):
#     poly=Polygon(Exy)
#     print(poly.contains(Point(x,y)))
#     return poly.contains(Point(x,y))

def inPolygon(x, y, playerId):
    up = 0
    right = 0
    left = 0
    down = 0
    for i in range(0, len(arr)):
        for j in range(y, len(arr)):
            if arr[x][j] == playerId:
                right = 1
                break
                # --->

    for i in range(x, len(arr)):
        for j in range(0, len(arr)):
            if arr[i][y] == playerId:
                down = 1
                break
                # down

    for i in range(0, x + 1):
        for j in range(0, y + 1):
            if arr[x][j] == playerId:
                left = 1
                break
                # left

    for i in range(0, x + 1):
        for j in range(0, x + 1):
            if arr[i][y] == playerId:
                up = 1
                break
                # up
    print(up, down, left, right)
    return (up + down + left + right)


'''
Смотрим координаты точки, если сверху есть данная цифра, слева , справа и снизу - то она в контуре .
'''


def move(arr, player):
    if player.direction == 1 and player.positionx > 0:  # ^
        player.positionx -= 1
        # print("up")
    if player.direction == -1 and player.positionx < (len(arr) - 1):
        player.positionx += 1
        # print("down")
    if player.direction == 0 and player.positiony > 0:
        player.positiony -= 1
        # print("left")
    if player.direction == 2 and player.positiony < (len(arr) - 1):
        player.positiony += 1
        # print("right")
    # print(player.positionx, player.positiony)

    for i in range(len(players)):
        # print("i", i)
        if players[i].id != player.id:
            # print(players[i].id, player.id, i)
            if [player.positionx, player.positiony] in players[i].claimed_dots:
                # print("OWW")
                player.live = 0
                print("boom", players[i].id, player.id)
                break

    if player.positiony == (len(arr) - 1) or player.positionx == (
                len(arr[0]) - 1) or player.positionx == 0 or player.positiony == 0:
        player.live = 0

    if [player.positionx, player.positiony] not in player.claimed_dots and player.live == 1:
        player.claimed_dots.append([player.positionx, player.positiony])
        arr[player.positionx][player.positiony] = player.id
    else:
        if player.live == 1:
            arrX = []
            arrY = []

            for i in range(len(player.claimed_dots)):
                arrX.append(player.claimed_dots[i][0])
                arrY.append(player.claimed_dots[i][1])

            print(player.claimed_dots)
            print(arrX, arrY)
            for i in range(len(arr)):
                for j in range(len(arr[0])):
                    if inPolygon(i, j, player.id) > 3:
                        flood_fill(arr, player, i, j)


def move_all(arr):
    for i in range(len(players)):
        move(arr, players[i])


def remove_player(index):
    print("Delete player: ", index)
    print(players)
    # print(players[index].claimed_dots[0])
    for i in range(len(arr)):  # @TODO проверить на -1
        for j in range(len(arr)):
            if arr[i][j] == players[index].id:
                arr[i][j] = free_space
                # print(players[index].claimed_dots[0][i][0],players[index].claimed_dots[i][0])
                # arr[players[index].claimed_dots[i][0]][players[index].claimed_dots[i][1]] = 0
    try:
        players[index].conn.close()
    except Exception:
        pass
    # players.pop(index)
    players[index] = player("", -1, "nickname", -3, -3, -3, [], 0)
    print(players)


# move(arr, players[0])

def check_live_users():
    global players
    count = 0
    for i in range(len(players)):
        if players[i].live == 1:
            count += 1
    return count


def update_map():
    global players
    while True:
        # if check_live_users()==0:
        #     players=[]
        if players:
            move_all(arr)
            time.sleep(1)
            # else:
            #     init(sizemap)


threading.Thread(target=update_map).start()


def manipulation_with_connected_player(i):
    while True:
        if players[i].live == 0:
            remove_player(i)
            break
        else:  # @TODO переделать
            try:
                data = ((players[i].conn.recv(1024)).decode()).split()
                data1 = data[1:]
                res = show_map(arr)
                if len(data) > 0:
                    try:
                        if data[0] == "show_map":
                            res = show_map(arr)

                        if data[0] == "getplayerspos":
                            res = get_players_pos(players)
                            # print("show map for", players[i].id)
                        if data[0] == "move":
                            if not (players[i].direction == 0 and int(data[1]) == 2 or players[
                                i].direction == 2 and int(data[1]) == 0 or players[i].direction == -1 and int(
                                data[1]) == 1 or players[i].direction == 1 and int(data[1]) == -1):
                                players[i].direction = int(data[1])
                            print(str(players[0]))
                            # move(arr, players[0])
                    except Exception as e:
                        res = e
                # move_all(arr)
                # res = show_map(arr)
                players[i].conn.send(str(res).encode())
                # time.sleep(0.5)
                # print(arr)
            except Exception as e:
                remove_player(i)
                break


# whie True:
#     if players:
#         for i in range(len(players)):
#             threading.Thread(target=manipulation_with_connected_player, args=i).start()

def generate_id():
    print("GENERATE NEW ID")
    a = None
    ex_ids = []
    if players:
        for i in range(len(players)):
            ex_ids.append(players[i].id)
    while a not in ex_ids:
        a = int(random.uniform(1, 9))
        if a not in ex_ids:
            print(ex_ids, a)
            return a
    print("ERROR GENERATION")


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
        print('Connected by', addr)
        temp_player = player(conn, generate_id(), "nickname", int(random.uniform(0, len(arr))),
                             int(random.uniform(0, len(arr))), int(random.uniform(-1, 2)), [], 1)
        players.append(temp_player)
        threading.Thread(target=manipulation_with_connected_player, args=[getIndex(temp_player.id)]).start()
        # players.append(conn)
        # move(arr, players[len(players)-1])
        print(players)


threading.Thread(target=get_connections).start()

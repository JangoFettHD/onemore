import asyncore
import socket
import random
import threading
import time
import sys
from shapely.geometry import Point, Polygon


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


MAX_PLAYERS = 10
sizeMap = 50  # размер карты X*X
free_space = '_'  # символ для обозначения пустоты
arrMap = [[free_space for _ in range(0, sizeMap)] for _ in range(0, sizeMap)]  # сама карта
players = {}  # массив игроков

HOST = "0.0.0.0"
PORT = 50015


def map_to_json():
    return {"map": arrMap,
            "players_positions": [p.position for p in players.values()],
            "all_dots": [p1.claimed_dots[j] for p1 in players.values() for j in
                         range(0, len(p1.claimed_dots))]}


# def show_map():  # delete in release
#     str_arr = ""
#     claimed_dots = []
#     for z in range(0, len(players)):
#         for j in range(0, len(players[z].claimed_dots)):
#             claimed_dots.append(players[z].claimed_dots[j])
#
#     print("cm", claimed_dots)
#     for i in range(sizeMap):
#         for j in range(sizeMap):
#             if [i, j] in [players[i].position for i in range(0, len(players))]:
#                 str_arr += ('(' + str(arrMap[i][j]) + ')')
#             else:
#                 if [i, j] in claimed_dots:
#                     str_arr += ('{' + str(arrMap[i][j]) + '}')
#                 else:
#                     str_arr += ('[' + str(arrMap[i][j]) + ']')
#         str_arr += "\n"
#     return str_arr


'''
player must be alive
'''


def flood_fill(player, i, j):
    if arrMap[i][j] != player.id:
        arrMap[i][j] = player.id
        if i != 0:
            flood_fill(player, i - 1, j)
        if j != 0:
            flood_fill(player, i, j - 1)
        if i != (len(arrMap) - 1):
            flood_fill(player, i + 1, j)
        if j != (len(arrMap[0]) - 1):
            flood_fill(player, i, j + 1)
        player.claimed_dots.append([i,j])


def inPolygon(x, y, xp, yp):
   c=0
   for i in range(len(xp)):
       if (((yp[i]<=y and y<yp[i-1]) or (yp[i-1]<=y and y<yp[i])) and \
           (x > (xp[i-1] - xp[i]) * (y - yp[i]) / (yp[i-1] - yp[i]) + xp[i])): c = 1 - c
   return c

print( inPolygon(100, 0, (-100, 100, 100, -100), (100, 100, -100, -100)))


def delete_player(player):
    # if player.live == 0:
    #     print("P{0} ! Player {1} disconnected".format(player.id, player.nickname))
    # else:
    all_temp_dots = []
    for p in players.values():
        for j in range(0, len(p.temp_dots)):
            all_temp_dots.append([p.temp_dots[j], p])
    all_claimed_dots = []
    for p in players.values():
        for j in range(0, len(p.claimed_dots)):
            all_claimed_dots.append([p.claimed_dots[j], p])


    print("P{0} ! Player #{0} died!".format(player.id))
    for i in range(len(player.claimed_dots)):
        if player.id == arrMap[player.claimed_dots[i][0]][player.claimed_dots[i][1]]:
            arrMap[player.claimed_dots[i][0]][player.claimed_dots[i][1]] = free_space
    for i in range(len(player.temp_dots)):
        if player.id == arrMap[player.temp_dots[i][0]][player.temp_dots[i][1]]:
            arrMap[player.temp_dots[i][0]][player.temp_dots[i][1]] = free_space
    # players.pop(z)
    player.claimed_dots = []
    player.temp_dots = []
    player.position = 0
    player.live = 0
    player.id = -1
    player.direction = -5

    # time.sleep(1)
    # players[z].conn.close()


def move_player(player):
    all_temp_dots = []
    for p in players.values():
        for j in range(0, len(p.temp_dots)):
            all_temp_dots.append([p.temp_dots[j], p])

    claimed_dots = []
    for z in range(len(player.claimed_dots)):
        claimed_dots.append([player.claimed_dots[z][0], player.claimed_dots[z][1]])
    temp_dots = []
    # print("len(td)", len(players[i].temp_dots))
    for z in range(len(player.temp_dots)):
        temp_dots.append([player.temp_dots[z][0], player.temp_dots[z][1]])

    x = player.position[0]
    y = player.position[1]
    dir = player.direction
    live = 1


    rules = {
        1: [x > 0, [x - 1, y], 0, -1, [x + 1, y -1],[x + 1, y +1]],
        -1: [x < (sizeMap - 1), [x + 1, y], 0, 1, [x - 1, y -1],[x - 1, y +1]],
        0: [y > 0, [x, y - 1], 1, -1, [x - 1, y +1],[x + 1, y +1]],
        2: [y < (sizeMap - 1), [x, y + 1], 1, 1,[x + 1, y -1],[x - 1, y -1]]
    }

    if dir in rules:
        if rules.get(dir)[0]:
            for k in range(len(all_temp_dots)):
                if all_temp_dots and rules.get(dir)[1] in all_temp_dots[k]:
                    delete_player(all_temp_dots[k][1])
                    # print("die", k)
                    live = 0
            if live != 0:
                player.temp_dots.append(rules.get(dir)[1])
                if rules.get(dir)[1] in claimed_dots:

                    player.claimed_dots += temp_dots
                    player.temp_dots = []
                    #
                    
                    # arrX = []
                    # arrY = []
                    # for z in range(len(player.claimed_dots)):
                    #     arrX.append(player.claimed_dots[z][0])
                    #     arrY.append(player.claimed_dots[z][1])
                    # print(temp_dots, player,rules.get(dir)[4][0],rules.get(dir)[4][1])
                    if claimed_dots:
                        poly=Polygon(claimed_dots)
                        for i in range(0, len(arrMap)):
                            for j in range(0, len(arrMap)):
                                print(i,j,poly.contains(Point(i, j)))
                                if poly.contains(Point(i, j)):
                                    #print("paint",player.id,rules.get(dir)[4][0],rules.get(dir)[4][1], player.position)
                                    flood_fill(player,i,j)

                    # elif inPolygon(rules.get(dir)[5][0], rules.get(dir)[5][1], arrX, arrY):
                    #     print("paint",player.id,rules.get(dir)[5][0],rules.get(dir)[5][1], player.position)
                    #     flood_fill(player,rules.get(dir)[5][0],rules.get(dir)[5][1])
                    # # if inPolygon(rules.get(dir)[1][0], rules.get(dir)[1][1], arrX, arrY):
                    #     print("paint", x, y, player.id)
                    #     flood_fill(player, x, y)

                    #

                player.position[rules.get(dir)[2]] += rules.get(dir)[3]
                arrMap[player.position[0]][player.position[1]] = player.id
        else:
            player.live = 0
            delete_player(player)


def update_map():
    while True:
        try:
            alive_players = 0
            if players:
                for p in players.values():
                    alive_players += p.live
            if alive_players > 0:
                for p in players.values():
                    if p.live == 1:
                        move_player(p)
                time.sleep(0.6)
        except Exception:
            print("-")


threading.Thread(target=update_map).start()

# @TODO TODO

def get_notfree_dots():
    all_temp_dots = []
    all_claimed_dots = []
    for p in players.values():
        for j in range(0, len(p.temp_dots)):
            all_temp_dots.append([p.temp_dots[j]])
        for j in range(0, len(p.claimed_dots)):
            all_claimed_dots.append([p.claimed_dots[j]])
    print(all_claimed_dots, all_temp_dots)
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


class CommandHandler(asyncore.dispatcher_with_send):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def handle_read(self):
        command = self.recv(1024)

        if not command:
            return

        else:
            command = command.decode().split()
            # print(command)

        if self.addr in players:
            player = players[self.addr]
            if command[0] == "move":
                if not (player.direction == 0 and int(command[1]) == 2 or player
                        .direction == 2 and int(command[1]) == 0 or player.direction == -1 and int(
                    command[1]) == 1 or player.direction == 1 and int(
                    command[1]) == -1) and player.live == 1 and player.direction != int(command[1]):
                    player.direction = int(command[1])
                    print("P{0} | Change dir to {1}".format(player.id, player.direction))
            elif command[0] == "getId":
                self.send(str(player.id).encode())
            elif command[0] == "getData":
                # print("getData")
                res = map_to_json()
                self.send(str(res).encode())
            else:
                vals = {}
                vals["error"] = "Command not found"
                # self.send(json.dumps(vals).encode())
        else:
            if command[0] == "reg":
                print("[  \n=> Generate a new player:", '\n   Connected by', self.addr, )
                print("   players: ", players)
                nick = command[1]
                print("   Nickname=", nick)
                temp_coords = give_init_player_position()
                temp_id = generate_id()
                temp_player = Player(self.addr, temp_id, nick,
                                     [temp_coords[0], temp_coords[1]], int(random.uniform(-1.4, 2.4)),
                                     generate_init_base(temp_coords, temp_id),
                                     [],
                                     1)
                print("   NEW PLAYER is: ", str(temp_player))
                players[self.addr] = temp_player
                print("  ", players, "\n]")

    def handle_close(self):
        print("Disconnect " + str(self.addr))
        if self.addr in players:
            players.pop(self.addr)
        self.close()


#
# def manipulation_with_connected_player(i):
#     # print("tt")
#     while True:
#         try:
#             data = ((players[i].conn.recv(1024)).decode()).split()
#             data1 = data[1:]
#             res = map_to_json()
#             if len(data) > 0:
#                 try:
#                     if data[0] == "getId":
#                         res = players[i].id
#                         players[i].conn.send(str(res).encode())
#                     if data[0] == "getData":
#                         # print("getData")
#                         res = map_to_json()
#                         players[i].conn.send(str(res).encode())
#                         # if data[0] == "getplayerspos":
#                         #     res = get_players_pos(players)
#                         # print("show map for", players[i].id)
#                     if data[0] == "move":
#                         # print("move")
#
#                         if not (players[i].direction == 0 and int(data[1]) == 2 or players[
#                             i].direction == 2 and int(data[1]) == 0 or players[i].direction == -1 and int(
#                             data[1]) == 1 or players[i].direction == 1 and int(data[1]) == -1) and players[
#                             i].live == 1 and players[i].direction != int(data[1]):
#                             players[i].direction = int(data[1])
#                             print("P{0} | Change dir to {1}".format(players[i].id, players[i].direction))
#
#                             # move(arr, players[0])
#                 except Exception as e:
#                     res = e
#         except Exception as e:
#             players[i].conn.close()
#             delete_player(i)
#             # or crush this thread
#             break


def generate_id():
    while True:
        try:
            ex_ids = []
            if players:
                for p in players.values():
                    ex_ids.append(p.id)
            a = []
            for i in range(MAX_PLAYERS):
                a.append(i)
            # a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            print(a)
            for x in ex_ids:
                if x in a:
                    a.remove(x)
            z = a[int(random.uniform(0, len(a)))]
            print("   NEW ID is: ", z)
            return z
        except Exception as e:
            print(">> EXCEPTION: ", e)


def getIndex(id):
    for i in range(len(players)):
        if id == players[i].id:
            return i


def generate_init_base(temp_coords, z):
    arrBaseDots = []
    for i in range(temp_coords[0] - 1, temp_coords[0] + 2):
        for j in range(temp_coords[1] - 1, temp_coords[1] + 2):
            arrMap[i][j] = z
            arrBaseDots.append([i, j])
    return arrBaseDots


class Server(asyncore.dispatcher):
    def __init__(self, host="localhost", port=1566):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)
        self.handler = None
        print("Server running on {}:{}".format(host, port))

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            return
        else:
            if len(players) < 10:
                sock, addr = pair
                print('Incoming connection from %s' % repr(addr))
                self.handler = CommandHandler(str(addr), sock)
                # self.handler = get_connections(str(addr), sock)

    @staticmethod
    def main(host="localhost", port=1566):
        server = Server(host, port)
        try:
            asyncore.loop(timeout=2)
        except KeyboardInterrupt as e:
            print("Ctrl+C pressed. Shutting down.")
            server.close()


# def get_connections(addr, sock):
#     conn = sock
#     conn.settimeout(3)
#     print("[  \n=> Generate a new player:", '\n   Connected by', addr, )
#     print("   players: ", players)
#
#     nick = "Unknown"
#     try:
#         data = ((conn.recv(200)).decode()).split()
#         if data[1] != "Unknown":
#             nick = data[1]
#     except Exception as e:
#         print(">> EXCEPTION: ", e)
#
#     print("   Nickname=", nick)
#     temp_coords = give_init_player_position()
#     temp_id = generate_id()
#     temp_player = Player(conn, temp_id, nick,
#                          [temp_coords[0], temp_coords[1]], int(random.uniform(-1.4, 2.4)),
#                          generate_init_base(temp_coords, temp_id),
#                          [],
#                          1)
#     print("   NEW PLAYER is: ", str(temp_player))
#     players.append(temp_player)
#     threading.Thread(target=manipulation_with_connected_player, args=[getIndex(temp_player.id)]).start()
#
#     print("  ", players, "\n]")
#
#
# threading.Thread(target=get_connections).start()

Server.main("0.0.0.0")

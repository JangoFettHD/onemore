import asyncore
import socket
import random
import threading
import time
import sys
from shapely.geometry import Point, Polygon

MAX_PLAYERS = 10

str_json = ""
#@TODO

# update(){
#     0.6sec
#     move()
#     gen(str_json)
#
# }

class Dot:
    coord = []
    x = 0
    y = 0

    def __init__(self, x, y):
        self.coord = [x, y]
        self.x = x
        self.y = y

    def __eq__(self, other):
        if type(other)==type(self):
            return self.coord == other.coord
        return False

    def __str__(self):
        return "[{0},{1}]".format(self.x, self.y)

    def to_list(self):
        return [self.x, self.y]

    def __getitem__(self, i):
        if i==0:
            return self.x
        elif i==1:
            return self.y

    def __setitem__(self, key, value):
        if key==0:
            self.x=value
        elif key==1:
            self.y=value


class Player:
    conn = 0,
    id = 0,
    color = "",
    nickname = 0,
    position = 0,
    direction = 0,
    claimed_dots = 0,
    temp_dots = 0,
    live = 0

    def __init__(self, conn, id, color, nickname, position, direction, claimed_dots, temp_dots, live):
        self.conn = conn
        self.id = id
        self.color = color
        self.nickname = nickname
        self.position = position
        self.direction = direction
        self.claimed_dots = claimed_dots
        self.temp_dots = temp_dots
        self.live = live

    def __str__(self):
        return self.to_json()

    def to_json(self):
        # print(self.id, self.nickname, self.color, self.position, self.claimed_dots, self.temp_dots)
        str_json = "{"
        str_json += "\"id\": {0}," \
                    "\"nickname\": \"{1}\"," \
                    "\"color\": \"{2}\"," \
                    "\"position\": {3}," \
                    "\"claimed_dots\": [{4}]," \
                    "\"temp_dots\": [{5}]".format(self.id, self.nickname, self.color, self.position,
                                                  ", ".join(str(x) for x in self.claimed_dots),
                                                  ", ".join(str(x) for x in self.temp_dots))
        str_json += "},"
        return str_json


def flood_fill(player, i, j):
    if Dot(i,j) not in player.claimed_dots:
        player.claimed_dots.append(Dot(i,j))
        if i != 0:
            flood_fill(player, i - 1, j)
        if j != 0:
            flood_fill(player, i, j - 1)
        if i != (mapa.sizeMap - 1):
            flood_fill(player, i + 1, j)
        if j != (mapa.sizeMap - 1):
            flood_fill(player, i, j + 1)
        #player.claimed_dots.append([i, j])


class GameMap:
    players = {}
    sizeMap = 40
    dots = [[]]

    def __init__(self, sizeMap):
        self.sizeMap = sizeMap
        self.players = {}
        self.dots = [[0 for _ in range(0, sizeMap)] for _ in range(0, sizeMap)]

    def add_player(self, player):
        self.players[player.conn] = player

    def remove_player(self, player):
        player.live = 0
        player.claimed_dots = []
        player.direction = -10
        player.temp_dots = []
        player.id = -1

    def disconnect_player(self, player=0, addr=0):
        if addr == 0:
            addr = player.conn
        self.players.pop(addr)

    def is_claimed(self, dot):
        for p in self.players.values():
            if dot in p.claimed_dots:
                return p
        return False

    def is_temp(self, dot):
        for p in self.players.values():
            if dot in p.temp_dots:
                return p
        return False

    def to_json(self):
        str_json = "{ \"data\":[ "
        for p in self.players.values():
            if (p.id != -1):
                str_json += p.to_json()
        str_json = str_json[:-1]
        str_json += "],"
        str_json += "\"size_map\": {0}".format(self.sizeMap)
        str_json += " }"
        return str_json

    def not_free_dots(self):
        all_temp_dots = []
        all_claimed_dots = []
        for p in self.players.values():
            for j in range(0, len(p.temp_dots)):
                all_temp_dots.append([p.temp_dots[j]])
            for j in range(0, len(p.claimed_dots)):
                all_claimed_dots.append([p.claimed_dots[j]])
        return all_claimed_dots + all_temp_dots

    def all_temp_dots(self):
        temp_dots = []
        for p in self.players.values():
            for j in range(0, len(p.temp_dots)):
                temp_dots.append([p.temp_dots[j], p])
        return temp_dots

    def update_map(self):
        for p in self.players.values():
            if p.live != 0:

                all_temp_dots = self.all_temp_dots()
                x = p.position.x
                y = p.position.y
                dir = p.direction
                live = 1

                rules = {
                    1: [x > 0, Dot(x - 1, y), 0, -1, Dot(x + 1, y - 1), Dot(x + 1, y + 1)],
                    -1: [x < (self.sizeMap - 1), Dot(x + 1, y), 0, 1, Dot(x - 1, y - 1), Dot(x - 1, y + 1)],
                    0: [y > 0, Dot(x, y - 1), 1, -1, Dot(x - 1, y + 1), Dot(x + 1, y + 1)],
                    2: [y < (self.sizeMap - 1), Dot(x, y + 1), 1, 1, Dot(x + 1, y - 1), Dot(x - 1, y - 1)]
                }

                if dir in rules:
                    print(p)
                    # poly_claimed_dots = []
                    # dot.to_list() for dot in p.claimed_dots:
                    #     poly_claimed_dots.append(dot.to_list())

                    if rules.get(dir)[0]:
                        for k in range(len(all_temp_dots)):
                            if all_temp_dots and rules.get(dir)[1] in all_temp_dots[k]:
                                self.remove_player(all_temp_dots[k][1])
                                live = 0
                        if live != 0:
                            p.temp_dots.append(rules.get(dir)[1])
                            if rules.get(dir)[1] in p.claimed_dots:

                                p.claimed_dots += p.temp_dots

                                if p.claimed_dots:
                                    poly = Polygon([dot.to_list() for dot in p.claimed_dots])
                                    for i in range(0, self.sizeMap):
                                        for j in range(0, self.sizeMap):
                                            # print(i, j, poly.contains(Point(i, j)))
                                            if poly.contains(Point(i, j)) and p.temp_dots:
                                                # print("paint",player.id,rules.get(dir)[4][0],rules.get(dir)[4][1], player.position)
                                                flood_fill(p, i, j)
                                p.temp_dots = []
                            p.position[rules.get(dir)[2]] += rules.get(dir)[3]
                            #arrMap[player.position[0]][player.position[1]] = player.id
                    else:
                        p.live = 0
                        self.remove_player(p)


mapa = GameMap(30)


# mapa.add_player(Player(("0.0.0.0", 5152), 4, "#FFFFFF", "Jon", Dot(5, 2), 1,
#                        [Dot(1, 1), Dot(1, 2), Dot(4, 4)],
#                        [Dot(5, 2), Dot(3, 1), Dot(7, 7)], 1))
# mapa.add_player(Player(("125.211.1.0", 5166), 1, "#DDDFFF", "Kenny", Dot(3, 1), -1,
#                        [Dot(2, 2), Dot(5, 2), Dot(7, 7)],
#                        [Dot(1, 1), Dot(1, 2), Dot(5, 5)], 1))
# print(mapa.to_json())
# print(mapa.is_claimed(Dot(0, 1)))
# print(mapa.is_claimed(Dot(5, 2)))

def update():
    global str_json
    while True:
        if mapa.players:
            time.sleep(0.7)
            mapa.update_map()
            str_json=mapa.to_json()

threading.Thread(target=update).start()


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

        if self.addr in mapa.players:
            player = mapa.players[self.addr]
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
                res = str_json
                self.send(str(res).encode())
            else:
                vals = {}
                vals["error"] = "Command not found"
        else:
            if command[0] == "reg":
                nick = command[1]
                temp_coords = generate_init_pos()
                temp_id = generate_id()
                temp_player = Player(self.addr, temp_id, "", nick,
                                     temp_coords, int(random.uniform(-1.4, 2.4)),
                                     generate_init_base(temp_coords),
                                     [],
                                     1)
                mapa.add_player(temp_player)
                print(temp_player.to_json())

    def handle_close(self):
        print("Disconnect " + str(self.addr))
        if self.addr in mapa.players:
            mapa.disconnect_player(addr=self.addr)
        self.close()


def generate_id():
    while True:
        try:
            ex_ids = []
            if mapa.players:
                for p in mapa.players.values():
                    ex_ids.append(p.id)
            a = []
            for i in range(MAX_PLAYERS):
                a.append(i)
            for x in ex_ids:
                if x in a:
                    a.remove(x)
            z = a[int(random.uniform(1, len(a)))]
            return z
        except Exception as e:
            print(">> EXCEPTION: ", e)


def generate_init_pos():
    base = []
    x = -1
    y = -1

    while not (0 < x < (mapa.sizeMap - 1) > y > 0) and not (base in mapa.not_free_dots()):
        x = int(random.uniform(1, (mapa.sizeMap - 2)))
        y = int(random.uniform(1, (mapa.sizeMap - 2)))
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                base.append(Dot(i, j))
                # print("   init pos: [", x, y, "]")

    return Dot(x, y)


def generate_init_base(temp_coords):
    arrBaseDots = []
    for i in range(temp_coords.x - 1, temp_coords.x + 2):
        for j in range(temp_coords.y - 1, temp_coords.y + 2):
            arrBaseDots.append(Dot(i, j))
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
            if len(mapa.players) < MAX_PLAYERS:
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


Server.main("0.0.0.0")

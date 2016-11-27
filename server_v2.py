import socket
import random
import threading
import time
import sys

sizemap=25
arr = []


class player():
    conn=""
    id = ""
    positiony = 0
    positionx = 0
    direction = 1

    def __init__(self, conn, id, positionx, positiony, direction):
        self.conn = conn
        self.id = id
        self.positiony = positionx
        self.positionx = positiony
        self.direction = direction

    def __str__(self):
        return "conn: {4}, id: {0}, x: {1}, y: {2}, dir: {3}".format(self.id, self.positiony, self.positionx, self.direction, self.conn)


def init(size_map):
    global arr
    n = size_map
    arr = [[0 for _ in range(0, n)] for _ in range(0, n)]


init(sizemap)
print(arr, len(arr))

HOST = "0.0.0.0"               # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

players=[]

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
        players.append(player(conn, len(players)+1, int(random.uniform(0, len(arr))), int(random.uniform(0, len(arr))), 1))
        #players.append(conn)
        #move(arr, players[len(players)-1])
        print(players)

threading.Thread(target=get_connections).start()

def show_map(arr):
    str_arr = ""
    for i in range(len(arr)):
        for j in range(len(arr)):
            str_arr += str(arr[i][j])
        str_arr += "\n"
    return str_arr


def move(arr, player):
    if player.direction == 1 and player.positionx>0: #^
        player.positionx -= 1
        print("up")
    if player.direction == -1 and player.positionx<(len(arr)-1):
        player.positionx += 1
        print("down")
    if player.direction == 0 and player.positiony>0:
        player.positiony -= 1
        print("left")
    if player.direction == 2 and player.positiony<(len(arr)-1):
        player.positiony += 1
        print("right")
    print(player.positionx, player.positiony)
    arr[player.positionx][player.positiony] = player.id


def move_all(arr):
    for i in range(len(players)):
        move(arr, players[i])


#move(arr, players[0])


def update_map():
    while True:
        if players:
            move_all(arr)
            time.sleep(1)
        else:
            init(sizemap)


threading.Thread(target=update_map).start()

while True:
    if players:
        for i in range(len(players)):
            try:
                data = ((players[i].conn.recv(1024)).decode()).split()
                data1 = data[1:]
                res = show_map(arr)
                if len(data) > 0:
                    try:
                        if data[0] == "get_id": ##@TODO
                            pass
                            #res=addr ##@TODO
                        if data[0] == "show_map":
                            res = show_map(arr)
                        if data[0] == "move":
                            players[i].direction = int(data[1])
                            print(str(players[0]))
                            #move(arr, players[0])
                            #res = show_map(arr)
                    except Exception as e:
                        res = e
                #move_all(arr)
                #res = show_map(arr)
                players[i].conn.send(str(res).encode())
                #time.sleep(0.5)
                #print(arr)
            except Exception:
                players[i].conn.close()
                players.pop(i)
                print(players)

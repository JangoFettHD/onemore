import socket
import random
import threading
import time

s = socket.socket(socket.AF_INET)
s.bind(("0.0.0.0", 6001))
s.listen(0)

sock, addr = s.accept()
print("Incoming connection: ", addr)

arr = []
players = []


class player():
    id = ""
    positionx = 0
    positiony = 0
    direction = 1

    def __init__(self, id, positionx, positiony, direction):
        self.id = id
        self.positionx = positionx
        self.positiony = positiony
        self.direction = direction

    def change_direction(self, direction):
        self.direction = direction

    def __str__(self):
        return "{0}, x: {1}, y: {2}, dir: {3}".format(self.id, self.positionx, self.positiony, self.direction)


players.append(player("1", int(random.uniform(0, len(arr))), int(random.uniform(0, len(arr))), 1))


def init(size_map):
    global arr
    n = size_map
    arr = [[0 for _ in range(0, n)] for _ in range(0, n)]


init(10)
print(arr)


def show_map(arr):
    str_arr = ""
    for i in range(len(arr)):
        for j in range(len(arr)):
            str_arr += str(arr[i][j])
        str_arr += "\n"
    return str_arr


def move(arr, player):
    if player.direction == 1:
        player.positionx -= 1
    if player.direction == -1:
        player.positionx += 1
    if player.direction == 0:
        player.positiony -= 1
    if player.direction == 2:
        player.positiony += 1
    arr[player.positionx][player.positiony] = player.id


def move_all(arr):
    for i in range(len(players)):
        move(arr, players[i])


move(arr, players[0])


def update_map():
    while True:
        move_all(arr)
        time.sleep(1)


threading.Thread(target=update_map).start()

while True:
    data = ((sock.recv(1024)).decode()).split()
    data1 = data[1:]
    res = show_map(arr)
    if len(data) > 0:
        try:
            if data[0] == "show_map":
                res = show_map(arr)
            if data[0] == "move":
                players[0].direction = int(data[1])
                print(str(players[0]))
                #move(arr, players[0])
                #res = show_map(arr)
        except Exception as e:
            res = e
    #move_all(arr)
    #res = show_map(arr)
    sock.send(str(res).encode())
    #time.sleep(0.5)
    #print(arr)

import sys
from shapely.geometry import Point, Polygon

a = [[1, 0], [4, 0], [4, 4], [1, 4]]
poly = Polygon(a)
print(poly.contains(Point(3, 2)))


class Dot:
    coord = []

    def __init__(self, x, y):
        self.coord = [x, y]

    def __eq__(self, other):
        return self.coord == other.coord

    def __str__(self):
        return "({0},{1})".format(self.coord[0], self.coord[1])


'''
{
"data":
[
    {
        "id": 2,
        "nickname":"Oleg",
        "color": "#FWOKWW",
        "position"=[10,2],
        "claimed_dots":[[1,1],[...]],
        "temp_dots":[[1,1],[...]],

    },
    {
        "id": 3,
        "nickname":"Sasha228",
        "color": "#WWWWWW",
        "position"=[10,2],
        "claimed_dots":[[1,1],[...]],
        "temp_dots":[[1,1],[...]],
    }
]
}

'''


class Dot:
    coord = []

    def __init__(self, x, y):
        self.coord = [x, y]

    def __eq__(self, other):
        return self.coord == other.coord

    def __str__(self):
        return "[{0},{1}]".format(self.coord[0], self.coord[1])


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
        # return "conn={0}, id={1}, pos={3}, dir={4}, cd_dots={5}, tp_dots{6}".format(self.conn, self.id, self.nickname,
        #                                                                             self.position, self.direction,
        #                                                                             self.claimed_dots,
        #                                                                             self.temp_dots, self.live)

    def to_json(self):
        print(self.id, self.nickname, self.color, self.position, self.claimed_dots, self.temp_dots)
        str_json="{"
        str_json+="\"id\": {0}," \
                  "\"nickname\": \"{1}\"," \
                  "\"color\": \"{2}\"," \
                  "\"position\": {3}," \
                  "\"claimed_dots\": [{4}]," \
                  "\"temp_dots\": [{5}]".format(self.id, self.nickname,self.color, self.position, ", ".join(str(x) for x in self.claimed_dots), ", ".join(str(x) for x in self.temp_dots))
        str_json+="},"
        return str_json
        # return "\{\"id\": {0}," + "\"nickname\": {1},"+ "\"color\": {2}," + "\"position\": {3},"+ "\"claimed_dots\": {4},"+"\"temp_dots\": {5}\},".format(self.id, self.nickname,self.color, self.position,self.claimed_dots, self.temp_dots)


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

    def disconnect_player(self, player):
        self.players.pop(player.conn)

    def is_claimed(self, dot):
        return

    def to_json(self):
        str_json = "{ \"data\":[ "
        for p in self.players.values():
            str_json += p.to_json()
        str_json = str_json[:-1]
        str_json += "]}"
        return str_json


mapa = GameMap(30)
mapa.add_player(Player(("0.0.0.0",5152), 4, "#FFFFFF", "Jon", Dot(5, 2), 1,
                       [Dot(1, 1), Dot(1, 2), Dot(4, 4)],
                       [Dot(5, 2), Dot(3, 1), Dot(7, 7)], 1))
mapa.add_player(Player(("125.211.1.0",5166), 1, "#DDDFFF", "Kenny", Dot(3, 1), -1,
                       [Dot(2, 2), Dot(5, 2), Dot(7, 7)],
                       [Dot(1, 1), Dot(1, 2), Dot(5, 5)], 1))

# mapa.add_player(Player(5152, 4, "#FFFFFF", "Jon", [1,1], 1,
#                        [[1,4],[1,4],[1,4],[1,4]],
#                        [[1,4],[1,4],[1,4],[1,4]], 1))
# mapa.add_player(Player(5222, 1, "#DDDFFF", "Kenny",[4,4] , -1,
#                        [[1,4],[1,4],[1,4],[1,4]],
#                        [[1,4],[1,4],[1,4],[1,4]], 1))
print(mapa.to_json())

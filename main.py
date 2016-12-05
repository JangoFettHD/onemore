import random
import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QLineEdit, QApplication, QPushButton)
import socket
import time
import threading
import json


# compitable with server_version==4
class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):


        self.lbl = QLabel(self)
        tv_leaderboard = QLabel(self)
        textview_id = QLabel(self)
        qpb_up = QPushButton(self)
        qpb_right = QPushButton(self)
        qpb_down = QPushButton(self)
        qpb_left = QPushButton(self)

        textview_id.move(264, 554)
        tv_leaderboard.move(700, 40)
        qpb_up.move(250, 500)
        qpb_right.move(300, 550)
        qpb_down.move(250, 600)
        qpb_left.move(200, 550)
        self.lbl.move(60, 40)

        qpb_up.clicked.connect(self.move_up)
        qpb_down.clicked.connect(self.move_down)
        qpb_left.clicked.connect(self.move_left)
        qpb_right.clicked.connect(self.move_right)

        tv_leaderboard.setText("LOL")
        self.setGeometry(200, 100, 930, 670)
        self.setWindowTitle('OneMore')
        self.show()

        direction = 0

        # s = socket.socket(socket.AF_INET)
        # s.connect(("127.0.0.1", 6001))
        # s.send('getData'.encode())  # str->byte
        # print((s.recv(1024)).decode())  # byte->str

        def generate_nickname():
            d = {
                'part1': [
                    'Ae',
                    'Di',
                    'Mo',
                    'Ki',
                    'Ro',
                    'Fam',
                    'Mi',
                    'Jan'],
                'part2': [
                    'go',
                    'dar',
                    'kil',
                    'glar',
                    'tres', ],
            }
            return '{0}{1}'.format(d['part1'][int(random.uniform(0, len(d['part1'])))],
                                   d['part2'][int(random.uniform(0, len(d['part2'])))])

        nick = generate_nickname()
        print(nick)
        try:
            s.send(('reg ' + str(nick)).encode())
        except Exception:
            exit()
        time.sleep(1)


        def show_leaderboard(dict):
            str_lb=""
            leadboard=[]
            data=dict["data"]
            for p in data:
                leadboard.append([len(p["claimed_dots"]), p["nickname"]])
            # leadboard.sort(key=leadboard[0])
            print(leadboard)
            for i in range(len(leadboard)):

                str_lb+=str(leadboard[i][1])
                str_lb+=" | "+str(leadboard[i][0])+" | {0}% \n".format(((leadboard[i][0]*0.1)/dict["size_map"]*dict["size_map"]))

            return str_lb

        def dict_to_str(dict):
            free_space = '[_]'  # символ для обозначения пустоты
            claimed_space = ':{0}:'  # символ для обозначения пустоты
            temp_space = '[{0}]'  # символ для обозначения пустоты
            head_space = '({0})'  # символ для обозначения пустоты
            size_map = dict["size_map"]
            print(size_map)
            data = dict["data"]
            print(data)
            arrMap = [[free_space for _ in range(0, size_map)] for _ in range(0, size_map)]  # сама карта (1 layout)

            for p in data:
                p_id = p["id"]
                p_claimed_dots = p["claimed_dots"]
                for pos in p_claimed_dots:
                    arrMap[pos[0]][pos[1]] = claimed_space.format(p_id)
            for p in data:
                p_id = p["id"]
                p_position = p["position"]
                p_temp_dots = p["temp_dots"]
                for pos in p_temp_dots:
                    arrMap[pos[0]][pos[1]] = temp_space.format(p_id)
                arrMap[p_position[0]][p_position[1]] = head_space.format(p_id)

            str_arr = ""
            for i in range(size_map):
                for j in range(size_map):
                    str_arr += arrMap[i][j]
                str_arr += "\n"
            return str_arr





            # str_arr = ""
            # for i in range(size_map):
            #     for j in range(size_map):
            #         if [i, j] in [dict["players_positions"][i] for i in range(0, len(dict["players_positions"]))]:
            #             str_arr += ('(' + str(dict["map"][i][j]) + ')')
            #         else:
            #             if [i, j] in dict["all_dots"]:
            #                 str_arr += (':' + str(dict["map"][i][j]) + ':')
            #             else:
            #                 str_arr += ('[' + str(dict["map"][i][j]) + ']')
            #     str_arr += "\n"

        def send_command(command):
            # try:
            if command != "None":
                s.send(command.encode())
            print(command)
            in1 = (s.recv(500000)).decode().replace("\'", "\"")
            #print(in1, type(in1))
            json1_data = json.loads(in1)
            # print(dict_to_str(json1_data))
            str_map = dict_to_str(json1_data)
            print(str_map)
            self.onChanged(str_map)
            # print(dict_to_str(json1_data))
            time.sleep(0.1)
            s.send('getId'.encode())
            textview_id.setText((s.recv(10)).decode())
            tv_leaderboard.setText(show_leaderboard(json1_data))
            tv_leaderboard.adjustSize()
            # except Exception as e:
            #     print(e)
            #     exit()

        def show_map():
            while True:
                send_command("getData")
                time.sleep(0.2)

        threading.Thread(target=show_map).start()
        # while True:
        #     s.send(input("Enter \"move 1\"").encode())
        #     print((s.recv(1024)).decode())

    def move_up(self):
        s.send("move 1".encode())
        print("1")

    def move_down(self):
        s.send("move -1".encode())
        print("-1")

    def move_left(self):
        s.send("move 0".encode())
        print("0")

    def move_right(self):
        s.send("move 2".encode())
        print("2")

    def onChanged(self, text):
        # print("SFSFSSFSFSSF")

        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == '__main__':
    # s = socket.socket(socket.AF_INET)
    # s.connect(("127.0.0.1", 6001))

    # HOST = 'jangofetthd.me'  # The remote host
    HOST = '127.0.0.1'  # The remote host
    PORT = 1566  # The same port as used by the server
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

# direction = 0
#
# s = socket.socket(socket.AF_INET)
# s.connect(("127.0.0.1", 6001))
# s.send('show_map'.encode())  # str->byte
# print((s.recv(1024)).decode())  # byte->str
#
#
# def send_command(command):
#     s.send(command.encode())
#     ex.onChanged((s.recv(1024)).decode())
#
#
# def show_map():
#     while True:
#         send_command("show_map")
#         time.sleep(1)
#
#
# threading.Thread(target=show_map).start()
# while True:
#     s.send(input("Enter \"move 1\"").encode())
#     print((s.recv(1024)).decode())

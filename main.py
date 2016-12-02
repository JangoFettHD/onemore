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
        textview_id = QLabel(self)
        qpb_up = QPushButton(self)
        qpb_right = QPushButton(self)
        qpb_down = QPushButton(self)
        qpb_left = QPushButton(self)

        textview_id.move(264, 554)
        qpb_up.move(250, 500)
        qpb_right.move(300, 550)
        qpb_down.move(250, 600)
        qpb_left.move(200, 550)
        self.lbl.move(60, 40)

        qpb_up.clicked.connect(self.move_up)
        qpb_down.clicked.connect(self.move_down)
        qpb_left.clicked.connect(self.move_left)
        qpb_right.clicked.connect(self.move_right)

        self.setGeometry(200, 100, 530, 670)
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
            return '{0}{1}'.format(d['part1'][int(random.uniform(0,len(d['part1'])))],d['part2'][int(random.uniform(0,len(d['part2'])))])
        nick=generate_nickname()
        print(nick)
        try:s.send(('reg '+str(nick)).encode())
        except Exception: exit()
        time.sleep(1)
        def dict_to_str(dict):
            str_arr = ""
            for i in range(len(dict["map"])):
                for j in range(len(dict["map"])):
                    if [i, j] in [dict["players_positions"][i] for i in range(0, len(dict["players_positions"]))]:
                        str_arr += ('(' + str(dict["map"][i][j]) + ')')
                    else:
                        if [i, j] in dict["all_dots"]:
                            str_arr += (':' + str(dict["map"][i][j]) + ':')
                        else:
                            str_arr += ('[' + str(dict["map"][i][j]) + ']')
                str_arr += "\n"
            return str_arr

        def send_command(command):
            try:
                if command != "None":
                    s.send(command.encode())
                print(command)
                in1 = (s.recv(10000)).decode().replace("\'", "\"").split("}")[0] + "}"
                print(in1, type(in1))

                json1_data = json.loads(in1)
                self.onChanged(dict_to_str(json1_data))
                time.sleep(0.1)
                s.send('getId'.encode())

                textview_id.setText((s.recv(10)).decode())
            except Exception:
                exit()

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

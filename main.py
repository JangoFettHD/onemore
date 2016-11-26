import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QLineEdit, QApplication, QPushButton)
import socket
import time
import threading


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        qpb_up = QPushButton(self)
        qpb_right = QPushButton(self)
        qpb_down = QPushButton(self)
        qpb_left = QPushButton(self)

        qpb_up.move(60, 200)
        qpb_right.move(160, 250)
        qpb_down.move(60, 300)
        qpb_left.move(10, 250)
        self.lbl.move(60, 40)

        qpb_up.clicked.connect(self.move_up)
        qpb_down.clicked.connect(self.move_down)
        qpb_left.clicked.connect(self.move_left)
        qpb_right.clicked.connect(self.move_right)

        self.setGeometry(300, 300, 380, 370)
        self.setWindowTitle('OneMore')
        self.show()

        direction = 0

        #s = socket.socket(socket.AF_INET)
        # s.connect(("127.0.0.1", 6001))
        s.send('show_map'.encode())  # str->byte
        print((s.recv(1024)).decode())  # byte->str

        def send_command(command):
            s.send(command.encode())
            self.onChanged((s.recv(1024)).decode())

        def show_map():
            while True:
                send_command("show_map")
                time.sleep(1)

        threading.Thread(target=show_map).start()
        # while True:
        #     s.send(input("Enter \"move 1\"").encode())
        #     print((s.recv(1024)).decode())

    def move_up(self):
        s.send("move 1".encode())

    def move_down(self):
        s.send("move -1".encode())

    def move_left(self):
        s.send("move 0".encode())

    def move_right(self):
        s.send("move 2".encode())

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET)
    s.connect(("127.0.0.1", 6001))
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

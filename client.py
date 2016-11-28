import socket
import time
import threading

'''
0 (left)
-1 (back)
1 (up)
2 (right)
'''
direction = 0

s = socket.socket(socket.AF_INET)
s.connect(("127.0.0.1", 6001))
s.send('show_map'.encode())  # str->byte
print((s.recv(1024)).decode())  # byte->str


def send_command(command):
    s.send(command.encode())
    print((s.recv(1024)).decode())


def show_map():
    while True:
        send_command("show_map")
        time.sleep(1)


threading.Thread(target=show_map).start()
while True:
    s.send(input("Enter \"move 1\"").encode())
    print((s.recv(1024)).decode())



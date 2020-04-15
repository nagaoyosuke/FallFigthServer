#ローカル用


import logging
import psycopg2
import os
import json
import random

import socket
import threading

from bottle import route, run
from LobbyBase import LobbyBase

# from LobbyBase import LobbyBase

bind_ip = "127.0.0.1" #お使いのサーバーのホスト名を入れます
bind_port = 12345 #クライアントで設定したPORTと同じもの指定してあげます

Lobby = LobbyBase(16)


# thread processing a task from clients
def on_message(client_socket):
    while True:
        request = client_socket.recv(1024)
        # print data (max buffer size 1024) sent from client
        print ("Received: %s" % request)
        # send a message "Ack" to client
        # client_socket.send("Ack!, connecting..".encode('utf_8'))

        data = json.loads(request)

        print(data['state'])

        if data['state'] == 'Init':
            sendData = InitMessage(data)
        elif data['state'] == 'Battle':
            sendData = Lobby.Battle(client,server,data)
        elif data['state'] == 'Login':
            Lobby.Login(client,server,data)
        elif data['state'] == 'Matching':
            Lobby.MatchingRequest(client,server,data)
        elif data['state'] == 'MemberList':
            Lobby.LobbyMemberList(client,server,data)
        elif data['state'] == 'MyBattleReSet':
            Lobby.MyBattleReSet(client,server,data)
        elif data['state'] == 'OpenChat':
            Lobby.OpenChat(client,server,data)
        elif data['state'] == 'DirectChat':
            Lobby.DirectChat(client,server,data)    

    # client_socket.close()

@route('/')
def hello():
    print("hello")
    return ""

# Main
if __name__ == "__main__":
    # create socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind ip + port as a server 
    server.bind((bind_ip, bind_port))
    # listen with maximum 5 waiting queues
    server.listen(5)  ### server while loop
    print ("Listening on %s: %d" % (bind_ip, bind_port))
    while True:
        # event: a conncetion from client
        client, addr = server.accept()
        print ("Accepted connection from %s: %d" % (addr[0], addr[1]))
        #接続してきたやつの受信待機用に個別にスレッドを作成
        message = threading.Thread(target=on_message, args=(client,))
        message.start()
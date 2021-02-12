import socket
import select
from threading import *
import sys
import _thread
import random
import time


list_of_ans = ["hello", "world", "python"]
lives = 6
correct = 0
used = []
ans = random.choice(list_of_ans)
temp = []
for i in ans :
    if i not in temp :
        temp.append(i)
gotcha = len(temp)

    


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
server.listen(100)
list_of_clients = []
encoding = 'utf-8'


def clientthread(conn, addr):
    global lives, ans, used
    temp = []
    for i in used:
        temp.append(i)
    temp.append(lives)
    temp.append(ans)
    conn.send(str.encode("Welcome to Hangman game!!"))
    time.sleep(1)
    # temp = [lives, ans]
    conn.send(str.encode(str(temp)))
    time.sleep(1)
    # sends a message to the client whose user object is conn
    while True:
        try:
            message = conn.recv(2048)
            print(addr[0], "send:", str(message, encoding))
            if "exit" not in str(message, encoding):
                # conn.send(str.encode("ack"))
                # print("<", addr[0], "> ", message)
                # message_to_send = "<" + str(addr[0]) + "> " + message
                broadcast(str(message, encoding), conn, addr[0])
                # prints the message and address of the user who just sent the message on the server terminal
                play(str(message, encoding))
            else:
                # print(1)
                remove(conn, addr[0])
        except:
            continue


def broadcast(message, connection, sender):
    for clients in list_of_clients:
        # print(connection == clients)
        if clients != connection:
            try:
                # print(connection)
                clients.send(str.encode(str(sender + " >>> choose: " + message.replace("\n", ""))))
                # clients.send(str.encode(str(" >>> choose: " + message)))
                # clients.send(str.encode(str(message)))
            except:
                clients.close()
                # remove(clients)


def remove(connection, ip):
    connection.close()
    if connection in list_of_clients:
        print(ip, "disconnected")
        list_of_clients.remove(connection)


def play(letter):
    # print("letter:", letter)
    global correct, lives, ans
    letter = letter.replace("\n", "")
    if letter not in used:
        used.append(letter)
        temp = []
        for i in used:
            temp.append(i)
        if letter in ans :
            correct+=1
        else:
            lives-=1
        for client in list_of_clients:
            temp.append(lives)
            temp.append(ans)
            # client.send(str.encode(str(lives)))
            client.send(str.encode(str(temp)))


def playHangman(num1, num2):
    # hangman = Hangman()
    global lives, used, correct, ans, gotcha
    while True:
        # print("lives:", lives, "   correct:", correct, "   ans:", ans, "   gotcha:", gotcha)    # debug line
        if lives == 0 or correct == gotcha:
            time.sleep(5)
            for client in list_of_clients:
                client.send(str.encode(str("Start new game")))
            # del hangman
            lives = 6
            correct = 0
            used = []
            ans = random.choice(list_of_ans)
            temp = []
            for i in ans :
                if i not in temp :
                    temp.append(i)
            gotcha = len(temp)
            for client in list_of_clients:
            #     client.send(str.encode(str("Start new game")))
                # temp = [lives, ans]
                client.send(str.encode(str([lives, ans])))


# hangman = Hangman()
_thread.start_new_thread(playHangman, (1, 2))
while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    _thread.start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
import socket
import time
from _thread import *
import _pickle as pickle
import pygame
from player import Player





server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # IPv4, TCP protocol
server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # avoid bind exception

PORT = 12345

WIDTH, HEIGHT = 600, 500

SERVER_IP = socket.gethostbyname(socket.gethostname())

try:
    server_s.bind((SERVER_IP, PORT))    # associate socket with IP and PORT
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

server_s.listen()   # started listen for connection from clients
print(f"Server has started on IP: {SERVER_IP}")

# dynamic variables
players = []
connections = 0
id = 0
start = False



STARTING_POSITIONS = [(40, 100), (40, 150), (80, 100), (80, 150)]
def get_starting_positions():
    i = 0
    for player in players:
        player.x = STARTING_POSITIONS[i][0]
        player.y = STARTING_POSITIONS[i][1]
        i += 1

def threaded_client(conn, _id):
    global connections, players

    opponents = []

    current_id = _id
    # receive a name from client
    data = conn.recv(16)
    name = data.decode("utf-8")
    print(f"{name} was connected!")

    # setup properties for each player
    x, y = STARTING_POSITIONS[current_id]
    players.append(Player(4, 4, x, y, current_id, name))

    conn.send(str.encode(str(current_id)))  # send ID and wait

    while True:
        try:
            data = conn.recv(1000)
            if not data:    # if receives empty bytes object, then client disconnected
                print("RECEIVED empty bytes => DISCONNECTING")
                break

            data = data.decode("utf-8")

            if data.split(" ")[0] == "move":
                #print("POSITION changed")
                splited_data = data.split(" ")
                new_x = int(splited_data[1])
                new_y = int(splited_data[2])
                new_angle = int(splited_data[3])

                players[current_id].x = new_x
                players[current_id].y = new_y
                players[current_id].angle = new_angle

                send_data = pickle.dumps(players)
                conn.send(send_data)


            elif data.split(" ")[0] == "id":
                print("Sending ID of player")
                send_data = str.encode(str(current_id))
                conn.send(send_data)

            else:
                #print(f"ELSE - Sending list of players = len(players): {str(len(players))}")
                send_data = pickle.dumps(players)
                conn.send(send_data)

        except Exception as e:
            print(e)
            break
        time.sleep(0.001)

    print(f"DISCONNECTED: {name}")
    connections -= 1
    players.remove(players[current_id])



# MAIN LOOP
print("Setting up everything")

while True:
    host, addr = server_s.accept()      # here the code waits for connection
                                        # host =  obtained client socket
                                        # addr = IP address of client
    print(f"Connected to server: {addr}")

    if addr[0] == SERVER_IP and not(start):
        start = True
        print("Game started")
    connections += 1
    start_new_thread(threaded_client,(host, id))
    id += 1
    # create a thread for new client and wait for another connection

print("SERVER is offline")

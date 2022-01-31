import socket
import _pickle as pickle


class Client:   # send, receive info from server
    def __init__(self):
        self.client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
        self.host = "192.168.31.120"     # server IP address
        self.port = 12345                # server PORT
        self.addr = (self.host, self.port) # socket

    def connect(self, name):
        self.client_s.connect(self.addr)          # connect to socket
        self.client_s.send(str.encode(name))
        id_value = self.client_s.recv(8)          # response of server, assigns client ID
        return int(id_value.decode())             # return ID value (int)

    def disconnect(self):
        self.client_s.close()

    def send(self, data, pick=False):   # serialization of object data
        try:
            if pick:
                self.client_s.send(pickle.dumps(data))
            else:
                self.client_s.send(str.encode(data))
            reply = self.client_s.recv(2048*4)
            try:
                reply = pickle.loads(reply)
            except Exception as e:
                print(e)

            return reply
        except socket.error as e:
            print(e)
import socket
import sys
import threading
import subprocess
import re

class Server:
    def __init__(self):
        #Bind the socket to talk with the client
        s = socket.socket()
        s.bind((socket.gethostname(), 5000))
        self.__s = s
        print("Ecoute sur {}:{}".format(socket.gethostname(), 5000))

        #Regex for client messages
        t1 = r"^[a-zA-Z0-9]+$"
        t2 = r"^/[a-zA-Z]+$"
        self.__user_pattern = re.compile(t1)
        self.__command_pattern = re.compile(t2)
        self.__clients = {}

        self.__handlers = {"/clients": self._clients,
                           "/quit": self._quit}

    def run(self):
        self.__s.listen()
        self.__running = True
        while self.__running:
            self._listening()

    def _listening(self):
        """Listenning if the client sends a message"""
        while self.__running:
            client, addr = self.__s.accept()

            try:
                data = self._receive(client).decode()
                #Pseudo message
                if self.__user_pattern.match(data):
                    self.__clients[data] = addr
                    print(self.__clients)
                    sys.stdout.flush()
                #Command message
                elif self.__command_pattern.match(data):
                    if data in self.__handlers:
                        self.__handlers[data](addr)
                    else:
                        self._send(addr, "Commande inconnue")
                client.close()

            except OSError as e:
                print(e)
                print('Erreur de reception')

    def _send(self, addr, dt):
        """Sends a answer to the client"""
        cl = socket.socket()
        cl.connect((addr[0], 5001))

        message = "server " + dt
        data = message.encode()
        totalsent = 0
        while totalsent < len(data):
            sent = cl.send(data[totalsent:])
            totalsent += sent
        cl.close()

    def _receive(self, client):
        """Reception loop"""
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)

    def _clients(self, addr):
        """Sends a list of contacts"""
        client_list = ""
        for i in self.__clients:
            client_list += i + "-" + self.__clients[i][0] + "\n"
        if len(self.__clients) != 0:
            self._send(addr, client_list)
        else:
            self._send(addr, "None")

    def _quit(self, addr):
        pseudo = ""
        for i in self.__clients:
            if self.__clients[i][0] == addr[0]:
                pseudo += i
        self._send(addr, "Deconnexion")
        del self.__clients[pseudo]

class Client:
    def __init__(self):
        #Bind socket and regex for server answer
        se = socket.socket()
        se.bind((socket.gethostname(), 5001))
        self.__se = se

        t1 = r"^server\s(?P<answer>[a-zA-Z0-9\s.-]+)$"
        self.__serverans = re.compile(t1)

        #Bind socket and regex for peer-to-peer communicatie

    def run(self):
        self.__se.listen()
        data = self.who().encode()
        self._sendserv(data)

        self.__running = True
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            command = line[:line.index(' ')]
            dt = command.encode()
            if command == "/clients" or command == "/quit":
                self._sendserv(dt)
            self._listeningserv()

    def _sendserv(self, data):
        """Send commands to the server """
        self.__s = socket.socket()
        self.__s.connect((socket.gethostname(), 5000))

        totalsent = 0
        while totalsent < len(data):
            sent = self.__s.send(data[totalsent:])
            totalsent += sent
        self.__s.close()

    def _listeningserv(self):
        """Listening to server answer"""
        server, addr = self.__se.accept()
        try:
            data = self._receive(server).decode()
            if self.__serverans.match(data):
                m = self.__serverans.match(data)
                print("[Server] ", m.group("answer"))
            server.close()

        except OSError as e:
            print(e)
            print('Erreur de reception')

    def who(self):
        """Say who I am"""
        proc = subprocess.Popen(['Whoami'], stdout=subprocess.PIPE,
                                universal_newlines=True)

        out, err = proc.communicate()

        if "\\" in str(out):
            spl = out.split("\\")
            user = spl[0]

        return str(user)

    def _receive(self, client):
        """Reception loop"""
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)

if __name__ == '__main__':
    if sys.argv[1] == 'server':
        Server().run()
    elif sys.argv[1] == 'client':
        Client().run()
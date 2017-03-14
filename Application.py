import socket
import sys
import threading
import subprocess
import re

class Server:
    def __init__(self):
        s = socket.socket()
        s.bind((socket.gethostname(), 5000))
        self.__s = s
        print("Ecoute sur {}:{}".format(socket.gethostname(), 5000))

        t1 = r"^[a-zA-Z0-9]+$"
        t2 = r"/[a-zA-Z]+"
        self.__user_pattern = re.compile(t1)
        self.__command_pattern = re.compile(t2)
        self.__clients = {}

        self.__handlers = {"/clients": self._clients
                    }

    def run(self):
        self.__s.listen()
        self.__running = True
        while self.__running:
            self._listening()

    def _listening(self):
        while self.__running:
            client, addr = self.__s.accept()

            try:
                data = self._receive(client).decode()

                if self.__user_pattern.match(data):
                    self.__clients[data] = addr
                    print(self.__clients)
                    sys.stdout.flush()

                elif self.__command_pattern.match(data):
                    if data in self.__handlers:
                        self.__handlers[data](addr)

                client.close()

            except OSError:
                print('Erreur de reception')

    def _send(self, addr, data):
        cl = socket.socket()
        cl.connect(addr)

        totalsent = 0
        while totalsent < len(data):
            sent = cl.send(data[totalsent:])
            totalsent += sent
        cl.close()

    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)

    def _clients(self, addr):
        self._send(addr, self.__clients)

class Client:
    def __init__(self):
        self.__s = socket.socket()

    def run(self):
        data = self.who().encode()
        self._sendserv(data)

        self.__running = True
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            command = line[:line.index(' ')]
            dt = command.encode()
            self._sendserv(dt)

    def _sendserv(self, data):
        self.__s = socket.socket()
        self.__s.connect((socket.gethostname(), 5000))
        totalsent = 0
        while totalsent < len(data):
            sent = self.__s.send(data[totalsent:])
            totalsent += sent
        self.__s.close()

    def who(self):
        proc = subprocess.Popen(['Whoami'], stdout=subprocess.PIPE,
                                universal_newlines=True)

        out, err = proc.communicate()

        if "\\" in str(out):
            spl = out.split("\\")
            user = spl[0]

        return str(user)

if __name__ == '__main__':
    if sys.argv[1] == 'server':
        Server().run()
    elif sys.argv[1] == 'client':
        Client().run()
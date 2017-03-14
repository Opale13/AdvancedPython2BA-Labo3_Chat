import socket
import sys
import threading
import subprocess

class Serveur:
    def __init__(self):
        s = socket.socket()
        s.bind((socket.gethostname(), 5000))
        self.__s = s
        print("Ecoute sur {}:{}".format(socket.gethostname(),
                                        5000))
        self.__clients = {}

    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                self.__clients[self._receive(client).decode()] = addr
                print(self.__clients)
            except OSError:
                print('Erreur de reception')

    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)


class Client:
    def __init__(self):
        s = socket.socket()
        self.__s = s

    def run(self):
        self.__s.connect((socket.gethostname(), 5000))
        data = self.who().encode()

        totalsent = 0
        while totalsent < len(data):
            sent = self.__s.send(data[totalsent:])
            totalsent += sent

    def who(self):
        proc = subprocess.Popen(['Whoami'], stdout=subprocess.PIPE,
                                universal_newlines=True)

        out, err = proc.communicate()

        if "\\" in str(out):
            spl = out.split("\\")
            user = spl[0]

        return str(user)

if __name__ == '__main__':
    if sys.argv[1] == 'serveur':
        Serveur().run()
    elif sys.argv[1] == 'client':
        Client().run()
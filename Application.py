import socket
import sys
import threading
import subprocess



class Serveur:
    def __init__(self):
        s = socket.socket()
        s.bind((socket.gethostname(), 5000))
        self.__s = s
        print("Ecoute sur {}:{}".format(socket.gethostname(), 5000))
        self.__clients = {}

    def run(self):
        self.__s.listen()
        self.__running = True
        threading.Thread(target=self._addclient).start()

    def _listening(self):
        while self.__running:
            try:
                data, address = self.__s.recv(1024)
                dt = data.decode()
                print(dt)
                sys.stdout.flush()
            except socket.timeout:
                pass
            except OSError:
                return

    def _addclient(self):
        while self.__running:
            client, addr = self.__s.accept()

            try:
                user = self._receive(client).decode()

                if "/" not in user:
                    self.__clients[user] = addr
                    print(self.__clients)
                    sys.stdout.flush()
                client.close()

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
        s.settimeout(0.5)
        self.__s = s

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
    if sys.argv[1] == 'serveur':
        Serveur().run()
    elif sys.argv[1] == 'client':
        Client().run()
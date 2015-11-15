import socket
import md5sum
from threading import Thread

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print(" New thread started for "+ip+":"+str(port))

    def run(self):
        protocol = self.sock.recv(BUFFER_SIZE)
        if protocol.decode('ascii') == 'MD5SUM_COMPARE':
            self.createMD5SUM()
            self.recFile(name='MD5Client\\MD5SUM'+str(port)+'.txt')
            listDiff = md5sum.compareFileDifference('MD5SUM.txt','MD5Client\\MD5SUM'+str(port)+'.txt')
            for (file, status) in listDiff:
                if status == 'MISMATCH':
                    self.sendFile(file)
    def sendFile(self, filename):
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                self.sock.send('END_FILE_TRANSFER'.encode('ascii'))
                f.close()
                break
            
    def createMD5SUM(self):
        x = md5sum.grab_files('Data\\')
        lista = []
        for i in x:
            y = md5sum.md5(i)
            lista.append((i,y))
        md5sum.createFile(lista)
            
    def recFile(self, name):
        """
        Recieve single file from client
        """
        
        with open(name, 'wb') as f:
            while True:
                print('receiving data...')
                data = self.sock.recv(BUFFER_SIZE)
                if data.decode('ascii') == 'END_FILE_TRANSFER':
                    break
                f.write(data)
        f.close()
        
        
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

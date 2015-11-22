import socket
import md5sum
import time
from threading import Thread
import os
import shutil

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
            print(listDiff)
            for (file, status) in listDiff:
                if status == 'MISMATCH' or status == 'MISSING':
                    self.sock.send(file.encode('ascii'))
                    self.sendFile(file)
            self.sock.send('FILES_MATCH'.encode('ascii'))
        if protocol.decode('ascii') == 'FILE_UPLOAD':
            name = self.sock.recv(BUFFER_SIZE)
            self.recFile(name.decode('ascii'))
            self.createMD5SUM()
        if protocol.decode('ascii') == 'FILE_DELETE':
            name = self.sock.recv(BUFFER_SIZE)
            try:
                os.remove(name.decode('ascii'))
            except:
                shutil.rmtree(name.decode('ascii'))
            self.createMD5SUM()
            
    def sendFile(self, filename):
        file = open(filename,'rb')
        while True:
            data = file.read(BUFFER_SIZE)
            while data:
                self.sock.send(data)
                print('Sent ',filename)
                data = file.read(BUFFER_SIZE)
            if not data:
                time.sleep(0.1)
                self.sock.send('END_FILE_TRANSFER'.encode('ascii'))
                file.close()
                break
            
    def createMD5SUM(self):
        x = md5sum.grab_files('Data\\')
        print(x)
        lista = []
        for i in x:
            y = md5sum.md5(i)
            lista.append((i,y))
        md5sum.createFile(lista)
            
    def recFile(self, name):
        """
        Recieve single file from client
        """
        try:
            with open(name, 'wb') as f:
                while True:
                    data = sock.recv(BUFFER_SIZE)
                    print('data=%s', (data.decode('ascii')))
                    if data.decode('ascii') == 'END_FILE_TRANSFER':
                        f.close()
                        print('file close()')
                        break
                    f.write(data)
        except FileNotFoundError:
            os.chdir(FILE_PATH)
            name = name.split('\\')
            filepath = name[:-1]
            filepath = filepath[1:]
            for path in filepath:
                try:
                    os.mkdir(path)
                except FileExistsError:
                    pass
                os.chdir(path)
            with open(name[-1], 'wb') as f:
                while True:
                    data = sock.recv(BUFFER_SIZE)
                    print('data=%s', (data.decode('ascii')))
                    if data.decode('ascii') == 'END_FILE_TRANSFER':
                        f.close()
                        print('file close()')
                        break
                    f.write(data)
        
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    (conn, (ip,port)) = tcpsock.accept()
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

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
        if protocol == 'MD5SUM_FILE':
            self.createMD5SUM(self)
            self.recMD5SUM(self)
            
    def sendFile(filename='Data\\Text.txt'):
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                break
            
    def createMD5SUM(self):
        x = md5sum.grab_files('.')
        lista = []
        for i in x:
            y = md5sum.md5(i[1])
        lista.append((i[0],y))
        md5sum.createFile(lista)
        
    def md5Compare(self):
        """
        TODO: Not final, needs to find file difference
        """
        clientMD5 = open('MD5SUM'+str(port)+'.txt')
        while True:
            data = self.sock.recv(BUFFER_SIZE)
            if not data:
                clientMD5.close()
                break
            clientMD5.write(data)
        clientHash = md5sum.md5('MD5SUM'+str(port)+'.txt')
        serverHash = md5sum.md5('MD5SUM.txt')
        result = md5sum.compareMD5(clientHash, serverHash)
        if result:
            self.sock.send('Files Match'.encode('ascii'))
        else:
            self.sock.send('Files does not Match'.encode('ascii'))              
    
    def recMD5SUM(self):
        """
        Recieve MD5SUM.txt from client
        """
        pass
    
        
        
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

import socket
import md5sum
import time
import os

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024
FILE_PATH = 'Data\\'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
def createMD5SUM():
    x = md5sum.grab_files(FILE_PATH)
    lista = []
    for i in x:
        y = md5sum.md5(i)
        lista.append((i,y))
    md5sum.createFile(lista)
    
def sendMD5SUM():
    sock.send('MD5SUM_COMPARE'.encode('ascii'))
    file = open('MD5SUM.txt', 'rb')
    time.sleep(0.1)
    while True:
        data = file.read(BUFFER_SIZE)
        while data:
            sock.sendall(data)
            data = file.read(BUFFER_SIZE)
        if not data:
            time.sleep(0.1)
            sock.send('END_FILE_TRANSFER'.encode('ascii'))
            file.close()
            break
    
def recFile(name):
    """
    Recieve and create file, if directory not found then create
    directory 
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

def sendFile(filename):
    sock.send('FILE_UPLOAD'.encode('ascii'))
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

def delFile(filename):
    sock.send('FILE_DELETE'.encode('ascii'))
    sock.send(filename.encode('ascii'))

def closeConnection():
    sock.close()
    print('connection closed')

createMD5SUM()
sendMD5SUM()
name = sock.recv(BUFFER_SIZE)
if name.decode('ascii') == 'FILES_MATCH':
    closeConnection()
else:
    recFile(name.decode('ascii'))


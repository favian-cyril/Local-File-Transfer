import socket
import md5sum
import time

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
    with open(name, 'wb') as f:
        print('file opened')
        while True:
            #print('receiving data...')
            data = sock.recv(BUFFER_SIZE)
            print('data=%s', (data))
            if data.decode('ascii') == 'END_FILE_TRANSFER':
                f.close()
                print('file close()')
                break
            # write data to a file
            f.write(data)
def closeConnection():
    sock.close()
    print('connection closed')

createMD5SUM()
sendMD5SUM()
name = sock.recv(BUFFER_SIZE)
recFile(name.decode('ascii'))

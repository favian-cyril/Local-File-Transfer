import socket
import md5sum

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024
FILE_PATH = 'Data\\'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
def createMD5SUM():
    x = md5sum.grab_files('.')
    lista = []
    for i in x:
        y = md5sum.md5(i[1])
    lista.append((i[0],y))
    md5sum.createFile(lista)
    
def sendMD5SUM(md5):
    sock.send('MD5SUM_FILE'encode('ascii'))
    file = open(md5)
    while True:
        data = file.read(BUFFER_SIZE)
        while data:
            sock.send(data)
            data = file.read(BUFFER_SIZE)
        if not data:
            file.close()
            break
    
def recieveFile(name):
    with open(FILE_PATH+name, 'wb') as f:
        print('file opened')
        while True:
            #print('receiving data...')
            data = sock.recv(BUFFER_SIZE)
            print('data=%s', (data))
            if not data:
                f.close()
                print('file close()')
                break
            # write data to a file
            f.write(data)
def closeConnection():
    print('Successfully get the file')
    sock.close()
    print('connection closed')

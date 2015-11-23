import socket, md5sum, time, os, sys, argparse, shutil
from threading import Timer

#Global variables
global TCP_IP, TCP_PORT, FILE_PATH, LATEST_UPDATE
TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 4096
FILE_PATH = 'Data\\'
LATEST_UPDATE = 'No new updates'

def setInit(args):
    """
    Initialise when arguments are parsed
    """
    TCP_IP = args.ip
    TCP_PORT = args.port
    FILE_PATH = args.file

def connect():
    """
    connect to socket
    """
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((TCP_IP, TCP_PORT))
    except ConnectionRefusedError:
        print('Cant connect to server')
        sys.exit()

def run():
    """
    Controls the interval between calling updateLocalFiles() and
    checkWithServer()
    """
    print("Server ip: {}\nPort: {}\nPath: {}".format(TCP_IP,TCP_PORT,FILE_PATH))
    if not os.access(FILE_PATH, os.F_OK):
        os.mkdir(FILE_PATH)
    print('Syncing with server...')
    date = sock.recv(BUFFER_SIZE)
    print('Server time is {}'.format(date.decode('ascii')))
    checkWithServer()
    print('Client Up-to-date')
    sync()

def sync():
    global threadsync
    if not updateLocalFiles():
        checkWithServer()
    threadsync = Timer(6, sync)
    threadsync.start()

def stopSync():
    threadsync.cancel()

def updateLocalFiles():
    """
    Checks if there is a change (update or delete) in the client
    file using compareLocalMD5() from md5sum
    """
    global LATEST_UPDATE
    change = False
    result = md5sum.compareLocalMD5(FILE_PATH)
    for (file,status) in result:
        if status == 'UPDATE' or status == 'UPLOAD':
            sendFile(file)
            change = True
            LATEST_UPDATE = file + ' ' +status
            print(LATEST_UPDATE)
            print('Changes Sent')
        elif status == 'DELETE':
            delFile(file)
            change = True
            LATEST_UPDATE = file + ' ' +status
            print('Changes Sent')
        elif status == 'MATCH':
            pass
    createMD5SUM()
    return change
def checkWithServer():
    """
    send current md5sum to server to compare with server files.
    new files are downloaded. When initialising with server, any
    extra files are deleted.
    """
    global LATEST_UPDATE
    createMD5SUM()
    sendMD5SUM()
    prot = sock.recv(BUFFER_SIZE)
    while True:
        if prot == b'MISSINGCLIENT':
            time.sleep(0.1)
            name = sock.recv(BUFFER_SIZE)
            if name.decode('ascii') == 'FILES_MATCH':
                break
            time.sleep(0.1)
            recFile(name.decode('ascii'))
            LATEST_UPDATE = name.decode('ascii') + ' Downloaded'
            createMD5SUM()
            print('New Files downloaded')
        elif prot == b'MISSINGSERVER':
            name = sock.recv(BUFFER_SIZE)
            if name.decode('ascii') == 'FILES_MATCH':
                break
            try:
                os.remove(name.decode('ascii'))
            except:
                shutil.rmtree(name.decode('ascii'))
            LATEST_UPDATE = name.decode('ascii') + ' Removed'
            print('Extra file removed')
        elif prot.decode('ascii') == 'FILES_MATCH':
            break

def lastUpdate():
    return LATEST_UPDATE

def createMD5SUM():
    """
    Create md5sum.txt from file path
    """
    x = md5sum.grab_files(FILE_PATH)
    lista = []
    for i in x:
        y = md5sum.md5(i)
        lista.append((i,y))
    md5sum.createFile(lista)
    
def sendMD5SUM():
    """
    Send md5sum to server to compare
    """
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
                if data == b'END_FILE_TRANSFER':
                    f.close()
                    break
                f.write(data)
    except FileNotFoundError:
        current = os.getcwd()
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
                if data == b'END_FILE_TRANSFER':
                    f.close()
                    break
                f.write(data)
        os.chdir(current)

def sendFile(filename):
    """
    Open file and send the data in bytes to current socket
    """
    sock.send('FILE_UPLOAD'.encode('ascii'))
    time.sleep(0.1)
    sock.send(filename.encode('ascii'))
    file = open(filename,'rb')
    while True:
        data = file.read(BUFFER_SIZE)
        while data:
            sock.send(data)
            data = file.read(BUFFER_SIZE)
        if not data:
            time.sleep(0.1)
            print('Sent ',filename)
            sock.send('END_FILE_TRANSFER'.encode('ascii'))
            file.close()
            break

def delFile(filename):
    """
    Request the server to delete file
    """
    sock.send('FILE_DELETE'.encode('ascii'))
    sock.send(filename.encode('ascii'))

def closeConnection():
    stopSync()
    sock.close()
    print('connection closed')

#Constructor function
def setPath(path):
    global FILE_PATH
    FILE_PATH = path

def setIP(ip):
    global TCP_IP
    TCP_IP = ip

def setPort(port):
    global TCP_PORT
    TCP_PORT = port
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Set the folder to sync', default=FILE_PATH)
    parser.add_argument('-i', '--ip', help='Set IP of sync server', default=TCP_IP)
    parser.add_argument('-p', '--port', help='Set Port of server', default=TCP_PORT)
    
    args = parser.parse_args()
    setInit(args)
    connect()
    run()

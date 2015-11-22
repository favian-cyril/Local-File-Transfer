from client import *

createMD5SUM()
sendMD5SUM()
name = sock.recv(BUFFER_SIZE) #NOTE: must infinite loop until all the name is finished 
recFile(name.decode('ascii'))

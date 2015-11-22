# Local-File-Transfer 

Basis for file transfer & multithreading server:
http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php

More info on threading & socket: 

https://docs.python.org/3/library/threading.html 

https://docs.python.org/3/library/socket.html

TODO:
- Basic GUI for client VELTA

- Create thread for server to handle input while handling client NOTE:not priority
- main.py to connect gui and modules. also to automatically do the file checking with server

DONE:
- Implement protocol for client-server interaction(file upload, file deletion)
- send MD5SUM.txt
- Implement MD5SUM check to find file difference
- - Create module to check file and simultaneously compare to current MD5SUM.txt and return the update such as insertion or deletion. If there is a change then create new MD5SUM.txt 

NOTE: Basic operation for main.py can be found in client.py and server.py

# Local-File-Transfer 

Basis for file transfer & multithreading server:
http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php

More info on threading & socket: 

https://docs.python.org/3/library/threading.html 

https://docs.python.org/3/library/socket.html

DONE:
- Implement protocol for client-server interaction(file upload, file deletion)
- send MD5SUM.txt
- Client GUI
- Implement MD5SUM check to find file difference
- Create module to check file and simultaneously compare to current MD5SUM.txt and return the update such as insertion or deletion. If there is a change then create new MD5SUM.txt 
- main.py to connect gui and modules. also to automatically do the file checking with server

PROTOCOL NOTES:
- MD5SUM_COMPARE : get file difference from server
- MISSINGCLIENT : file missing in client -> download new file
- MISSINGSERVER : file missing in server -> delete in client
- FILES_MATCH : end of file compare
- FILE_UPLOAD : new file from client
- FILE_DELETE : client deletes file
- END_FILE_TRANSFER : end of file data -> so that file can be closed

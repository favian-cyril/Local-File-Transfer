# Local-File-Transfer 

Basis for file transfer & multithreading server:
http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php

More info on threading & socket: 

https://docs.python.org/3/library/threading.html 

https://docs.python.org/3/library/socket.html

TODO:
- Implement protocol for client-server interaction(file upload, file deletion)
- Basic GUI for client
- Create module to check file and simultaneously compare to current MD5SUM.txt and return the update such as insertion or deletion. If there is a change then create new MD5SUM.txt
- Create thread for server to handle input while handling client
- BUG: compareFileDifference() in md5sum.py cannot handle filename with space because of split function

DONE:
- send MD5SUM.txt
- Implement MD5SUM check to find file difference

Protocol Note:
- send and compare MD5SUM = MD5SUM_COMPARE
- end of file transfer = END_FILE_TRANSFER

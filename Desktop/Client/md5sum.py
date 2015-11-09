import hashlib
import os

def md5(fname):
    """
    Creates a md5sum hash from filepath to be used for checksum
    """
    hashmd5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashmd5.update(chunk)
    return hashmd5.hexdigest()

def compareMD5(file1, file2):
    """
    Compares between 2 MD5SUM hash to compare between file
    """
    if file1 == file2:
        return True
    else:
        return False

def grab_files(directory):
    """
    Traverses from the top directory and returns a list containing the file
    name and file path
    """
    arrPath = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            filedir = os.path.join(os.getcwd(),root,name)          
            arrPath.append((name,filedir))
    return arrPath

def createFile(arrPath,name='MD5SUM.txt'):
    """
    Create file containing name and md5sum value
    """
    filetext = open(name, mode='w+')
    for name, filedir in arrPath:
        print(name, filedir, file=filetext)
    print("File MD5SUM Created")

##x = grab_files('.')
##lista = []
##for i in x:
##    y = md5(i[1])
##    lista.append((i[0],y))
##createFile(lista)

    

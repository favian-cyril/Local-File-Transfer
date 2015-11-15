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
            filedir = os.path.join(root,name)          
            arrPath.append((filedir))
    return arrPath

def createFile(arrPath,name='MD5SUM.txt'):
    """
    Create file containing name and md5sum value
    """
    filetext = open(name, mode='w+')
    for name, filedir in arrPath:
        print(name, filedir, file=filetext)
    print("File MD5SUM Created")
def compareFileDifference(checksum1 = None, checksum2 = None):
    """
    TODO: Compare actual file difference and
    return a list with status of file
    """
    # Open Files
    fileMD = open(checksum1, "r").read()
    fileMDOutput = open(checksum2, "r").read()
    # Split 'em and put 'em as dicks
    listMD = fileMD.split()
    listMDOutput = fileMDOutput.split()
    dictMD = dict(zip(*[iter(listMD)]*2))
    dictMDOutput = dict(zip(*[iter(listMDOutput)]*2))
    # Determine which have the same key and same md5 value
    result = []
    for key in dictMD:
        if key in dictMDOutput:
            if dictMD[key] == dictMDOutput[key]: 
                result.append((key, "MATCH"))
            elif dictMD[key] != dictMDOutput[key]:
                result.append((key, "MISMATCH"))
        if key not in dictMDOutput:
            result.append((key, "MISSING"))
    for key in dictMDOutput:
        if key not in dictMD:
            result.append((key, "MISSING"))
    return result


##x = grab_files('Data//')
##lista = []
##for i in x:
##    y = md5(i)
##    lista.append((i,y))
##createFile(lista)

    

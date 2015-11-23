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

def compareLocalMD5(path = None, checksum1 = 'MD5SUM.txt'):
    """
    Compares local file with latest MD5SUM. Input must be in the form of string
    ex: .\thisFolder
    """
    # Creates the md5 of local content
    files_in_dir = grab_files(path)
    local_list = [] # List of filenames and its md5 value
    for i in files_in_dir:
        y = md5(i)
        local_list.append((i,y))
    local_dict = dict(local_list) # Change it to a dictionary

    # Open the previously created MD5SUM
    fileMD = open(checksum1, "r").read()
    listMD = fileMD.split("\n")
    temp =[]
    for i in listMD:
        temp.append(i[:-33])
        temp.append(i[-32:])
    listMD = temp
    dictMD = dict(zip(*[iter(listMD)]*2))
    try:
        dictMD.pop("",None)
    except:
        pass
    
    
    # Determine which files are missing/created anew
    result = []
    for key in dictMD:
        if key in local_dict:
            if dictMD[key] == local_dict[key]: 
                result.append((key, "MATCH"))
            elif dictMD[key] != local_dict[key]:
                result.append((key, "UPDATE"))
        if key not in local_dict:
            result.append((key, "DELETE"))
    for key in local_dict:
        if key not in dictMD:
            result.append((key, "UPLOAD"))
    return result
    
    
def compareFileDifference(checksum1 = None, checksum2 = None):
    """
    Compare actual file difference and
    return a list with status of file
    """
    # Open Files
    fileMD = open(checksum1, "r").read()
    fileMDOutput = open(checksum2, "r").read()
    # Split 'em and put 'em as dicks
    listMD = fileMD.split("\n")
    listMDOutput = fileMDOutput.split("\n")

    temp =[]
    for i in listMD:
        temp.append(i[:-33])
        temp.append(i[-32:])
    listMD = temp
    temp =[]
    for i in listMDOutput:
        temp.append(i[:-33])
        temp.append(i[-32:])
    listMDOutput = temp

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
            result.append((key, "MISSINGCLIENT"))
    for key in dictMDOutput:
        if key not in dictMD:
            result.append((key, "MISSINGSERVER"))
    return result



##    x = md5sum.grab_files(FILE_PATH)
##    lista = []
##    for i in x:
##        y = md5sum.md5(i)
##        lista.append((i,y))
##    md5sum.createFile(lista)



    

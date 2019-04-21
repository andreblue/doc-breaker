import msoffcrypto
import sys, getopt
import os
import urllib.request

def download_PasswordList():
    #Grabbed from https://github.com/danielmiessler/SecLists
    url = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt'
    try:
        urllib.request.urlretrieve(url, "10000-password-top-list.txt")
    except Exception as e:
        handleException(e)
        sys.exit()
    

def handleException(e):
    print ('Error: ' + str(e))

def breakFile(fileHandle, passwordStr):
    try:
        fileHandle.load_key(password=passwordStr)
    except Exception as e:
        if str(e) != 'Key verification failed':
            handleException(e)
    else:
        print ('Password FOUND!')
        print ('Saving document as decrypted_file.docx next to main script')
        print ('Password was: "' + passwordStr + '"')
        fileHandle.decrypt(open('decrypted_file.docx', "wb"))
        sys.exit()
    

def main(argv):
    inputfile = ''
    doCommonPasswordChecks = False
    verbose = False
    customList = False
    try:
        opts, args = getopt.getopt(argv,"hi:cvl:",["ifile=", "common", "verbose", "list="])
    except getopt.GetoptError:
        print ('doc-break.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('doc-break.py -i <inputfile> -c -v -l <listfile>')
            print ('| -i  |  Required  | <input file> | Will use that file as the one to open  | Somefile.docx')
            print ('| -c  |  Optional  |     None     | Use the 10000 common list              |              ')
            print ('| -v  |  Optional  |     None     | Will spam console with info            |              ')
            print ('| -l  |  Optional  | <input file> | Will use the file as the password list | Password.txt ')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-c", "--common"):
            doCommonPasswordChecks = True
        elif opt in ("-l", "--list"):
            customList = arg
    if inputfile == '':
        print ('No file passed.')
        print ('doc-break.py -i <inputfile>')
        sys.exit()
    
    exists = os.path.isfile(inputfile)
    
    if not exists:
        print ('Failed to find file. Please check your file location: ')
        print (inputfile)
        sys.exit()
    fh = msoffcrypto.OfficeFile(open(inputfile, "rb"))
    
    found = False
    if doCommonPasswordChecks:
        exists = os.path.isfile("10000-password-top-list.txt")
        if not exists:  
            download_PasswordList()
        common_passwords = open('10000-password-top-list.txt')
        currentLine = 1
        print ("Checking against the 10000 common password list")
        for line in common_passwords:
            if verbose:
                print ('Trying "' + line.rstrip() + '"')
                print ( str(currentLine) + '/' + str(10000))
            if breakFile(fh, line.rstrip()):
                break
            currentLine = currentLine+1
        common_passwords.close()
        
    if customList:
        exists = os.path.isfile(customList)
        if not exists:  
            print ('Could not find list "' + customList + '" Please check your file')
            sys.exit()
        
        password_list = open(customList)
        #this is ugly. I know
        linecount = 0
        for line in password_list:
            linecount = linecount+1
        password_list.close()
        password_list = open(customList)
        linecount = str(linecount)
        currentLine = 1
        for line in password_list:
            if verbose:
                print ('Trying "' + line.rstrip() + '"')
                print ( str(currentLine) + '/' + linecount)
            if breakFile(fh, line.rstrip()):
                break
            currentLine = currentLine+1
        password_list.close()
        
    print ('Could not find the password. Perhaps try a larger list')
    
    

if __name__ == "__main__":
   main(sys.argv[1:]) 


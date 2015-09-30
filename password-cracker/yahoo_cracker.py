import sys
import time

#Password Store
class Password:
    def __init__(self, passwordOrginalText, strippedPassword):
        self.passwordOrginalText = passwordOrginalText
        self.strippedPassword = strippedPassword

# Strips clear password from sql dump
class YahooPasswordStripper:
    def __init__(self, sqlDumpFile):
        self.sqlDumpFile = sqlDumpFile
        self.strippedPwdList = []
        self.counter = 0
    
    # strips last word after : for password
    def stripPasswordFromSqlDump(self):
        with open(self.sqlDumpFile) as dumpFile:
            contents = dumpFile.readlines()
            for content in contents:
                block = content.split(":")
                if len(block) > 2:
                    self.strippedPwdList.append(Password(content.strip(),block[2].strip()))
                    self.counter = self.counter + 1
                else:
                    print "<<ERROR - Could not convert>> Line number", self.counter+1, ":", content
        print "Stripped password from", self.counter,"entries"
        
    # Generates the txt file in required format
    def generateReport(self):
        with open('yahoo-cracked.txt','w') as crackedFile:
            for crackedPwd in self.strippedPwdList:
                crackedFile.write(crackedPwd.passwordOrginalText+" "+crackedPwd.strippedPassword+"\n")
        print "Generated report of stripped passwords"
                
# Main method - Entry point
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage : python yahoo_cracker.py <password sql dump file>"
    else:
        start = time.time();
        print "\n"
        print "********************************************************"
        passwordDumpFile = sys.argv[1]
        cracker = YahooPasswordStripper(passwordDumpFile)
        cracker.stripPasswordFromSqlDump()
        cracker.generateReport()
        print "Took",time.time() - start,"seconds for execution."
        print "********************************************************"
        print "\n"
                
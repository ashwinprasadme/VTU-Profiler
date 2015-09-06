import time
import os
from settings import APP_STATIC
class USN(object):
    """docstring for USN"""
    def __init__(self, usn):
        #make each part of USN an attribute to check against for validation
        self.usn = usn.lower()
        self.region = ''
        self.college = ''
        self.batch = ''
        self.stream = ''
        #create a dictionary which holds - in what part of USN an error has occured
        self.error = { 'Length Error' : False,
                       'Region Error' : False,
                       'College Error': False,
                       'Batch Error'  : False,
                       'Stream Error' : False,
                       'Count Error'  : False }
        #functions to read college and stream codes from a text file
        self.cc = self.readCollegeCode()
        self.sc = self.readStreamCode()

    def isValidUSN(self):
        '''
        split each part of USN and check each of these parts for errors.
        if an error is found, corresponding part is set as error
        returns True or False (based on validity of USN)
        '''
        if len(self.usn) != 10:
            self.error['Length Error'] = True           #if len is not 10 characters, then LengthError is True

        if self.usn[0] == '1':
            self.region = 'Bangalore'
        elif self.usn[0] == '2':
            self.region = "Belgaum"
        elif self.usn[0] == '3':
            self.region = "Gulbarga"
        elif self.usn[0] == '4':
            self.region = "Mysore"
        else:
            self.error['Region Error'] = True           #if region doesn't belong to any of the above, regionError is True

        givenCC = self.usn[1:3]
        for i in self.cc.keys():
            if givenCC == i:
                self.college = self.cc[i]
                self.error['College Error'] = False
                break
            else:
                self.error['College Error'] = True      #if given college code not in dictionary as the key, then collegeError is True

        curYear = int(time.strftime("%y"))              #gets current year in YY format and convert it to int

        try:
            givenYear = int(self.usn[3:5])
            if givenYear in range(0,curYear):    #though VTU started in '98, i'll use 00 for ease
                self.batch = str(givenYear)
        except ValueError:
            self.error['Batch Error'] = True


        givenStream = self.usn[5:7]
        for i in self.sc.keys():
            if givenStream == i:
                self.stream = self.sc[i]
                self.error['Stream Error'] = False
                break
            else:
                self.error['Stream Error'] = True       #if given stream code not in dictionary as the key, then streamError is True
        try:
            seatNo = int(self.usn[7:])
            if seatNo not in range(1,150):
                self.error['Count Error'] = True
        except ValueError:
            self.error['Count Error'] = True
        if self.getErrors() == '':
            return True
        else:
            return False

    def getErrors(self,):
        '''
        this function creates an error string with all errors using error dictionary
        '''
        errString = ''
        for i in self.error.keys():
            if self.error[i] == True:
                errString += str(i) + ' - '
        return errString


    def printUSN(self):
        '''
        print the Details in readable format
        '''
        result = ''
        result += 'Region : '+self.region+'\n'
        result += 'College: '+self.college+'\n'
        result += 'Batch  : '+self.batch+'\n'
        result += 'Stream : '+self.stream+'\n'
        return result

    def readCollegeCode(self,):
        '''
        opens collegeCodes.txt file in same folder and maps each code to its college nameas key-value pairs
        and returns this dictionary
        '''
        d = {}
        lines = [line.strip() for line in open(os.path.join(APP_STATIC, 'collegeCodes.txt'))]
        for i in range(len(lines)):
            d[lines[i][1:3].lower()] = lines[i][5:]
        return d

    def readStreamCode(self,):
        '''
        opens branchCodes.txt file in same folder and maps each code to its branch name as key-value pairs
        and returns this dictionary
        '''
        d ={}
        lines = [line.strip() for line in open(os.path.join(APP_STATIC, 'branchCodes.txt'))]
        for i in range(len(lines)):
            d[lines[i][0:2].lower()] = lines[i][3:]
        return d

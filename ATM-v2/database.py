import csv

class Database():
    def __init__(self) -> None:
        
        self.data = []
        self.lastSearchedUserIndex = None
        self.readfile = "data.csv"
        self.writefile = "data.csv"
        
        with open(self.readfile, 'r') as file:
            csvreader = csv.DictReader(file)
            for row in csvreader:
                self.data.append(row)
                
    #  return index of user
    def searchForID(self,ID):
        for row in self.data:
            if row['ID'] == ID:
                self.lastSearchedUserIndex = self.data.index(row)
                return self.lastSearchedUserIndex
            
        return None
    
    #  if the ID is different from last user research for ID index and return name
    def getName(self,ID) -> str:
        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID :
            return self.data[self.lastSearchedUserIndex]['Name']
        else:
            return self.data[self.searchForID(ID)]['Name']
    
    # edit name of user and updata csv file
    def setName(self,ID,newName):
        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            self.data[self.lastSearchedUserIndex]['Name'] = newName
        else:
            self.data[self.searchForID(ID)]['Name'] = newName
        self.updateDataBase()
            
        
    #  if the ID is different from last user research for ID index and return password    
    def getPassword(self,ID):
        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            return self.data[self.lastSearchedUserIndex]['Password']
        else:
            return self.data[self.searchForID(ID)]['Password']
    
    # edit password of user and updata csv file
    def setPassword(self,ID,newPassword):
        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            self.data[self.lastSearchedUserIndex]['Password'] = newPassword
        else:
            self.data[self.searchForID(ID)]['Password'] = newPassword
        self.updateDataBase()
        
    #  if the ID is different from last user research for ID index and return balance
    def getBalance(self,ID):
        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            return int(self.data[self.lastSearchedUserIndex]['Balance'])
        else:
            return int(self.data[self.searchForID(ID)]['Balance'])
    
    # edit balance of user and updata csv file
    def setBalance(self,ID,newbalnce):
        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            self.data[self.lastSearchedUserIndex]['Balance'] = newbalnce
        else:
            self.data[self.searchForID(ID)]['Balance'] = newbalnce
        self.updateDataBase()

     
    #  if the ID is different from last user research for ID index and return status
    def getStatus(self,ID):
        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            return self.data[self.lastSearchedUserIndex]['Status']
        else:
            return self.data[self.searchForID(ID)]['Status']
    
    # edit status of user and updata csv file
    def setStatus(self,ID,newStatus):

        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            self.data[self.lastSearchedUserIndex]['Status'] = newStatus
        else:
            self.data[self.searchForID(ID)]['Status'] = newStatus
        self.updateDataBase()

    #  if the ID is different from last user research for ID index and return status
    def getEmail(self,ID):
        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            return self.data[self.lastSearchedUserIndex]['Email']
        else:
            return self.data[self.searchForID(ID)]['Email']
    
    # edit Email of user and updata csv file
    def setEmail(self,ID,newEmail):

        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            self.data[self.lastSearchedUserIndex]['Email'] = newEmail
        else:
            self.data[self.searchForID(ID)]['Email'] = newEmail
        self.updateDataBase()

   #  if the ID is different from last user research for ID index and return status
    def getMobileNum(self,ID):
        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            return self.data[self.lastSearchedUserIndex]['MobileNum']
        else:
            return self.data[self.searchForID(ID)]['MobileNum']
    
    # edit MobileNum of user and updata csv file
    def setMobileNum(self,ID,newMobileNum):

        if self.lastSearchedUserIndex != None and self.data[self.lastSearchedUserIndex]['ID'] == ID:
            self.data[self.lastSearchedUserIndex]['MobileNum'] = newMobileNum
        else:
            self.data[self.searchForID(ID)]['MobileNum'] = newMobileNum
        self.updateDataBase()
            
    # print all data in csv
    def printAllData(self):
        for row in self.data:
            print(row)
        
    # update csv file
    def updateDataBase(self):
        # header
        fields = ['ID', 'Name', 'Password', 'Balance','Email','Mobile', 'Status'] 

        with open(self.writefile, 'w', newline='') as file: 
            writer = csv.DictWriter(file, fieldnames = fields)
            writer.writeheader() 
            writer.writerows(self.data)
            
    # remove user from csv file
    def removeUser(self,ID):
        index = self.searchForID(ID)
        if index != -1:
            self.data.remove(self.data[index])
    
    # add user to csv file
    def addUser(self, UserData:dict):
        if self.searchForID(UserData['ID']) == -1:
            self.data.append(UserData)

 

def test():

    data = Database()
    print(data.getEmail("201455998011"))

# test()
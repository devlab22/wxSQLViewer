import sqlite3

class MySqlite:
    
    def __init__(self, path):
        
        self.__Path = path
        self.__MasterData = []
        self.__readMasterData()
        
    def __del__(self):
        
        self.__Path = ''
        self.__MasterData.clear()
        
    def __readMasterData(self):
        
        con = sqlite3.connect(self.__Path)
        cur = con.cursor()
        cur.execute("select * from sqlite_master")
        self.__MasterData = cur.fetchall()
        cur.close()
        con.close()
        
    def readTable(self, table):
        
        con = sqlite3.connect(self.__Path)
        cur = con.cursor()
        tableContent = []
        cur.execute('select * from {0}'.format(table))
        tableContent = cur.fetchall()
        cur.close()
        con.close()
        return tableContent
    
    def readTableFields(self, table):
        
        con = sqlite3.connect(self.__Path)
        cur = con.cursor()
        tableFields = []
        cur.execute('pragma table_info({0}) '.format(table))
        tableFields = cur.fetchall()
        cur.close()
        con.close()
        return tableFields
    
    def printTable(self, table):
        
        tableContent = self.readTable(table)
        print('Content of table {0}, count {1}'.format(table, len(tableContent)))
        
        for line in tableContent:
            print(line)
        
    def printTableFields(self, table):
        
        tableFields = self.readTableFields(table)
        print('Fields of table {0}, count {1}'.format(table, len(tableFields)))
        for line in tableFields:
            print(line)
        
    def printMasterData(self):
        
        print('Content of table master_table, count {0}'.format(len(self.__MasterData)))
        
        for line in self.__MasterData:
            print(line)
        
    def printTables(self):
        
        for item in self.__MasterData:
            table = item[1]
            self.printTable(table)
            
    def getMasterData(self):
        
        return self.__MasterData
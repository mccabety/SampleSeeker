# DatabaseManager.py

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from datetime import datetime

class InventoryItem:
    def __init__(self, age = 0, location = '', genotype = '', birthDate = datetime.now(), sacDate = datetime.now()):
        self.Age = age
        self.Location = location
        self.Genotype = genotype
        self.BirthDate = birthDate
        self.SacDate = sacDate

class DatabaseManager:
    def __init__(self,
        serverHost = 'localhost', serverPort = 3306,
        databaseName = '', serverUserName = '',
        serverPassword = ''):
        # todo: Read from configuration JSON
        self.ServerHost = serverHost
        self.ServerPort = serverPort
        self.DatabaseName = databaseName

        # Enter in credentials here:
        self.ServerUserName = serverUserName
        self.ServerPassword = serverPassword


        self.engine = create_engine(
            'mysql://' + self.ServerUserName + 
            ':' + self.ServerPassword + '@'
             + self.ServerHost + ':' + str(self.ServerPort)
              + '/' + self.DatabaseName)


    def Test(self):

        self.DatabaseName = ''

        # Enter in credentials here:
        self.ServerUserName = ''
        self.ServerPassword = ''

        self.engine = create_engine(
        'mysql://' + self.ServerUserName + 
        ':' + self.ServerPassword + '@'
            + self.ServerHost + ':' + str(self.ServerPort)
            + '/' + self.DatabaseName)

        self.CreateTables()

        newInventoryItem = InventoryItem()
        self.InsertInventoryItem(newInventoryItem)

        results = self.GetAllInventoryItems()

        for result in results:
            print(result)  

    def CreateTables(self):
        meta = MetaData()

        if not self.engine.dialect.has_table(self.engine, "Inventory"):
            print('Attempting to create table...')

            Inventory = Table(
                'Inventory', meta, 
                Column('Id', Integer, primary_key = True), 
                Column('Age', Integer),
                Column('Location', String(250)), 
                Column('Genotype', String(250)), 
                Column('BirthDate', DateTime), 
                Column('SacDate', DateTime),
            )
            
            meta.create_all(self.engine)


            print('ATable creatation complete!')
        else:
            print('Tables already created')

    def InsertInventoryItem(self, inventoryItem):
        metaData = MetaData()

        metaData.reflect(bind=self.engine)

        Inventory = metaData.tables['Inventory']


        valuesToInsert = Inventory.insert()
        valuesToInsert = Inventory.insert().values(
                Age = inventoryItem.Age,
                Location = inventoryItem.Location,
                Genotype = inventoryItem.Genotype,
                BirthDate = inventoryItem.BirthDate,
                SacDate = inventoryItem.SacDate)

        connection = self.engine.connect()

        result = connection.execute(valuesToInsert)

    # todo: Improve this method
    def ConvertResultsProxyToDictionary(self, rawResults):
        results = []
        for result in rawResults:
            results.append(dict(zip(result.keys(), result)))
        return results

    def GetAllInventoryItems(self):
        selectAllQuery = 'SELECT * FROM Inventory'
        
        inventoryEntries = self.engine.execute(selectAllQuery)

        return self.ConvertResultsProxyToDictionary(inventoryEntries)

if __name__ == '__main__':
    dbManager = DatabaseManager()

    dbManager.Test()

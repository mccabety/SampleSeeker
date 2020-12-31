'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# DatabaseManager.py

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from datetime import datetime
from ConfigurationManager import ConfigurationManager

class InventoryItem:
    def __init__(self, age = 0, location = '', genotype = '', birthDate = datetime.now(), sacDate = datetime.now()):
        self.Age = age
        self.Location = location
        self.Genotype = genotype
        self.BirthDate = birthDate
        self.SacDate = sacDate

class DatabaseManager:
    def __init__(self):
        self.configurationManager = ConfigurationManager()
        databaseConfigurations = configurationManager.GetDatabaseConfiguration()
        
        self.ServerHost = databaseConfigurations['ServerHostName']
        self.ServerPort = databaseConfigurations['ServerPortNumber']
        self.DatabaseName = databaseConfigurations['DatabaseName']

        # Enter in credentials here:
        self.ServerUserName = databaseConfigurations['ServerUsername']
        self.ServerPassword = databaseConfigurations['ServerPassword']


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

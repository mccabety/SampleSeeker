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

class InventoryItem:
    def __init__(self, age = 0, location = '', genotype = '', birthDate = datetime.now(), sacDate = datetime.now()):
        self.Age = age
        self.Location = location
        self.Genotype = genotype
        self.BirthDate = birthDate
        self.SacDate = sacDate
    

def CreateTables(engine):
    meta = MetaData()

    if not engine.dialect.has_table(engine, "Inventory"):
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
        
        meta.create_all(engine)


        print('ATable creatation complete!')
    else:
        print('Tables already created')

def InsertInventoryItem(engine, inventoryItem):
    metaData = MetaData()

    metaData.reflect(bind=engine)

    Inventory = metaData.tables['Inventory']


    valuesToInsert = Inventory.insert()
    valuesToInsert = Inventory.insert().values(
            Age = inventoryItem.Age,
            Location = inventoryItem.Location,
            Genotype = inventoryItem.Genotype,
            BirthDate = inventoryItem.BirthDate,
            SacDate = inventoryItem.SacDate)

    connection = engine.connect()

    result = connection.execute(valuesToInsert)

def GetAllInventoryItems(engine):
    selectAllQuery = 'SELECT * FROM Inventory'
    
    inventoryEntries = engine.execute(selectAllQuery)

    return inventoryEntries


def main():

    # todo: Read from configuration JSON
    serverHost = 'localhost'
    serverPort = 3306
    databaseName = ''

    # Enter in credentials here:
    serverUserName = ''
    serverPassword = ''


    engine = create_engine('mysql://' + serverUserName +':' + serverPassword + '@' + serverHost + ':' + str(serverPort) + '/' + databaseName)

    CreateTables(engine)

    newInventoryItem = InventoryItem()
    InsertInventoryItem(engine, newInventoryItem)

    results = GetAllInventoryItems(engine)

    for result in results:
        print(result)

InventoryItem
if __name__ == '__main__':
    main()

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
# Note: Requires version 1.4+
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ConfigurationManager import ConfigurationManager


Base = declarative_base()

class InventoryItem(Base):
    __tablename__ = 'InventoryItems'

    PrimaryKey = Column(Integer, primary_key=True)
    InventoryId =  Column(Integer)
    Age = Column(Integer)
    Location = Column(String(500))
    Genotype = Column(String(250))
    BirthDate = Column(DateTime)
    SacDate = Column(DateTime)

    def __repr__(self):
        return "<InventoryItem(PrimaryKey='%s', InventoryId='%s', Age='%s', Location='%s', Genotype='%s', BirthDate='%s', SacDate='%s')>" % (
            self.PrimaryKey, self.InventoryId, self.Age, self.Location, self.Genotype, self.BirthDate, self.SacDate)

class DatabaseManager:
    def __init__(self):
        self.configurationManager = ConfigurationManager()
        databaseConfigurations = self.configurationManager.GetDatabaseConfiguration()
        
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

        Session = sessionmaker(bind=self.engine)

        self.session = Session()

    def Test(self):
        self.CreateTables()

        newInventoryItem = InventoryItem(InventoryId = 4324, Age=4, Location="Lab Z", Genotype = 'X-12', BirthDate = datetime.now())
        self.InsertInventoryItem(newInventoryItem)

        newInventoryItem = InventoryItem(InventoryId = 765, Age=4, Location="Lab Z", Genotype = 'X-12', BirthDate = datetime(2020,5,3), SacDate = datetime(2020,10,5))
        self.InsertInventoryItem(newInventoryItem)

        results = self.GetAllInventoryItems()

        for result in results:
            print(result)

    def CreateTables(self):
        if not self.engine.dialect.has_table(self.engine, "InventoryItems"):
            print('Attempting to create table...')

            Base.metadata.create_all(self.engine)

            print('ATable creatation complete!')
        else:
            print('Tables already created')

    def InsertInventoryItem(self, inventoryItem):
        self.session.add(inventoryItem)

        self.session.commit()

    def DeleteInventoryItems(self, itemsToDelete):
        for item in itemsToDelete:
            self.session.query(InventoryItem).filter(InventoryItem.PrimaryKey == item.PrimaryKey).delete()
        self.session.commit()   

    def GetAllInventoryItems(self):
        return self.session.query(InventoryItem).all()

if __name__ == '__main__':
    dbManager = DatabaseManager()
    dbManager.Test()

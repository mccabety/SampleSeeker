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

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey
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
    Location = Column(String(500))
    Genotype = Column(String(250))
    BirthDate = Column(DateTime)
    SacDate = Column(DateTime)

    def __repr__(self):
        return "<InventoryItem(PrimaryKey='%s', InventoryId='%s', Location='%s', Genotype='%s', BirthDate='%s', SacDate='%s')>" % (
            self.PrimaryKey, self.InventoryId, self.Location, self.Genotype, self.BirthDate, self.SacDate)

class Sample(Base):
    __tablename__ = 'Samples'

    PrimaryKey = Column(Integer, primary_key=True)
    SampleId =  Column(Integer)
    Name = Column(String(260))
    Type = Column(String(260))
    Location = Column(String(260))
    Description = Column(String(1000))
    CreationDate = Column(DateTime)

    AssociatedInventoryItem = Column(Integer, ForeignKey('InventoryItems.PrimaryKey', ondelete='CASCADE'))


    def __repr__(self):
        return "<Sample(PrimaryKey='%s', SampleId='%s', Name='%s', Location='%s',  Description='%s', CreationDate='%s', InventoryId='%s)>" % (
            self.PrimaryKey, self.SampleId, self.Name, self.Location, self.Description, self.CreationDate, self.AssociatedInventoryItem)

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

        newInventoryItem = InventoryItem(InventoryId = 4324, Location="Lab Z", Genotype = 'X-12', BirthDate = datetime.now())
        self.InsertInventoryItem(newInventoryItem)

        newInventoryItem = InventoryItem(InventoryId = 765, Location="Lab Z", Genotype = 'X-12', BirthDate = datetime(2020,5,3), SacDate = datetime(2020,10,5))
        self.InsertInventoryItem(newInventoryItem)

        results = self.GetAllInventoryItems()

        newSample = Sample(SampleId = 56436, Name = 'Cell Culture A', Location = "Lab RED", Description='A cool sample', CreationDate = datetime(2020,5,3), AssociatedInventoryItem = results[0].PrimaryKey)

        self.InsertSample(newSample)

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

    # Todo: All of the DB calls could easily be made generic.
    def InsertInventoryItem(self, inventoryItem):
        self.session.add(inventoryItem)

        self.session.commit()

    def EditInventoryItem(self, editedItem):
        itemToEdit = self.session.query(InventoryItem).filter(InventoryItem.PrimaryKey == editedItem.PrimaryKey).one()
        
        itemToEdit.InventoryId = editedItem.InventoryId
        itemToEdit.Location = editedItem.Location
        itemToEdit.Genotype = editedItem.Genotype
        itemToEdit.Location = editedItem.Location
        itemToEdit.BirthDate = editedItem.BirthDate
        itemToEdit.SacDate = editedItem.SacDate
 
        self.session.commit()

    def DeleteInventoryItems(self, itemsToDelete):
        for item in itemsToDelete:
            self.session.query(InventoryItem).filter(InventoryItem.PrimaryKey == item.PrimaryKey).delete()
        self.session.commit()   
    
    def InsertSample(self, sample):
        self.session.add(sample)
        
        self.session.commit()

    def EditSample(self, editedSample):
        sampleToEdit = self.session.query(Sample).filter(Sample.PrimaryKey == editedSample.PrimaryKey).one()
        
        sampleToEdit.SampleId = editedSample.SampleId
        sampleToEdit.Name = editedSample.Name
        sampleToEdit.Type = editedSample.Type
        sampleToEdit.Location = editedSample.Location
        sampleToEdit.Description = editedSample.Description
        sampleToEdit.CreationDate = editedSample.CreationDate
 
        self.session.commit()

    def DeleteSamples(self, itemsToDelete):
        for item in itemsToDelete:
            self.session.query(Sample).filter(Sample.PrimaryKey == item.PrimaryKey).delete()
        self.session.commit()

    def GetAllInventoryItems(self):
        return self.session.query(InventoryItem).all()

    def GetAllSamplesForInventoryItem(self, inventoryItem):
        return self.session.query(Sample).filter(Sample.AssociatedInventoryItem == inventoryItem.PrimaryKey).all()

if __name__ == '__main__':
    dbManager = DatabaseManager()
    dbManager.Test()

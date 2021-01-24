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

# Smaple Seeker Main

import sys
import datetime

from DatabaseManager import DatabaseManager, InventoryItem, Sample

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)

class TableDisplayModel(QtGui.QStandardItemModel):
    def __init__(self, data, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        self._data = data

        for row in data:
            data_row = [ QtGui.QStandardItem("{0}".format(x)) for x in row ]
            self.appendRow(data_row)
        return

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        if self.rowCount() > 0:
            return len(self._data[0])
        else:
            return 0

class MainWindow(QWidget):
    def __init__(self, databaseManager):
        super().__init__()

        self.dataHeaderLabels = ['PrimaryKey', 'ID', 'Age (Weeks)', 'Location',' Genotype', 'Birth Date', 'Sac Date']

        self.searchComboBox = QtWidgets.QComboBox()
        self.searchComboBox.addItems( [headerLabel for headerLabel in self.dataHeaderLabels if headerLabel != 'PrimaryKey'])

        self.searchTextBox = QtWidgets.QLineEdit()

        self.table = QtWidgets.QTableView()

        self.databaseManager = databaseManager

        self.RefreshInventoryTable()

        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setColumnHidden(0, True)

        verticalBox = QtWidgets.QVBoxLayout()

        searchButton = QtWidgets.QPushButton("Search")
        clearSearchButton = QtWidgets.QPushButton("Reset")
        clearSearchButton.clicked.connect(self.RefreshInventoryTable)

        searchLayout = QtWidgets.QHBoxLayout()
        searchLayout.addWidget(self.searchComboBox)
        searchLayout.addWidget(self.searchTextBox)
        searchLayout.addWidget(searchButton)
        searchLayout.addWidget(clearSearchButton)

        addButton = QtWidgets.QPushButton("Add")
        addButton.clicked.connect(self.AddButtonClicked)

        editButton = QtWidgets.QPushButton("Edit")
        editButton.clicked.connect(self.EditButtonClicked)

        deleteButton = QtWidgets.QPushButton("Delete")
        deleteButton.clicked.connect(self.DeleteButtonClicked)

        viewSamplesButton = QtWidgets.QPushButton("View Samples")
        viewSamplesButton.clicked.connect(self.ViewSamplesButtonClicked)

        buttonsLayout = QtWidgets.QHBoxLayout()
        buttonsLayout.addWidget(addButton)
        buttonsLayout.addWidget(editButton)
        buttonsLayout.addWidget(deleteButton)
        buttonsLayout.addWidget(viewSamplesButton)

        verticalBox.addLayout(searchLayout)
        verticalBox.addWidget(self.table)
        verticalBox.addLayout(buttonsLayout)
        verticalBox.setAlignment(Qt.AlignHCenter)

        self.setLayout(verticalBox)

        self.setGeometry(300, 300, 700, 800)
        self.setWindowTitle('Sample Seeker')
        self.show()
    
    def RefreshInventoryTable(self):
        # Load inventory items from database 
        data = []
        for item in self.databaseManager.GetAllInventoryItems():
            age = 0
            if item.BirthDate:
                age = (item.SacDate - item.BirthDate).days//7 if item.SacDate else (datetime.datetime.now() - item.BirthDate).days//7
            data.append([item.PrimaryKey, item.InventoryId, age, item.Location, item.Genotype, item.BirthDate, item.SacDate])
 
        self.tableDisplayModel = TableDisplayModel(data)

        self.tableDisplayModel.setHorizontalHeaderLabels(self.dataHeaderLabels)
        self.tableDisplayModel.setVerticalHeaderLabels('' for item in data)

        self.table.setModel(self.tableDisplayModel)

    def closeEvent(self, event):
        print("Child window closed properly")

    def AddButtonClicked(self):
        self.showAddItemDialog()

    def DeleteButtonClicked(self):
        self.showDeleteItemDialog()
    
    def EditButtonClicked(self):
        if( not self.IsOnlyOneItemSelected() ):
            return

        self.hide()
        self.editInventoryWindow = EditInventoryWindow(self, self.databaseManager, self.GetSelectedInventoryItem())
        self.editInventoryWindow.show()
    
    def ViewSamplesButtonClicked(self):
        if( not self.IsOnlyOneItemSelected() ):
            return

        self.hide()
        self.viewSamplesWindow = ViewSamplesWindow(self, self.databaseManager, self.GetSelectedInventoryItem())
        self.viewSamplesWindow.show()

    def GetSelectedInventoryItem(self):
        if( not self.IsOnlyOneItemSelected() ):
            None

        item = self.table.selectionModel().selectedRows()[0]
        model = self.table.model()

        relatedInventoryItem = InventoryItem(
                    PrimaryKey = model.index(item.row(),0).data(), InventoryId = model.index(item.row(),1).data(),
                    # Skip 2, which maps to Age
                    Location = model.index(item.row(),3).data(),
                    Genotype = model.index(item.row(),4).data(), BirthDate = model.index(item.row(),5).data(),
                    SacDate = model.index(item.row(),6).data() ) 

        return relatedInventoryItem

    def IsOnlyOneItemSelected(self):
        selectedItems = self.table.selectionModel().selectedRows()
        itemCount = len(selectedItems)

        return False if itemCount != 1 else True

    def showAddItemDialog(self):
        self.hide()
        self.addInventoryItemWindow = AddInventoryItemWindow(self, self.databaseManager)
        self.addInventoryItemWindow.show()

    def showDeleteItemDialog(self):
        itemsToDelete = self.table.selectionModel().selectedRows()
        itemCount = len(itemsToDelete)

        if(itemCount == 0):
            return

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setWindowTitle("Warning")
        msgBox.setText("Delete selected %d items?" % itemCount)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            inventoryItems = []
            model = self.table.model()

            # Todo: should the entire object be sent to the database deletion method?
            for item in itemsToDelete:
                inventoryItems.append( InventoryItem(
                    PrimaryKey = model.index(item.row(),0).data(), InventoryId = model.index(item.row(),1).data(),
                    Location = model.index(item.row(),2).data(),
                    Genotype = model.index(item.row(),3).data(), BirthDate = model.index(item.row(),4).data(),
                    SacDate = model.index(item.row(),5).data() ) )
            
            self.databaseManager.DeleteInventoryItems(inventoryItems)

            self.RefreshInventoryTable()
 
class AddInventoryItemWindow(QWidget):
    def __init__(self,parent, databaseManager):
        super().__init__()

        self.parent = parent
        self.databaseManager = databaseManager

        self.verticalBox = QtWidgets.QVBoxLayout()

        self.inventoryIdSection = QtWidgets.QHBoxLayout()
        self.inventoryIdLabel = QtWidgets.QLabel('ID: ')
        self.inventoryIdInput = QtWidgets.QLineEdit()
        self.inventoryIdSection.addWidget(self.inventoryIdLabel)
        self.inventoryIdSection.addWidget(self.inventoryIdInput)

        self.locationSection = QtWidgets.QHBoxLayout()
        self.locationLabel = QtWidgets.QLabel('Location: ')
        self.locationInput = QtWidgets.QLineEdit()
        self.locationSection.addWidget(self.locationLabel)
        self.locationSection.addWidget(self.locationInput)

        self.genotypeSection = QtWidgets.QHBoxLayout()
        self.genotypeLabel = QtWidgets.QLabel('Genotype: ')
        self.genotypeInput = QtWidgets.QLineEdit()
        self.genotypeSection.addWidget(self.genotypeLabel)
        self.genotypeSection.addWidget(self.genotypeInput)

        self.birthDateSection = QtWidgets.QHBoxLayout()
        self.birthDateLabel = QtWidgets.QLabel('Birth Date: ')
        self.birthDateInput = QtWidgets.QDateEdit()
        self.birthDateSection.addWidget(self.birthDateLabel)
        self.birthDateSection.addWidget(self.birthDateInput)


        self.sacDateSection = QtWidgets.QHBoxLayout()
        self.sacDateToggleButton = QPushButton("Sac Date?")
        self.sacDateToggleButton.setCheckable(True)
        self.sacDateToggleButton.clicked.connect(self.SacDateToggled)

        self.sacDateLabel = QtWidgets.QLabel('Sac Date: ')
        self.sacDateInput = QtWidgets.QDateEdit()
        self.sacDateLabel.setVisible(False)
        self.sacDateInput.setVisible(False)
        self.sacValueProvided = False
        
        self.sacDateSection.addWidget(self.sacDateToggleButton)
        self.sacDateSection.addWidget(self.sacDateLabel)
        self.sacDateSection.addWidget(self.sacDateInput)
        



        self.buttonSection = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton("Add")
        self.addButton.clicked.connect(self.AddButtonClicked)

        self.clearButton = QtWidgets.QPushButton("Clear")
        self.clearButton.clicked.connect(self.ClearButtonClicked)

        self.buttonSection.addWidget(self.addButton)
        self.buttonSection.addWidget(self.clearButton)



        self.verticalBox.addLayout(self.inventoryIdSection)
        self.verticalBox.addLayout(self.locationSection)
        self.verticalBox.addLayout(self.genotypeSection)
        self.verticalBox.addLayout(self.birthDateSection)
        self.verticalBox.addLayout(self.sacDateSection)

        self.verticalBox.addLayout(self.buttonSection)


        self.setLayout(self.verticalBox)

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Add New Inventory Item')
        
        self.ClearInput()
    
    def ClearInput(self):
        self.inventoryIdInput.setText('')
        self.locationInput.setText('')
        self.genotypeInput.setText('')
        self.birthDateInput.setDate(datetime.date.today())
        self.sacDateInput.setDate(datetime.date.today())

    def SacDateToggled(self):
        if self.sacValueProvided:
            self.sacDateLabel.setVisible(False)
            self.sacDateInput.setVisible(False)
            self.sacValueProvided = False
        else:
            self.sacDateLabel.setVisible(True)
            self.sacDateInput.setVisible(True)
            self.sacValueProvided = True

    def AddButtonClicked(self):
        
        inventoryItemToAdd = InventoryItem(
            InventoryId = self.inventoryIdInput.text(), Location = self.locationInput.text(),
            Genotype = self.genotypeInput.text(), BirthDate = self.birthDateInput.date().toPyDate(),
            SacDate = self.sacDateInput.date().toPyDate() if self.sacValueProvided else None)

        self.databaseManager.InsertInventoryItem(inventoryItemToAdd)
        self.parent.RefreshInventoryTable()
        self.close()

    def ClearButtonClicked(self):
        self.ClearInput()

    def closeEvent(self, event):
        self.parent.show()

class EditInventoryWindow(AddInventoryItemWindow):
    def __init__(self, parent, databaseManager, selectedInventoryItem):
        super().__init__(parent, databaseManager)

        self.selectedInventoryItem = selectedInventoryItem
        
        self.DisplayCurrentSampleValues()

        self.addButton.disconnect()
        self.addButton.clicked.connect(self.SaveEdit)
        self.addButton.setText('Save')

    def DisplayCurrentSampleValues(self):
        self.inventoryIdInput.setText(self.selectedInventoryItem.InventoryId)
        self.locationInput.setText(self.selectedInventoryItem.Location)
        self.genotypeInput.setText(self.selectedInventoryItem.Genotype)
        self.birthDateInput.setDate( self.GetDateFromString(self.selectedInventoryItem.BirthDate) )
        
        if(self.selectedInventoryItem.SacDate != 'None'):
            self.sacDateInput.setDate(self.GetDateFromString(self.selectedInventoryItem.SacDate))
            self.SacDateToggled()

    def GetDateFromString(self, dateString):
        return datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
    
    def SaveEdit(self): 
        inventoryItemToEdit = InventoryItem( PrimaryKey = self.selectedInventoryItem.PrimaryKey,
            InventoryId = self.inventoryIdInput.text(), Location = self.locationInput.text(),
            Genotype = self.genotypeInput.text(), BirthDate = self.birthDateInput.date().toPyDate(),
            SacDate = self.sacDateInput.date().toPyDate() if self.sacValueProvided else None)

        self.databaseManager.EditInventoryItem(inventoryItemToEdit)
        self.parent.RefreshInventoryTable()
        self.close()


class ViewSamplesWindow(QWidget):
    def __init__(self, parent, databaseManager, relatedInventoryItem):
        super().__init__()
    
        self.parent = parent
        self.databaseManager = databaseManager
        self.relatedInventoryItem = relatedInventoryItem

        self.dataHeaderLabels = ['PrimaryKey', 'ID', 'Name', 'Location',' Description', 'Creation Date', 'InventoryId']


        self.table = QtWidgets.QTableView()

        self.RefreshSampleTable()

        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setColumnHidden(0, True)


        self.buttonSection = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton("Add")
        self.addButton.clicked.connect(self.AddButtonClicked)

        self.editButton = QtWidgets.QPushButton("Edit")
        self.editButton.clicked.connect(self.EditButtonClicked)

        self.deleteButton = QtWidgets.QPushButton("Delete")
        self.deleteButton.clicked.connect(self.DeleteButtonClicked)

        self.buttonSection.addWidget(self.addButton)
        self.buttonSection.addWidget(self.editButton)
        self.buttonSection.addWidget(self.deleteButton)

        self.verticalBox = QtWidgets.QVBoxLayout()

        self.verticalBox.addWidget(self.table)
        self.verticalBox.addLayout(self.buttonSection)

        self.setLayout(self.verticalBox)
        self.setGeometry(300, 300, 700, 800)
        self.setWindowTitle('View and Edit Samples')

    def AddButtonClicked(self):
        self.addSampleWindow = AddSampleWindow(self, self.databaseManager, self.relatedInventoryItem)
        self.addSampleWindow.show()

    def EditButtonClicked(self):
        if(not self.IsOneSampleSelected()):
            return

        self.selectedSample = self.GetSelectedSample()

        self.editSamplesWindow = EditSamplesWindow(self, self.databaseManager, self.relatedInventoryItem, self.selectedSample)
        self.editSamplesWindow.show()

    def IsOneSampleSelected(self):
        if(len(self.table.selectionModel().selectedRows()) != 1):
            return False
        return True

    def GetSelectedSample(self):
        if(not self.IsOneSampleSelected()):
            None

        sample = self.table.selectionModel().selectedRows()[0]
        model = self.table.model()

        return Sample(
                    PrimaryKey = model.index(sample.row(),0).data(), SampleId = model.index(sample.row(),1).data(),
                    Name = model.index(sample.row(),2).data(),
                    Location = model.index(sample.row(),3).data(), Description = model.index(sample.row(),4).data(),
                    CreationDate = model.index(sample.row(),5).data(), AssociatedInventoryItem = model.index(sample.row(),6).data() )

    def DeleteButtonClicked(self):
        self.showDeleteSampleDialog()
    
    def showDeleteSampleDialog(self):

        itemsToDelete = self.table.selectionModel().selectedRows()
        itemCount = len(itemsToDelete)

        if(itemCount == 0):
            return

        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setWindowTitle("Warning")
        msgBox.setText("Delete selected %d samples?" % itemCount)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            samples = []
            model = self.table.model()

            # Todo: should the entire object be sent to the database deletion method?
            for sample in itemsToDelete:
                samples.append( Sample(
                    PrimaryKey = model.index(sample.row(),0).data(), SampleId = model.index(sample.row(),1).data(),
                    Name = model.index(sample.row(),2).data(),
                    Location = model.index(sample.row(),3).data(), Description = model.index(sample.row(),4).data(),
                    CreationDate = model.index(sample.row(),5).data(), AssociatedInventoryItem = model.index(sample.row(),6).data() ) )
            
            self.databaseManager.DeleteSamples(samples)

            self.RefreshSampleTable()

    def RefreshSampleTable(self):
        # Load inventory items from database 
        data = []

        samples = self.databaseManager.GetAllSamplesForInventoryItem(inventoryItem = self.relatedInventoryItem)

        for sample in samples:
            data.append([sample.PrimaryKey, sample.SampleId, sample.Name, sample.Location, sample.Description, sample.CreationDate, sample.AssociatedInventoryItem])

        self.tableDisplayModel = TableDisplayModel(data)

        self.tableDisplayModel.setHorizontalHeaderLabels(self.dataHeaderLabels)
        self.tableDisplayModel.setVerticalHeaderLabels('' for item in data)

        self.table.setModel(self.tableDisplayModel)

    def closeEvent(self, event):
        self.parent.show()

class AddSampleWindow(QWidget):
    def __init__(self,parent, databaseManager, relatedInventoryItem):
        super().__init__()

        self.parent = parent
        self.databaseManager = databaseManager
        self.relatedInventoryItem = relatedInventoryItem

        self.verticalBox = QtWidgets.QVBoxLayout()

        self.sampleIdSection = QtWidgets.QHBoxLayout()
        self.sampleIdLabel = QtWidgets.QLabel('ID: ')
        self.sampleIdInput = QtWidgets.QLineEdit()
        self.sampleIdSection.addWidget(self.sampleIdLabel)
        self.sampleIdSection.addWidget(self.sampleIdInput)

        self.nameSection = QtWidgets.QHBoxLayout()
        self.nameLabel = QtWidgets.QLabel('Name: ')
        self.nameInput = QtWidgets.QLineEdit()
        self.nameSection.addWidget(self.nameLabel)
        self.nameSection.addWidget(self.nameInput)


        self.locationSection = QtWidgets.QHBoxLayout()
        self.locationLabel = QtWidgets.QLabel('Location: ')
        self.locationInput = QtWidgets.QLineEdit()
        self.locationSection.addWidget(self.locationLabel)
        self.locationSection.addWidget(self.locationInput)

        self.descriptionSection = QtWidgets.QHBoxLayout()
        self.descriptionLabel = QtWidgets.QLabel('Description: ')
        self.descriptionInput = QtWidgets.QLineEdit()
        self.descriptionSection.addWidget(self.descriptionLabel)
        self.descriptionSection.addWidget(self.descriptionInput)


        self.creationDateSection = QtWidgets.QHBoxLayout()
        self.creationDateLabel = QtWidgets.QLabel('Creation Date: ')
        self.creationDateInput = QtWidgets.QDateEdit()
        self.creationDateSection.addWidget(self.creationDateLabel)
        self.creationDateSection.addWidget(self.creationDateInput)


        self.buttonSection = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton("Add")
        self.addButton.clicked.connect(self.AddButtonClicked)

        self.clearButton = QtWidgets.QPushButton("Clear")
        self.clearButton.clicked.connect(self.ClearButtonClicked)

        self.buttonSection.addWidget(self.addButton)
        self.buttonSection.addWidget(self.clearButton)



        self.verticalBox.addLayout(self.sampleIdSection)
        self.verticalBox.addLayout(self.nameSection)
        self.verticalBox.addLayout(self.locationSection)
        self.verticalBox.addLayout(self.descriptionSection)
        self.verticalBox.addLayout(self.creationDateSection)

        self.verticalBox.addLayout(self.buttonSection)

        self.setLayout(self.verticalBox)

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Add New Sample')
        
        self.ClearInput()
    
    def ClearInput(self):
        self.sampleIdInput.setText('')
        self.nameInput.setText('')
        self.locationInput.setText('')
        self.descriptionInput.setText('')
        self.creationDateInput.setDate(datetime.date.today())

    def AddButtonClicked(self):
        sampleToAdd = Sample(SampleId = self.sampleIdInput.text(), Name = self.nameInput.text(),
            Location = self.locationInput.text(), Description = self.descriptionInput.text(),
            CreationDate = self.creationDateInput.date().toPyDate(),  AssociatedInventoryItem = self.relatedInventoryItem.PrimaryKey)

        self.databaseManager.InsertSample(sampleToAdd)
        self.parent.RefreshSampleTable()
        self.close()

    def ClearButtonClicked(self):
        self.ClearInput()

class EditSamplesWindow(AddSampleWindow):
    def __init__(self, parent, databaseManager, relatedInventoryItem, selectedSample):
        super().__init__(parent, databaseManager, relatedInventoryItem)

        self.selectedSample = selectedSample
        
        self.DisplayCurrentSampleValues()

        self.addButton.disconnect()
        self.addButton.clicked.connect(self.SaveEdit)
        self.addButton.setText('Save')

    def DisplayCurrentSampleValues(self):
        self.sampleIdInput.setText(self.selectedSample.SampleId)
        self.nameInput.setText(self.selectedSample.Name)
        self.locationInput.setText(self.selectedSample.Location)
        self.descriptionInput.setText(self.selectedSample.Description)
        self.creationDateInput.setDate(self.GetDateFromString(self.selectedSample.CreationDate))

    def GetDateFromString(self, dateString):
        return datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
    
    def SaveEdit(self): 
        sampleToEdit = Sample(PrimaryKey = self.selectedSample.PrimaryKey, SampleId = self.sampleIdInput.text(), Name = self.nameInput.text(),
            Location = self.locationInput.text(), Description = self.descriptionInput.text(),
            CreationDate = self.creationDateInput.date().toPyDate(),  AssociatedInventoryItem = self.relatedInventoryItem.PrimaryKey)

        self.databaseManager.EditSample(sampleToEdit)
        self.parent.RefreshSampleTable()
        self.close()


def main():
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

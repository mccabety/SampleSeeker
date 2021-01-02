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

from DatabaseManager import DatabaseManager, InventoryItem

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)

class InventoryDisplayModel(QtGui.QStandardItemModel):
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
        return len(self._data[0])

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.dataHeaderLabels = ['PrimaryKey', 'ID', 'Age (Weeks)', 'Location',' Genotype', 'Birth Date', 'Sac Date']

        self.searchComboBox = QtWidgets.QComboBox()
        self.searchComboBox.addItems( [headerLabel for headerLabel in self.dataHeaderLabels if headerLabel != 'PrimaryKey'])

        self.searchTextBox = QtWidgets.QLineEdit()

        self.table = QtWidgets.QTableView()

        self.databaseManager = DatabaseManager()

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

        deleteButton = QtWidgets.QPushButton("Delete")
        deleteButton.clicked.connect(self.DeleteButtonClicked)

        buttonsLayout = QtWidgets.QHBoxLayout()
        buttonsLayout.addWidget(addButton)
        buttonsLayout.addWidget(editButton)
        buttonsLayout.addWidget(deleteButton)

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
            data.append([item.PrimaryKey, item.InventoryId, item.Age, item.Location, item.Genotype, item.BirthDate, item.SacDate])
 
        self.InventoryDisplayModel = InventoryDisplayModel(data)

        self.InventoryDisplayModel.setHorizontalHeaderLabels(self.dataHeaderLabels)
        self.InventoryDisplayModel.setVerticalHeaderLabels('' for item in data)

        self.table.setModel(self.InventoryDisplayModel)

    def closeEvent(self, event):
        print("Child window closed properly")

    def AddButtonClicked(self):
        self.showAddItemDialog()

    def DeleteButtonClicked(self):
        self.showDeleteItemDialog()

    def showAddItemDialog(self):
        self.addInventoryItemWindow = AddInventoryItemWindow(self, self.databaseManager)
        self.addInventoryItemWindow.show()
        self.RefreshInventoryTable()


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
                    Age = model.index(item.row(),2).data(), Location = model.index(item.row(),3).data(),
                    Genotype = model.index(item.row(),4).data(), BirthDate = model.index(item.row(),5).data(),
                    SacDate = model.index(item.row(),6).data() ) )
            
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
        self.sacDateLabel = QtWidgets.QLabel('Sac Date: ')
        self.sacDateInput = QtWidgets.QDateEdit()
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
        self.locationInput.setText('')
        self.genotypeInput.setText('')
        self.birthDateInput.setDate(datetime.date.today())
        self.sacDateInput.setDate(datetime.date.today())

    def AddButtonClicked(self):
        
        inventoryItemToAdd = InventoryItem(
            InventoryId = self.inventoryIdInput.text(), Age = 34, Location = self.locationInput.text(),
            Genotype = self.genotypeInput.text(), BirthDate = self.birthDateInput.date().toPyDate(), SacDate = self.sacDateInput.date().toPyDate())

        self.databaseManager.InsertInventoryItem(inventoryItemToAdd)
        self.parent.RefreshInventoryTable()
        self.close()

    def ClearButtonClicked(self):
        self.ClearInput()



def main():
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

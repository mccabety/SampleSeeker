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
        self.searchComboBox.addItems(self.dataHeaderLabels)

        self.searchTextBox = QtWidgets.QLineEdit()

        self.table = QtWidgets.QTableView()

        self.databaseManager = DatabaseManager()

        self.RefreshInventoryTable()

        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setColumnHidden(0, True)

        verticalBox = QtWidgets.QVBoxLayout()

        searchButton = QtWidgets.QPushButton("Search")
        clearSearchButton = QtWidgets.QPushButton("Clear")

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

    def AddButtonClicked(self):
        self.showAddItemDialog()

    def DeleteButtonClicked(self):
        self.showDeleteItemDialog()

    def showAddItemDialog(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Add Item Menu")
        msgBox.setText("Add Button Clicked")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:

            self.table
            print('OK clicked')

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
 
def main():
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

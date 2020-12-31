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

from DatabaseManager import DatabaseManager

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)

class InventoryModel(QtGui.QStandardItemModel):
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

        dataHeaderLabels = ['ID','Age (Weeks)','Location','Genotype', 'Birth Date', 'Sac Date']

        self.searchComboBox = QtWidgets.QComboBox()
        self.searchComboBox.addItems(dataHeaderLabels)

        self.searchTextBox = QtWidgets.QLineEdit()

        self.table = QtWidgets.QTableView()

        self.databaseManager = DatabaseManager()

        # Load inventory items from database 
        results = self.databaseManager.GetAllInventoryItems()
        data = []
        for entry in results:
            data.append([entry["Id"], entry["Age"], entry['Location'], entry['BirthDate'], entry['SacDate']])

        print(data)
 
        # todo: Remove sample Data
        ''' 
        data = [
          [3243, 9, 2, 'Z-43', datetime.datetime(2020,10,5),datetime.datetime(2020,11,21)],
          [5743, 1, 0,'Z-43', datetime.datetime(2020,11,2),],
          [4541, 5, 0,'Z-43', datetime.datetime(2020,3,6),datetime.datetime(2020,5,8)],
          [5544, 3, 2,'X-34', datetime.datetime(2020,5,12),],
          [8985, 8, 9, 'X-34', datetime.datetime(2020,9,4),datetime.datetime(2020,12,16)],
        ]
        '''

        self.inventoryModel = InventoryModel(data)

        self.inventoryModel.setHorizontalHeaderLabels(dataHeaderLabels)
        self.inventoryModel.setVerticalHeaderLabels('' for item in data)

        self.table.setModel(self.inventoryModel)
        self.table.resizeColumnsToContents()
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        verticalBox = QtWidgets.QVBoxLayout()

        searchButton = QtWidgets.QPushButton("Search")
        clearSearchButton = QtWidgets.QPushButton("Clear")

        searchLayout = QtWidgets.QHBoxLayout()
        searchLayout.addWidget(self.searchComboBox)
        searchLayout.addWidget(self.searchTextBox)
        searchLayout.addWidget(searchButton)
        searchLayout.addWidget(clearSearchButton)

        addButton = QtWidgets.QPushButton("Add")
        editButton = QtWidgets.QPushButton("Edit")
        deleteButton = QtWidgets.QPushButton("Delete")

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

def main():
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

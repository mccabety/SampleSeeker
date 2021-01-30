'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public LicenseStartupManager
'''

# StartupManager.py

import sys
import datetime

from SampleSeeker import MainWindow
from ConfigurationManager import ConfigurationManager, ConfigurationJsonWindow
from DatabaseManager import DatabaseManager, InventoryItem, Sample

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)

class StartupManager:
    def __init__(self):
        print("Startup Manager Constructor")
        self.app=QtWidgets.QApplication(sys.argv)
        self.configurationManager = ConfigurationManager()
        self.configurationJsonWindow = ConfigurationJsonWindow(self.configurationManager)


        if(self.configurationManager.DoesConfigurationFileExist()):
            print("Config file exists")
            if(self.configurationManager.IsConfigurationFileFormattedCorrectly()):
                print("Config file formatted correctly")
                self.LaunchMainWindow()
            else:
                print("Config file formatted incorrectly")
                sys.exit(0)
        else:
            print("Config file does NOT Exist")

            if(self.CreateNewConfigurationDialog() == QtWidgets.QMessageBox.Ok):
                print("Creating new config")
                self.configurationJsonWindow.exec()
                self.LaunchMainWindow()

            else:
                print("NOT creating new config")
                sys.exit(0)

        sys.exit(self.app.exec_())

    def CreateNewConfigurationDialog(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setWindowTitle("Warning")
        msgBox.setText("No configuration file found, would you like to create a new one?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        return msgBox.exec()

    def LaunchMainWindow(self):
        self.databaseManager = DatabaseManager(self.configurationManager)
        self.mainWindow = MainWindow(self.databaseManager)
        self.mainWindow.show()




class StartupManagerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Add New Sample')

def main():
    StartupManager()

if __name__ == '__main__':
    main()
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
from ConfigurationManager import ConfigurationManager
from DatabaseManager import DatabaseManager, InventoryItem, Sample

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)


class StartupManager:
    def __init__(self):
        print("Startup Manager Constructor")

        self.configurationManager = ConfigurationManager()
        self.databaseManager = DatabaseManager(self.configurationManager)

        self.app=QtWidgets.QApplication(sys.argv)
        self.mainWindow = MainWindow(self.databaseManager)

        self.LaunchMainWindow()

        # --- End Construction ---


        if(self.configurationManager.DoesConfigurationFileExist()):
            print("Config file exists")
        else:
            print("Config file does NOT")
    
    def LaunchMainWindow(self):
        self.mainWindow.show()
        self.app.exec_()



def main():
    StartupManager()

if __name__ == '__main__':
    main()
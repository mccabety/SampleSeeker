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

# ConfigurationManager

import json

import os.path
from os import path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QDialog)
class ConfigurationManager:
    def __init__(self):
        self.configurations = {}
        
        # Todo: Add error handling
        # Requires Configuration.json, see Configuration.json.example for format
        # with open('Configuration.json') as configuration:
        #    jsonFile = json.load(configuration)
        #    self.configurations = jsonFile['Configurations']
    '''
        self.configurationFieldKeys = {'ServerHostName',
                                       'ServerPortNumber',
                                       'DatabaseName',
                                       'ServerUsername',
                                       'ServerPassword'
                                       }
    '''
    def CreateDatabaseConfiguration(self, configurationValues):
        print(configurationValues)
        try:
            with open('Configuration.json', "x") as configurationFile:
                json.dump(configurationValues, configurationFile)
        except:
            print("Error: Could not write to configuration file")
    
    def GetDatabaseConfiguration(self):
        try:
            with open('Configuration.json') as configuration:
                databaseConfigurations = json.load(configuration)['Configurations']['DatabaseConfigurations']   
                return databaseConfigurations
        except:
            print("Could not retrieve database configurations")
            return None

    def DoesConfigurationFileExist(self):
        return path.exists('Configuration.json')
    
    def IsConfigurationFileFormattedCorrectly(self):
        try:
            with open('Configuration.json') as configuration:
                jsonFile = json.load(configuration)

                if('Configurations' in jsonFile):
                    databaseConfigurations = jsonFile['Configurations']['DatabaseConfigurations']                    

                    if( 'ServerHostName' in databaseConfigurations and
                        'ServerPortNumber' in databaseConfigurations and
                        'DatabaseName' in databaseConfigurations and
                        'ServerUsername'in databaseConfigurations and
                        'ServerPassword' in databaseConfigurations):
                        return True
                    else:
                        return False
                else:
                    return False
        except:
            print("An error occured, could not start Sample Seeker")


                
if __name__ == '__main__':
    configurationManager = ConfigurationManager()
    databaseConfigurations = configurationManager.GetDatabaseConfiguration()
    
    for value in databaseConfigurations.values():
        print ("Value: " + str(value))
        

class ConfigurationJsonWindow(QDialog):
    def __init__(self, configurationManager):
        super().__init__()

        self.configurationManager = configurationManager

        self.verticalBox = QtWidgets.QVBoxLayout()

        self.serverHostNameSection = QtWidgets.QHBoxLayout()
        self.serverHostNameLabel = QtWidgets.QLabel('Server Host Name: ')
        self.serverHostNameInput = QtWidgets.QLineEdit()
        self.serverHostNameSection.addWidget(self.serverHostNameLabel)
        self.serverHostNameSection.addWidget(self.serverHostNameInput)

        self.serverPortNumberSection = QtWidgets.QHBoxLayout()
        self.serverPortNumberLabel = QtWidgets.QLabel('Server Port Number: ')
        self.serverPortNumberInput = QtWidgets.QLineEdit()
        self.serverPortNumberSection.addWidget(self.serverPortNumberLabel)
        self.serverPortNumberSection.addWidget(self.serverPortNumberInput)

        self.serverUserNameSection = QtWidgets.QHBoxLayout()
        self.serverUserNameLabel = QtWidgets.QLabel('Server User Name: ')
        self.serverUserNameInput = QtWidgets.QLineEdit()
        self.serverUserNameSection.addWidget(self.serverUserNameLabel)
        self.serverUserNameSection.addWidget(self.serverUserNameInput)

        self.serverUserPasswordSection = QtWidgets.QHBoxLayout()
        self.serverUserPasswordLabel = QtWidgets.QLabel('Server Password: ')
        self.serverUserPasswordInput = QtWidgets.QLineEdit()
        self.serverUserPasswordSection.addWidget(self.serverUserPasswordLabel)
        self.serverUserPasswordSection.addWidget(self.serverUserPasswordInput)

        self.databaseNameSection = QtWidgets.QHBoxLayout()
        self.databaseNameLabel = QtWidgets.QLabel('Database Name: ')
        self.databaseNameInput = QtWidgets.QLineEdit()
        self.databaseNameSection.addWidget(self.databaseNameLabel)
        self.databaseNameSection.addWidget(self.databaseNameInput)

        self.buttonSection = QtWidgets.QHBoxLayout()
        self.saveButton = QtWidgets.QPushButton("Create")
        self.saveButton.clicked.connect(self.createConfiguration)

        self.clearButton = QtWidgets.QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearInput)

        self.buttonSection.addWidget(self.saveButton)
        self.buttonSection.addWidget(self.clearButton)



        self.verticalBox.addLayout(self.serverHostNameSection)
        self.verticalBox.addLayout(self.serverPortNumberSection)
        self.verticalBox.addLayout(self.serverUserNameSection)
        self.verticalBox.addLayout(self.serverUserPasswordSection)
        self.verticalBox.addLayout(self.databaseNameSection)

        self.verticalBox.addLayout(self.buttonSection)

        self.setLayout(self.verticalBox)

        self.setGeometry(300, 300, 400, 500)
        self.setWindowTitle('Create Configuration')
        
    def createConfiguration(self):
        configuration = {
                "Configurations" :
                {
                    "DatabaseConfigurations":
                        {
                        "ServerHostName": self.serverHostNameInput.text(),
                        "ServerPortNumber": self.serverPortNumberInput.text(),
                        'ServerUsername' : self.serverUserNameInput.text() ,
                        'ServerPassword' : self.serverUserPasswordInput.text(),
                        'DatabaseName' : self.databaseNameInput.text()
                        }
                }
            }
            
        self.configurationManager.CreateDatabaseConfiguration(configuration)

        self.close()

    def clearInput(self):
        self.serverHostNameInput.setText('')
        self.serverPortNumberInput.setText('')
        self.serverUserNameInput.setText('')
        self.serverUserPasswordInput.setText('')
        self.databaseNameInput.setText('')
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

class ConfigurationManager:
    def __init__(self):
        self.configurations = {}
        
        # Todo: Add error handling
        # Requires Configuration.json, see Configuration.json.example for format
        with open('Configuration.json') as configuration:
            jsonFile = json.load(configuration)
            self.configurations = jsonFile['Configurations']
        
    
    def GetDatabaseConfiguration(self):
        return self.configurations['DatabaseConfigurations']

    def DoesConfigurationFileExist(self):
        return path.exists('Configuration.json')

                
if __name__ == '__main__':
    configurationManager = ConfigurationManager()
    databaseConfigurations = configurationManager.GetDatabaseConfiguration()
    
    for value in databaseConfigurations.values():
        print ("Value: " + str(value))
        


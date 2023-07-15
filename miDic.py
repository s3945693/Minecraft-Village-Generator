
import csv

class minecraftItems:
    def __init__(self, name ='none', id = 'none', version = 'none'):
        self.name = name[0]
        self.inGameID = name #minecraft:blockName
        self.id = id #block id
        self.version = version #colours
    def __str__(self):
        print(self.name)
        return ''

class dicOfItems:
    def __init__(self):
        self.items = {}
   
    def createDic(self):
        with open('minecraft_ids.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                self.items[line[1]] = minecraftItems(line[0].split('('), line[1], line[2])
    
    def printDic(self):
        for key in self.items:
            print(key, self.items[key])


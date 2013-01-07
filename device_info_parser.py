#! /usr/bin/env python
#coding=utf-8
import os
class DeviceInfo:
    def __init__(self,brand = None, model = None):
        self.brand = brand
        self.model = model
        
        self.modelKey = 'ro.product.model'
        self.brandKey = 'ro.product.brand'
        
        self.modelKeyLen = len(self.modelKey)
        self.brandKeyLen = len(self.brandKey)
    def getDisplayName(self):
        if self.brand and self.model:
            return self.brand + ' ' + self.model
        return 'Unknow' 

class DeviceInfoParser:
    def __init__(self, infoFilePath):
        self.deviceInfo = DeviceInfo()
        self.parse(infoFilePath)
    
    def parse(self,infoFilePath):
        f = open(infoFilePath)
        info = self.deviceInfo
        try:
            allLines = f.readlines()
            for line in allLines:
                line = line.strip()
                if info.model == None or info.brand == None:
                    start = line.find(info.brandKey)
                    if start > -1:
                        info.brand = line[start+ info.brandKeyLen + 1:]
                    else:
                        start = line.find(info.modelKey)
                        if start > -1:
                            info.model = line[start+ info.modelKeyLen + 1:]
        finally:
            f.close()
            
if __name__ == '__main__':
    deviceInfoParser = DeviceInfoParser('build.prop')
    print deviceInfoParser.deviceInfo.getDisplayName()
            
            
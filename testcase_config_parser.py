#! /usr/bin/env python
#coding=utf-8
import xml.dom.minidom
import time
import ConfigParser
import os
class TestSuitInfo:
    def __init__(self, name, repeat = 1):
        self.name = name
        self.testCaseArray = []
        if repeat == None:
            repeat = 1
        self.repeat = int(repeat)
    def appendTestCase(self, caseName):
        if caseName != None:
            self.testCaseArray.append(caseName)
        else:
            print 'test case method name must not be empty'

class TestConfigInfo:
    def __init__(self):
        self.testPkg = None
        self.testProPath = None
        self.testProName = None
        
        
        self.testedPkg = None        
        self.testedProPath = None
        self.testedProName = None
        
        self.targetType = 'debug'
        self.exector = 'unknow'
        
        
        self.customInfo = None
    def loadConfig(self,file):
        cf = ConfigParser.ConfigParser()
        cf.read(file)        
        
        optKey = 'tested_proj'
        self.testedPkg = cf.get(optKey, 'package')
        self.testedPath = cf.get(optKey, 'path')
        self.testedProName = cf.get(optKey, 'name')
        
        optKey = 'test_proj'
        self.testPkg = cf.get(optKey, 'package')
        self.testPath = cf.get(optKey, 'path')
        self.testProName = cf.get(optKey, 'name')
        
        self.customInfo = cf.items("custom_info")
        
        targetType = cf.get('custom_info', 'targetType')
        exector = cf.get('custom_info', 'exector')
        if targetType:
            self.targetType = targetType
        if exector:
            self.exector = exector
    
    def getTestApkPath(self):
        if  self.testPath and self.testProName:
            return self.testPath + r'\\bin\\' + self.testProName + '-' + self.targetType + '.apk'
        return None
    def getTestedApkPath(self):
        if  self.testedPath and self.testedProName:
            return self.testedPath + r'\\bin\\' + self.testedProName + '-' + self.targetType + '.apk'
        return None
    
    def getTestProjectBuildXml(self):
        if  self.testPath:
            return self.testPath + r'\\build.xml';
        return None
class TestCaseConfigInfo:
    def __init__(self):
        self.testSuits = []


class ReportInfo:
    def __init__(self):
        self.exector = 'unknow'
        self.device = 'unknow'
        self.startTime =   time.time()        
          
class TestCaseConfigParser:
    def __init__(self,file=None):
        self.cofigFile = file
        self.testCaseConfig = TestCaseConfigInfo()        
    def doParse(self):
        if(self.cofigFile == None):
            print 'TestCase config file must not be null'
            return
        dom = xml.dom.minidom.parse(self.cofigFile)        
        testInfo = dom.documentElement
       
        pkgInfo = testInfo.getElementsByTagName('classes')
        if len(pkgInfo) > 0:
            pkgInfo = pkgInfo[0]            
        domTestSuits = pkgInfo.getElementsByTagName('class')
        
        for domTestSuit in domTestSuits:
            tsName = domTestSuit.getAttribute('name')
            repeatValue = domTestSuit.getAttribute('repeat')          
            testSuit = TestSuitInfo(tsName, repeatValue)     
            domMethod = domTestSuit.getElementsByTagName('methods')
            if len(domMethod) > 0:
                domIncludes = domMethod[0].getElementsByTagName('include')
                for domInclude in domIncludes:
                    testSuit.appendTestCase(domInclude.getAttribute('name'))
            self.testCaseConfig.testSuits.append(testSuit)        
                
             
if __name__ == '__main__':     
    parser = TestCaseConfigParser('testcase_config.xml')
    parser.doParse()   
    print parser.testCaseConfig.testSuits[0].name
    
    tc = TestConfigInfo()
    tc.loadConfig('test.conf')
    print tc.testedPkg
    print tc.testedPath
    print tc.testPkg
    print tc.testPath
    print tc.getTestProjectBuildXml()
            
        
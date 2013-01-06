#! /usr/bin/env python
#coding=utf-8
import xml.dom.minidom
import time
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
    
        
class TestCaseConfigInfo:
    def __init__(self):
        self.appPkg = None
        self.testPkg = None
        self.appPath = None
        self.testAppPath = None
        self.testSuits = []


class ReportInfo:
    def __init__(self):
        self.exector = 'unknow'
        self.startTime =   time.time()        
          
class TestCaseConfigParser:
    def __init__(self,file=None):
        self.cofigFile = file
        self.testCaseConfig = TestCaseConfigInfo()
        self.reportInfo = ReportInfo()
    def doParse(self):
        if(self.cofigFile == None):
            print 'TestCase config file must not be null'
            return
        dom = xml.dom.minidom.parse(self.cofigFile)        
        testInfo = dom.documentElement        
        exector = testInfo.getAttribute('exector')
        if exector != None and len(exector) > 0:
            self.reportInfo.exector =  exector
        pkgInfo = testInfo.getElementsByTagName('classes')
        if len(pkgInfo) > 0:
            pkgInfo = pkgInfo[0]
            appPkg = pkgInfo.getAttribute('appPkg')
            if len(appPkg) > 0:
                self.testCaseConfig.appPkg = appPkg
            else:
                 print 'appPkg attri of the class tag must not be empty'

            testPkg = pkgInfo.getAttribute('testPkg')
            if len(testPkg) > 0:
                self.testCaseConfig.testPkg = testPkg
            else:
                 print 'testPkg attri of the class tag must not be empty'
                
            appPath = pkgInfo.getAttribute('appPath')
            if len(appPkg) > 0:
                self.testCaseConfig.appPath = appPath
            else:
                 print 'appPath attri of the class tag must not be empty'
            
            testAppPath = pkgInfo.getAttribute('testAppPath')
            if len(testAppPath) > 0:
                self.testCaseConfig.testAppPath = testAppPath
            else:
                print 'testAppPath attri of the class tag must not be empty'

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
    print parser.testCaseConfig.appPkg
    print parser.testCaseConfig.testPkg
    print parser.testCaseConfig.testSuits[0].name
            
        
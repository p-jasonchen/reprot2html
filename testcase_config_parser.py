#! /usr/bin/env python
#coding=utf-8
import xml.dom.minidom

class TestSuitInfo:
    def __init__(self, name):
        self.name = name
        self.testCaseArray = []
    def appendTestCase(self, caseName):
        if caseName != None:
            self.testCaseArray.append(caseName)
        else:
            print 'test case method name must not be empty'
    
        
class TestCaseConfigInfo:
    def __init__(self):
        self.appPkg = None
        self.testPkg = None
        self.testSuits = []
        
class TestCaseConfigParser:
    def __init__(self,file=None):
        self.cofigFile = file
        self.testCaseConfig = TestCaseConfigInfo()
    def doParse(self):
        if(self.cofigFile == None):
            print 'TestCase config file must not be null'
            return
        dom = xml.dom.minidom.parse(self.cofigFile)        
        pkgInfo = dom.documentElement;
        if pkgInfo.nodeName == 'classes':
            appPkg = pkgInfo.getAttribute('appPkg')
            if len(appPkg) > 0:
                self.testCaseConfig.appPkg = appPkg
            else:
                print 'package name of the apk to test must not be empty'

            testPkg = pkgInfo.getAttribute('testPkg')
            if len(testPkg) > 0:
                self.testCaseConfig.testPkg = testPkg
            else:
                print 'package name of the test apk  must not be empty'

        domTestSuits = pkgInfo.getElementsByTagName('class')
        for domTestSuit in domTestSuits:
            tsName = domTestSuit.getAttribute('name')
            testSuit = TestSuitInfo(tsName)     
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
            
        
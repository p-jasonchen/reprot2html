#! /usr/bin/env python
#coding=utf-8
import testcase_config_parser
import adb_action
import result_parser
import html_creator
import os

class TestControler:   
    def __init__(self):
        self.dstPath =  os.path.join(os.getcwd(), 'result')    
        self.Report_File_Array = []
    def initPCEnv(self):    
        dstPath = self.dstPath
        if not os.path.exists(dstPath):
            os.mkdir(dstPath)       
        else:
            paths = os.listdir(dstPath)
            for path in paths:
                filePath = os.path.join(dstPath, path)
                if os.path.isfile(filePath) :
                    try: os.remove(filePath)
                    except os.error:
                     pass
    
    def initPhoneEvn(self, configInfo):
        appPkg = configInfo.appPkg
        testPkg = configInfo.testPkg
        appPath = configInfo.appPath
        testAppPath = configInfo.testAppPath
        
        ret = True
        
        action = adb_action.AdbAction()        
        if appPkg != None:
            print 'uninstalling package ' + appPkg + ' ...'
            action.executeUninstallPkg(appPkg)
        else:
            ret = False
            
        if testPkg != None:
            print 'uninstalling package ' + testPkg + ' ...'
            action.executeUninstallPkg(testPkg)
        else:
            ret = False
            
        if appPath != None:
            print 'installing app  ' + appPath + ' ...'
            action.executeInstallPkg(appPath)
        else:
            ret = False
        
        if testAppPath != None:
            print 'uninstalling app ' + testAppPath + ' ...'
            action.executeInstallPkg(testAppPath)
        else:
            ret = False
        
        return ret
        

        
    def doTest(self):
        self.initPCEnv()        
        parser = testcase_config_parser.TestCaseConfigParser('testcase_config.xml')
        parser.doParse()
        configInfo = parser.testCaseConfig
        
        ret = self.initPhoneEvn(configInfo)
        if not ret:
            print 'init phone env failed...'
            return
        adbActionArray = []
        if configInfo.testPkg != None:
            testRunner = configInfo.testPkg + '/com.zutubi.android.junitreport.JUnitReportTestRunner'
            for testSuit in configInfo.testSuits:
                repeat = testSuit.repeat               
                testCaseArray = testSuit.testCaseArray
                if len(testCaseArray) == 0:
                    for i in range(0, repeat):
                        action = adb_action.AdbAction(testSuit.name, testRunner)   
                        adbActionArray.append(action)
                else:
                    for case in testCaseArray:
                        for i in range(0, repeat):
                            action = adb_action.AdbAction(testSuit.name + '#' + case, testRunner)
                            adbActionArray.append(action)

            print 'adbActionArray length:\t' + str(len(adbActionArray))
            for action in adbActionArray:
                action.executeTest()
                self.Report_File_Array.append(action.executePullTestResultFile())

    def createHtmlResult(self):
        resultParser = result_parser.ResultParser(self.dstPath)        
        resultParser.traverseAllResult(self.Report_File_Array)  
      
        htmlCreator = html_creator.HtmlCreator(resultParser.testSuitMap)
        htmlCreator.saveHtmlDoc()
        

if __name__ == '__main__':
    controler = TestControler()
    controler.doTest()
    controler.createHtmlResult()
    print 'test finished...'
    
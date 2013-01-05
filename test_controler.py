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
    
    def initEnv(self):    
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
    def doTest(self):
        self.initEnv()        
        parser = testcase_config_parser.TestCaseConfigParser('testcase_config.xml')
        parser.doParse()
        configInfo = parser.testCaseConfig
        adbActionArray = []
        if configInfo.testPkg != None:
            testRunner = configInfo.testPkg + '/com.zutubi.android.junitreport.JUnitReportTestRunner'
            for testSuit in configInfo.testSuits:
                testCaseArray = testSuit.testCaseArray
                if len(testCaseArray) == 0:
                    action = adb_action.AdbAction(testSuit.name, testRunner)   
                    adbActionArray.append(action)
                else:
                    for case in testCaseArray:
                        action = adb_action.AdbAction(testSuit.name + '#' + case, testRunner)
                        adbActionArray.append(action)

            for action in adbActionArray:
                action.executeTest()
                action.executePullTestResultFile()

    def createHtmlResult(self):
        resultParser = result_parser.ResultParser(self.dstPath)        
        resultParser.traverseAllResult()  
      
        htmlCreator = html_creator.HtmlCreator(resultParser.testSuitMap)
        htmlCreator.saveHtmlDoc()
        

if __name__ == '__main__':
    controler = TestControler()
    controler.doTest()
    controler.createHtmlResult()
    
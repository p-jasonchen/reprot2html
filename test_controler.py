#! /usr/bin/env python
#coding=utf-8
import testcase_config_parser
import adb_action
import result_parser
import html_creator
import os
import sys
import device_info_parser

mainPath = sys.path[0]

class TestControler:   
    def __init__(self):        
        print 'path:    ' + mainPath
        #print 'pwd:    ' + os.getcwd()
        self.dstPath =  os.path.join(mainPath, 'result')    
        self.Report_File_Array = []
        self.deviceName = None
        self.serialNo = None
        self.reportInfo = None
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
       
        self.initPCEnv()        
        
    def checkDeviceAttached(self):
        action = adb_action.AdbAction()
        serialNo = action.getDeviceAttach()
        devName = 'Unkonw'  
       
        if serialNo != None:
             print 'device serialNo is:' + serialNo
             devFileName = 'build.prop'
             ok = action.getAttachDeviceDetail(serialNo,devFileName)
             if ok:
                 devParser = device_info_parser.DeviceInfoParser(devFileName)
                 print 'get device info file successfully'
                 self.deviceName = devParser.deviceInfo.getDisplayName()
                 print 'device name is ' + self.deviceName
             else:
                 print 'failed to get device info file '
        else:
            print 'no device found ! Make sure at least one device attach'        
        self.serialNo = serialNo
        return serialNo
        
    def initPhoneEvn(self, configInfo):
        if self.checkDeviceAttached() == None:
            return
        appPkg = configInfo.appPkg
        testPkg = configInfo.testPkg
        appPath = configInfo.appPath
        testAppPath = configInfo.testAppPath
        
        
        ret = True
        serialNo = self.serialNo
        action = adb_action.AdbAction()
        if appPkg != None:
            print 'uninstalling package ' + appPkg + ' ...'
            action.executeUninstallPkg(appPkg, serialNo)
        else:
            ret = False
            
        if testPkg != None:
            print 'uninstalling package ' + testPkg + ' ...'
            action.executeUninstallPkg(testPkg, serialNo)
        else:
            ret = False
            
        if appPath != None:
            print 'installing app  ' + appPath + ' ...'
            action.executeInstallPkg(appPath, serialNo)
        else:
            ret = False
        
        if testAppPath != None:
            print 'installing app ' + testAppPath + ' ...'
            action.executeInstallPkg(testAppPath, serialNo)
        else:
            ret = False
        
        return ret
        

        
    def doTest(self):        
        configFile = os.path.join(mainPath, 'testcase_config.xml')
        parser = testcase_config_parser.TestCaseConfigParser(configFile)
        parser.doParse()
        configInfo = parser.testCaseConfig
        self.reportInfo = parser.reportInfo
        ret = self.initPhoneEvn(configInfo)
        self.reportInfo.device= self.deviceName
        self.reportInfo.serialNo = self.serialNo
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

            print 'total test case  size is:\t' + str(len(adbActionArray))
            print 'starting to exec test ...'
            curCase = 1
            for action in adbActionArray:
                print 'executing test case ' + str(curCase)
                curCase += 1
                action.executeTest(self.serialNo)
                self.Report_File_Array.append(action.executePullTestResultFile(self.serialNo))

    def createHtmlResult(self):
        resultParser = result_parser.ResultParser(self.dstPath)        
        resultParser.traverseAllResult(self.Report_File_Array)  
      
        htmlCreator = html_creator.HtmlCreator(resultParser.testSuitMap, self.reportInfo)
        htmlCreator.saveHtmlDoc()
        

if __name__ == '__main__':
    controler = TestControler()
    controler.doTest()
    controler.createHtmlResult()
    print 'test finished...'    
    
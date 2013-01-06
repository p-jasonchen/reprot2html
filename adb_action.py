#! /usr/bin/env python
#coding=utf-8

import subprocess
import os

class AdbAction:
    #adb 工具所在目录
    ANDROID_PLATFORM_TOOLS_HOME = "D:/develop/android-sdk-windows/platform-tools/"
    #avd 管理工具所在目录
    ANDROID_TOOLS_HOME = "D:/develop/android-sdk-windows/tools/"
    
    REPORT_FILE_COUNT = 1  
    
    def __init__(self, testSuit = None, testRunner = None):
        self.testSuit = testSuit
        self.testRunner = testRunner        
        
    def executeTest(self):
        commandLine = [AdbAction.ANDROID_PLATFORM_TOOLS_HOME + 'adb',
                        'shell',
                        'am',
                        'instrument',
                        '-w',
                        '-e',
                        'class',
                        self.testSuit,
                        self.testRunner]         
        p = subprocess.Popen(commandLine, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        p.wait()
       

    def showProcessLog(self, p):
         while p.poll() == None:
            line = p.stdout.readline()
            if(line != None and len(line)>3):
                print line                               
            print p.stdout.read()
    
    def executePullTestResultFile(self):
        dstPath =  os.path.join(os.getcwd(), 'result')   
        if not os.path.exists(dstPath):
            print 'sub directory named "result" must  exist,make sure it and retry'
            return
        
        dstFile =  os.path.join(dstPath, 'junit-report' + str(AdbAction.REPORT_FILE_COUNT) + '.xml')       
        AdbAction.REPORT_FILE_COUNT +=  1
        commandLine = [AdbAction.ANDROID_PLATFORM_TOOLS_HOME + 'adb',                            
                            'pull',
                            '/data/data/com.example.demoapp/files/junit-report.xml',
                            dstFile]
        p = subprocess.Popen(commandLine, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        p.wait()
        return dstFile
    
    def executeUninstallPkg(self,pkg):
        commandLine = [AdbAction.ANDROID_PLATFORM_TOOLS_HOME + 'adb',                            
                            'uninstall', pkg]
        p = subprocess.Popen(commandLine, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        self.showProcessLog(p)
        p.wait()
    
    def executeInstallPkg(self,apkPath):
        commandLine = [AdbAction.ANDROID_PLATFORM_TOOLS_HOME + 'adb',                            
                            'install', apkPath]
        p = subprocess.Popen(commandLine, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        self.showProcessLog(p)
        p.wait()
                                
if __name__ == '__main__':
    action = AdbAction('com.example.demoapp.test.TestOperation','com.example.demoapp.test/com.zutubi.android.junitreport.JUnitReportTestRunner')
    action.executeTest()
    action.executePullTestResultFile()
        
        


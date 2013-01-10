#! /usr/bin/env python
#coding=utf-8

import subprocess
import os
import test_controler

class AdbAction:
	#adb 工具所在目录
	ANDROID_PLATFORM_TOOLS_HOME = "D:/develop/android-sdk-windows/platform-tools/"
	#avd 管理工具所在目录
	ANDROID_TOOLS_HOME = "D:/develop/android-sdk-windows/tools/"
	
	REPORT_FILE_COUNT = 1  
	
	def __init__(self, testSuit = None, testRunner = None):
		self.testSuit = testSuit
		self.testRunner = testRunner		
		
	def executeTest(self, serialNo):
		commandLine = [AdbAction.ANDROID_PLATFORM_TOOLS_HOME + 'adb',
					   '-s',
					   serialNo,
						'shell',
						'am',
						'instrument',
						'-w',
						'-e',
						'class',
						self.testSuit,
						self.testRunner]	
		#print 'cmd:\t' + ' '.join(commandLine)	 
		p = subprocess.Popen(commandLine, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		self.showProcessLog(p)
		p.wait()
	   

	def showProcessLog(self, p):
		 while p.poll() == None:
			line = p.stdout.readline()
			if(line != None and len(line.strip())>0):
				print line			  
			#print p.stdout.read()	
		
	def executePullTestResultFile(self, serialNo):
		dstPath =  os.path.join(test_controler.mainPath, 'result')   
		if not os.path.exists(dstPath):
			print 'sub directory named "result" must  exist,make sure it and retry'
			return
		
		dstFile =  os.path.join(dstPath, 'junit-report' + str(AdbAction.REPORT_FILE_COUNT) + '.xml')	   
		AdbAction.REPORT_FILE_COUNT +=  1
		commandLine = [AdbAction.ANDROID_PLATFORM_TOOLS_HOME + 'adb', 
					   '-s',
					   serialNo,						   
							'pull',
							'/data/data/com.example.demoapp/files/junit-report.xml',
							dstFile]
		p = subprocess.Popen(commandLine, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		p.wait()
		return dstFile
	
	def executeUninstallPkg(self,pkg, serialNo):
		commandLine = [AdbAction.ANDROID_PLATFORM_TOOLS_HOME + 'adb',	 
					   '-s',
					   serialNo,					   
							'uninstall', pkg]
		p = subprocess.Popen(commandLine, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		self.showProcessLog(p)
		p.wait()
	
	def executeInstallPkg(self,apkPath, serialNo):
		commandLine = [AdbAction.ANDROID_PLATFORM_TOOLS_HOME + 'adb', 
					   '-s',
					   serialNo,						   
							'install', apkPath]
		p = subprocess.Popen(commandLine, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		self.showProcessLog(p)
		p.wait()
	
	
	def getDeviceAttach(self):
		commandLine = [AdbAction.ANDROID_PLATFORM_TOOLS_HOME + 'adb','devices']
		serialNo = None
		p = subprocess.Popen(commandLine, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		while p.poll() == None:
			line = p.stdout.readline()
			if(line != None):
				line  = line.strip()
				end = line.find('device')
				if end >= 0 and  end + 6 == len(line):
					serialNo = line[0: end].strip()
					break					
		p.wait()
		return serialNo
	
	def getAttachDeviceDetail(self, serialNo, savePath):
		commandLine = [AdbAction.ANDROID_PLATFORM_TOOLS_HOME + 'adb','-s', serialNo,
					   'pull', '/system/build.prop', savePath]		
		p = subprocess.Popen(commandLine, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		ok = True
		while p.poll() == None:
		   line = p.stdout.readline()
		   if(line != None):				
				end = line.find('not exist')
				if end >= 0:
					ok = False					
					break					
		p.wait()
		return ok
if __name__ == '__main__':   
	action = AdbAction('com.example.demoapp.test.TestOperation','com.example.demoapp.test/com.zutubi.android.junitreport.JUnitReportTestRunner')
	#action.executeTest('016B23BA0301E01B')
	#action.executePullTestResultFile('016B23BA0301E01B')
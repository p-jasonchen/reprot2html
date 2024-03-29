#! /usr/bin/env python
#coding=utf-8
import testcase_config_parser
import adb_action
import result_parser
import html_creator
import os
import sys
import shutil
import device_info_parser

mainPath = os.getcwd()

class TestControler:   
	def __init__(self):			
		print 'path:	' + mainPath		
		self.dstPath =  os.path.join(mainPath, 'result')
		self.Report_File_Array = []
		self.deviceName = None
		self.serialNo = None	
		self.testConfigInfo = None
		self.configInfo = None
		self.reportInfo = testcase_config_parser.ReportInfo()	
		self.initPCEnv()
		self.ok = True
		
		tc = testcase_config_parser.TestConfigInfo()
		ok = tc.loadConfig(os.path.join(mainPath,'test.conf'))
		if ok:
			self.testConfigInfo = tc		
		self.ok = self.ok and ok
		
		configFile = os.path.join(mainPath, 'testcase_config.xml')
		parser = testcase_config_parser.TestCaseConfigParser(configFile)
		ok = parser.doParse()
		if ok:
			self.configInfo = parser.testCaseConfig		
		self.ok = self.ok and ok
		
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
			print 'no device found ! Make sure at least one device attached'		
		self.serialNo = serialNo
		return serialNo
	
	
	
	def compileTestProject(self):
		compiler = adb_action.ProjectCompileAction(self.testConfigInfo)
		return compiler.doCompile()	
	
		
	def initPhoneEvn(self):
		if self.checkDeviceAttached() == None:
			return
		
		tc = self.testConfigInfo
		testPkg = tc.testPkg
		testedPkg = tc.testedPkg		
		
		ret = True
		serialNo = self.serialNo
		action = adb_action.AdbAction()
		if testedPkg != None:
			print 'uninstalling tested package ' + testedPkg + ' ...'
			action.executeUninstallPkg(testedPkg, serialNo)
		else:
			ret = False
			
		if testPkg != None:
			print 'uninstalling test package ' + testPkg + ' ...'
			action.executeUninstallPkg(testPkg, serialNo)
		else:
			ret = False
		
		testedApk = tc.getTestedApkPath()	
		if testedApk != None:
			print 'installing tested app  ' + testedApk + ' ...'
			action.executeInstallPkg(testedApk, serialNo)
		else:			
			ret = False
		
		testApk = tc.getTestApkPath()
		if testApk != None:
			print 'installing test app ' + testApk + ' ...'
			action.executeInstallPkg(testApk, serialNo)
		else:
			ret = False
		
		return ret
		

		
	def doTest(self):
		if not self.ok:
			return
		ret = self.initPhoneEvn()		
		if not ret:
			print 'init phone env failed...'
			return
		adbActionArray = []
		configInfo = self.configInfo
		if self.testConfigInfo.testPkg != None:
			testRunner = self.testConfigInfo.testPkg + '/com.zutubi.android.junitreport.JUnitReportTestRunner'
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
		   
			self.createHtmlResult() 
	def createHtmlResult(self):
		resultParser = result_parser.ResultParser(self.dstPath)		
		resultParser.traverseAllResult(self.Report_File_Array)  
		
		reportInfo = self.reportInfo
		
		reportInfo.device = self.deviceName
		reportInfo.serialNo = self.serialNo
		reportInfo.exector = self.testConfigInfo.exector
	  
		htmlCreator = html_creator.HtmlCreator(resultParser.testSuitMap, reportInfo)
		htmlCreator.saveHtmlDoc()
		
		self.copyCssFileToDst()
		
	def copyCssFileToDst(self):
		fileName = 'report.css'
		cssFile  = os.path.join(os.sys.path[0],fileName)
		dstFile = os.path.join(mainPath,fileName)
		shutil.copy(cssFile,  dstFile)
		
if __name__ == '__main__':
	controler = TestControler()
	controler.doTest()	
	print 'test finished...'	
	
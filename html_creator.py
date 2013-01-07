#! /usr/bin/env python
#coding=utf-8
import xml.dom.minidom
import codecs
import result_parser
import time
import os
import test_controler
import re
class NodeInfo:
	def __init__(self,tag, value = None,attrArray = None):
		self.tag = tag
		self.attrArray = attrArray
		self.value = value
	
class HtmlCreator:
	def __init__(self, testSuitMap, reportInfo):
		self.testSuitMap = testSuitMap
		self.reportInfo = reportInfo
		impl = xml.dom.minidom.getDOMImplementation()
		dom = impl.createDocument(None, 'html', None)
		body = dom.createElement('body')
		self.dom = dom


		headNode = dom.createElement('head');
		cssNode = dom.createElement('link');
		cssNode.setAttribute('rel', 'Stylesheet');
		cssNode.setAttribute('type', 'text/css');
		cssNode.setAttribute('href', 'report.css');

		headNode.appendChild(cssNode)

		dom.documentElement.appendChild(headNode)
		dom.documentElement.appendChild(body)
		self.body = body

		self.setReportInfo(reportInfo)
		self.setAllCaseTestCaseTable()
		self.setFailedCaseTestCaseTable()
		self.setPassedCaseTestCaseTable()

	def createNode(self,info):
		tag = info.tag
		attrArray = info.attrArray
		value = info.value
		dom = self.dom
		if tag != None and len(tag) > 0:
			node = dom.createElement(tag)
			if attrArray and len(attrArray) > 0:
				for attr in attrArray:
					node.setAttribute(attr['name'], attr['value'])
			if value != None:				
				value = str(value)
				text = dom.createTextNode(value)
				node.appendChild(text)
			return node
		else:
			print 'node tag name must not be empty'
			return None
		
	def setReportInfo(self, reportInfo):
		dom = self.dom
		tableNode = self.createNode(NodeInfo('table',None,[{'name':'class','value':'report_info'}]))
		tr = self.createNode(NodeInfo('tr'))
		
		
		th = self.createNode(NodeInfo('th','Phone'))
		tr.appendChild(th)
		
		th = self.createNode(NodeInfo('th','Test Executor'))
		tr.appendChild(th)
		
		th = self.createNode(NodeInfo('th','Start Time'))
		tr.appendChild(th)
		
		th = self.createNode(NodeInfo('th','End Time'))
		tr.appendChild(th)
		
		th = self.createNode(NodeInfo('th','Time Consumed(second)'))
		tr.appendChild(th)
		
		tableNode.appendChild(tr)
		
		tr = self.createNode(NodeInfo('tr'))
		
		th = self.createNode(NodeInfo('td',reportInfo.device))
		tr.appendChild(th)
		
		th = self.createNode(NodeInfo('td',reportInfo.exector))
		tr.appendChild(th)
		
		startTimeTxt = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(reportInfo.startTime))
		th = self.createNode(NodeInfo('td',startTimeTxt))
		tr.appendChild(th)
		
		endTime = time.time()
		endTimeTxt = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(endTime))
		th = self.createNode(NodeInfo('td',endTimeTxt))
		tr.appendChild(th)
		
		timeConsumed = endTime - reportInfo.startTime
		th = self.createNode(NodeInfo('td',timeConsumed))
		print 'test consumes time :' + str(timeConsumed)
		tr.appendChild(th)
		
		tableNode.appendChild(tr)
		
		self.body.appendChild(tableNode)
		
	def setAllCaseTestCaseTable(self):
		testSuitMap = self.testSuitMap
		dom = self.dom
		tableNode = self.createNode(NodeInfo('table',None,[{'name':'class','value':'all_case'}]))
		
		tr = self.createNode(NodeInfo('tr'))
		th = self.createNode(NodeInfo('th','All TestCase Results',[{'name':'colspan','value':'5'}]))
		tr.appendChild(th)		
		tableNode.appendChild(tr)
		
		tr = self.createNode(NodeInfo('tr'))
		
		th = self.createNode(NodeInfo('th','Class'))
		tr.appendChild(th)
		
		th = self.createNode(NodeInfo('th','Number of Methods'))
		tr.appendChild(th)
		
		th = self.createNode(NodeInfo('th','Passed'))
		tr.appendChild(th)
		
		th = self.createNode(NodeInfo('th','Failed'))
		tr.appendChild(th)
		
		th = self.createNode(NodeInfo('th','Total Time(second)'))
		tr.appendChild(th)	
		
		
		tableNode.appendChild(tr)
				
		totalMethods = 0
		totalFailedMethods = 0
		totalTimes = 0
		if testSuitMap != None:
			for suitName, testSuit  in testSuitMap.items():
				suitMethods = 0
				failedMethods = 0
				suitTimes = 0.0
				testCaseArray = testSuit.testCaseArray
				for testCase in testCaseArray:
					suitTimes = suitTimes + float(testCase.time)
					suitMethods += 1
					if testCase.failInfo:
						failedMethods += 1	
						
				totalMethods += suitMethods
				totalFailedMethods += failedMethods
				totalTimes += suitTimes
				
				tr = self.createNode(NodeInfo('tr'))
				td = self.createNode(NodeInfo('td',suitName))
				tr.appendChild(td)
				td = self.createNode(NodeInfo('td',suitMethods))
				tr.appendChild(td)
				td = self.createNode(NodeInfo('td',suitMethods - failedMethods))
				tr.appendChild(td)
				td = self.createNode(NodeInfo('td',failedMethods,[{'name':'class','value':'red'}]))
				tr.appendChild(td)
				td = self.createNode(NodeInfo('td',suitTimes))
				tr.appendChild(td)	
				tableNode.appendChild(tr)
			
			tr = self.createNode(NodeInfo('tr',None,[{'name':'class', 'value':'total_row'}]))
			td = self.createNode(NodeInfo('th','Total'))
			tr.appendChild(td)
			td = self.createNode(NodeInfo('th',totalMethods))
			tr.appendChild(td)
			td = self.createNode(NodeInfo('th',totalMethods - totalFailedMethods))
			tr.appendChild(td)
			td = self.createNode(NodeInfo('th',totalFailedMethods,[{'name':'class','value':'red'}]))
			tr.appendChild(td)
			td = self.createNode(NodeInfo('th',totalTimes))
			tr.appendChild(td)	
			tableNode.appendChild(tr)
		else:
			tr = self.createNode(NodeInfo('tr'))
			td = self.createNode(NodeInfo('td','All TestCase Results is empty'),[{'name':'colspan','value':'5'}])
			tr.appendChild(td)		
			tableNode.appendChild(tr)
			
		self.body.appendChild(tableNode)

	def setPassedCaseTestCaseTable(self):
		testSuitMap = self.testSuitMap
		dom = self.dom
		tableNode = self.createNode(NodeInfo('table',None,[{'name':'class','value':'passed_case'}]))
		
		tr = self.createNode(NodeInfo('tr'))
		th = self.createNode(NodeInfo('th','Passed TestCase Results',[{'name':'colspan','value':'3'}]))
		tr.appendChild(th)		
		tableNode.appendChild(tr)
		
		tr = self.createNode(NodeInfo('tr'))
		th = self.createNode(NodeInfo('th','Class'))
		tr.appendChild(th)
		th = self.createNode(NodeInfo('th','Method'))
		tr.appendChild(th)		
		th = self.createNode(NodeInfo('th','Time(second)'))
		tr.appendChild(th)	
		
		
		tableNode.appendChild(tr)
		hasPassedCase = False
		if testSuitMap != None:
			for suitName, testSuit in testSuitMap.items():
				testCaseArray = testSuit.testCaseArray
				for testCase in testCaseArray:
					if testCase.failInfo == None:
						hasPassedCase = True
						tr = self.createNode(NodeInfo('tr', None,[{'name':'class','value':'green'}]))
						td = self.createNode(NodeInfo('td',suitName))
						tr.appendChild(td)
						td = self.createNode(NodeInfo('td',testCase.name))
						tr.appendChild(td)						
						td = self.createNode(NodeInfo('td',testCase.time))
						tr.appendChild(td)	
						tableNode.appendChild(tr)
				if not hasPassedCase:
					tr = self.createNode(NodeInfo('tr'))
					td = self.createNode(NodeInfo('td','Passed TestCase Results is empty',[{'name':'colspan','value':'3'}]))
					tr.appendChild(td)		
					tableNode.appendChild(tr)
		self.body.appendChild(tableNode)
	
	def setFailedCaseTestCaseTable(self):
		testSuitMap = self.testSuitMap
		dom = self.dom
		tableNode = self.createNode(NodeInfo('table',None,[{'name':'class','value':'failed_case'}]))
		
		tr = self.createNode(NodeInfo('tr'))
		th = self.createNode(NodeInfo('th','Failed TestCase Results',[{'name':'colspan','value':'5'}]))
		tr.appendChild(th)		
		tableNode.appendChild(tr)
		
		tr = self.createNode(NodeInfo('tr'))
		th = self.createNode(NodeInfo('th','Class'))
		tr.appendChild(th)
		th = self.createNode(NodeInfo('th','Method'))
		tr.appendChild(th)
		th = self.createNode(NodeInfo('th','Message'))
		tr.appendChild(th)
		th = self.createNode(NodeInfo('th','Type'))
		tr.appendChild(th)
		th = self.createNode(NodeInfo('th','Time(second)'))
		tr.appendChild(th)	
		
		
		tableNode.appendChild(tr)		
		
		hasFailedCase = False
		if testSuitMap != None:
			for suitName, testSuit  in testSuitMap.items():				
				testCaseArray = testSuit.testCaseArray
				for testCase in testCaseArray:
					if testCase.failInfo != None:
						hasFailedCase = True										
						tr = self.createNode(NodeInfo('tr',None,[{'name':'class','value':'red'}]))
						td = self.createNode(NodeInfo('td',suitName))
						tr.appendChild(td)
						td = self.createNode(NodeInfo('td',testCase.name))
						tr.appendChild(td)
						td = self.createNode(NodeInfo('td',testCase.failInfo.message))
						tr.appendChild(td)
						td = self.createNode(NodeInfo('td',testCase.failInfo.type))
						tr.appendChild(td)
						td = self.createNode(NodeInfo('td',testCase.time))
						tr.appendChild(td)	
						tableNode.appendChild(tr)
				if not hasFailedCase:
					tr = self.createNode(NodeInfo('tr'))
					td = self.createNode(NodeInfo('td','Failed TestCase Results is empty',[{'name':'colspan','value':'5'}]))
					tr.appendChild(td)		
					tableNode.appendChild(tr)
					
		self.body.appendChild(tableNode)

	

	def saveHtmlDoc(self):
		reportInfo = self.reportInfo		
		fileName = reportInfo.device + '_' + reportInfo.serialNo + '_report.html'	
		#过滤文件名中的非法字符，这些不被系统接受	
		fileName = re.sub(r'[\\/:*"<>?|]','',fileName)
		fileName= os.path.join(test_controler.mainPath, fileName)
		print 'report result file path:\t' + fileName
		f = file(fileName, 'w')
		writer = codecs.lookup('utf-8')[3](f)
		self.dom.writexml(writer, encoding='utf-8')
		writer.close()

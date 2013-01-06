#! /usr/bin/env python
#coding=utf-8
import xml.dom.minidom
import os

class FailureInfo:   
	def __init__(self,type,message,value):
		self.type = type
		self.message = message
		self.value = value


class TestCase:  
	def __init__(self,name,time):
		self.name = name
		self.time = time 
		self.failInfo = None	 
		
	def setFailureInfo(self, failInfo):
		self.failInfo = failInfo

class TestSuit:   
	def __init__(self, name):
	   self.name = name
	   self.testCaseArray = []
	

class ResultParser:	
	def __init__(self,resultPath):
		self.resultPath = resultPath	   
		self.testSuitMap = {}
		self.prefix = 'junit-report'
		self.prefixLength = len(self.prefix)
	
	def parseReportXml(self,file):
		if(file == None):
			print 'file name must be a valid value'
			return
		dom = xml.dom.minidom.parse(file)
		root = dom.documentElement
		domTestSuits = root.childNodes

		for domTestSuit in domTestSuits:	
			if domTestSuit.nodeType == domTestSuit.ELEMENT_NODE and domTestSuit.nodeName == 'testsuite':
				suitName = domTestSuit.getAttribute('name')				
				if suitName in self.testSuitMap:
					ts = self.testSuitMap[suitName]
				else:
					ts = TestSuit(suitName)
					self.testSuitMap[suitName] = ts
				for domTestCase in domTestSuit.childNodes:
					if domTestCase.nodeType == domTestCase.ELEMENT_NODE and domTestCase.nodeName == 'testcase':
						time = domTestCase.getAttribute('time')
						caseName = domTestCase.getAttribute('name')
						tc = TestCase(caseName, time)					
						ts.testCaseArray.append(tc)	 
						domFailure = domTestCase.getElementsByTagName('failure')
						if domFailure.length != 0:
							type = domFailure[0].getAttribute('type')
							message = domFailure[0].getAttribute('message')
							value = domFailure[0].childNodes[0].data
							tc.setFailureInfo(FailureInfo(type,message,value))
		
	def traverseAllResult(self, reportFileArray):
		if reportFileArray == None:
			return
		for file in reportFileArray:			
			self.parseReportXml(file)
	


	
	def getTestSuitMap(self):		
		return self.testSuitMap

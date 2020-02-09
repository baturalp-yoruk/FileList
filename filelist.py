#!/usr/bin/python

import os
import pwd
import sys
import datetime
from collections import deque
import subprocess
import re
from sets import Set

#Mehmet Berk Kemaloglu | Baturalp Yoruk
#2015400081            | 2015400036


#We create this Class to hold the data of the file
class MyFile():
	path=""
	size=0
	date=""
	own=""
	myName=""

	#this is our Class's comparable function we use this for sorting
	def __eq__(self, other):
        	return (self.myName) == (other.myName)
    	def __lt__(self, other):
        	return (self.myName) < (other.myName)



#dirList is for the directory list arg
dirList=deque()
#optList is for the options list arg
optList=deque()
#itList is for the file list we reach
itList=deque()	

#fileList1 takes all the arguments
fileList1 = sys.argv

# in this loop we seperate options and directory list arguments
# into 2 different deque
for i in range (1,len(fileList1)):
	name = fileList1[i]
	if "/" in name:
		dirList.append(name)
	elif  "." in name:
	 	dirList.append(name)
	else:
		optList.append(name)

#if there is no directory given we put current directory to dirList
if not len(dirList) :
	dirList.append(".")

""" in this loop we take all elements of dirList
and for every element we go down levels recursively
for every element in directory we create an instance of myFile
we put the data into the instance then we push it to itList"""
while dirList:
	currentdir = dirList.popleft()
	dircontents = os.listdir(currentdir)
	for name in dircontents:
		currentitem = currentdir + "/" + name
		if os.path.isdir(currentitem):
			dirList.append(currentitem)
		else:
			st = os.stat(currentitem)
			filesize = st.st_size
			fileowner = pwd.getpwuid(st.st_uid).pw_name
			modtime = os.path.getmtime(currentitem)
			tempFile=MyFile()
			tempFile.path=currentitem
			tempFile.size=filesize
			tempFile.own=fileowner
			tempFile.date=datetime.datetime.fromtimestamp(modtime).strftime('%Y%m%dT%H%M%S')
			tempFile.myName=name
			itList.append(tempFile)
#end while


#these variables are boolean variables for different situations

#for noFileList option
noFile=0
#for delete option
deleteFiles=0
#for zip option
zipFiles=0
#for zip file name
zipFile=""
#for match option
isRegex=0
#for match pattern
pattern=""
#for duplcontent option
duplcontent=0
#for duplname option
duplnamim=0
#for stats option
statBoolean=0
#for statistics
visitedItem=len(itList)
byteCount=0
pItem=0
pByteCount=0
uniqueName=0
uniqueSize=0
#we evaluate sum of all visited files 
for i in range (0,len(itList)):
	byteCount=byteCount+itList[i].size




#in this loop we renew itList according to given option
#also we change some boolean variables according to given options
while optList:
	#opt is a name of one of options
	opt=optList.popleft()
	

	#if before option given we renew itList
	if "-before" == opt:
		#opDate is the given date in options
		opDate=optList.popleft()
		for i in range (0,len(itList)):
			tempFile2=itList.popleft()
			if tempFile2.date<opDate:
				itList.append(tempFile2)
	
	
	#if after option given we renew itList			
	elif "-after" == opt:
		#opDate is the given date in options
		opDate=optList.popleft()
		for i in range (0,len(itList)):
			tempFile2=itList.popleft()
			if tempFile2.date>opDate:
				itList.append(tempFile2)


	#if bigger option given we renew itList	
	elif "-bigger" == opt:
		#opSize is the given size in options
		opSize=optList.popleft()
		for i in range (0,len(itList)):
			tempFile2=itList.popleft()
			#we translate the given size to byte value
			bit=0
			if "K" in  opSize:
				bit=int(opSize[0:len(opSize)-1])*(2**10)
			elif "M" in  opSize:
				bit=int(opSize[0:len(opSize)-1])*(2**20)
			elif "G" in  opSize:
				bit=int(opSize[0:len(opSize)-1])*(2**30)	
			if bit<tempFile2.size:
				itList.append(tempFile2)
				

	#if smaller option given we renew itList			
	elif "-smaller" == opt:
		#opSize is the given size in options
		opSize=optList.popleft()
		for i in range (0,len(itList)):
			tempFile2=itList.popleft()
			#we translate the given size to byte value
			bit=0
			if "K" in  opSize:
				bit=int(opSize[0:len(opSize)-1])*(2**10)
			elif "M" in  opSize:
				bit=int(opSize[0:len(opSize)-1])*(2**20)
			elif "G" in  opSize:
				bit=int(opSize[0:len(opSize)-1])*(2**30)		
			if bit>tempFile2.size:
				itList.append(tempFile2)
	

    #if nofilelist option is given we activate noFile boolean
    #and we deactivate isRegex, dulpnamim and dulpcontent boolean
	elif "-nofilelist" == opt:
		noFile=1
		isRegex=0
		duplcontent=0
		duplnamim=0

	
	#if delete option is given we activate deleteFiles boolean
	elif "-delete" == opt:
		deleteFiles=1

	
	#if zip option is given we activate zipFiles boolean
	elif "-zip" == opt:
		zipFiles=1
		#zipFile is the given file option
		zipFile=optList.popleft()


	#if match option is given we activate isRegex boolean
	elif "-match" == opt:
		if not noFile:		
		    isRegex=1
		#pattern is the given pattern
		pattern=optList.popleft()
		"""
		for i in range (0,len(itList)):
			tempFile2=itList.popleft()
			if pattern in tempFile2.myName:
				 itList.append(tempFile2) """




	#if dulpcont option is given and nofile wasn't activated we activate dulpcontent boolean
	elif "-duplcont" == opt:
		if not noFile:
			duplcontent=1


	#if dulpname option is given and nofile wasn't activated we activate dulpnamim boolean
	elif "-duplname" == opt:
		if not noFile:
			duplnamim=1


	#if stats option is given we activate statboolean
	elif "-stats" == opt:
		statBoolean=1


#end while	

#for statistics
pItem=len(itList)
for i in range (0,len(itList)):
	pByteCount=pByteCount+itList[i].size

#if this condition activated, this deletes all files
#which were remain after the other options
if deleteFiles:
	for i in range (0,len(itList)):
		#here we call a shell command
		os.system("rm " + itList[i].path)


#if this condition activated, this zips all files
#which were remain after the other options , creates 
#zip in the current directory named by the given option
if zipFiles:
	zipFileList="zip "+zipFile
	for i in range (0,len(itList)):
		 zipFileList=zipFileList + " " + itList[i].path
	os.system(zipFileList)



#if this condition activated this prints the file paths in given duplcontent order
#also here we evaluate number of files printed,number of unique content files printed,
#total size of files printed and total size of unique files printed
if duplcontent:

	newList=[]
	for i in range (0,len(itList)):
		a=itList.pop()
		newList.append(a)
	newList.sort()
	for i in range (0,len(newList)):
		firstFile=newList[i]
		count=0
		for j in range (i+1,len(newList)):
			secondFile=newList[j]
			if firstFile.size == secondFile.size:
				count=count+1
				newList.insert(i+count,secondFile)
				del newList[j+1]

	for i in range (0,len(newList)-1):
		print newList[i].path
		if not(newList[i].size == newList[i+1].size):
			#for statistics
			uniqueName+=1
			uniqueSize=uniqueSize+newList[i].size
			
			print "------"

	print newList[-1].path


#if this condition activated this prints the file paths in given duplname order
#also here we evaluate number of files printed,number of unique name files printed and
#total size of files printed 
if duplnamim:

	newList=[]
	for i in range (0,len(itList)):
		a=itList.pop()
		newList.append(a)
	newList.sort()

	for i in range (0,len(newList)-1):

		print newList[i].path
		if not(newList[i].myName == newList[i+1].myName):
			#for statistics
			uniqueName+=1
			print "------"

	print newList[-1].path



#if this condition activated this prints only the files
#which matches with given regex expression
if isRegex:
	nameList=[]
	itList2=[]
	for i in range (0,len(itList)):
		tempFile3=itList.pop()
		itList2.append(tempFile3)
		nameList.append(tempFile3.myName)
	r= re.compile(pattern)
	regList= filter(r.match,nameList)
	for i in range (0, len(regList)):
		print regList[i]
	
	#for statistics	
	pItem=len(regList)
	for i in range (0, len(regList)):
		fName=regList[i]
		for j in range (0,len(itList2)):
			tempFile4=itList2[j]
			if tempFile4.myName==fName:
				pByteCount=pByteCount+tempFile4.size


#this condition prints what remains in the itList	
if (not noFile) & (not duplnamim)  & (not isRegex) & (not duplcontent):

	for i in range (0,len(itList)):
		a=itList.pop()
		print a.path
		

#if this condition activated, this prints the statistics which are expected in the project
if statBoolean:
	print "number of visited files: " ,visitedItem
	print "visited files' total size: ",byteCount
	print "number of files we print: " ,pItem
	print "total size of printed files: " ,pByteCount
	if duplcontent:
		print "number of unique name: ",uniqueName
		print "number of unique size: ",uniqueSize
	if duplnamim:
		print "number of unique name: ",uniqueName

	

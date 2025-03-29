#!/usr/bin/python
import csv  # working with csv files
import os   # reading/writing files/directories
import sys  # for sys.exit if no valid file is found
from ollama import chat


#---------------------------------------- Change in here -------------------------------------
aiModel = "gemma3:27b"

# which columns have the question responses?
q1Col=4
q2Col=6
q3Col=8
# ---------------------------------------------------------------------------------------------

# build the query string for ollama from the passed column of the csv
#entryCol is the column with the data,
#hRow is the header row of the csv,
#dLst is the csv file read into a data list
def makeQuery(entryCol, hRow, dList):
	strFull = ''
	for row in dList:
		if len(row) > entryCol:
			strFull = strFull + '\n' + row[entryCol]
		#else:
		#	print( "This row is too short: ", row)
	return 'Students were asked this question: \" ' + hRow[entryCol] + '\". Their responses were: \"' + strFull + '\". Their instructor would like to understand their classes responses. Please give a summary of their responses, highlighting any common themes among their answers, for the instructor to read formatted in MarkDown. Do not include any suggestions or recommendations, only the summary.'


# make the query in ollama and return the response string
def summarize( queryString ):
	messages = [
	{
		'role': 'user',
		'content': queryString
	},
	]

	response = chat( aiModel , messages=messages)
	return response['message']['content']

def writeQuestionHeader(outFile, entryCol, hRow):
	outFile.write("\n\n------------------------------------------------------------------\n\n")
	outFile.write( "Students were asked: \n\n" + hRow[entryCol] + '\n\n')
	outFile.write( "Below is a summary of their responses: \n\n")
	outFile.write("------------------------------------------------------------------\n\n")

# -- prompt for the survey results file from Carmen --
# search the directory for ".csv" files
fileList = []
for file in os.listdir("./"):
	if file.endswith(".csv"):
		fileList.append( file )
if len(fileList) < 1:
	sys.exit("Move a valid file into this directory. ")

sectionList = [ fil[:-4] for fil in fileList ]
print( sectionList )
cNum = input("Which check-in week is this?: ")
cTxt = "Check-in Week " + str(cNum)
tmpList = [ x for x in sectionList ]

#print( f"Using model: {aiModel} " )

for sectn in sectionList:
	tmpList.remove(sectn)
	print("Working on class: " + str(sectn) +" using model: " + aiModel )
	surveyFilename = sectn + ".csv"
	outputFilename = sectn + "_Week" + str(cNum)+".md"

	# open the survey csv file exported from Carmen, attach it to a reader, and read it into a list
	surveyFile = open(surveyFilename, 'r', encoding="utf-8")
	csvSurvey =csv.reader( surveyFile )
	surveyDataList = list( csvSurvey )
	surveyFile.close()

	tmp = [row for row in surveyDataList if len(row)>0 and row[0] == 'section']
	headerRow = tmp[0]
	surveyDataList = [row for row in surveyDataList if row != headerRow]

	outputFile = open(outputFilename, 'w', encoding="utf-8")
	outputFile.write("****************** 1151 " + cTxt + " Summary ***********************\n\n\n")

	for qCol in [ q1Col, q2Col, q3Col]:
		writeQuestionHeader(outputFile, qCol, headerRow)
		print("Thinking about question in column: ", qCol )
		sumry = summarize( makeQuery(qCol, headerRow, surveyDataList) )
		print("Writing summary of responses in column: ", qCol )
		outputFile.write( sumry )

	print("Responses written to file: " + outputFilename)
	print("----------------------------------------------------------\n")
	#for st in outputList:
	#    outputWriter.writerow([st])
	outputFile.close()
	if len( tmpList ) > 0:
		print("There are " + str(len(tmpList)) + " more sections to go.")

print("All sections summarized.\n\n")
exit()


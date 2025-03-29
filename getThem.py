from canvasapi import Canvas
from urllib import request
import csv
import time


#-------------------------------------------------- Change in here ----------------------------

API_URL = "******"  # replace *'s with your Canvas URL
API_KEY = "******" # replace *'s with your Canvas API key

# section numbers
sections = [ 101, 102, 103 ] # list of section numbers from Registrar's system. Replace these with your own section numbers.
# dictionary to get lookup canvas course_id from section numbers. Replace these with your own section and course ID numbers.
dictCourseID = { 101:0001, 102:0031, 103:0047 } # keys are the section numbers from sections list. Values are the corresponding Canvas course ID numbers (from course URL)

# The assignment name in Canvas is set to "Check-in: Week __". Change this to the name of the assignment you are using.
cNum = input("Which check-in week is this?: ")
strCName = "Check-in: Week " + str(cNum) 

# ---------------------------------------------------------------------------------------------



# initialize the canvas object
canvas = Canvas( API_URL, API_KEY )

#setup dictionary of courses
dictCourse = {}
for sec in sections:
    dictCourse[sec] = canvas.get_course( dictCourseID[sec] )
    print( "Section: " + str(sec) + " is course: " + str(dictCourse[sec]))




# create dictionary of the checkin surveys
dictCheckin = {}
# setup dictionary of checkin reports.
dictReport = {}
for sec in sections:
    print( "Searching for Check-in in section " + str(sec) )
    quizzes = dictCourse[sec].get_quizzes()
    tmp = [t for t in quizzes if t.title == strCName]
    if len(tmp) > 0:
        dictCheckin[sec] = tmp[0]
        print(strCName + " found in section " + str(sec))
        # may be making initial call to create the reports...
        dictReport[sec] = dictCheckin[sec].create_report('student_analysis')
        print("First contact with report for section: " + str(sec))
    else:
        print("Section " + str(sec) + " does not have survey named: " + strCName)
        exit()

# list of sections for whom the "files" attribute is not yet ready to download
# the section numbers will be removed from here as their files are downloaded
reportFlag = [sec for sec in sections]

# After the first contact, find them again to check for file attribute
for sec in sections:
    quizzes = dictCourse[sec].get_quizzes()
    tmp = [t for t in quizzes if t.title == strCName]
    if len(tmp) > 0:
        dictCheckin[sec] = tmp[0]
        # canvas will throw errors calling create_report if it's currently being made...
        try:
            # may be making initial call to create the reports...
            dictReport[sec] = dictCheckin[sec].create_report('student_analysis')
        except Exception as e:
            print(f"Waiting... ({e})")


# loop through sections for which there are still reports to download
while len(reportFlag) > 0:
    for sec in reportFlag:
        # it's ready to download once the report has the "file" attribute
        try:
            if hasattr( dictReport[sec], "file" ):
                # download the report and write to a csv, then mark the section as having been read (remove section from reportFlag list)
                print(str(sec) + " is ready.")
                response=request.urlopen(dictReport[sec].file['url'])
                csvResp = response.read()
                csvstr = str(csvResp).strip("b'")
                lines=csvstr.split("\\n")
                print("Writing file: " + str(sec) + ".csv")
                f = open(str(sec)+".csv", "w", encoding="utf-8")
                for line in lines:
                    f.write( line + "\n")
                f.close()
                reportFlag.remove(sec)
        except Exception as e:  # Canvas throws a conflict error if the file was already being generated, so try to handle that by waiting
            print(f"Waiting... ({e})")
            time.sleep(1)
            
    # if there are  still reports to find, wait 3 seconds
    if len(reportFlag)>0:
        time.sleep(1)
exit()



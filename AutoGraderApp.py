from AutoGraderAppInfo import *
from console import console
from AutoGrader3 import AutoGrader3
from lms.LmsSimulator import LmsSimulator
from ReportGenerator import ReportGenerator
import os

# =======================================================================
# public static void main(String[] args)
# Entry point into the application.
# ======================================================================
def main():
    console("main...")

    # 1 instantiate the AutoGrader3 object
    autoGrader = AutoGrader3()

    # 2 instantiate an LMS object
    #assignmentDirectory = '/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/P1005 Short'
    assignmentDirectory = '/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/P1005'
    simulator = LmsSimulator(assignmentDirectory, autoGrader.LANGUAGE_PYTHON3)

    # 3 attach LMS object to the autoGrader
    autoGrader.setLms(simulator)

    # 4 set the list of test data and data files here
    autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/CIS 113 - Python I/TestData/P1005/P1005-1.txt')
    autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/CIS 113 - Python I/TestData/P1005/P1005-2.txt')
    autoGrader.addDataFile('/Users/jvolcy/Documents/words.txt')

    # 5 retrieve an assignment from the LMS (for non-simulated LMS, there is likely some LMS configuration that
    # will need to be done before making this call.
    autoGrader.getAssignmentFromLms()

    # 6 Execute the grading
    autoGrader.grade()

    # 7 Retrieve the html report
    rg = ReportGenerator("AutoGrader 3.0",  autoGrader._assignment.assignmentDirectory , autoGrader._assignment.submissions, autoGrader._agDocument.dataFiles)
    rg.generateReport()
    htmlReport = rg.getDocument()
    rg.writeReportToFile(os.path.join(assignmentDirectory, 'report.html'))

    #htmlReport = ReportGenerator.generateAnnotatedReport(autoGrader._agDocument)

    print(htmlReport[:500])
    #htmlReport = agDoc.htmlReport
    #print(">>",htmlReport[:1000], "<<")

    autoGrader.saveConfiguration()

    # ** THIS IS WHERE WE GATHER THE INFORMATION NORMALLY GATHERED THROUGH THE GUI.
    # THEN, EXECUTE THE GRADING ENGINE

        
    #---------- Commit the AG options to the JSON file ----------
    # TEMP autoGrader.saveConfiguration()
    console("Exiting main()...")

main()





# =======================================================================
# To Do
# Auto version incrementing
# copy data files to submission folders
# make a subdirectory in the TLD for extracted test files
# clean up data files and extracted test files
# ======================================================================


# =======================================================================
# xxx
# ======================================================================

#----------  ----------
#----------  ----------
#----------  ----------
#----------  ----------

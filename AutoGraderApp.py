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
    workingDirectory = '/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment'

    pythonAssignment = True

    # 2 instantiate an LMS object
    #assignmentDirectory = '/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/P1005 Short'
    # simulator = LmsSimulator(assignmentDirectory, autoGrader.LANGUAGE_PYTHON3)
    autoGrader.lms = LmsSimulator(workingDirectory)

    courses = autoGrader.lms.getCourses()
    for course in courses:
        print(course.courseID)

    autoGrader.lms.selectCourse(courses[1])

    assignments = autoGrader.lms.getAssignments()
    for assignment in assignments:
        print(assignment.assignmentID)

    autoGrader.lms.selectAssignment(assignments[0])

    # 3 attach LMS object to the autoGrader
    # autoGrader.setLms(simulator)

    # ** THIS IS WHERE WE GATHER THE INFORMATION NORMALLY GATHERED THROUGH THE GUI.
    # THEN, EXECUTE THE GRADING ENGINE

    # Warning: This will fail if there are no submissions
    if autoGrader.lms.getSelectedAssignment().submissions[0].language == autoGrader.LANGUAGE_PYTHON3:
        # 4 set the list of test data and data files here
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/P1005-1.txt')
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/P1005-2.txt')
        autoGrader.addDataFile('/Users/jvolcy/Documents/words.txt')
    else:
        # 4 set the list of test data and data files here
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/C1014.txt')
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/C1014a.txt')
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/C1014b.txt')
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/C1014c.txt')

        #autoGrader.addDataFile('/Users/jvolcy/Documents/words.txt')

    # 5 retrieve an assignment from the LMS (for non-simulated LMS, there is likely some LMS configuration that
    # will need to be done before making this call.
    #autoGrader.lms.getSelectedAssignment()
    autoGrader._agDocument.assignmentName = autoGrader.lms.getSelectedAssignment().assignmentName
    autoGrader._agDocument.gradingEngine.submissions = autoGrader.lms.getSelectedAssignment().submissions

    # 6 Execute the grading
    autoGrader.grade()

    # 7 Retrieve the html report
    rg = ReportGenerator(title="AutoGrader 3.0",
                         headerText=autoGrader.lms.getSelectedAssignment().assignmentName + " (" + autoGrader.lms.getSelectedAssignment().assignmentID + ")",
                         submissions=autoGrader.lms.getSelectedAssignment().submissions,
                         testDataFiles=autoGrader._agDocument.gradingEngine.testDataFiles)
    rg.generateReport()
    #htmlReport = rg.getDocument()

    assignmentDirectory = os.path.join(workingDirectory, 'courses', autoGrader.lms.getSelectedCourse().courseID, autoGrader.lms.getSelectedAssignment().assignmentID)
    rg.writeReportToFile(os.path.join(os.path.dirname(assignmentDirectory), os.path.basename(assignmentDirectory) + '.html'))

    autoGrader.saveConfiguration()

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

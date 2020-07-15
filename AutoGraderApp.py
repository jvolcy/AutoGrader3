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

    # define the working directory where courses are stored
    workingDirectory = '/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment'

    # 1 instantiate the AutoGrader3 object
    autoGrader = AutoGrader3()

    # 2 instantiate an LMS object, specifying the working directory
    autoGrader.lms = LmsSimulator(workingDirectory)

    # 3 fetch the available courses
    courses = autoGrader.lms.getCourses()
    for course in courses:
        print(course.courseID)

    # 4 select one of the courses.
    autoGrader.lms.selectCourse(courses[0])

    # 5 fetch the available assignments for the selected course
    assignments = autoGrader.lms.getAssignments()
    for assignment in assignments:
        print(autoGrader.lms.getSelectedCourse().courseID, '-->', assignment.assignmentID)

    # 6 select one of the assignments.
    autoGrader.lms.selectAssignment(assignments[1])

    # 7 configure the autoGrader
    autoGrader._agDocument.assignmentName = autoGrader.lms.getSelectedAssignment().assignmentName
    autoGrader._agDocument.gradingEngine.submissions = autoGrader.lms.getSelectedAssignment().submissions

    # ** THIS IS WHERE WE PUT THE INFORMATION NORMALLY GATHERED THROUGH THE GUI.
    # Warning: This will fail if there are no submissions
    if autoGrader.lms.getSelectedAssignment().submissions[0].language == autoGrader.LANGUAGE_PYTHON3:
        # 7a set the list of test data and data files for python assignments
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/P1005-1.txt')
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/P1005-2.txt')
        autoGrader.addDataFile('/Users/jvolcy/Documents/words.txt')
    else:
        # 7b set the list of test data and data files for c++ assignments
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/C1014.txt')
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/C1014a.txt')
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/C1014b.txt')
        autoGrader.addTestDataFile('/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/testData/C1014c.txt')


    # 8 Execute the grading
    autoGrader.grade()

    # 9 Retrieve the html report
    rg = ReportGenerator(title="AutoGrader 3.0",
                         headerText=autoGrader.lms.getSelectedAssignment().assignmentName + " (" + autoGrader.lms.getSelectedAssignment().assignmentID + ")",
                         submissions=autoGrader.lms.getSelectedAssignment().submissions,
                         testDataFiles=autoGrader._agDocument.gradingEngine.testDataFiles)
    rg.generateReport()

    assignmentDirectory = os.path.join(workingDirectory, 'courses', autoGrader.lms.getSelectedCourse().courseID, autoGrader.lms.getSelectedAssignment().assignmentID)
    rg.writeReportToFile(os.path.join(os.path.dirname(assignmentDirectory), os.path.basename(assignmentDirectory) + '.html'))

    # 10 save AG config options
    autoGrader.saveConfiguration()

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

from AutoGrader3.console import console
from AutoGrader3.AutoGrader3 import AutoGrader3
from AutoGrader3.lms.LmsSimulator import LmsSimulator
from AutoGrader3.ReportGenerator import ReportGenerator
import os
from pathlib import Path

# =======================================================================
# public static void main(String[] args)
# Entry point into the application.
# ======================================================================
def main():
    console("main...")

    # define the working directory where courses are stored
    workingDirectory = os.path.join(str(Path.home()), '_auto_grader')
    os.makedirs(workingDirectory, exist_ok=True)

    #workingDirectory = '/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment'

    # 1 instantiate the AutoGrader3 object
    autoGrader = AutoGrader3()

    # 2 instantiate an LMS object, specifying the working directory
    autoGrader.lms = LmsSimulator()

    '''autoGrader.lms = Moodle(server = autoGrader.getConfiguration(autoGrader.AG_CONFIG.MOODLE_SERVER),
                            securityKey = autoGrader.getConfiguration(autoGrader.AG_CONFIG.MOODLE_KEY),
                            email = autoGrader.getConfiguration(autoGrader.AG_CONFIG.MOODLE_EMAIL)
                            )
    '''
    autoGrader.lms.setWorkingDirectory(workingDirectory)

    # 3 fetch the available courses
    courses = autoGrader.lms.getCourses()
    for course in courses:
        print(course)

    # 4 select one of the courses.
    autoGrader.lms.selectCourse(courses[1])  #8

    # 5 fetch the available assignments for the selected course
    assignments = autoGrader.lms.getAssignments()
    for assignment in assignments:
        #print(autoGrader.lms.getSelectedCourse().courseID, '-->', assignment.assignmentID)
        print(assignment)

    # 6 select one of the assignments.
    autoGrader.lms.selectAssignment(assignments[0])  #13

    print('--------------------')
    print('Selected Course\n', autoGrader.lms.getSelectedCourse())
    print('--------------------')
    print('Selected Assignment\n', autoGrader.lms.getSelectedAssignment())

    print('--------------------')
    print('7 submissions:\n')

    # 7 configure the autoGrader
    autoGrader.agDocument.assignmentName = autoGrader.lms.getSelectedAssignment().assignmentName
    autoGrader.agDocument.assignment.submissions = autoGrader.lms.getSelectedAssignment().submissions
    autoGrader.gradingEngine.agDocument = autoGrader.agDocument


    '''for i in range(7):
        print('--------------------')
        print(autoGrader.lms.getSelectedAssignment().submissions[i])'''

    autoGrader.lms.downloadSubmissions()

    '''for i in range(7):
        print('--------------------')
        print(autoGrader.lms.getSelectedAssignment().submissions[i])'''

    # ** THIS IS WHERE WE PUT THE INFORMATION NORMALLY GATHERED THROUGH THE GUI.
    # Warning: This will fail if there are no submissions

    # this is a hack needed for the purposes of selecting which set of testfiles will be used in simulation.
    # the grading engine calls _autoDetectLanguage() when it runs grade()
    autoGrader._autoDetectLanguage()

    if autoGrader.lms.getSelectedAssignment().submissions[0].language == autoGrader.LANGUAGE_PYTHON3:
        # 7a set the list of test data and data files for python assignments
        autoGrader.addTestDataFile(os.path.join(workingDirectory, 'testData/P1005-1.txt'))
        autoGrader.addTestDataFile(os.path.join(workingDirectory, 'testData/P1005-2.txt'))
        autoGrader.addDataFile('/Users/jvolcy/Documents/words.txt')
    else:
        # 7b set the list of test data and data files for c++ assignments
        autoGrader.addTestDataFile(os.path.join(workingDirectory, 'testData/C1014.txt'))
        autoGrader.addTestDataFile(os.path.join(workingDirectory, 'testData/C1014a.txt'))
        autoGrader.addTestDataFile(os.path.join(workingDirectory, 'testData/C1014b.txt'))
        autoGrader.addTestDataFile(os.path.join(workingDirectory, 'testData/C1014c.txt'))


    # 8 Execute the grading
    autoGrader.grade()

    # 9 Retrieve the html report
    rg = ReportGenerator(title = "AutoGrader 3.0",
                         headerText = f"{autoGrader.lms.getSelectedAssignment().assignmentName}  ({autoGrader.lms.getSelectedAssignment().assignmentID})",
                         submissions = autoGrader.lms.getSelectedAssignment().submissions,
                         testDataFiles = autoGrader.agDocument.testDataFiles)
    rg.generateReport()

    assignmentDirectory = os.path.join(workingDirectory, 'courses', str(autoGrader.lms.getSelectedCourse().courseID), str(autoGrader.lms.getSelectedAssignment().assignmentID))
    outputFile = os.path.join(os.path.dirname(assignmentDirectory), os.path.basename(assignmentDirectory) + '.html')
    rg.writeReportToFile(outputFile)

    autoGrader.agDocument.htmlReport = rg.getDocument()

    console('Report Generator output: file://' + outputFile)
    # 10 save AG config options
    autoGrader.saveConfiguration()

    console("Exiting main()...")


main()




# =======================================================================
# To Do
# Auto version incrementing
# ======================================================================


# =======================================================================
# xxx
# ======================================================================

#----------  ----------
#----------  ----------
#----------  ----------
#----------  ----------

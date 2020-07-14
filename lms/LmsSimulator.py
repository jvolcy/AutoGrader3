from IAssignmentStore import IAssignmentStore
from Assignment import Assignment, Course
from Submission import Submission
from IAGConstant import IAGConstant
import os
from console import console

# =======================================================================
# LmsSimulator class
# =======================================================================
class LmsSimulator(IAssignmentStore):
    def __init__(self, workingDirectory, language):
        # instantiate the assignment object
        console('initializing LmsSimulator...')

        self.__workingDirectory = workingDirectory
        self.__courses = []
        self.__selectedCourse = Course()

        self.__assignments = []
        self.__selectedAssignment = Assignment()

        self.__selectedAssignment.assignmentDirectory = self.__workingDirectory.rstrip('/')
        self.__selectedAssignment.assignmentName = os.path.basename(self.__selectedAssignment.assignmentDirectory)
        self.__selectedAssignment.assignmentID = '000000'
        self.__selectedAssignment.courseDescription = ''

        self.__language = language
        # for the simulation, we immediately call __buildAssignment()
        # to generate the data used to simulate an LMS request
        self.__buildAssignment()

    # =======================================================================
    # for a normal LMS, the working directory would be provided through
    # a call to setWorkingDirectory().  In our case, the files are
    # locally on disk in an arbitrary location, so the working directory
    # is wherever those files happen to be.
    # =======================================================================
    def __buildAssignment(self):

        console('self.__selectedAssignment.assignmentDirectory = ' + self.__selectedAssignment.assignmentDirectory)

        # get items in the assignment directory
        subDirs = os.listdir(self.__selectedAssignment.assignmentDirectory)
        for item in subDirs:

            # get the full path of each item.  If the item is not a directory, ignore it
            full_path = os.path.join(self.__selectedAssignment.assignmentDirectory, item)
            if not os.path.isdir(full_path):
                continue

            # if it is a directory, assume the directory name is the student's name
            # and register the full path name
            submissionDirectory = full_path
            studentName = item

            # console(submissionDirectory + ' --> ' + studentName)

            # build the submission object for this submission
            submission = Submission()
            submission.submissionDirectory = submissionDirectory
            submission.language = self.__language
            submission.studentName = studentName

            # find all programming files in the subdirectory
            files = os.listdir(submission.submissionDirectory)

            # go through each file in the submission directory
            for file in files:
                # get the file extension
                filename, file_extension = os.path.splitext(file)
                file_extension = file_extension.lstrip('.')

                if self.__language == IAGConstant.LANGUAGE_PYTHON3 and file_extension in IAGConstant.PYTHON_EXTENSIONS:
                    submission.submissionFiles.append(file)

                elif self.__language == IAGConstant.LANGUAGE_CPP and file_extension in IAGConstant.CPP_EXTENSIONS:
                    submission.submissionFiles.append(file)

                else:
                    console('Unknown file extension: ' + file_extension)

            self.__selectedAssignment.submissions.append(submission)

        # the __assignments array will have only 1 item
        self.__assignments = [self.__selectedAssignment]

    # =======================================================================
    # function to retrieve available courses from the LMS
    # =======================================================================
    def getCourses(self) -> [Course]:
        # for the simulator, we will have only 1 legit course.
        # two are provided here for debugging purposes only.  The
        # second should never be selected.
        return ['CIS 113 CRN 123456 Spring 2018', 'some other course']

    # =======================================================================
    # function that selects which of the available courses returned
    # by getCourses() we will be working with
    # =======================================================================
    def selectCourse(self, course):
        # nothing to do for the simulator
        pass

    # =======================================================================
    # function that returns the currently selected course
    # =======================================================================
    def getSelectedCourse(self) -> Course:
        return self.__selectedCourse

    # =======================================================================
    # function to retrieve assignments from the LMS
    # returns a list of assignments associated with the selected course
    # the course must be set before this can be used
    # =======================================================================
    def getAssignments(self) -> [Assignment]:
        return self.__assignments

    # =======================================================================
    # function that selects which of the available assignments returned
    # by getAssignments() we will be working with
    # =======================================================================
    def selectAssignment(self, assignment):
        # nothing to do here
        pass

    # =======================================================================
    # function that returns the currently selected assignment
    # =======================================================================
    def getSelectedAssignment(self) -> Assignment:
        return self.__selectedAssignment

    # =======================================================================
    # function to submit graded assignments back to the LMS
    # =======================================================================
    def submitAssignment(self, assignment):
        # nothing to do here
        pass

    # =======================================================================
    # specify a place where the LMS will download and store assignment files
    # =======================================================================
    def setWorkingDirectory(self, workingDirectory):
        self.__workingDirectory = workingDirectory

    # =======================================================================
    # function that returns the currently selected assignment
    # =======================================================================
    def getWorkingDirectory(self) -> str:
        return self.__workingDirectory

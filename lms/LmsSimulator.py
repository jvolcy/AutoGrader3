from IAssignmentStore import IAssignmentStore
from Assignment import Assignment
from Submission import Submission
from IAGConstant import IAGConstant
import os
from console import console

# =======================================================================
# LmsSimulator class
# =======================================================================
class LmsSimulator(IAssignmentStore):
    def __init__(self, assignmentDirectory, language):
        # instantiate the assignment object
        console('initializing LmsSimulator...')
        self.__assignment = Assignment()

        self.__assignment.assignmentDirectory = assignmentDirectory.rstrip('/')
        self.__assignment.assignmentName = os.path.basename(self.__assignment.assignmentDirectory)
        self.__assignment.assignmentID = '000000'

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

        console('self.__assignment.assignmentDirectory = ' + self.__assignment.assignmentDirectory)

        # get items in the assignment directory
        subDirs = os.listdir(self.__assignment.assignmentDirectory)
        for item in subDirs:

            # get the full path of each item.  If the item is not a directory, ignore it
            full_path = os.path.join(self.__assignment.assignmentDirectory, item)
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

            self.__assignment.submissions.append(submission)



    # =======================================================================
    # function to retrieve assignments from the LMS
    # returns an assignment name, assignment ID and a list of assignments
    # =======================================================================
    def getAssignmentFromLms(self) -> Assignment:
        return self.__assignment


    # =======================================================================
    # function to submit graded assignments back to the LMS
    # =======================================================================
    def submitAssignmentToLms(self, assignment):
        #not used for the simulator
        return

    # =======================================================================
    # specify a place where the LMS can download and store assignment files
    # =======================================================================
    def setAssignmentDirectory(self, dir):
        #not used for the simulator (there are no submission files to save to disk)
        return


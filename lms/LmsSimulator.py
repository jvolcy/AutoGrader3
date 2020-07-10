from IAssignmentStore import IAssignmentStore
from Assignment import Assignment
from Submission import Submission


# =======================================================================
# LmsSimulator class
# =======================================================================
class LmsSimulator(IAssignmentStore):
    def __init__(self):
        # instantiate the assignment object
        self.__assignment = Assignment()

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
        # -----------------------------------------------------------
        self.__assignment.assignmentName = 'P1005 Test Assignment'
        self.__assignment.assignmentID = '0123456'
        self.__assignment.assignmentDirectory = '/Users/jvolcy/Documents/Spelman/Projects/AutoGrader3/test_assignment/P1005'

        # -----------------------------------------------------------
        # SUBMISSION #1
        submission = Submission()
        submission.submissionDirectory = self.__assignment.assignmentDirectory + "/" + "Abiodun Scott"
        submission.submissionFiles.append("P1005.py")
        submission.language = 'Python 3'
        submission.studentName = 'Abiodun Scott'

        # add submissions
        self.__assignment.submissions.append(submission)

        # -----------------------------------------------------------
        # SUBMISSION #2
        submission = Submission()
        submission.submissionDirectory = self.__assignment.assignmentDirectory + "/" + "Adia Haynes"
        submission.submissionFiles.append("P1005.py")
        submission.language = 'Python 3'
        submission.studentName = 'Adia Haynes'

        # add submissions
        self.__assignment.submissions.append(submission)

        # -----------------------------------------------------------
        # SUBMISSION #3
        submission = Submission()
        submission.submissionDirectory = self.__assignment.assignmentDirectory + "/" + "Amore Daniels"
        submission.submissionFiles.append("P1005 - Spellchecker.py")
        submission.language = 'Python 3'
        submission.studentName = 'Amore Daniels'

        # add submissions
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


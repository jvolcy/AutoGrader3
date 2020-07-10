from IAssignmentStore import IAssignmentStore
from Assignment import Assignment

# =======================================================================
# Moodle LMS Interface class
# =======================================================================
class Moodle(IAssignmentStore):
    def __init__(self):
        pass

    # =======================================================================
    # function to retrieve assignments from Moodle
    # returns an assignment name, assignment ID and a list of assignments
    # =======================================================================
    def getAssignmentFromLms(self) -> Assignment:
        pass

    # =======================================================================
    # function to submit graded assignments back to Moodle
    # =======================================================================
    def submitAssignmentToLms(self, assignment):
        pass

    # =======================================================================
    # specify a place where the LMS can download and store assignment files
    # =======================================================================
    def setAssignmentDirectory(self, dir):
        pass


import Submission
#import Assignment
# =======================================================================
# =======================================================================

# =======================================================================
# set the lms interface object
# =======================================================================
def setLms(self, lmsInterface):
    self._lmsInterface = lmsInterface


# =======================================================================
# function to retrieve assignments from the LMS and transfer contents
# to the AGDocument object.  You must specify the language used for the
# assignment
# =======================================================================
def getAssignmentFromLms(self):
    self._assignment = self._lmsInterface.getAssignmentFromLms()
    self._agDocument.assignmentName = self._assignment.assignmentName
    self._agDocument.gradingEngine.submissions = self._assignment.submissions


# =======================================================================
# function to transfer contents from the AGDocument to
# the assignment object and submit back to the LMS
# =======================================================================
def submitAssignmentToLms(self, assignment):
    self._lmsInterface.submitAssignmentToLms(assignment)


# =======================================================================
# specify a place where the LMS can download and store assignment files
# =======================================================================
def setAssignmentDirectory(self, dir):
    self._lmsInterface.setAssignmentDirectory(dir)


# =======================================================================
# =======================================================================

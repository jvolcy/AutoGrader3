from Assignment import Assignment

# =======================================================================
# Interface of AG3 LMSes.
# ======================================================================
class IAssignmentStore(object):
    # function to retrieve assignments from the LMS
    # returns an assignment name, assignment ID and a list of assignments
    def getAssignmentFromLms(self) -> Assignment:
        raise NotImplementedError()

    # function to submit graded assignments back to the LMS
    def submitAssignmentToLms(self, assignmentID, assignment):
        raise NotImplementedError()

    # specify a place where the LMS can download and store assignment files
    def setWorkingDirectory(self, dir):
        raise NotImplementedError()





# =======================================================================
# xxx
# ======================================================================

# ----------  ----------
# ----------  ----------
# ----------  ----------
# ----------  ----------

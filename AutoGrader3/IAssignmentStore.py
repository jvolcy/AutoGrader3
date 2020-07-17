from .Assignment import Assignment, Course


# =======================================================================
# Interface of AG3 LMSes.
# ======================================================================
class IAssignmentStore(object):
    # =======================================================================
    # function to retrieve available courses from the LMS
    # =======================================================================
    def getCourses(self) -> [Course]:
        raise NotImplementedError()

    # =======================================================================
    # function that selects which of the available courses returned
    # by getCourses() we will be working with
    # =======================================================================
    def selectCourse(self, course):
        raise NotImplementedError()

    # =======================================================================
    # function that returns the currently selected course
    # =======================================================================
    def getSelectedCourse(self) -> Course:
        raise NotImplementedError()

    # =======================================================================
    # function to retrieve assignments from the LMS
    # returns a list of assignments associated with the selected course
    # the course must be set before this can be used
    # =======================================================================
    def getAssignments(self) -> [Assignment]:
        raise NotImplementedError()

    # =======================================================================
    # function that selects which of the available assignments returned
    # by getAssignments() we will be working with
    # =======================================================================
    def selectAssignment(self, assignment):
        raise NotImplementedError()

    # =======================================================================
    # function that returns the currently selected assignment
    # =======================================================================
    def getSelectedAssignment(self) -> Assignment:
        raise NotImplementedError()


    # =======================================================================
    # function that downloads all submissions to disk following the convention
    # course->assignment->[submissions]
    # =======================================================================
    def downloadSubmissions(self):
        raise NotImplementedError

    # =======================================================================
    # function to submit graded assignments back to the LMS
    # =======================================================================
    def submitAssignment(self, assignment):
        raise NotImplementedError()

    # =======================================================================
    # specify a place where the LMS will download and store assignment files
    # =======================================================================
    def setWorkingDirectory(self, workingDirectory):
        raise NotImplementedError()

    # =======================================================================
    # function that returns the currently selected assignment
    # =======================================================================
    def getWorkingDirectory(self) -> str:
        raise NotImplementedError()

# =======================================================================
# xxx
# ======================================================================

# ----------  ----------
# ----------  ----------
# ----------  ----------
# ----------  ----------

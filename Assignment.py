
# =======================================================================
# structure to represent an lms course
# ======================================================================
class Course(object):
    def __init__(self, courseName=None, courseID=None, courseDescription=None, term=None):
        self.courseName = courseName
        self.courseID = courseID
        self.courseDescription = courseDescription
        self.term = term


# =======================================================================
# Assignment
# This is an LMS exchange object.  All transactions to and from the
# LMS is through an Assignment object
# =======================================================================
class Assignment(object):
    def __init__(self):
        self.assignmentName = None
        self.assignmentID = None
        self.assignmentDirectory = None
        self.submissions = []  # array of Submission objects


# =======================================================================
# xxx
# =======================================================================

# ----------  ----------
# ----------  ----------
# ----------  ----------
# ----------  ----------

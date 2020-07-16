# =======================================================================
# structure to represent an lms course
# ======================================================================
class Participant(object):
    def __init__(self, lmsID=None, name=None, schoolID=None, email=None, role=None):
        self.lmsID = lmsID
        self.name = name
        self.schoolID = schoolID
        self.email = email
        self.role = role

    def __str__(self):
        return f'LMS ID: {self.lmsID}\nName: {self.name}\nSchool ID: {self.schoolID}\nemail: {self.email}\nRole: {self.role}'


# =======================================================================
# structure to represent an lms course
# ======================================================================
class Course(object):
    def __init__(self, courseName=None, courseID=None, courseDescription=None, term=None):
        self.courseName = courseName
        self.courseID = courseID
        self.courseDescription = courseDescription
        self.term = term

    def __str__(self):
        return f'Course ID: {self.courseID}\nCourse Name: {self.courseName}\nCourse Description: {self.courseDescription}'


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

    def __str__(self):
        return f'Assignment ID: {self.assignmentID}\nAssignment Name: {self.assignmentName}\n\
Assignment Directory: {self.assignmentDirectory}\n{len(self.submissions)} submissions'


#=======================================================================
# Submission
# =======================================================================
class Submission(object):
    def __init__(self):
        # ---------- general members ----------
        self.submissionID = None
        self.studentName = ''
        self.submissionDirectory = ''
        self.submissionFiles = []  # array of file names
        self.primarySubmissionFile = None  # file name
        self.language = ''
        # ---------- code analysis members ----------
        # self.linesOfCode = 0
        # self.numComments = 0
        # self.nunDocStrings = 0
        # self.numFunctions = 0
        # self.numClasses = 0
        # ---------- errors ----------
        self.compilerErrors = ''
        self.runtimeErrors = []     # string array: there are as many entries as we have test cases
        # ---------- processing/execution members ----------
        self.progOutputs = []       # string array: there are as many entries as we have test cases
        self.executionTimes = []    # string array: the # of seconds required to complete execution
        # ---------- grading members ----------
        self.bAutoGraded = False
        self.grade = 0
        self.instructorComment = ''
        # ---------- directives ----------
        self.nameDirective = ''        # student name
        self.titleDirective = ''       # submission title
        self.dateDirective = ''        # date
        self.mainDirective = ''        # main module
        self.dataDirective = ''        # misc. data

    def __str__(self):
        return f'Submission ID: {self.submissionID}\nStudent Name: {self.studentName}\n\
Submission Directory: {self.submissionDirectory}\n{len(self.submissionFiles)} Submitted File(s): {self.submissionFiles}'


# =======================================================================
# xxx
# =======================================================================

# ----------  ----------
# ----------  ----------
# ----------  ----------
# ----------  ----------

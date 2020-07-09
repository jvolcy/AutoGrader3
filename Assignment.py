
# =======================================================================
# Assignment
# =======================================================================
class Assignment(object):
    def __init__(self):
        # ---------- general members ----------
        self.studentName = ''
        self.assignmentDirectory = ''
        self.assignmentFiles = []  # array of file objects
        self.primaryAssignmentFile = None  # file object
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
        self.titleDirective = ''       # assignment title
        self.dateDirective = ''        # date
        self.mainDirective = ''        # main module
        self.dataDirective = ''        # misc. data




# =======================================================================
# xxx
# =======================================================================

# ----------  ----------
# ----------  ----------
# ----------  ----------
# ----------  ----------

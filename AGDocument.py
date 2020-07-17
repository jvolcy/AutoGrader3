from Assignment import Assignment

# =======================================================================
# AGDocument class
# =======================================================================
class AGDocument(object):
    def __init__(self):
        self.assignmentName = ''
        self.assignmentID = ''
        self.assignment = Assignment()  # the one and only assignment object
        self.htmlReport = ''
        self.dataFiles = []       # a list of input data files needed by the programs under test
        self.testDataFiles = []       # a list of test files.

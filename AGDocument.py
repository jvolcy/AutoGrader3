from GradingEngine import GradingEngine

# =======================================================================
# AGDocument class
# =======================================================================
class AGDocument(object):
    def __init__(self):
        self.assignmentName = ''
        self.gradingEngine = GradingEngine()       # a GradingEngine() object
        self.htmlReport = ''
        self.dataFiles = []       # a list of input data files needed by the program

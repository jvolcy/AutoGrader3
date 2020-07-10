from console import console
import os, sys, time
from shutil import copy
from pathlib import Path

# =======================================================================
# 
# =======================================================================
def _setAssignmentName(self, submissionName):
    self._agDocument.assignmentName = submissionName

def addTestDataFile(self, testDataFile):
    self._agDocument.gradingEngine.testDataFiles.append(testDataFile)

def addDataFile(self, dataFile):
    self._agDocument.dataFiles.append(dataFile)

def addSubmission(self, submission):
    self._agDocument.gradingEngine.submissions.append(submission)

# =======================================================================
# prepareDataFiles()
# This function copies all data files to the submission directory of
# every submission
# =======================================================================
def _prepareDataFiles(self):
    #---------- copy all data files into each submission directory ----------
    #go through every data file in the listDataFiles list box
    for src in  self._agDocument.dataFiles:
        # copy each data file to each of the submission directories
        for submission in self._agDocument.gradingEngine.submissions:
            dst = submission.submissionDirectory + "/" + os.path.basename(src)
            try:
                console("copying \"" + src + "\" to \"" + dst + "\"")
                copy(src, dst)
            except:
                e = sys.exc_info()[0]
                print(e)
                console("AGDocument::_prepareDataFiles() " + str(e))

# =======================================================================
# prepareDataFiles()
# This function removes all data files in the submission directory
# that were placed by _prepareDataFiles()
# =======================================================================
def _cleanupDataFiles(self):
    for src in  self._agDocument.dataFiles:
        # delete the data files from each of the submission directories
        for submission in self._agDocument.gradingEngine.submissions:
            dst = submission.submissionDirectory + "/" + os.path.basename(src)
            try:
                console('removing "' + dst + '"')
                os.remove(dst)
            except:
                e = sys.exc_info()[0]
                console(str(e))
    pass

# ======================================================================
# breakOutTestFiles()
# function that returns the list of test files in the listTestData
# list box.  If any of the files contain multiple test cases, these
# are separated into as many test cases in the supplied output
# directory.  Multiple test cases within a single file are separated
# by a TEST_CASE_SEPARATOR string.
# ===================================================================== */
#private ArrayList<File> breakOutTestFiles(File outputDirectory) {
def breakOutTestFiles(self,  outputDirectory):
    pass
    '''
    {
ArrayList<File> testFiles = new ArrayList<>();

//go through every file in the listTestData list box
for (Object s : listTestData.getItems()) {
    String filename = s.toString();

    //read the content of the test file
    String content = readFromFile(filename);

    //search for test case separators
    String[] subCases = content.split(IAGConstant.TEST_CASE_SEPARATOR);

    //if none are found, the length of subCases array will be 1.
    //In that case, add the test files from the 'ListTestData' to the testFiles list
    if (subCases.length == 1) {
        testFiles.add(new File(filename));
    } else {
        //create temporary files in the output directory for each sub-case
        for (int counter = 1; counter <= subCases.length; counter++) {
            String testDataFileName = outputDirectory.getAbsolutePath() + "/" + fileNameFromPathName(filename) + "-" + counter;
            writeToFile(testDataFileName, subCases[counter - 1]);
            testFiles.add(new File(testDataFileName));
            console("creating sub-test case file " + testDataFileName);
        }
    }
}
return testFiles;
}
'''

# =======================================================================
# _discoverPrimarySubmissionFile()
# function that attempts to automatically detect the primary programming
# file for python.  This works only if the user hasn't specified a
# primary file or when there is only 1 python file.  If more than
# one python source file exists, the user MUST specify a primary.
# for python programs, we must idenfity the primary code file if
# multiple files are present.  If only one submission file is given,
# set it as the primary.
# =======================================================================
def _discoverPrimarySubmissionFile(self, submission):
    #if the user has already specified a primary submission file, do nothing
    if submission.primarySubmissionFile is not None:
        return

    #if we only have 1 submissionFile, make it the primary
    if len(submission.submissionFiles) == 1:
        submission.primarySubmissionFile = submission.submissionFiles[0]

    #return without setting the value of the primarySubmissionFile (at this point, it should be None)
    #This does not matter for C++.
    return

# =======================================================================
# _updateAutoGraderConfiguration
# =======================================================================
def _updateAutoGraderConfiguration(self):
    self.setCppCompiler(self.getConfiguration(self.AG_CONFIG.CPP_COMPILER))
    self.setPython3Interpreter(self.getConfiguration(self.AG_CONFIG.PYTHON3_INTERPRETER))
    self.setShellInterpreter(self.getConfiguration(self.AG_CONFIG.SHELL))
    self.setTempOutputDirectory(str(Path.home()))  #use the home directory as the temp directory
    self.setMaxOutputLines(int(self.getConfiguration(self.AG_CONFIG.MAX_OUTPUT_LINES)))
    self.setMaxRunTime(int(self.getConfiguration(self.AG_CONFIG.MAX_RUNTIME)))


# =======================================================================
# grade()
# =======================================================================
def grade(self):
    self._updateAutoGraderConfiguration()

    # copy data files to each submission directory
    self._prepareDataFiles()

    # ****** TO DO ***********
    '''        //---------- generate break out test files ----------
        //first make a directory named ag_data in the moodle directory
        File testDataDirectory = new File( autoGrader.getAgDocument().moodleDirectory.getAbsolutePath() + "/.ag_data");
        testDataDirectory.mkdir();

        //now put the break out test files in the ag_data directory
        autoGrader.getAgDocument().testDataFiles = breakOutTestFiles(testDataDirectory);
        gradingEngine.testDataFiles = autoGrader.getAgDocument().testDataFiles;

    '''
    self.breakOutTestFiles("")


    #attempt to discover the primary submission file for each submission
    for submission in self._agDocument.gradingEngine.submissions:
        self._discoverPrimarySubmissionFile(submission)


    # perform grading
    console("Processing submissions...")
    self._agDocument.gradingEngine.processSubmissions()

    # grading happens is a separate thread.  We can monitor the state of that thread through the status
    # variable returned by gradingEngine.getProcessingStatus()
    status = self._agDocument.gradingEngine.getProcessingStatus()

    # wait for grading thread to complete
    while status.bRunning == True:
        time.sleep(0.5)
        #print('#')

    # cleanup data files
    self._cleanupDataFiles()

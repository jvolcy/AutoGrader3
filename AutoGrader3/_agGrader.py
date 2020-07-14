from console import console
import os, sys, time
from shutil import copy, rmtree
from pathlib import Path
from IAGConstant import IAGConstant
#from MossClient import MossClient
import threading

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
# This function creates a symbolic link of all data needed files in the
# submission directory of every submission
# =======================================================================
def _prepareDataFiles(self):
    #---------- symlink all data files into each submission directory ----------
    #go through every data file in the listDataFiles list box
    for src in  self._agDocument.dataFiles:
        # symlink each data file to each of the submission directories
        for submission in self._agDocument.gradingEngine.submissions:
            dst = submission.submissionDirectory + "/" + os.path.basename(src)
            try:
                #console("copying \"" + src + "\" to \"" + dst + "\"")
                #copy(src, dst)
                console("Crearing sybmolic link \"" + dst + "\" --> \"" + src + "\"")
                os.symlink(src, dst)
            except:
                e = sys.exc_info()[0]
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
    self._agDocument.gradingEngine.setCppCompiler(self.getConfiguration(self.AG_CONFIG.CPP_COMPILER))
    self._agDocument.gradingEngine.setPython3Interpreter(self.getConfiguration(self.AG_CONFIG.PYTHON3_INTERPRETER))
    self._agDocument.gradingEngine.setShellInterpreter(self.getConfiguration(self.AG_CONFIG.SHELL))
    self._agDocument.gradingEngine.setTempOutputDirectory(str(Path.home()))
    self._agDocument.gradingEngine.setMaxOutputLines(int(self.getConfiguration(self.AG_CONFIG.MAX_OUTPUT_LINES)))
    self._agDocument.gradingEngine.setMaxRunTime(int(self.getConfiguration(self.AG_CONFIG.MAX_RUNTIME)))

# =======================================================================
# breakOutTestFiles()
# function that replaces the list of test files in the gradingEngine.testDataFiles
# list.  If any of the files contain multiple test cases, these
# are separated into as many test cases and used to replace the single
# entry in the gradingEngine.testDataFiles list.  Multiple test cases
# within a single file are separated by a TEST_CASE_SEPARATOR string.
# ======================================================================
def breakOutTestFiles(self, outputDirectory):

    console("breakOutTestFiles directory set to " + outputDirectory)

    #go through every file in the listTestData list box
    for filename in self._agDocument.gradingEngine.testDataFiles:

        #read the content of the test file
        with open(filename, 'r') as file:
            content = file.read()

        #search for test case separators
        subCases = content.split(IAGConstant.TEST_CASE_SEPARATOR)

        #if none are found, the length of subCases array will be 1.
        #In that case, leave the the current entry in the _agDocument.gradingEngine.testDataFiles list
        if len(subCases) == 1:
            continue
        else:
            #remove the top-level test data file
            self._agDocument.gradingEngine.testDataFiles.remove(filename)

            #create temporary files in the output directory for each sub-case
            for counter in range(1, len(subCases)+1):
                testDataFileName = os.path.join( outputDirectory, os.path.basename(filename) + '-' + str(counter) )


                # write the sub-case to file
                with open(testDataFileName, 'w') as file:
                    file.write(subCases[counter-1])

                # add this to the testFiles list
                self._agDocument.gradingEngine.testDataFiles.append(testDataFileName)
                console("creating sub-test case file " + testDataFileName)


# =======================================================================
# runMoss()
# =======================================================================
def _runMoss(self, assignment):
    # ---------- configure the Moss client ----------

    #set server and port
    self._mossClient.setServer(self.getConfiguration(self.AG_CONFIG.MOSS_SERVER))
    self._mossClient.setServerPort(int(self.getConfiguration(self.AG_CONFIG.MOSS_PORT)))

    #set userid
    self._mossClient.setUserId(self.getConfiguration(self.AG_CONFIG.MOSS_USERID))

    #set m
    self._mossClient.setIgnoreLimit(int(self.getConfiguration(self.AG_CONFIG.MOSS_MAX_MATCHES)))

    #set n
    self._mossClient.setNumberOfMatchingFiles(int(self.getConfiguration(self.AG_CONFIG.MOSS_NUM_MATCH_FILES)))

    self._mossClient.setCommentString(self._assignment.assignmentName)

    #set language
    #assume the language of the first submission is the language for all submissions
    if assignment.submissions[0].language == IAGConstant.LANGUAGE_PYTHON3:
        self._mossClient.setLanguage("python")
    elif assignment.submissions[0].language == IAGConstant.LANGUAGE_CPP:
        self._mossClient.setLanguage("cc")
    else:
        console('Failed to invoke MOSS: Must specify a language.')
        return ''

    #add base files
    #self._mossClient.addBaseFile("submission/test_student.py");

    # Add Submission Files
    for submission in assignment.submissions:
        for submissionFile in submission.submissionFiles:
            #console('submissionFile = ' + os.path.join(submission.submissionDirectory, submissionFile))
            self._mossClient.addFile( os.path.join(submission.submissionDirectory, submissionFile) )

    self._mossUrl = ''
    self._mossThreadHandle = threading.Thread(target=_mossThread, args=(self,))
    console("Attempting to launch moss thread...")
    self._mossThreadHandle.start()

    return

# =======================================================================
# _mossThread()
# =======================================================================
def _mossThread(self):
    console('Moss thread starting...')
    self._mossUrl = self._mossClient.send()
    console('Moss thread ending...')

# =======================================================================
# grade()
# =======================================================================
def grade(self):
    self._updateAutoGraderConfiguration()

    # copy data files to each submission directory
    self._prepareDataFiles()


    # ---------- generate break out test files ----------
    # create a directory to house the breakout files
    #testOutputDir = os.path.join(os.path.join(self._assignment.assignmentDirectory), "breakout")
    testOutputDir = os.path.join(os.path.join(self.lms.getWorkingDirectory()), "breakout")
    try:
        os.mkdir(testOutputDir)
    except:
        #the directory may already exist: don't error out
        pass

    self.breakOutTestFiles( testOutputDir )

    #attempt to discover the primary submission file for each submission
    for submission in self._agDocument.gradingEngine.submissions:
        self._discoverPrimarySubmissionFile(submission)


    # ---------- MOSS ----------
    # if using MOSS, setup here and start the moss thread
    bUseMoss = self.getConfiguration(IAGConstant.AG_CONFIG.USE_MOSS) == IAGConstant.YES

    if bUseMoss:
        self._runMoss(self._assignment)
    else:
        console("Moss not enabled.")

    # perform grading
    console("Processing submissions...")
    self._agDocument.gradingEngine.processSubmissions()

    # grading happens is a separate thread.  We can monitor the state of that thread through the status
    # variable returned by gradingEngine.getProcessingStatus()
    status = self._agDocument.gradingEngine.getProcessingStatus()

    # wait for grading thread to complete
    console('Waiting for grading thread...')
    progressStartVal = self._agDocument.gradingEngine.processingStatus.startVal
    progressEndVal = self._agDocument.gradingEngine.processingStatus.endVal
    while status.bRunning == True:
        #print('$$$$$', self._agDocument.gradingEngine.processingStatus.progress, progressStartVal, type(progressStartVal), progressEndVal, type(progressEndVal))
        x = (f"Grading status... {format(100 * self._agDocument.gradingEngine.processingStatus.progress / (progressEndVal - progressStartVal), '.1f')}pct")
        console(x)
        time.sleep(0.5)
    console('Grading thread ended.')

    if bUseMoss:
        # wait for MOSS thread to complete
        console('Waiting for MOSS thread...')
        while self._mossThreadHandle.isAlive():
            print('#', end='')
            time.sleep(0.5)

        console('MOSS thread ended')
        console('MOSS URL = ' + self._mossUrl)


    # remove breakout sub directory and all its contents
    try:
        rmtree(testOutputDir)
    except:
        #the directory may not exist: don't error out
        pass


    # cleanup data files
    self._cleanupDataFiles()

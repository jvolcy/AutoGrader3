import os
import sys
import time
from shutil import rmtree
from pathlib import Path
import threading
import subprocess
from .IAGConstant import IAGConstant
from .console import console
from .AGDocument import AGDocument
from .MossClient import MossClient
from .GradingEngine import GradingEngine
import json


# =======================================================================
# AutoGrader3 class
#
# Structure of AutoGrader3 class
#
# AutoGrader3 classes ("has a")
# 	AGDocument
# 	Simulator, MoodleClient, CanvasClient, etc.  all implement (IAssignmentStore)
# 	GradingEngine
# 	MossClient
# 	ReportGenerator
# 	IAssignmentStore (implements: submissionName, submissionDirectory, [[submissionFiles], studentName, studentID, submitGrade(grade, msg)], setWorkingDirectory() )
#
# AutoGrader3 files structure -> what objects/functions the file manages
# 	_agConfig.py -> misc configurations
# 	_agLmsInterface.py -> Moodle, Canvas, Simulator
# 	AutoGrader3.py -> pre-processing, GradingEngine, MossClient
# 	_agReport.py -> ReportGenerator, CodeAnalyzer, teacher grade & feedback
#
# =======================================================================
class AutoGrader3(IAGConstant):

    '''# General configurations
    from ._agConfig import _autoLocateCppCompiler
    from ._agConfig import _autoLocatePython3Interpreter
    from ._agConfig import _autoLocateShell
    from ._agConfig import _loadConfiguration
    from ._agConfig import _setupConfiguration
    from ._agConfig import getConfiguration
    from ._agConfig import saveConfiguration
    from ._agConfig import setConfiguration

    # Grading Engine module functions
    from .AutoGrader3 import _updateAutoGraderConfiguration
    from .AutoGrader3 import _setAssignmentName
    from .AutoGrader3 import _cleanupDataFiles
    from .AutoGrader3 import _discoverPrimarySubmissionFile
    from .AutoGrader3 import _prepareDataFiles
    from .AutoGrader3 import addSubmission
    from .AutoGrader3 import addDataFile
    from .AutoGrader3 import addTestDataFile
    from .AutoGrader3 import breakOutTestFiles
    from .AutoGrader3 import grade
    from .AutoGrader3 import _autoDetectLanguage

    # MOSS
    from .AutoGrader3 import _runMoss
    from .AutoGrader3 import _mossThread'''


    # =======================================================================
    # AutoGraderApp()
    # constructor
    # =======================================================================
    def __init__(self):
        # private GradingEngine gradingEngine
        console("AutoGraderApp constructor...")

        # ---------- setup app configurations ----------
        self._setupConfiguration()

        # ---------- instantiate the AGDocument object ----------
        self.agDocument = AGDocument()

        # ---------- create the LMS interface ----------
        #self._lmsInterface = None   # this is an IAssignmentStore object
        #self._assignment = None     # this is an LMS exchange object (Assignment class)

        # ---------- MOSS ----------
        self._mossClient = MossClient()
        self._mossUrl = ''          #the URL of the resulting MOSS comparison
        self._mossThreadHandle = None     #handle the the MOSS thread


        # ---------- instantiate a grading engine ----------
        self.gradingEngine = GradingEngine()

    # =======================================================================
    # Configuration functions
    # =======================================================================


    # =======================================================================
    # private String autoLocatePython3Interpreter() {
    # This function attempts to automatically find the path to an
    # installed python3 interpreter on the current system.  The function
    # assumes that the 'which' command is available on the system.  That
    # is, it assumes that we are on a *nix system or a Windows system
    # with cygwin installed.  The function also assumes that the
    # interpreter is called, aliased or linked as 'python3'.
    # The function first uses the 'which python3' system command to
    # check for the p3 interpreter in the current search path.  If that
    # fails, the function specifically checks the path "/usr/local/bin/python3".
    # If a p3 interpreter is found, its path is returned.  If not,
    # the function returns null.
    # =======================================================================
    def _autoLocatePython3Interpreter(self):
        python3Path = ''
        try:
            # first, use "which python3" to try to find a Python 3 interpreter
            p = subprocess.Popen('which python3', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            python3Path = p.stdout.read().decode("UTF-8").strip()

            # if "which python3" did not yield a suitable interpreter, check for one at /usr/local/bin/python3.
            if python3Path == '':
                FALLBACK_PYTHON3_PATH = "/usr/local/bin/python3"

                if os.path.isfile(FALLBACK_PYTHON3_PATH):
                    python3Path = FALLBACK_PYTHON3_PATH

        except:
            e = sys.exc_info()[0]
            console("autoLocatePython3Interpreter(): " + str(e))

        return python3Path

    # =======================================================================
    # private String autoLocateCppCompiler()
    # This function attempts to automatically find the path to an
    # installed C++ compiler on the current system.  The function
    # assumes that the 'which' command is available on the system.  That
    # is, it assumes that we are on a *nix system or a Windows system
    # with cygwin installed.  The function also assumes that the
    # interpreter is called, aliased or linked as 'g++' or 'c++'.
    # If a c++ compiler is found, its path is returned.  If not,
    # the function returns null.
    # =======================================================================
    def _autoLocateCppCompiler(self):
        cppPath = ''
        try:
            # use "which g++" to try to find a c++ compiler
            p = subprocess.Popen('which g++', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            cppPath = p.stdout.read().decode("UTF-8").strip()

            # if "which g++" did not yield a suitable compiler, check for 'c++'
            if cppPath == '':
                p = subprocess.Popen('which c++', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p.wait()
                cppPath = p.stdout.read().decode("UTF-8").strip()

            # if still not found, check for 'cpp'
            if cppPath == '':
                # use "which c++" to try to find a Python 3 interpreter
                p = subprocess.Popen('which cpp', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p.wait()
                cppPath = p.stdout.read().decode("UTF-8").strip()
        except:
            e = sys.exc_info()[0]
            console("autoLocateCppCompiler(): " + str(e))

        return cppPath

    # =======================================================================
    # private String autoLocateShell()
    # =======================================================================
    def _autoLocateShell(self):
        shellPath = ''
        try:
            p = subprocess.Popen('which bash', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            shellPath = p.stdout.read().decode("UTF-8").strip()

            # if "which bash" did not yield a suitable shell, check for 'sh'
            if shellPath == '':
                # use "which sh" to try to find a shell interpreter
                p = subprocess.Popen('which sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p.wait()
                shellPath = p.stdout.read().decode("UTF-8").strip()

        except:
            e = sys.exc_info()[0]
            console("autoLocateShell(): " + str(e))

        return shellPath

    # =======================================================================
    # public String getConfiguration(String key)
    # This function returns the value for the supplied configuration key.
    # If the key is not in the configuraiton dictionary ag_config, the
    # function returns null.  All configuration keys and values are strings.
    # =======================================================================
    def getConfiguration(self, key):
        # console("getting conf. for " + key)
        return self._ag_config[key]

    # =======================================================================
    # public String setConfiguration(String key, String value)
    # This function returns the value for the supplied configuration key.
    # If the key is not in the configuraiton dictionary ag_config, the
    # function returns null.  All configuration keys and values are strings.
    # =======================================================================
    def setConfiguration(self, key, value):
        # console("setting conf. for " + key)
        self._ag_config[key] = value

    # =======================================================================
    # private void setupConfiguration()
    # This function sets up default AG2 configurations.
    # The values used for the configurations are either hardcoded defaults
    # or generated by probing the system.
    # =======================================================================
    def _setupConfiguration(self):
        # ---------- AutoGrader options ----------
        self._ag_config = {}

        # ---------- set the path to the JSON config file ----------
        self._configFileName = IAGConstant.CONFIG_FILENAME

        # get the user's home directory and set the path to the config file
        home = str(Path.home())
        home = home.rstrip('/')  # remove the trailing '/' if it is present
        self.configFile = home + '/' + self._configFileName
        console("Config file path = '" + self.configFile + "'")

        # ---------- auto-locate python3 interpreter ----------
        python3Path = self._autoLocatePython3Interpreter()
        if python3Path == '':
            console("No auto-detected python3 interpreter.")
        else:
            console("Found a Python3 interpreter at '" + python3Path + "'")

        # ---------- auto-locate c++ compiler ----------
        cppPath = self._autoLocateCppCompiler()
        if cppPath == '':
            console("No auto-detected c++ compiler.")
        else:
            console("Found a c++ compiler at '" + cppPath + "'")

        # ---------- auto-locate shell interpreter ----------
        shellPath = self._autoLocateShell()
        if shellPath == '':
            console("No auto-detected shell interpreter.")
        else:
            console("Found a shell interpreter at '" + shellPath + "'")

        # ---------- Generate or set the default AG options ----------
        self._ag_config[IAGConstant.AG_CONFIG.LANGUAGE] = IAGConstant.LANGUAGE_AUTO
        self._ag_config[IAGConstant.AG_CONFIG.MAX_RUNTIME] = "3"
        self._ag_config[IAGConstant.AG_CONFIG.MAX_OUTPUT_LINES] = "100"
        self._ag_config[IAGConstant.AG_CONFIG.INCLUDE_SOURCE] = IAGConstant.YES
        self._ag_config[IAGConstant.AG_CONFIG.AUTO_UNCOMPRESS] = IAGConstant.YES
        self._ag_config[IAGConstant.AG_CONFIG.PROCESS_RECURSIVELY] = IAGConstant.YES
        self._ag_config[IAGConstant.AG_CONFIG.PYTHON3_INTERPRETER] = python3Path
        self._ag_config[IAGConstant.AG_CONFIG.CPP_COMPILER] = cppPath
        self._ag_config[IAGConstant.AG_CONFIG.SHELL] = shellPath

        self._ag_config[IAGConstant.AG_CONFIG.USE_MOSS] = IAGConstant.NO
        self._ag_config[IAGConstant.AG_CONFIG.MOSS_USERID] = ""
        self._ag_config[IAGConstant.AG_CONFIG.MOSS_SERVER] = MossClient.getDefaultMossServer()
        self._ag_config[IAGConstant.AG_CONFIG.MOSS_PORT] = str(MossClient.getDefaultMossPort())
        self._ag_config[IAGConstant.AG_CONFIG.MOSS_MAX_MATCHES] = "10"  # -m
        self._ag_config[IAGConstant.AG_CONFIG.MOSS_NUM_MATCH_FILES] = "250"  # -n

        self._ag_config[IAGConstant.AG_CONFIG.MOODLE_SERVER] = ""
        self._ag_config[IAGConstant.AG_CONFIG.MOODLE_EMAIL] = ""
        self._ag_config[IAGConstant.AG_CONFIG.MOODLE_KEY] = ""

        # ---------- Overwrite the default AG options with data from the JSON file ----------
        self._loadConfiguration()

    # =======================================================================
    # private void loadConfiguration()
    # This function loads the AG2 configurations from a JSON file.
    #
    # configFileName is the full path of the JSON configuration file.
    # =======================================================================
    def _loadConfiguration(self):

        console("AutoGrader3: Loading configuration from " + str(self.configFile))
        try:
            with open(self.configFile) as f:
                config = json.load(f)

            for item in config:
                self._ag_config[item] = config[item]

        except:
            # if the file does not exist, or is otherwise inaccessible, do nothing
            console("Warning: unable to source " + self.configFile)
            return

    # =======================================================================
    # public void saveConfiguration()
    # This function saves the AG2 configurations to a JSON file.
    #
    # configFileName is the full path of the JSON configuration file.
    # =======================================================================
    def saveConfiguration(self):

        console("AutoGrader3: Saving configuration to " + str(self.configFile))

        with open(self.configFile, 'w') as json_file:
            json.dump(self._ag_config, json_file)

    # =======================================================================
    # xxx
    # =======================================================================


    # =======================================================================
    # Pre-processor and Misc functions
    # =======================================================================
    def _setAssignmentName(self, submissionName):
        self.agDocument.assignmentName = submissionName

    def addTestDataFile(self, testDataFile):
        self.agDocument.testDataFiles.append(testDataFile)
        #self.gradingEngine.testDataFiles.append(testDataFile)

    def addDataFile(self, dataFile):
        self.agDocument.dataFiles.append(dataFile)
        #self.agDocument.dataFiles.append(dataFile)

    #def addSubmission(self, submission):
        #self.agDocument.assignment.submissions.
        #self.agDocument.assignment.submissions.append(submission)

    # =======================================================================
    # prepareDataFiles()
    # This function creates a symbolic link of all data needed files in the
    # submission directory of every submission
    # =======================================================================
    def _prepareDataFiles(self):
        # ---------- symlink all data files into each submission directory ----------
        # go through every data file in the listDataFiles list box
        for src in self.agDocument.dataFiles:
            # symlink each data file to each of the submission directories
            for submission in self.agDocument.assignment.submissions:
                dst = submission.submissionDirectory + "/" + os.path.basename(src)
                try:
                    # console("copying \"" + src + "\" to \"" + dst + "\"")
                    # copy(src, dst)
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
        for src in self.agDocument.dataFiles:
            # delete the data files from each of the submission directories
            for submission in self.agDocument.assignment.submissions:
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
        # if the user has already specified a primary submission file, do nothing
        if submission.primarySubmissionFile is not None:
            return

        # if we only have 1 submissionFile, make it the primary
        if len(submission.submissionFiles) == 1:
            submission.primarySubmissionFile = submission.submissionFiles[0]

        # return without setting the value of the primarySubmissionFile (at this point, it should be None)
        # This does not matter for C++.
        return

    # =======================================================================
    # _autoDetectLanguage
    # =======================================================================
    def _autoDetectLanguage(self):
        # define a variable that will be used to set the language for all submissions assignment
        submissionLanguage = IAGConstant.LANGUAGE_AUTO

        # now go through every submission until we find either a python of c++ file
        # the first one we find will be assumed to represent the language for all submissions
        for submission in self.agDocument.assignment.submissions:
            # attempt to auto-detect the language.  This is a very primitive method:  The very first
            # file that is in the pythons or C++ extension list sets the langauge for the entire assignment
            if submission.language == IAGConstant.LANGUAGE_AUTO or submission.language == '':
                for file in submission.submissionFiles:
                    # get the file extension
                    filename, file_extension = os.path.splitext(file)
                    file_extension = file_extension.lstrip('.')

                    if file_extension in IAGConstant.PYTHON_EXTENSIONS:
                        submissionLanguage = IAGConstant.LANGUAGE_PYTHON3
                        console("Python auto-detected.")
                        break

                    if file_extension in IAGConstant.CPP_EXTENSIONS:
                        submissionLanguage = IAGConstant.LANGUAGE_CPP
                        console("C++ auto-detected")
                        # language changed: change the language of the current submission
                        break
            else:
                # we already have a language.  Use it for all submissions
                submissionLanguage = submission.language
                break

        # update all submissions with the same language.
        for submission in self.agDocument.assignment.submissions:
            submission.language = submissionLanguage

    # =======================================================================
    # _updateAutoGraderConfiguration
    # =======================================================================
    def _updateAutoGraderConfiguration(self):
        self.gradingEngine.setCppCompiler(self.getConfiguration(self.AG_CONFIG.CPP_COMPILER))
        self.gradingEngine.setPython3Interpreter(self.getConfiguration(self.AG_CONFIG.PYTHON3_INTERPRETER))
        self.gradingEngine.setShellInterpreter(self.getConfiguration(self.AG_CONFIG.SHELL))
        self.gradingEngine.setTempOutputDirectory(str(Path.home()))
        self.gradingEngine.setMaxOutputLines(int(self.getConfiguration(self.AG_CONFIG.MAX_OUTPUT_LINES)))
        self.gradingEngine.setMaxRunTime(int(self.getConfiguration(self.AG_CONFIG.MAX_RUNTIME)))

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

        # go through every file in the listTestData list box
        for filename in self.agDocument.testDataFiles:

            # read the content of the test file
            with open(filename, 'r') as file:
                content = file.read()

            # search for test case separators
            subCases = content.split(IAGConstant.TEST_CASE_SEPARATOR)

            # if none are found, the length of subCases array will be 1.
            # In that case, leave the the current entry in the agDocument.gradingEngine.testDataFiles list
            if len(subCases) == 1:
                continue
            else:
                # remove the top-level test data file
                self.gradingEngine.testDataFiles.remove(filename)

                # create temporary files in the output directory for each sub-case
                for counter in range(1, len(subCases) + 1):
                    testDataFileName = os.path.join(outputDirectory, os.path.basename(filename) + '-' + str(counter))

                    # write the sub-case to file
                    with open(testDataFileName, 'w') as file:
                        file.write(subCases[counter - 1])

                    # add this to the testFiles list
                    self.gradingEngine.testDataFiles.append(testDataFileName)
                    console("creating sub-test case file " + testDataFileName)

    # =======================================================================
    # runMoss()
    # =======================================================================
    def _runMoss(self, assignment):
        # ---------- configure the Moss client ----------

        # set server and port
        self._mossClient.setServer(self.getConfiguration(self.AG_CONFIG.MOSS_SERVER))
        self._mossClient.setServerPort(int(self.getConfiguration(self.AG_CONFIG.MOSS_PORT)))

        # set userid
        self._mossClient.setUserId(self.getConfiguration(self.AG_CONFIG.MOSS_USERID))

        # set m
        self._mossClient.setIgnoreLimit(int(self.getConfiguration(self.AG_CONFIG.MOSS_MAX_MATCHES)))

        # set n
        self._mossClient.setNumberOfMatchingFiles(int(self.getConfiguration(self.AG_CONFIG.MOSS_NUM_MATCH_FILES)))

        self._mossClient.setCommentString(self.agDocument.assignment.assignmentName)

        # set language
        # assume the language of the first submission is the language for all submissions
        if assignment.submissions[0].language == IAGConstant.LANGUAGE_PYTHON3:
            self._mossClient.setLanguage("python")
        elif assignment.submissions[0].language == IAGConstant.LANGUAGE_CPP:
            self._mossClient.setLanguage("cc")
        else:
            console('Failed to invoke MOSS: Must specify a language.')
            return ''

        # add base files
        # self._mossClient.addBaseFile("submission/test_student.py");

        # Add Submission Files
        for submission in assignment.submissions:
            for submissionFile in submission.submissionFiles:
                # console('submissionFile = ' + os.path.join(submission.submissionDirectory, submissionFile))
                self._mossClient.addFile(os.path.join(submission.submissionDirectory, submissionFile))

        self._mossUrl = ''
        self._mossThreadHandle = threading.Thread(target=self._mossThread)
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
        # testOutputDir = os.path.join(os.path.join(self._assignment.assignmentDirectory), "breakout")
        testOutputDir = os.path.join(os.path.join(self.lms.getWorkingDirectory()), "breakout")
        try:
            os.mkdir(testOutputDir)
        except:
            # the directory may already exist: don't error out
            pass

        self.breakOutTestFiles(testOutputDir)

        #  attempt to auto-detect the language for the entire assignment
        self._autoDetectLanguage()

        # attempt to discover the primary submission file for each submission
        for submission in self.agDocument.assignment.submissions:
            self._discoverPrimarySubmissionFile(submission)

        # ---------- MOSS ----------
        # if using MOSS, setup here and start the moss thread
        bUseMoss = self.getConfiguration(IAGConstant.AG_CONFIG.USE_MOSS) == IAGConstant.YES

        if bUseMoss:
            self._runMoss(self.agDocument.assignment)
        else:
            console("Moss not enabled.")

        # perform grading
        console("Processing submissions...")
        self.gradingEngine.processSubmissions()

        # grading happens is a separate thread.  We can monitor the state of that thread through the status
        # variable returned by gradingEngine.getProcessingStatus()
        status = self.gradingEngine.getProcessingStatus()

        # wait for grading thread to complete
        console('Waiting for grading thread...')
        progressStartVal = self.gradingEngine.processingStatus.startVal
        progressEndVal = self.gradingEngine.processingStatus.endVal
        while status.bRunning == True:
            # print('$$$$$', self.agDocument.gradingEngine.processingStatus.progress, progressStartVal, type(progressStartVal), progressEndVal, type(progressEndVal))
            x = (
                f"Grading status... {format(100 * self.gradingEngine.processingStatus.progress / (progressEndVal - progressStartVal), '.1f')}pct")
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
            # the directory may not exist: don't error out
            pass

        # cleanup data files
        self._cleanupDataFiles()

# =======================================================================
# xxx
# =======================================================================

# ----------  ----------
# ----------  ----------
# ----------  ----------
# ----------  ----------

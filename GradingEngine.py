from IAGConstant import IAGConstant
from console import console
import subprocess
import os
import sys
import time
import threading

#import static AutoGraderApp.Controller.message;

# =======================================================================
# structure to hold the results returned by the shellExec() function.
# ======================================================================
class shellExecResult(object):
    def __init__(self, bTimedOut=False, bMaxLinesExceeded=False, output=None, execTimeSec=0.0):
        self.bTimedOut = bTimedOut
        self.bMaxLinesExceeded = bMaxLinesExceeded
        self.output = output
        self.execTimeSec = execTimeSec


# =======================================================================
# structure to reports the status of the grading process,
# processSubmissions().  This function is expected to be run inside
# of a thread, service or task.  The status structure is used to "peek"
# inside the running process.
# ======================================================================
class ProcessingStatus(object):
    def __init__(self, bRunning, message, progress, startVal, endVal):
        self.bRunning = bRunning
        self.message = message
        self.progress = progress
        self.startVal = startVal
        self.endVal = endVal


# =======================================================================
# GradingEngine class
# This class compiles and executes (or interprets) student submissions.
# The central function of the class is processFiles().
# At a minimum, the caller should specify the following prior to
# calling processFiles:
# - an ArrayList of Submissions
# - a cppCompiler or python3Interpreter, as appropriate
# - testDataFiles, if required
# ======================================================================
class GradingEngine(IAGConstant):

    # =======================================================================
    # GradingEngine()
    # GradingEngine Constructor
    # ======================================================================
    def __init__(self):
        # The submissions list.
        self.agDocument = None
        #self.agDocument.testDataFiles = []
        #private String outputFileName;
        self.__tempOutputDirectory = None
        self.__bIncludeSourceInOutput = True
        self.__maxRunTime = 3
        self.__maxOutputLines = 100
        self.__cppCompiler = None
        self.__python3Interpreter = None
        self.__shell = None
        self.processingStatus = ProcessingStatus(False, "", 0, 0, 0)

        self.bAbortRequest = None
        self.__gradingServiceThread = None
        self.__bLastReadExceedsMaxLines = None
        self.__MAX_COMPILE_TIME_SEC = 10
        self.__MAX_COMPILER_OUTPUT_LINES = 200


    # =======================================================================
    # public ProcessingStatus getProcessingStatus()
    # ======================================================================
    def getProcessingStatus(self):
        return self.processingStatus


    # =======================================================================
    # public void setMaxRunTime(int maxRunTime)
    # ======================================================================
    def setMaxRunTime(self, maxRunTime):
        self.__maxRunTime = maxRunTime


    # public void setMaxOutputLines(int maxOutputLines)
    def setMaxOutputLines(self, maxOutputLines):
        self.__maxOutputLines = maxOutputLines


    # public void setPython3Interpreter(String python3Interpreter)
    def setPython3Interpreter(self, python3Interpreter):
        self.__python3Interpreter = python3Interpreter


    # public void setCppCompiler(String cppCompiler)
    def setCppCompiler(self, cppCompiler):
        self.__cppCompiler = cppCompiler


    # public void setShellInterpreter(String shell)
    def setShellInterpreter(self, shell):
        self.__shell = shell


    # =======================================================================
    #     public void setTempOutputDirectory(String dirName)
    # ======================================================================
    def setTempOutputDirectory(self, dirName):
        self.__tempOutputDirectory =  dirName
        console("output directory = " + self.__tempOutputDirectory)


    # =======================================================================
    # private String fileNameFromPathName(String pathName)
    # ======================================================================
    def __fileNameFromPathName(self, pathName):
        #extract the filename from the path name
        return os.path.split(pathName)[1]

    # =======================================================================
    # private String readFromFile(String filepath)
    # ======================================================================
    def __blockReadFromFile(self, filepath):
        #console("__blockReadFromFile() " + filepath)
        self.__bLastReadExceedsMaxLines = False
        try:
            inFile = open(filepath, 'rt')
            text = inFile.read()
            inFile.close()
            return text
        except:
            e = sys.exc_info()[0]
            console("__blockReadFromFile(): " + str(e))

        return None



    # =======================================================================
    # private String readFromFile(String filepath, int maxLines)
    # set maxLines to 0 to read the entire file.  This is the default.
    # Also, for maxLines > 0, limit the length of each line to maxCharsPerLine.
    # (this avoids large output files due to ridiculously long lines)
    # ======================================================================
    def __readFromFile(self, filepath, maxLines = 0, maxCharsPerLine = 200):
        #console("__readFromFile() " + filepath)

        self.__bLastReadExceedsMaxLines = False

        #simulate the overloaded verson of __readFromFile()
        if maxLines == 0:
            return self.__blockReadFromFile(filepath)

        #initialize the output string
        text = ""

        #attempt to read the file line by line
        try:
            b = open(filepath, 'rt')

            numLines = 0   #line #

            #read the file line by-line until we are out of lines or have
            #reached the max allowed
            readLine = 'x'     #individual lines in the file
            while readLine !='' and numLines < maxLines:
                readLine = b.readline()
                if readLine == '':
                    #do nothing.  We are at the end of the file
                    pass
                elif len(readLine) > maxCharsPerLine:
                    #truncate the line
                    text += readLine[:maxCharsPerLine] + '...\n' # limit the line length
                    numLines += 1
                else:
                    text += readLine
                    numLines += 1

            if numLines == maxLines:
                self.__bLastReadExceedsMaxLines = True

        except:
            e = sys.exc_info()[0]
            console("__readFromFile(): " + str(e))

        #console("__readFromFile(): " + text[:50] + '...')
        return text


    # =======================================================================
    # private String getFileExtension(String fileName)
    # returns the extension of the given filename.
    # ======================================================================
    def __getFileExtension(self, fileName):
        return os.path.splitext(fileName)[1].lstrip('.')


    # =======================================================================
    # private ArrayList<Integer> getPidFromToken(String token)
    #
    # This function attempts to determine the PID of a running process
    # based on any substring, the token, found on the command line used
    # to launch the the process.  The token should be as unique a
    # substring as possible.  A good substring would be the name of a
    # file that is a part of the command-line argument.
    # The function uses the "ps -eo pid,command" command to list the
    # PID and associated command-line used to launch the different
    # running processes on the system.  The returned ArraList is a list
    # of PIDs for all commands that match the token.
    # ======================================================================
    def __getPidFromToken(self, token):
        pids = []
        try:
            out = subprocess.Popen(['ps', '-eo', 'pid,command'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

            stdout, stderr = out.communicate()
            # print("stderr = ", stderr)
            stdoutList = stdout.decode("utf-8").split('\n')

            for line in stdoutList:
                if token in line:
                    pidStr = line.strip().split(" ")[0]
                    pids.append(int(pidStr))
                    #console(pidStr + "-->" + line.strip().split(" ")[1])
        except:
            e = sys.exc_info()[0]
            #console("getPidFromToken():" + str(e))

        return pids

    # =======================================================================
    # private shellExecResult compileCppFiles(String compiler, ArrayList<File>sourceFiles, File exeFile, Integer timeoutSec, Integer maxOutputLines)
    # ======================================================================
    def __compileCppFiles(self, compiler, sourceFiles, exeFile, timeoutSec, maxOutputLines):
        #Delineate the start of the unformatted py code output with a token: PROG_OUTPUT_START_TOKEN.
        #Flank with '\n's to ensure the token is on a line by itself


        # compile the code
        compile_args = "\"" + compiler + "\" -o \"" + exeFile + "\" "

        for sourceFile in sourceFiles:
            # include only .cpp files (not .h or .hpp files) on the g++ command line
            if self.__getFileExtension(sourceFile) in IAGConstant.CPP_COMPILER_EXTENSIONS:
                compile_args = compile_args + "\"" + sourceFile + "\" "


        #store the compiler output to a temp file
        #compile_args = compile_args + "> \"" + tmpFile + "\" 2>&1";

        #delete any previously compiled exe file in the output directory.
        try:
            os.remove(exeFile)
        except:
            # ignore errors from the delete operation
            pass


        #perform the compilation
        console("compiling:" + compile_args)
        execResult = self.__shellExec(compile_args, timeoutSec, maxOutputLines, os.path.abspath(exeFile), os.path.dirname(exeFile))

        return execResult

        #copy the first maxOutputLines from the temp file to the output file
        #Also, limit the #bytes to 40# maxOutputLines(this avoids large output files due to ridiculously long lines)



    # =======================================================================
    # private shellExecResult shellExec(String args, int timeout_sec, int maxOutputLines, String identifyingToken, String workingDirectory)
    #
    # function that executes a command inside a shell.  The function
    # returns the output of the shell session which is a combination of
    # the stdout and stderr.
    # The identifyingToken is an optional string that is part of
    # the command to be executed.  This should be as unique a string
    # as possible.  It is used to determine the ID of the launched
    # process by searching the output of "ps -eo pid,command" which
    # lists PID and the command line used to launch the corresponding
    # process.
    # ======================================================================
    def __shellExec(self, args, timeout_sec, maxOutputLines, identifyingToken, workingDirectory):
        execResult = shellExecResult()
        execResult.bTimedOut = False
        execResult.bMaxLinesExceeded = False
        execResult.execTimeSec = 0.0

        # create a temp file to capture program output
        tmpFile = self.__tempOutputDirectory + "/TEMP.AG2"

        # form the command string, redirecting both stdout and stderr to the temporary file
        cmd = [self.__shell, "-c", args + " >> \"" + tmpFile + "\" 2>&1"]
        cmd = [args + " >> \"" + tmpFile + "\" 2>&1"]

        # concatenate the cmd array string for display on the console
        cmdStr = ""
        for s in cmd:
            cmdStr += s + " "

        console("Executing " + args + "\n  as  " + cmdStr)

        try:
            start_time = time.time()
            p = subprocess.Popen(args=cmdStr, shell=True,
                                 cwd=workingDirectory)  # the pid returned appears to be the pid of the shell

            if timeout_sec > 0:
                elapsed_time = time.time() - start_time
                while p.poll() is None and elapsed_time < timeout_sec:
                    elapsed_time = time.time() - start_time
                    #print("*", end='')
                    time.sleep(0.2)
            else:  # user specified 0 or a negative value for the max run time --> wait indefinitely
                p.wait()  # wait indefinitely for process to terminate
                elapsed_time = time.time() - start_time

            execResult.execTimeSec = elapsed_time

            # kill the process, if it has exceeded its max run time
            if elapsed_time >= timeout_sec and timeout_sec > 0:
                execResult.bTimedOut = True
                console("Killing process {0}. Run time exceeds max value of {1} seconds.".format(p.pid, timeout_sec))
                p.terminate()  # try a s/w termination
                time.sleep(1)  # wait 1 second
                p.kill()  # force the termination

                # force the issue by killing all identified processes with
                # a unix kill command.

                # attempt to detect the PIDs of the launched shell and command
                pids = self.__getPidFromToken(identifyingToken)
                for pid in pids:
                    killCmd = "kill -9 " + str(pid)
                    console(killCmd);
                    os.system(killCmd)

                console(
                    "Maximum execution time of {0} seconds exceeded.  Process forcefully terminated... output may be lost.".format(
                        timeout_sec))

            # copy the first maxOutputLines from the temp file to the output file
            # Also, limit the # bytes to 100*maxOutputLines (this avoids large output files due to ridiculously long lines)
            # self._fileHead(tmpFile, outputFile, maxOutputLines, 40*maxOutputLines)
            # self._removeFile(tmpFile)

        except:
            e = sys.exc_info()[0]
            console("shellExec(): " + str(e))

        # read in the output of the executed command from the temp file
        execResult.output = self.__readFromFile(tmpFile, maxOutputLines)
        if self.__bLastReadExceedsMaxLines:
            execResult.bMaxLinesExceeded = True

        # delete the tmp file
        try:
            os.remove(tmpFile)
        except:
            e = sys.exc_info()[0]
            console("shellExec(): os.remove("+tmpFile+") " + str(e))

        return execResult

    # =======================================================================
    # private void pythonSubProcess(Submission submission, int numTests, boolean bNoTestFiles)
    # The functions pythonSubProcess() and cppSubProcess() exist simply
    # to reduce the size of the execSubmission() function.  Much of the
    # pre- and post-processing leading up to and following the calls to
    # these functions is common.  To the extent possible, that commonality
    # is captured in execSubmission().
    # ======================================================================
    def __pythonSubProcess(self, submission, numTests, bNoTestFiles):

        # For python, there should be a primary submission file;  for C++, it doesn't matter
        if submission.primarySubmissionFile is None:
            return

        #sourceFile = os.path.abspath(submission.primarySubmissionFile)
        sourceFile = submission.primarySubmissionFile

        # we have to add logic that handles the case where no test files are required differently
        # from the cases where test files are needed.  In the former case, there is no input
        # redirection (no user input).  In the latter case, we redirect stdin from the test
        # data files.  The command line includes a "< testFile" argument.

        # run the code for each test case.
        for i in range(numTests):
            # use bNoTestFiles to determine the format of the command string, cmd
            if bNoTestFiles:
                console("Warning: no test files.")
                # if we have no test files, do not include input redirection in the exec command
                cmd = "\"" + self.__python3Interpreter + "\" " + \
                        "\"" + sourceFile + "\""
            else:
                # we have test files: use them to redirect stdin in the exec command
                dataFileName = os.path.abspath(self.agDocument.testDataFiles[i])
                cmd = "\"" + self.__python3Interpreter + "\" " + \
                        "\"" + sourceFile + "\"" + " < \"" + dataFileName + "\""

            # the command string, cmd
            execResult = self.__shellExec(cmd, self.__maxRunTime, self.__maxOutputLines, sourceFile, submission.submissionDirectory)

            # store the output in the submission object
            submission.progOutputs[i] = execResult.output

            # store any runtime/compiler errors in the submission object
            submission.runtimeErrors[i] = ""   #initialize the runtimeErrors string
            if execResult.bTimedOut:
                submission.runtimeErrors[i] += "Maximum execution time of " + str(self.__maxRunTime) \
                        + " seconds exceeded.  Process forcefully terminated... output may be lost.\n"

            if execResult.bMaxLinesExceeded:
                submission.runtimeErrors[i] += "Maximum lines of output (" + str(self.__maxOutputLines) \
                        + ") exceeded.  Output truncated.\n"


            # store the execution time in the submission object
            submission.executionTimes[i] = execResult.execTimeSec


    # =======================================================================
    # private void cppSubProcess(Submission submission, int numTests, boolean bNoTestFiles)
    # The functions pythonSubProcess() and cppSubProcess() exist simply
    # to reduce the size of the execSubmission() function.  Much of the
    # pre- and post-processing leading up to and following the calls to
    # these functions is common.  To the extent possible, that commonality
    # is captured in execSubmission().
    # ======================================================================
    def __cppSubProcess(self, submission, numTests, bNoTestFiles):
        #console("cppSubProcess: " + submission.participant.name)

        exeFile = submission.submissionDirectory + "/AG.out"

        # Compile the source once.
        execResult = self.__compileCppFiles(self.__cppCompiler, submission.submissionFiles, exeFile, self.__MAX_COMPILE_TIME_SEC, self.__MAX_COMPILER_OUTPUT_LINES)
        submission.compilerErrors = execResult.output

        if os.path.isfile(exeFile):   #did the compilation succeed?
            console("Compilation succeeded.")
        else:
            console("Compilation Failed.")
            return


        # we have to add logic that handles the case where no test files are required differently
        # from the cases where test files are needed.  In the former case, there is no input
        # redirection (no user input).  In the latter case, we redirect stdin from the test
        # data files.  The command line includes a "< testFile" argument.

        # run the code for each test case.
        for i in range(numTests):
            # use bNoTestFiles to determine the format of the command string, cmd
            if bNoTestFiles:
                # if we have no test files, do not include input redirection in the exec command
                cmd = "\"" + exeFile + "\" "
            else:
                # we have test files: use them to redirect stdin in the exec command
                dataFileName = os.path.abspath(self.agDocument.testDataFiles[i])
                cmd = "\"" + exeFile + "\" " + " < \"" + dataFileName + "\""

            exeFile = os.path.abspath(exeFile)
            # the command string, cmd
            execResult = self.__shellExec(cmd, self.__maxRunTime, self.__maxOutputLines, exeFile, submission.submissionDirectory)

            # store the output in the submission object
            submission.progOutputs[i] = execResult.output

            # store any runtime/compiler errors in the submission object
            submission.runtimeErrors[i] = ""   #initialize the runtimeErrors string
            if execResult.bTimedOut:
                submission.runtimeErrors[i] += "Maximum execution time of " + str(self.__maxRunTime) \
                        + " seconds exceeded.  Process forcefully terminated... output may be lost.\n"
            if execResult.bMaxLinesExceeded:
                submission.runtimeErrors[i] += "Maximum lines of output (" + str(self.__maxOutputLines) \
                        + ") exceeded.  Output truncated.\n";


            # store the execution time in the submission object
            submission.executionTimes[i] = execResult.execTimeSec;

        # delete the exe file if it exists, ignoring any "file not found" errors.
        try:
            os.remove(exeFile)
        except:
            # ignore errors from the delete operation
            pass


    # =======================================================================
    # private void execSubmission(Submission submission)
    #
    # ======================================================================
    def execSubmission(self, submission):
        # numTests = the number of test cases.  This is either 1 if there
        # are no test files, or equal to the # of test files.
        # int numTests;
        # boolean bNoTestFiles;       #set a flag to denote no test files

        if self.agDocument.testDataFiles is None:
            #submission.testFiles is null.  Assume there are no test
            #files.  Set numTests to 1.
            numTests = 1
            bNoTestFiles = True
        else:
            numTests = len(self.agDocument.testDataFiles)

            if numTests == 0:
                # =while there are no test files, we must set numTests to 1 in order to
                # enter the for loop.  We set it to 1 so that the loop executes only
                # once.  We will use the boolean flag bNoTestFiles inside the loop
                # to indicate whether or not test data files are to be used.=
                numTests = 1   #we will have a single test w/o test files
                bNoTestFiles = True
            else:
                # here, numTests > 0.  Set bNoTestFiles to false
                bNoTestFiles = False

        #console("bNoTestFiles = " + str(bNoTestFiles))
        # create arrays to hold test results
        submission.runtimeErrors = [''] * numTests
        submission.progOutputs = [''] * numTests
        submission.executionTimes = [0.0] * numTests

        if submission.language == IAGConstant.LANGUAGE_PYTHON3:
            if self.__python3Interpreter is None or self.__python3Interpreter == "":
                submission.compilerErrors = "No Python interpreter found."
            elif submission.primarySubmissionFile is None or submission.primarySubmissionFile == "":
                submission.compilerErrors = "Submission not graded."
            else:
                self.__pythonSubProcess(submission, numTests, bNoTestFiles)
        elif submission.language == IAGConstant.LANGUAGE_CPP:
            if self.__cppCompiler is None or self.__cppCompiler == "":
                submission.compilerErrors = "No C++ compiler found."
            else:
                self.__cppSubProcess(submission, numTests, bNoTestFiles)

        # tag the submission as "auto-graded"
        submission.bAutoGraded = True


    # =======================================================================
    # public void processSubmissions()
    #
    # processFiles is the central function of the GradingEngine class.
    # This function performs the auto-grading.
    # At a minimum, the caller should specify the following prior to
    # calling processFiles():
    # - an ArrayList of Submissions
    # - a cppCompiler or python3Interpreter, as appropriate
    # - testDataFiles, if required
    # ======================================================================
    def processSubmissions(self):
        self.bAbortRequest = False
        self.processingStatus = ProcessingStatus(True, "", 1, 1, len(self.agDocument.assignment.submissions))

        #---------- start the grading service ----------
        self.__gradingServiceThread = threading.Thread(target=gradingServiceThread, args=(self,))
        console("Attempting to launch grading service...")
        self.__gradingServiceThread.start()



    # =======================================================================
    # public void dumpSubmissions()
    # dumpSubmissions is a  debugging function that dumps the contents
    # of the Submissions array list to the screen.
    # ======================================================================
    def dumpSubmissions(self):
        console("[" + str(len(self.agDocument.assignment.submissions)) + "] submission(s) found.")

        for submission in self.agDocument.assignment.submissions:
            console("------------------------------------------")
            console("studentName = " + submission.participant.name)
            console("submissionDirectory = " + submission.submissionDirectory)
            console("language = " + submission.language)

            console(str(len(submission.submissionFiles)) + " submissionFiles:")
            for f in submission.submissionFiles:
                console("\t" + f)

            console("primarySubmissionFile = " + str(submission.primarySubmissionFile))


            if submission.submissionFiles is not None:           # TEMP*******
                if len(submission.submissionFiles) == 0:
                    console("No programming files found.")
                else:
                    for i in range (len(self.agDocument.testDataFiles)):
                        console("---> Results for test file %s: ", self.agDocument.testDataFiles[i])
                        if submission.runtimeErrors is not None:
                            console("Compiler/Limit Errors: %s", submission.runtimeErrors[i])

                        if submission.progOutputs is not None:
                            console("Output: %s", submission.progOutputs[i])

                        if submission.executionTimes is not None:
                            console("Execution Time: %s sec.", submission.executionTimes[i])

            console("bAutograded = %s", submission.bAutoGraded)
            console("grade = %d", submission.grade)
            console("instructorComment = " + submission.instructorComment)


    # =======================================================================
    # public void abortGrading()
    # ======================================================================
    def abortGrading(self):
        self.bAbortRequest = True


# =======================================================================
# xxx
# ======================================================================
def gradingServiceThread(gradingEngine):

    console("gradingServiceThread() running...")

    #gradingEngine.dumpSubmissions()

    for submission in gradingEngine.agDocument.assignment.submissions:
        console("Processing " + submission.participant.name)
        gradingEngine.processingStatus.message = submission.participant.name
        gradingEngine.execSubmission(submission)
        gradingEngine.processingStatus.progress += 1

        #if a request is made to stop processing, break out of the loop
        if gradingEngine.bAbortRequest:
            break

    gradingEngine.dumpSubmissions()

    #indicate that the thread is done.
    gradingEngine.processingStatus.bRunning = False
    console("Grading thread ending...")
    return



# =======================================================================
# xxx
# ======================================================================

#----------  ----------
#----------  ----------
#----------  ----------
#----------  ----------

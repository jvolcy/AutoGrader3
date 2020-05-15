#from IAGConstant import IAGConstant
from console import console
#import GradingEngine

import static AutoGraderApp.Controller.message;

# =======================================================================
# structure to hold the results returned by the shellExec() function.
# ======================================================================
class shellExecResult implements java.io.Serializable {
    Boolean bTimedOut;
    Boolean bMaxLinesExceeded;
    String output;
    Double execTimeSec;

    shellExecResult() {}

    shellExecResult(Boolean bTimedOut, Boolean bMaxLinesExceeded, String output, Double execTimeSec) {
        this.bTimedOut = bTimedOut;
        this.bMaxLinesExceeded = bMaxLinesExceeded;
        this.output = output;
        this.execTimeSec = execTimeSec;
    }
}


# =======================================================================
# structure to reports the status of the grading process,
# processAssignments().  This function is expected to be run inside
# of a thread, service or task.  The status structure is used to "peek"
# inside the running process.
# ======================================================================
class ProcessingStatus implements java.io.Serializable {
    Boolean bRunning;
    String message;
    Integer progress;
    Integer startVal;
    Integer endVal;

    ProcessingStatus() {
        bRunning = false;
    };

    ProcessingStatus(Boolean bRunning, String message, Integer progress, Integer startVal, Integer endVal) {
        this.bRunning = bRunning;
        this.message = message;
        this.progress = progress;
        this.startVal = startVal;
        this.endVal = endVal;
    }
}


# =======================================================================
# GradingEngine class
# This class compiles and executes (or interprets) student assignments.
# The central function of the class is processFiles().
# At a minimum, the caller should specify the following prior to
# calling processFiles:
# - an ArrayList of Assignments
# - a cppCompiler or python3Interpreter, as appropriate
# - testDataFiles, if required
# ======================================================================
public class GradingEngine implements IAGConstant, java.io.Serializable {
    # =The assignments list.=
    public ArrayList<Assignment> assignments;
    public ArrayList<File> testDataFiles;
    #private String outputFileName;
    private String tempOutputDirectory;
    private boolean bIncludeSourceInOutput;
    private int maxRunTime;
    private int maxOutputLines;
    private String cppCompiler;
    private String python3Interpreter;
    private String shell;
    private ProcessingStatus processingStatus;

    private boolean bAbortRequest;
    private GradingService gradingService;
    private boolean bLastReadExceedsMaxLines;
    private final int MAX_COMPILE_TIME_SEC = 10;
    private final int MAX_COMPILER_OUTPUT_LINES = 200;

    # =======================================================================
    # GradingEngine Constructor
    # ======================================================================
    GradingEngine() {

        #---------- set a few default values ----------
        maxRunTime = 3;     #3 seconds
        maxOutputLines = 100;   #100 lines of output max per program
        bIncludeSourceInOutput = true;
    }


    # =======================================================================
    # xxx
    # ======================================================================
    public ProcessingStatus getProcessingStatus() {
        return processingStatus;
    }

    # =======================================================================
    # xxx
    # ======================================================================
    public void setMaxRunTime(int maxRunTime) {
        this.maxRunTime = maxRunTime;
    }

    public void setMaxOutputLines(int maxOutputLines) {
        this.maxOutputLines = maxOutputLines;
    }

    public void setPython3Interpreter(String python3Interpreter){
        this.python3Interpreter = python3Interpreter;
    }

    public void setCppCompiler(String cppCompiler) {
        this.cppCompiler = cppCompiler;
    }

    public void setShellInterpreter(String shell) {
        this.shell = shell;
    }

    # =======================================================================
    # xxx
    # ======================================================================
    public void setTempOutputDirectory(String dirName) {
        tempOutputDirectory =  dirName;
        console("output directory = " + tempOutputDirectory);
    }

    # =======================================================================
    # xxx
    # ======================================================================
    /*
    public void setOutputFileName(String fileName) {
        outputFileName = fileName;
        File f = new File(fileName);
        outputDirectory =  f.getParent();
        console("output directory = " + outputDirectory);
    }
*/
    # =======================================================================
    # xxx
    # ======================================================================
    /*
    public String getOutputFileName() {
        return outputFileName;
    }
*/
    # =======================================================================
    # xxx
    # ======================================================================
    private String fileNameFromPathName(String pathName)
    {
        #extract the filename from the path name
        File f = new File(pathName);
        return f.getName();
    }

    # =======================================================================
    # xxx
    # ======================================================================
    private String readFromFile(String filepath) {
        bLastReadExceedsMaxLines = false;
        try {
            String text = new String(Files.readAllBytes(Paths.get(filepath)), StandardCharsets.UTF_8);
            return text;
        } catch (Exception e) {
            console("readFromFile(): " + e.toString());
        }
        return null;
    }

    # =======================================================================
    # xxx
    # ======================================================================
    private String readFromFile(File file) {
        return readFromFile(file.getAbsolutePath());
    }

    # =======================================================================
    # xxx
    # ======================================================================
    private String readFromFile(String filepath, int maxLines) {
        #initialize the output string
        String text = "";
        bLastReadExceedsMaxLines = false;

        #attempt to read the file line by line
        try {
            BufferedReader b = new BufferedReader(new FileReader(new File(filepath)));

            String readLine;    #individual lines in the file
            int numLines = 0;   #line #

            #read the file line by-line until we are out of lines or have
            #reached the max allowed
            while ((readLine = b.readLine()) != null && numLines < maxLines) {
                text += readLine + "\n";
                numLines++;
            }

            if (numLines == maxLines) { bLastReadExceedsMaxLines = true; }
        } catch (Exception e) {
            console("readFromFile():" + e.toString());
        }
        return text;
    }

    # =======================================================================
    # xxx
    # ======================================================================
    private String readFromFile(File file, int maxLines) {
        return readFromFile(file.getAbsolutePath(), maxLines);
    }

    # =======================================================================
    # getFileExtension()
    # returns the extension of the given filename.
    # ======================================================================
    private String getFileExtension(String fileName) {
        return fileName.substring(fileName.lastIndexOf('.') + 1);
    }


    # =======================================================================
    # getFileExtension()
    # overloaded version of the getFileExtension() method that accepts
    # a File object as an argument and returns the string extension of the
    # corresponding file.
    # ======================================================================
    private String getFileExtension(File f) {
        String fileName = f.getName();
        return getFileExtension(fileName);
    }

    # =======================================================================
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
    private ArrayList<Integer> getPidFromToken(String token) {
        ArrayList<Integer> pids = new ArrayList<>();
        try {
            Process p = Runtime.getRuntime().exec("ps -eo pid,command");
            p.waitFor(1, TimeUnit.SECONDS);

            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));

            String line;
            while ((line = reader.readLine()) != null) {
                #check for the token
                if (line.contains(token)) {
                    String pidStr = line.trim().split(" ")[0];
                    pids.add( Integer.valueOf(pidStr) );
                    #console(pidStr + "-->" + line.trim().split(" ")[1]);
                }
            }
        } catch (Exception e) {
            console("getPidFromToken():" + e.toString());
        }
        return pids;
    }


    # =======================================================================
    # xxx
    # ======================================================================

    private shellExecResult compileCppFiles(String compiler, ArrayList<File>sourceFiles, File exeFile, Integer timeoutSec, Integer maxOutputLines) {
        #Delineate the start of the unformatted py code output with a token: PROG_OUTPUT_START_TOKEN.
        #Flank with '\n's to ensure the token is on a line by itself

        /*
        #create a temp file to capture program output
        File tmpFile = new File(tempOutputDirectory + "/TEMP.AB");

        #delete any previous temp file in the output directory.
        try {
            #delete the temporary file if it exists, ignoring any "file not found" errors.
            tmpFile.delete();
        } catch (Exception e) {
            #ignore errors from the delete operation
        }
       =
        #compile the code
        String compile_args = "\"" + compiler + "\" -o \"" + exeFile + "\" ";

        for (File sourceFile : sourceFiles){
            #include only .cpp files (not .h or .hpp files) on the g++ command line
            if (Arrays.asList(IAGConstant.CPP_COMPILER_EXTENSIONS).contains(getFileExtension(sourceFile))) {
                compile_args = compile_args + "\"" + sourceFile + "\" ";
            }
        }

        #store the compiler output to a temp file
        #compile_args = compile_args + "> \"" + tmpFile + "\" 2>&1";

        #delete any previously compiled exe file in the output directory.
        try {
            #delete the exe file if it exists, ignoring any "file not found" errors.
            exeFile.delete();
        } catch (Exception e) {
            #ignore errors from the delete operation
        }

        #perform the compilation
        console("compiling:" + compile_args);
        shellExecResult execResult;
        execResult = shellExec(compile_args, timeoutSec, maxOutputLines, exeFile.getAbsolutePath(), exeFile.getParent());

        return execResult;

        #copy the first maxOutputLines from the temp file to the output file
        #Also, limit the #bytes to 40# maxOutputLines(this avoids large output files due to ridiculously long lines)

    }

    # =======================================================================
    # shellExec()
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
    private shellExecResult shellExec(String args, int timeout_sec, int maxOutputLines, String identifyingToken, String workingDirectory) {
        shellExecResult execResult = new shellExecResult();
        execResult.bTimedOut = false;
        execResult.bMaxLinesExceeded = false;
        execResult.execTimeSec = 0.0;

        #create a temp file to capture program output
        File tmpFile = new File(tempOutputDirectory + "/TEMP.AG2");

        #delete any previous temp file in the output directory.
        try {
            #delete the temporary file if it exists, ignoring any "file not found" errors.
            tmpFile.delete();
        } catch (Exception e) {
            #ignore errors from the delete operation
        }

        #form the command string, redirecting both stdout and stderr to the temporary file
        String[] cmd = {shell, "-c", args + " >> \"" + tmpFile.getPath() + "\" 2>&1"};

        #concatenate the cmd array string for display on the console
        String cmdStr = "";
        for (String s : cmd) {
            cmdStr += s + " ";
        }
        #xxx console("Executing " + args + "\n  as  " + cmdStr );

        try {
            #attempt to execute the command
            long elpasedTime = System.currentTimeMillis();

            Process p;
            p = Runtime.getRuntime().exec(cmd, null, new File(workingDirectory));

            #wait no more than the specified timeout for the process to complete.
            #a timeout of zero means wait indefinitely.

            if (timeout_sec > 0)
                p.waitFor(timeout_sec, TimeUnit.SECONDS);
            else
                p.waitFor();

            elpasedTime = System.currentTimeMillis() - elpasedTime;
            execResult.execTimeSec = elpasedTime/1000.0;

            #check if the process is still alive.  If it is, set the timeout
            #flag and attempt to forcefully terminate it.
            if (p.isAlive()) {
                #attempt to detect the PIDs of the launched shell and command
                ArrayList<Integer> pids = getPidFromToken(identifyingToken);

                execResult.bTimedOut = true;
                console ("Killing process " + p.toString() + ". Run time exceeds max value of " + maxRunTime + " seconds.");

                #attempt to destroy the process using the Java supplied methods
                p.destroy();
                p.destroyForcibly();

                #force the issue by killing all identified processes with
                #a unix kill command
                for (Integer pid : pids) {
                    String killCmd = "kill -9 " + pid.toString();
                   console(killCmd);
                    Runtime.getRuntime().exec(killCmd);
                }
            }
        } catch (Exception e) {
            console("shellExec(): " + e.toString());
        }

        #read in the output of the executed command from the temp file
        execResult.output = readFromFile(tmpFile, maxOutputLines);
        if (bLastReadExceedsMaxLines)
            execResult.bMaxLinesExceeded = true;

        #delete the tmp file
        tmpFile.delete();

        return execResult;

    }

    # =======================================================================
    # pythonSubProcess()
    # The functions pythonSubProcess() and cppSubProcess() exist simply
    # to reduce the size of the execAssignment() function.  Much of the
    # pre- and post-processing leading up to and following the calls to
    # these functions is common.  To the extent possible, that commonality
    # is captured in execAssignment().
    # ======================================================================
    private void pythonSubProcess(Assignment assignment, int numTests, boolean bNoTestFiles) {
        #declare a results structure for the calls to shellExec()
        shellExecResult execResult = null;

        #For python, there should be a primary assignment file;  for C++, it doesn't matter
        if (assignment.primaryAssignmentFile == null) return;
        String sourceFile = assignment.primaryAssignmentFile.getAbsolutePath();

        # =we have to add logic that handles the case where no test files are required differently
        # from the cases where test files are needed.  In the former case, there is no input
        # redirection (no user input).  In the latter case, we redirect stdin from the test
        # data files.  The command line includes a "< testFile" argument.=

        #run the code for each test case.
        for (int i = 0; i < numTests; i++) {
            String cmd;

            #use bNoTestFiles to determine the format of the command string, cmd
            if (bNoTestFiles) {
                #if we have no test files, do not include input redirection in the exec command
                cmd = "\"" + python3Interpreter + "\" " +
                        "\"" + sourceFile + "\"";
            }
            else {
                #we have test files: use them to redirect stdin in the exec command
                String dataFileName = testDataFiles.get(i).getAbsolutePath();
                cmd = "\"" + python3Interpreter + "\" " +
                        "\"" + sourceFile + "\"" + " < \"" + dataFileName + "\"";
            }

            #the command string, cmd
            execResult = shellExec(cmd, maxRunTime, maxOutputLines, sourceFile, assignment.assignmentDirectory);

            #store the output in the assignment object
            assignment.progOutputs[i] = execResult.output;

            #store any runtime/compiler errors in the assignment object
            assignment.runtimeErrors[i] = "";   #initialize the runtimeErrors string
            if (execResult.bTimedOut) {
                assignment.runtimeErrors[i] += "Maximum execution time of " + maxRunTime
                        + " seconds exceeded.  Process forcefully terminated... output may be lost.\n";
            }
            if (execResult.bMaxLinesExceeded) {
                assignment.runtimeErrors[i] += "Maximum lines of output (" + maxOutputLines
                        + ") exceeded.  Output truncated.\n";
            }

            #store the execution time in the assignment object
            assignment.executionTimes[i] = execResult.execTimeSec;
        }

    }


    # =======================================================================
    # cppSubProcess()
    # The functions pythonSubProcess() and cppSubProcess() exist simply
    # to reduce the size of the execAssignment() function.  Much of the
    # pre- and post-processing leading up to and following the calls to
    # these functions is common.  To the extent possible, that commonality
    # is captured in execAssignment().
    # ======================================================================
    private void cppSubProcess(Assignment assignment, int numTests, boolean bNoTestFiles) {
        console("cppSubProcess: " + assignment.studentName);
        #declare a results structure for the calls to shellExec()
        shellExecResult execResult = null;

        File exeFile = new File(assignment.assignmentDirectory + "/AG.out");

        #Compile the source once.
        execResult = compileCppFiles(cppCompiler, assignment.assignmentFiles, exeFile, MAX_COMPILE_TIME_SEC, MAX_COMPILER_OUTPUT_LINES);
        assignment.compilerErrors = execResult.output;

        if (exeFile.isFile())   #did the compilation succeed?
                console("Compilation succeeded.");
        else {
            console("Compilation Failed.");
            return;
        }

        # =we have to add logic that handles the case where no test files are required differently
        # from the cases where test files are needed.  In the former case, there is no input
        # redirection (no user input).  In the latter case, we redirect stdin from the test
        # data files.  The command line includes a "< testFile" argument.=

        #run the code for each test case.
        for (int i = 0; i < numTests; i++) {
            String cmd;

            #use bNoTestFiles to determine the format of the command string, cmd
            if (bNoTestFiles) {
                #if we have no test files, do not include input redirection in the exec command
                cmd = "\"" + exeFile + "\" ";
            }
            else {
                #we have test files: use them to redirect stdin in the exec command
                String dataFileName = testDataFiles.get(i).getAbsolutePath();
                cmd = "\"" + exeFile + "\" " + " < \"" + dataFileName + "\"";
            }

            #the command string, cmd
            execResult = shellExec(cmd, maxRunTime, maxOutputLines, exeFile.getAbsolutePath(), assignment.assignmentDirectory);

            #store the output in the assignment object
            assignment.progOutputs[i] = execResult.output;

            #store any runtime/compiler errors in the assignment object
            assignment.runtimeErrors[i] = "";   #initialize the runtimeErrors string
            if (execResult.bTimedOut) {
                assignment.runtimeErrors[i] += "Maximum execution time of " + maxRunTime
                        + " seconds exceeded.  Process forcefully terminated... output may be lost.\n";
            }
            if (execResult.bMaxLinesExceeded) {
                assignment.runtimeErrors[i] += "Maximum lines of output (" + maxOutputLines
                        + ") exceeded.  Output truncated.\n";
            }

            #store the execution time in the assignment object
            assignment.executionTimes[i] = execResult.execTimeSec;
        }
    }


    # =======================================================================
    # execAssignment()
     *
    # ======================================================================
    private void execAssignment(Assignment assignment) {
        # =numTests = the number of test cases.  This is either 1 if there
        # are no test files, or equal to the # of test files.=
        int numTests;
        boolean bNoTestFiles;       #set a flag to denote no test files

        if (testDataFiles == null)
        {
            #assignment.testFiles is null.  Assume there are no test
            #files.  Set numTests to 1.
            numTests = 1;
            bNoTestFiles = true;
        }
        else {
            numTests = testDataFiles.size();

            if (numTests == 0) {
                # =while there are no test files, we must set numTests to 1 in order to
                # enter the for loop.  We set it to 1 so that the loop executes only
                # once.  We will use the boolean flag bNoTestFiles inside the loop
                # to indicate whether or not test data files are to be used.=
                numTests = 1;   #we will have a single test w/o test files
                bNoTestFiles = true;
            }
            else {
                # here, numTests > 0.  Set bNoTestFiles to false
                bNoTestFiles = false;
            }
        }

        #create arrays to hold test results
        assignment.runtimeErrors = new String[numTests];
        assignment.progOutputs = new String[numTests];
        assignment.executionTimes = new Double[numTests];

        if (assignment.language.equals(IAGConstant.LANGUAGE_PYTHON3))
            if (python3Interpreter == null || python3Interpreter == "")
                assignment.compilerErrors = "No Python interpreter found.";
            else if (assignment.primaryAssignmentFile == null || assignment.primaryAssignmentFile.equals("")) {
                assignment.compilerErrors = "Submission not graded.";
            }
            else
                pythonSubProcess(assignment, numTests, bNoTestFiles);
        else if (assignment.language.equals(IAGConstant.LANGUAGE_CPP))
            if (cppCompiler == null || cppCompiler == "")
                assignment.compilerErrors = "No C++ compiler found.";
            else
                cppSubProcess(assignment, numTests, bNoTestFiles);

        #tag the assignment as "auto-graded"
        assignment.bAutoGraded = true;

    }

    # =======================================================================
    # processAssignments()
    # processFiles is the central function of the GradingEngine class.
    # This function performs the auto-grading.
    # At a minimum, the caller should specify the following prior to
    # calling processFiles():
    # - an ArrayList of Assignments
    # - a cppCompiler or python3Interpreter, as appropriate
    # - testDataFiles, if required
    # ======================================================================
    public void processAssignments() {


        bAbortRequest = false;
        processingStatus = new ProcessingStatus(true, "", 1, 1, assignments.size());

        #---------- start the grading service ----------
        gradingService = new GradingService();
        message("Attempting to launch grading service...");
        gradingService.start();

    }



    # =======================================================================
    # xxx
    # ======================================================================
    private class GradingService extends Service<Void> implements java.io.Serializable {

        @Override
        protected Task<Void> createTask() {
            return new Task<Void>() {
                @Override
                protected Void call() throws Exception {

                    #xxx console("Grading service started...");
                    for (Assignment assignment : assignments) {
                        processingStatus.message = assignment.studentName;
                        execAssignment(assignment);
                        processingStatus.progress++;

                        #if a request is made to stop processing, break out of the loop
                        if (bAbortRequest) break;
                    }

                    #indicate that the thread is done.
                    processingStatus.bRunning = false;
                    console("Grading thread ending...");
                    return null;
                }
            };
        }
    }


    # =======================================================================
    # dumpAssignments()
    # dumpAssignments is a  debugging function that dumps the contents
    # of the Assignments array list to the screen.
    # ======================================================================
    public void dumpAssignments() {
        console("[" + assignments.size() + "] assignment(s) found.");

        for (Assignment assignment : assignments) {
            console("------------------------------------------");
            console("studentName = " + assignment.studentName);
            console("assignmentDirectory = " + assignment.assignmentDirectory);
            console("language = " + assignment.language);

            console(assignment.assignmentFiles.size() + " assignmentFiles:");
            for (File f : assignment.assignmentFiles) {
                console("\t" + f.getAbsolutePath());
            }
            console("primaryAssignmentFile = " + assignment.primaryAssignmentFile);

            if (assignment.assignmentFiles != null)           #TEMP*******
                if (assignment.assignmentFiles.size() == 0) {
                    console("No programming files found.");
                }
                else {
                    for (int i = 0; i < testDataFiles.size(); i++) {
                        console("---> Results for test file %s: ", testDataFiles.get(i).getName());
                        if (assignment.runtimeErrors != null)
                            console("Compiler/Limit Errors: %s", assignment.runtimeErrors[i]);

                        if (assignment.progOutputs != null)
                            console("Output: %s", assignment.progOutputs[i]);

                        if (assignment.executionTimes != null)
                            console("Execution Time: %s sec.", assignment.executionTimes[i]);
                    }
                }
            console("bAudograded = %s", assignment.bAutoGraded);
            console("grade = %d", assignment.grade);
            console("instructorComment = " + assignment.instructorComment);
        }
    }

    # =======================================================================
    # abortGrading
    # ======================================================================
    public void abortGrading() {
        bAbortRequest = true;
    }

}


# =======================================================================
# xxx
# ======================================================================

#----------  ----------
#----------  ----------
#----------  ----------
#----------  ----------

from IAGConstant import IAGConstant
from GradingEngine import GradingEngine
from console import console
import os, sys, time
from shutil import copy

# =======================================================================
# AGDocument class
# =======================================================================
class AGDocument(object):
    def __init__(self):
        self.assignmentName = ''
        self.gradingEngine = GradingEngine()       # a GradingEngine() object
        self.htmlReport = ''
        #self.moodleDirectory = None     # a File object
        self.dataFiles = []       # a list of input data files needed by the program

    def addTestDataFile(self, testDataFile):
        self.gradingEngine.testDataFiles.append(testDataFile)

    def addDataFile(self, dataFile):
        self.dataFiles.append(dataFile)

    def addAssignment(self, assignment):
        self.gradingEngine.assignments.append(assignment)

    # =======================================================================
    # prepareDataFiles()
    # This function copies all data files to the submission directory of
    # every submission
    # =======================================================================
    def __prepareDataFiles(self):
        #---------- copy all data files into each submission directory ----------
        #go through every data file in the listDataFiles list box
        for src in  self.dataFiles:
            # copy each data file to each of the assignment directories
            for assignment in self.gradingEngine.assignments:
                dst = assignment.assignmentDirectory + "/" + os.path.basename(src)
                try:
                    console("copying \"" + src + "\" to \"" + dst + "\"")
                    copy(src, dst)
                except:
                    e = sys.exc_info()[0]
                    print(e)
                    console("AGDocument::__prepareDataFiles() " + str(e))

    # =======================================================================
    # prepareDataFiles()
    # This function removes all data files in the submission directory
    # that were placed by __prepareDataFiles()
    # =======================================================================
    def __cleanupDataFiles(self):
        for src in  self.dataFiles:
            # delete the data files from each of the assignment directories
            for assignment in self.gradingEngine.assignments:
                dst = assignment.assignmentDirectory + "/" + os.path.basename(src)
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
    # __discoverPrimaryAssignmentFile()
    # function that attempts to automatically detect the primary programming
    # file for python.  This works only if the user hasn't specified a
    # primary file or when there is only 1 python file.  If more than
    # one python source file exists, the user MUST specify a primary.
    # for python programs, we must idenfity the primary code file if
    # multiple files are present.  If only one assignment file is given,
    # set it as the primary.
    # =======================================================================
    def __discoverPrimaryAssignmentFile(self, assignment):
        #if the user has already specified a primary assignment file, do nothing
        if assignment.primaryAssignmentFile is not None:
            return

        #if we only have 1 assignmentFile, make it the primary
        if len(assignment.assignmentFiles) == 1:
            assignment.primaryAssignmentFile = assignment.assignmentFiles[0]

        #return without setting the value of the primaryAssignmentFile (at this point, it should be None)
        #This does not matter for C++.
        return

    # =======================================================================
    # grade()
    # =======================================================================
    def grade(self):
        # copy data files to each submission directory
        self.__prepareDataFiles()

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


        #attempt to discover the primary assignment file for each submission
        for assignment in self.gradingEngine.assignments:
            self.__discoverPrimaryAssignmentFile(assignment)


        # perform grading
        console("Processing assignments...")
        self.gradingEngine.processAssignments()

        status = self.gradingEngine.getProcessingStatus()
        while status.bRunning == True:
            time.sleep(0.5)
            print('#')
        #time.sleep(2)

        # cleanup data files
        #self.__cleanupDataFiles()

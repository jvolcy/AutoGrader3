import os
from IAGConstant import IAGConstant
from console import console
#import GradingEngine


# =======================================================================
# MoodlePreprocessor
# Class that pre-processes the assignments downloaded from Moodle.
# All Moodle downloads must be done using the 'Download all assignments'
# method with the 'Download submissions in folders' checkbox checked.
# With this option, every student's submission will be in a separate
# folder once the downloaded zip file is extracted.  (You must extract
# the file).
# MoodlePreprocessor contains functions to extract the student names
# from the Moodle-assigned subfolder names.  It also recursively
# identifies all programming files within these directories.
# MoodlePreprocessor pre-populates and ArrayList of Assignment objects
# with the extracted student names, the program directories and the
# list of programming files contained in each directory.
# The class also optionally unzips files in the student directory.
# ======================================================================
class MoodlePreprocessor(IAGConstant):

    # =======================================================================
    # MoodlePreprocessor(String sourceDirectory, String language, boolean autoUncompress_)
    # Class constructor accepts the top-level assignment directory
    # and the assignment language.
    # The language can be either LANGUAGE_PYTHON3 or LANGUAGE_CPP
    # ======================================================================
    def __init__(self, sourceDirectory, language, autoUncompress_=True):
        self.__TopAssignmentsDirectory = sourceDirectory;
        self.__bAutoUncompress = autoUncompress_;

        # ---------- set the language and corresponding file extensions ----------
        self.setLanguage(language)

        # ---------- create assignments ArrayList ----------
        '''The key to the assignment files dictionary is the student's name.  The
        values are a list of files (.py, .cpp, .h, etc.) included with
        the particular student's submission.   Subdirectories are
        optionally recursively searched until at least one file of the
        specified language (Python or C++) is found.  compressed  files
        will be optionally uncompressed ahead of the recursive search. '''
        #private ArrayList<Assignment> assignments;
        self.__assignments = []        # array of Assignment objects
        # The key to the assignment directories dictionary is the student's
        # name.  The value is the directory that holds the student's
        # submission.  The student's name is derived from the assignment
        # directory.

        '''Steps
        # 1) get the name of all subdirectories inside the assignmentDirectory
        # 2) extract the student names from all these subdirectories.  Eliminate
        # subdirectories that do not sport a valid student name.  These student
        # names will be the keys to the dictionary.
        # 3) within each student directory search for the appropriate files.
        # these would be .zip, .py, .cpp and .h files, depending on the language.
        # 4) add the files of interest to the assignments dictionary under the
        # key that matches the student's name.
        '''

        # ---------- verify that TopAssignmentsDirectory is a valid directory ----------
        if not os.path.isdir(self.__TopAssignmentsDirectory):
            console("'" + self.__TopAssignmentsDirectory + "' is not a valid source directory.")
            return     #do nothing else


        # initialize 'assignments' array list of type 'ArrayList<Assignment>' and
        # populate .studentName and .assignmentDirectory fields
        self.__prepareStudentDirectories()


        # ----------  ----------
        self.__prepareAssignmentFiles()




    # =======================================================================
    # private void setLanguage(String language_)
    # This method sets the programming language and the file extensions
    # list.
    # ======================================================================
    def setLanguage(self, language_):

        #by default assign language to language_.  This may change below.
        self.__language = language_

        # ---------- set the default file extensions ----------
        if language_ ==  IAGConstant.LANGUAGE_CPP:
            #extensions = IAGConstant.CPP_EXTENSIONS;
            pass
        elif language_ ==  IAGConstant.LANGUAGE_PYTHON3:
            #extensions = IAGConstant.PYTHON_EXTENSIONS;
            pass
        elif language_ ==   IAGConstant.LANGUAGE_AUTO:
            #extensions = IAGConstant.PYTHON_AND_CPP_EXTENSIONS;
            pass
        else:
            #extensions = IAGConstant.PYTHON_AND_CPP_EXTENSIONS;;
            self.__language = IAGConstant.LANGUAGE_AUTO       #invalid language specified: use AUTO by default



    # =======================================================================
    # private ArrayList<File> getSubDirectories(String directoryPath, boolean omitHiddenDirs)
    # given the path to a directory, this function returns an array of
    # all sub-directories found in the directoryPath
    # ======================================================================
    def getSubDirectories(self, directoryPath, omitHiddenDirs):
        # ---------- get all files in the provided directory ----------
        dirsInFolder = []

        '''
        File folder = new File(directoryPath)
        for (File f : folder.listFiles()) {
            if (f.isDirectory()) {
                if (!f.isHidden() || !omitHiddenDirs)
                    dirsInFolder.add(f)
            }
        }
        return dirsInFolder;
        '''


    # =======================================================================
    # private ArrayList<File> getFilesInDirectory(String directoryPath, boolean omitHiddenFiles)
    # given the path to a directory, this function returns an array of
    # all files and sub-directories found in the directoryPath
    # ======================================================================
    def getFilesInDirectory(self, directoryPath, omitHiddenFiles):
        # ---------- get all files in the provided directory ----------
        filesInFolder = []  # list of file objects

        file_list = os.listdir(directoryPath)
        for  f in file_list:
            filepath = os.path.join(directoryPath, f)

            # for windows
            # os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

            # for macs
            if (not f.startswith('.')) or (not omitHiddenFiles):
                filesInFolder.append(filepath)

        #sort the list of files
        filesInFolder.sort()
        return filesInFolder


    # =======================================================================
    # private String getFileExtension(String fileName)
    # returns the extension of the given filename.
    # ======================================================================
    def getFileExtension(self, fileName):
        return os.path.splitext(fileName)[1].lstrip('.')

    # =======================================================================
    # private String getFileExtension(File f)
    # overloaded version of the getFileExtension() method that accepts
    # a File object as an argument and returns the string extension of the
    # corresponding file.
    # ======================================================================
    '''
    private String getFileExtension(File f) {
        String fileName = f.getName()
        return getFileExtension(fileName)
    }
    '''

    # =======================================================================
    # private String stripFileExtension(String fileName)
    # returns the extension of the given filename.
    # ======================================================================
    def stripFileExtension(self, fileName):
        return os.path.splitext(fileName)[0]


    # =======================================================================
    # private ArrayList<File> findFilesByExtension(String directory, String[] fileExtensions)
    # This function returns an array list of files in the specified
    # directory with file extension matching any of the extensions on
    # the 'extensions' list.
    # ======================================================================
    private ArrayList<File> findFilesByExtension(String directory, String[] fileExtensions) {
        # ---------- create an empty list of files ----------
        ArrayList<File> programmingFiles = new ArrayList<File>()

        # ---------- retrieve a list of all non-hidden files in the directory ----------
        ArrayList<File> progFiles = getFilesInDirectory(directory, true)

        # ---------- go through each file in the directory ----------
        for (File f : progFiles) {
            # ---------- we will ignore subdirectories ----------
            if (f.isFile()) {
                # ---------- retrieve the extension on the file ----------
                String f_extension = getFileExtension(f).toLowerCase()
                #if fileExtensions.contains()
                if (Arrays.asList(fileExtensions).contains(f_extension))
                    for (String ext : fileExtensions) {
                        # ---------- if the extension on the file matches
                        # one of the extension in the extensions list, add
                        # it to the programming files list. ----------
                        if (f_extension.equals(ext.toLowerCase()))
                            programmingFiles.add(f)
                    }

            }
        }

        return programmingFiles;
    }


    # =======================================================================
    # private void findAssignmentFiles(ArrayList<File> files, String directory)
    #
    # 1) Search for a zip file in the directory.  If any are found, unzip
    # unzip them to new folders.
    # 2) beginning with the provided directory, search for program files
    # (py or cpp).  If any are found, add them to the assignmentFiles list.
    # We are done.
    # 3) Search for subdirectories in the assignmentDirectory.  These may
    # already have existed or may have been created in step 1.
    # 4) In either case, for each sub-directory found, repeat step 1
    # with the subdirectory as the new assignmentDirectory.
    # 5) At this point, no assignment files were found, return an empty
    # ArrayList.
    # ======================================================================
    private void findAssignmentFiles(ArrayList<File> files, String directory) {

        # ---------- Step 1: find and uncompress zip files ----------
        if (bAutoUncompress) {
            ArrayList<File> compressedFiles = findFilesByExtension(directory, COMPRESSION_EXTENSIONS)
            for (File cFile : compressedFiles) {
                #uncompress each zip file
                String[] cmd = {"unzip", "-u", cFile.getAbsolutePath(), "-d", stripFileExtension(cFile.getAbsolutePath())};
                String cmdStr = "unzip -u \"" + cFile.getAbsolutePath() + "\" -d \"" + stripFileExtension(cFile.getAbsolutePath()) + "\"";
                console(cmdStr)

                try {
                    Runtime r = Runtime.getRuntime()
                    Process p = r.exec(cmd)        #execute the unzip command
                    #Process p = r.exec("unzip -u \34/Users/jvolcy/work/test/JordanStill_1124140_assignsubmission_file_/P0502b.zip\34 -d \34/Users/jvolcy/work/test/JordanStill_1124140_assignsubmission_file_/P0502b\34")
                    p.waitFor()
                } catch (Exception e) {
                    console("[findAssignmentFiles()]", e)
                }
            }
        }

        # ---------- Step 2: find programming files in the directory ----------
        ArrayList<File> programmingFiles = findFilesByExtension(directory, PYTHON_AND_CPP_EXTENSIONS)
        if (programmingFiles.size() > 0) {
            files.addAll(programmingFiles)
            #if we found any files, we are done
            return;
        }

        # ---------- Step 3: search for sub-directories ----------
        ArrayList<File> subDirs = getSubDirectories(directory, true)
        for (File sDir : subDirs) {
            #Step 4: recursively call findAssignmentFiles() if we find subdirectories
            findAssignmentFiles(files, sDir.toString())
        }

        # ---------- Step 5 ----------
        #No assignment files found.  This may be the end of the recursion.
    }

    # =======================================================================
    # private String autoDetectLanguage(ArrayList<File> progFiles)
    #
    # ======================================================================
    private String autoDetectLanguage(ArrayList<File> progFiles) {
        for (File f : progFiles) {
            String f_extension = getFileExtension(f).toLowerCase()
            if (Arrays.asList(IAGConstant.PYTHON_EXTENSIONS).contains(f_extension)) {
                return IAGConstant.LANGUAGE_PYTHON3;
            }
            if (Arrays.asList(IAGConstant.CPP_EXTENSIONS).contains(f_extension)) {
                return IAGConstant.LANGUAGE_CPP;
            }
        }
        return IAGConstant.LANGUAGE_UNKNOWN;
    }

    # =======================================================================
    # private void prepareAssignmentFiles()
    #
    # ======================================================================
    private void prepareAssignmentFiles() {
        for (Assignment assignment : assignments) {
            # ---------- initialize the assignmentFiles array list ----------
            assignment.assignmentFiles = new ArrayList<>()

            #create a temporary assignment files array list
            ArrayList<File> assignmentFiles = new ArrayList<>()

            # ---------- call the recursive findAssignmentFiles method ----------
            findAssignmentFiles(assignmentFiles, assignment.assignmentDirectory)

            # ---------- set the language for the assignment ----------
            if (language.equals( IAGConstant.LANGUAGE_AUTO) ) {
                assignment.language = autoDetectLanguage(assignmentFiles)
            }
            else {
                assignment.language = language;
            }

            String[] extensions;

            switch (assignment.language) {
                case IAGConstant.LANGUAGE_PYTHON3:
                    extensions = IAGConstant.PYTHON_EXTENSIONS;
                    break;
                case IAGConstant.LANGUAGE_CPP:
                    extensions = IAGConstant.CPP_EXTENSIONS;
                    break;
                default:        #unable to determine the language
                    extensions = new String[] {};
            }

            #add only files of the right type to the assignment file list
            for (File f: assignmentFiles) {
                String f_extension = getFileExtension(f).toLowerCase()
                if (Arrays.asList(extensions).contains(f_extension)){
                        # ---------- if the extension on the file matches
                        # one of the extension in the extensions list, add
                        # it to the programming files list. ----------
                    assignment.assignmentFiles.add(f)
                    }
            }
                assignment.bAutoGraded = false;     #indicate the assignment has not yet been auto-graded
        }

    }


    # =======================================================================
    # private String extractStudentNameFromMoodleDirectoryName(String moodleDirectoryName)
    # This function returns either a string representing a student's name,
    # an empty string, meaning that a valid student name could not be
    # found or null, meaning that the provided directory is not a student
    # assignment directory.
    # ======================================================================
    private String extractStudentNameFromMoodleDirectoryName(String moodleDirectoryName) {
        # =assume that directory names that begin with a "_" or a "__" are
        intended to be hidden or system directories.=

        if ( moodleDirectoryName.substring(0,1).equals("_") ) {
            return null;
        }

        if (moodleDirectoryName.length() > 1) {
            if (moodleDirectoryName.substring(0, 2).equals("__")) {
                return null;
            }
        }

        String[] data = moodleDirectoryName.split("_")
        if (data.length < 2)    #this is an error condition; not a valid Moodle directory name
            return "";

        return data[0];
    }

    # =======================================================================
    # private void prepareStudentDirectories()
    # This function performs the first step to building the 'assignments'
    # ArrayList.  The function searches the TopAssignmentsDirectory for
    # the sub-directories of student submissions.  It is assumed that all
    # directories under the TopAssignmentsDirectory corresponds to a
    # student submission.  These names of these directories should be
    # Moodle-formatted as "student name_assignment description".  This
    # function extracts the student name from the corresponding directory
    # names.  The function then creates a new "Assignment" object that is
    # added to the "assignemnts" ArrayList. Finally, the .studentName and
    # .assignmentDirectory fields of the newly created "Assignment" object
    # is populated.
    # In the case where the directory name does not conform to the
    # expected Moodle naming scheme, student names of "Anonymous 1",
    # "Anonymous 2", etc. are used.
    # At the conclusion of this function, the "assignments" ArrayList
    # should be populated with as many entries as there are sub-directories
    # under the TopAssignmentsDirectory.  Each entry should have a valid
    # .studentName and .assignmentDirectory value.
    # ======================================================================
    private void prepareStudentDirectories() {
        # ---------- get all directories in the top level directory ----------
        ArrayList<File> listOfFiles = getFilesInDirectory(TopAssignmentsDirectory, true)

        # =for directories that don't conform to Moodle names, we will label
        them "anonymous 1", "anonymous 2", etc...=
        int anonymousCounter = 1;

        # ---------- go through the list and identify subdirectories ----------
        for (File file : listOfFiles) {
            if (file.isDirectory()) {     #check that it is a directory

                Assignment newAssignment = new Assignment()

                #attempt to extract the student's name
                String studentName = extractStudentNameFromMoodleDirectoryName(file.getName())
                newAssignment.assignmentDirectory = file.toString()


                if (studentName == null) {
                    console("skipping directory " + file.getName())
                } else if (studentName.equals("")) {
                    newAssignment.studentName = "Anonymous " + anonymousCounter;
                    anonymousCounter++;
                    #add this assignment to the assignments ArrayList
                    assignments.add(newAssignment)
                } else {
                    #student name successfully extracted: add to the assignmentDirectories dictionary
                    newAssignment.studentName = studentName;
                    #add this assignment to the assignments ArrayList
                    assignments.add(newAssignment)
                }

            }
        }
    }

    # =======================================================================
    # public ArrayList<Assignment> getAssignments()
    # This function returns the list of assignments.
    # ======================================================================
    public ArrayList<Assignment> getAssignments() {
        return assignments;
    }

    # =======================================================================
    # xxx
    # ======================================================================
}




# =======================================================================
# xxx
# ======================================================================

# ----------  ----------
# ----------  ----------
# ----------  ----------
# ----------  ----------

from IAssignmentStore import IAssignmentStore
from Assignment import *
from IAGConstant import IAGConstant
import os
from console import console


# =======================================================================
# LmsSimulator class
# =======================================================================
class LmsSimulator(IAssignmentStore):
    def __init__(self, workingDirectory=None, language=IAGConstant.LANGUAGE_AUTO ):
        # instantiate the assignment object
        console('initializing LmsSimulator...')

        self.__workingDirectory = workingDirectory

        self.__courses = []
        self.__coursesDirectory = ''
        self.__selectedCourse = None    #Course()

        if self.__workingDirectory is not None:
            #this will set self.__coursesDirectory
            self.getCourses()

        self.__assignments = []
        self.__selectedAssignment = None

        self.__language = language
        # for the simulation, we immediately call __buildAssignment()
        # to generate the data used to simulate an LMS request


    # =======================================================================
    # function to retrieve available courses from the LMS
    # =======================================================================
    def getCourses(self) -> [Course]:

        # the working directory must be set before fetching course information in the simulator.
        if self.__workingDirectory is None:
            console('LmsSimulator::getCourses(): Working directory not set.')
            return None

        # for the simulator, courses are in the non-hidden
        # sub-directories of the "courses" directory in the working directory.
        self.__coursesDirectory = os.path.join(self.__workingDirectory, "courses")

        #empty the courses array
        self.__courses.clear()

        courseIDs = os.listdir(self.__coursesDirectory)
        for courseID in courseIDs:
            course_id_path = os.path.join(self.__coursesDirectory, courseID)
            if not os.path.isdir(course_id_path):
                continue

            #skip hidden courses
            if not courseID.startswith('.'):
                newCourse = Course(courseName=courseID + ' Name',
                                    courseID=courseID,
                                    courseDescription=courseID + ' Description',
                                    term=None)
                self.__courses.append(newCourse)
                #print(newCourse.courseID)

        return self.__courses

    # =======================================================================
    # function that selects which of the available courses returned
    # by getCourses() we will be working with
    # =======================================================================
    def selectCourse(self, course):
        if course in self.__courses:
            self.__selectedCourse = course


    # =======================================================================
    # function that returns the currently selected course
    # =======================================================================
    def getSelectedCourse(self) -> Course:
        return self.__selectedCourse

    # =======================================================================
    # function to retrieve assignments from the LMS
    # returns a list of assignments associated with the selected course
    # the course must be set before this can be used
    # =======================================================================
    def getAssignments(self) -> [Assignment]:
        assignmentsDirectory = os.path.join(self.__coursesDirectory, self.__selectedCourse.courseID)

        # clear the assignments list
        self.__assignments.clear()

        # get items in the assignment directory
        assignmentIDs = os.listdir(assignmentsDirectory)
        for assignmentID in assignmentIDs:
            # get the full path of each item.  If the item is not a directory, ignore it
            assignment_id_path = os.path.join(assignmentsDirectory, assignmentID)
            if not os.path.isdir(assignment_id_path):
                continue

            if not assignmentID.startswith('.'):
                newAssignment = Assignment()
                newAssignment.assignmentName = assignmentID + ' Name'
                newAssignment.assignmentID = assignmentID
                newAssignment.assignmentDirectory = assignment_id_path

                self.__assignments.append(newAssignment)
                #print(newAssignment.assignmentID)

        return self.__assignments


    # =======================================================================
    # function that selects which of the available assignments returned
    # by getAssignments() we will be working with
    # =======================================================================
    def selectAssignment(self, assignment):
        if assignment in self.__assignments:
            self.__selectedAssignment = assignment
            self.__getSubmissions()


    # =======================================================================
    # function that returns the currently selected assignment
    # =======================================================================
    def getSelectedAssignment(self) -> Assignment:
        return self.__selectedAssignment

    # =======================================================================
    # for a normal LMS, the working directory would be provided through
    # a call to setWorkingDirectory().  In our case, the files are
    # locally on disk in an arbitrary location, so the working directory
    # is wherever those files happen to be.
    # =======================================================================
    def __getSubmissions(self):

        # get items in the assignment directory
        studentNames = os.listdir(self.__selectedAssignment.assignmentDirectory)
        studentNames.sort()
        for studentName in studentNames:

            # get the full path of each item.  If the item is not a directory, ignore it
            submissionDirectory = os.path.join(self.__selectedAssignment.assignmentDirectory, studentName)
            if not os.path.isdir(submissionDirectory):
                continue

            # if it is a directory, assume the directory name is the student's name
            # and register the full path name

            # console(submissionDirectory + ' --> ' + studentName)

            # build the submission object for this submission
            submission = Submission()
            submission.submissionDirectory = submissionDirectory
            submission.language = self.__language
            #submission.studentName = studentName
            submission.participant = Participant(lmsID = 123456,
                                                 name = studentName,
                                                 schoolID = "900XXXXXX",
                                                 email = "jane.doe@scmail.spelman.edu",
                                                 role = "Student")

            # find all programming files in the subdirectory
            files = os.listdir(submission.submissionDirectory)

            # go through each file in the submission directory
            for file in files:
                # get the file extension
                filename, file_extension = os.path.splitext(file)
                file_extension = file_extension.lstrip('.')

                #attempt to auto-detect the language.  This is a very primitive method:  The very first
                #file that is in the pythons or C++ extension list sets the langauge for the entire assignment
                if self.__language == IAGConstant.LANGUAGE_AUTO:
                    if file_extension in IAGConstant.PYTHON_EXTENSIONS:
                        self.__language = IAGConstant.LANGUAGE_PYTHON3
                        console("Python auto-detected.")
                        # language changed: change the language of the current submission
                        submission.language = self.__language

                    if file_extension in IAGConstant.CPP_EXTENSIONS:
                        self.__language = IAGConstant.LANGUAGE_CPP
                        console("C++ auto-detected")
                        # language changed: change the language of the current submission
                        submission.language = self.__language

                if self.__language == IAGConstant.LANGUAGE_PYTHON3 and file_extension in IAGConstant.PYTHON_EXTENSIONS:
                    submission.submissionFiles.append(file)
                elif self.__language == IAGConstant.LANGUAGE_CPP and file_extension in IAGConstant.CPP_EXTENSIONS:
                    submission.submissionFiles.append(file)
                else:
                    #here, we ignore the file
                    console('Unknown file extension: ' + file_extension)

            self.__selectedAssignment.submissions.append(submission)

        # the __assignments array will have only 1 item
        #self.__assignments = [self.__selectedAssignment]


    # =======================================================================
    # function that downloads all submissions to disk following the convention
    # course->assignment->[submissions]
    # =======================================================================
    def downloadSubmissions(self):
        # nothing to do here
        pass

    # =======================================================================
    # function to submit graded assignments back to the LMS
    # =======================================================================
    def submitAssignment(self, assignment):
        # nothing to do here
        pass

    # =======================================================================
    # specify a place where the LMS will download and store assignment files
    # =======================================================================
    def setWorkingDirectory(self, workingDirectory):
        self.__workingDirectory = workingDirectory

    # =======================================================================
    # function that returns the currently selected assignment
    # =======================================================================
    def getWorkingDirectory(self) -> str:
        return self.__workingDirectory

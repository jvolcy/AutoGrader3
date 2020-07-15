from IAssignmentStore import IAssignmentStore
from Assignment import *
from urllib.request import urlopen
import json

# =======================================================================
# Moodle LMS Interface class
# =======================================================================
class Moodle(IAssignmentStore):

    # =======================================================================
    # specify the security key and server upon instantiation
    # ======================================================================
    def __init__(self, server, securityKey, email):
        self.__moodleWebServiceSecurityKey = securityKey
        self.__moodleServer = server
        self.__email = email

        # get the userid
        self.__getUserId()
        print('Moodle userid set to', self.__userid)

        self.__courses = []
        self.__selectedCourse = None    #Course()
        self.__participants = []        #individuals enrolled in the course (students, faculty, TAs, etc.)

        self.__assignments = []
        self.__selectedAssignment = None

    # =======================================================================
    # xxx
    # ======================================================================
    def __moodleBuildWebCmd(self, function, args_dictionary):
        cmd = f'https://{self.__moodleServer}/webservice/rest/server.php?wstoken={self.__moodleWebServiceSecurityKey}&wsfunction={function}&moodlewsrestformat=json'
        for key in args_dictionary:
            cmd += f'&{key}={args_dictionary[key]}'
        return cmd


    # =======================================================================
    # xxx
    # ======================================================================
    def __moodleExeWebCmd(self, url):
        # Get the html data for the website
        # print(url)
        client = urlopen(url)
        htmlByteData = client.read()
        client.close()
        result = json.loads(htmlByteData.decode())
        # print(result)
        return result


    # =======================================================================
    # returns the ID of the user accessing Moodle through the web service
    # ======================================================================
    def __getUserId(self):
        func = 'core_user_get_users_by_field'
        args = {}
        args['field'] = 'email'
        args['values[0]'] = self.__email

        cmdUrl = self.__moodleBuildWebCmd(func, args)
        result = self.__moodleExeWebCmd(cmdUrl)

        # print(result)
        if 'id' in result[0]:
            self.__userid = result[0]['id']
        else:
            self.__userid = None


    # =======================================================================
    # function to retrieve the list of users in the selected course.
    # This function should be called by selectCourse()
    # =======================================================================
    def __getParticipants(self):
        func = 'core_enrol_get_enrolled_users'
        args = {}
        args['courseid'] = self.__selectedCourse.courseID

        cmdUrl = self.__moodleBuildWebCmd(func, args)
        result = self.__moodleExeWebCmd(cmdUrl)

        # clear any existing list of participants
        self.__participants.clear()

        for item in result:
            newParticipant = Participant(lmsID = item['id'],
                                         name = item['fullname'],
                                         schoolID = item['idnumber'] if 'idnumber' in item else '',
                                         email = item['email'] if 'email' in item else '',
                                         role = item['roles'][0]['name']
                                        )
            self.__participants.append(newParticipant)

        return self.__participants

    # =======================================================================
    # function to retrieve a participant based on the LMS id number
    # =======================================================================
    def __getParticipantFromId(self, lsmID) -> Participant:
        for participant in self.__participants:
            if participant.lmsID == lsmID:
                return participant
        return None

    # =======================================================================
    # function to retrieve available courses from the LMS
    # =======================================================================
    def getCourses(self, sortOutputBy='lastaccess', reverseSort=True) -> [Course]:
        # By default, sort in reverse order based on 'lastaccess' key.
        # Alternate key choices include 'id', 'shortname', 'fullname',
        # 'displayname', 'enrolledusercount', 'idnumber', 'visible',
        # 'summary', 'summaryformat', 'format', 'showgrades', 'lang',
        # 'enablecompletion', 'completionhascriteria', 'category',
        # 'progress', 'completed', 'startdate', 'enddate', 'marker',
        # 'lastaccess', 'isfavourite', 'hidden', 'overviewfiles'

        func = 'core_enrol_get_users_courses'
        args = {}
        args['userid'] = self.__userid

        cmdUrl = self.__moodleBuildWebCmd(func, args)
        result = self.__moodleExeWebCmd(cmdUrl)

        if sortOutputBy not in result:
            # not a valid key
            sortOutputBy = 'lastaccess'

        # Note that we always compare strings even if the values are numeric.  That way, we can deal with missing values easily.
        result.sort(reverse=reverseSort,
                    key=lambda result: str(result[sortOutputBy]) if result[sortOutputBy] != None else '')


        #empty the courses array
        self.__courses.clear()

        for item in result:
            newCourse = Course(courseName=item['shortname'],
                               courseID=item['id'],
                               courseDescription=item['fullname'],
                               term=None)

            #classes.append({'class_id': item['id'], 'shortname': item['shortname'], 'fullname': item['fullname']})
            self.__courses.append(newCourse)

        return self.__courses

    # =======================================================================
    # function that selects which of the available courses returned
    # by getCourses() we will be working with
    # =======================================================================
    def selectCourse(self, course):
        if course in self.__courses:
            self.__selectedCourse = course
            #get the list of participants
            self.__getParticipants()

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
        func = 'mod_assign_get_assignments'
        args = {}
        args['courseids[0]'] = self.__selectedCourse.courseID

        cmdUrl = self.__moodleBuildWebCmd(func, args)
        result = self.__moodleExeWebCmd(cmdUrl)

        # clear the assignments list
        self.__assignments.clear()

        for item in result['courses'][0]['assignments']:
            newAssignment = Assignment()
            newAssignment.assignmentName = item['name']
            newAssignment.assignmentID = item['id']
            newAssignment.assignmentDirectory = ''

            self.__assignments.append(newAssignment)
            #assignments.append({'assignment_id': item['id'], 'name': item['name']})

        return self.__assignments

    # =======================================================================
    # function that selects which of the available assignments returned
    # by getAssignments() we will be working with
    # =======================================================================
    def selectAssignment(self, assignment):
        self.__selectedAssignment = assignment
        self.__getSubmissions()

    # =======================================================================
    # function that returns the currently selected assignment
    # =======================================================================
    def getSelectedAssignment(self) -> Assignment:
        return self.__selectedAssignment


    # =======================================================================
    # function that returns the currently selected assignment
    # =======================================================================
    def __getSubmissions(self, blindSubmission=False):
        func = 'mod_assign_get_submissions'
        args = {}
        args['assignmentids[0]'] = self.__selectedAssignment.assignmentID

        cmdUrl = self.__moodleBuildWebCmd(func, args)
        result = self.__moodleExeWebCmd(cmdUrl)

        fullSubmissions = result['assignments'][0]['submissions']

        self.__selectedAssignment.submissions.clear()
        # id, userid, status, gradingstatus, plugins[0*]['fileareas'*]['files']['filename' and 'fileurl']

        for fullSubmission in fullSubmissions:

            #create a new submission object
            newSubmission = Submission()

            for plugin in fullSubmissions[1]['plugins']:
                if plugin['type'] == 'file':
                    for filearea in plugin['fileareas']:
                        for file in filearea['files']:
                            newSubmission.submissionFiles.append(file['fileurl'])

            newSubmission.submissionID = fullSubmission['id']
            if blindSubmission:
                newSubmission.studentName = newSubmission.studentName = fullSubmission['userid']
            else:
                newSubmission.studentName = self.__getParticipantFromId(fullSubmission['userid']).name

            self.__selectedAssignment.submissions.append(newSubmission)

        return self.__selectedAssignment.submissions


    # =======================================================================
    # function to submit graded assignments back to the LMS
    # =======================================================================
    def submitAssignment(self, assignment):
        raise NotImplementedError()

    # =======================================================================
    # specify a place where the LMS will download and store assignment files
    # =======================================================================
    def setWorkingDirectory(self, workingDirectory):
        raise NotImplementedError()

    # =======================================================================
    # function that returns the currently selected assignment
    # =======================================================================
    def getWorkingDirectory(self) -> str:
        raise NotImplementedError()


# =======================================================================
# xxx
# ======================================================================

# ----------  ----------
# ----------  ----------
# ----------  ----------
# ----------  ----------

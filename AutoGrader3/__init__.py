from IAGConstant import IAGConstant
from console import console
from AGDocument import AGDocument
from MossClient import MossClient

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
# 	_agGrader.py -> pre-processing, GradingEngine, MossClient
# 	_agReport.py -> ReportGenerator, CodeAnalyzer, teacher grade & feedback
#
# =======================================================================
class AutoGrader3(IAGConstant):

    # General configurations
    from ._agConfig import _autoLocateCppCompiler
    from ._agConfig import _autoLocatePython3Interpreter
    from ._agConfig import _autoLocateShell
    from ._agConfig import _loadConfiguration
    from ._agConfig import _setupConfiguration
    from ._agConfig import getConfiguration
    from ._agConfig import saveConfiguration
    from ._agConfig import setConfiguration

    '''
    # Grading Engine configurations
    from ._agConfig import _setCppCompiler
    from ._agConfig import _setPython3Interpreter
    from ._agConfig import _setShellInterpreter
    from ._agConfig import _setTempOutputDirectory
    from ._agConfig import _setMaxOutputLines
    from ._agConfig import _setMaxRunTime
    '''

    # Grading Engine module functions
    from ._agGrader import _updateAutoGraderConfiguration
    from ._agGrader import _setAssignmentName
    from ._agGrader import _cleanupDataFiles
    from ._agGrader import _discoverPrimarySubmissionFile
    from ._agGrader import _prepareDataFiles
    from ._agGrader import addSubmission
    from ._agGrader import addDataFile
    from ._agGrader import addTestDataFile
    from ._agGrader import breakOutTestFiles
    from ._agGrader import grade

    # MOSS
    from ._agGrader import _runMoss
    from ._agGrader import _mossThread

    # LMS interface functions
    from ._agLmsInterface import setLms
    from ._agLmsInterface import getAssignmentFromLms
    from ._agLmsInterface import submitAssignmentToLms
    from ._agLmsInterface import setAssignmentDirectory



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
        self._agDocument = AGDocument()

        # ---------- create the LMS interface ----------
        self._lmsInterface = None   # this is an IAssignmentStore object
        self._assignment = None     # this is an LMS exchange object (Assignment class)

        # ---------- MOSS ----------
        self._mossClient = MossClient()
        self._mossUrl = ''          #the URL of the resulting MOSS comparison
        self._mossThreadHandle = None     #handle the the MOSS thread

'''
    # =======================================================================
    # public void deSerializeFromDisk(String fileName) throws Exception
    # Callback for File->Open
    # =======================================================================
    def deSerializeFromDisk(fileName):
        console('[AutoGrader3:deSerializeFromDisk() stub]')

        #De-serialization
        # Reading the object from a file
        FileInputStream file = new FileInputStream(fileName)
        ObjectInputStream in = new ObjectInputStream(file)

        # Method for deserialization of object
        agDocument = (AGDocument) in.readObject()

        in.close()
        file.close()

        console("Grading Engine successfully de-serialized.")



    # =======================================================================
    # public void serializeToDisk (String fileName) throws Exception
    # menuFileSave()
    # Callback for File->Save
    # =======================================================================
    def serializeToDisk (fileName):
        console('[AutoGrader3:serializeToDisk() stub]')

        # Serialization
        #Saving of object in a file
        FileOutputStream file = new FileOutputStream(fileName)
        ObjectOutputStream out = new ObjectOutputStream(file)

        # Method for serialization of object
        out.writeObject(agDocument)

        out.close()
        file.close()

        console("Grading Engine successfully serialized.")
'''





# =======================================================================
# xxx
# =======================================================================

# ----------  ----------
# ----------  ----------
# ----------  ----------
# ----------  ----------

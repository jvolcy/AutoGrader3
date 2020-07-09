import sys
import os
import subprocess
import json
from pathlib import Path
from IAGConstant import IAGConstant
from console import console
from AGDocument import AGDocument


# =======================================================================
# AutoGrader3 class
#
# Structure of AutoGrader3 class
#
# AutoGrader3 classes ("has a")
# 	AGDocument
# 	Simulator, MoodleClient, CanvasClient, etc.  all implement (IDataStore)
# 	GradingEngine
# 	MossClient
# 	ReportGenerator
# 	IAssignmentStore (implements: assignmentName, assignmentDirectory, [[assignmentFiles], studentName, studentID, submitGrade(grade, msg)], setWorkingDirectory() )
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

    # Grading Engine configurations
    from ._agConfig import setCppCompiler
    from ._agConfig import setPython3Interpreter
    from ._agConfig import setShellInterpreter
    from ._agConfig import setTempOutputDirectory
    from ._agConfig import setMaxOutputLines
    from ._agConfig import setMaxRunTime

    # Grading Engine module functions
    from ._agGrader import _setAssignmentName
    from ._agGrader import _cleanupDataFiles
    from ._agGrader import _discoverPrimaryAssignmentFile
    from ._agGrader import _prepareDataFiles
    from ._agGrader import addAssignment
    from ._agGrader import addDataFile
    from ._agGrader import addTestDataFile
    from ._agGrader import breakOutTestFiles
    from ._agGrader import grade

    # LMS interface functions
    from ._agLmsInterface import getAssignmentsFromLms
    from ._agLmsInterface import submitAssignmentsToLms
    from ._agLmsInterface import setWorkingDirectory


    # =======================================================================
    # AutoGraderApp()
    # constructor
    # =======================================================================
    def __init__(self):
        # private GradingEngine gradingEngine
        console("AutoGraderApp constructor...")


        # ---------- AutoGrader options ----------
        self._ag_config = {}

        # ---------- set the path to the JSON config file ----------
        self._configFileName = IAGConstant.CONFIG_FILENAME

        #get the user's home directory and set the path to the config file
        home = str(Path.home())
        home = home.rstrip('/')  #remove the trailing '/' if it is present
        self.configFile = home + '/' + self._configFileName
        console("Config file path = '" + self.configFile + "'")

        # ---------- setup app configurations ----------
        self._setupConfiguration()

        # ---------- initialize the grading engine ----------
        self._agDocument = AGDocument()

        # ---------- initialize other class members ----------

    # =======================================================================
    # public AGDocument getAgDocument()
    # =======================================================================
    #def getAgDocument(self):
    #    return self._agDocument


    # =======================================================================
    # public void deSerializeFromDisk(String fileName) throws Exception
    # Callback for File->Open
    # =======================================================================
    def deSerializeFromDisk(fileName):
        console('[AutoGrader3:deSerializeFromDisk() stub]')
        '''
        #De-serialization
        # Reading the object from a file
        FileInputStream file = new FileInputStream(fileName)
        ObjectInputStream in = new ObjectInputStream(file)

        # Method for deserialization of object
        agDocument = (AGDocument) in.readObject()

        in.close()
        file.close()

        console("Grading Engine successfully de-serialized.")
        '''


    # =======================================================================
    # public void serializeToDisk (String fileName) throws Exception
    # menuFileSave()
    # Callback for File->Save
    # =======================================================================
    def serializeToDisk (fileName):
        console('[AutoGrader3:serializeToDisk() stub]')
        '''
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

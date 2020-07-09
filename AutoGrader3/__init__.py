import sys
import os
import subprocess
import json
from pathlib import Path
from IAGConstant import IAGConstant
from console import console
from AGDocument import AGDocument


# =======================================================================
# AutoGraderApp class
# =======================================================================
class AutoGrader3(IAGConstant):

    from ._agConfig import _autoLocateCppCompiler
    from ._agConfig import _autoLocatePython3Interpreter
    from ._agConfig import _autoLocateShell
    from ._agConfig import _loadConfiguration
    from ._agConfig import _setupConfiguration
    from ._agConfig import getConfiguration
    from ._agConfig import saveConfiguration
    from ._agConfig import setConfiguration

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


    # =======================================================================
    # public AGDocument getAgDocument()
    # =======================================================================
    def getAgDocument(self):
        return self._agDocument


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

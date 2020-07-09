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

    # =======================================================================
    # AutoGraderApp()
    # constructor
    # =======================================================================
    def __init__(self):
        # private GradingEngine gradingEngine
        console("AutoGraderApp constructor...")


        # ---------- AutoGrader options ----------
        self.__ag_config = {}

        # ---------- set the path to the JSON config file ----------
        self.__configFileName = IAGConstant.CONFIG_FILENAME

        #get the user's home directory and set the path to the config file
        home = str(Path.home())
        home = home.rstrip('/')  #remove the trailing '/' if it is present
        self.configFile = home + '/' + self.__configFileName
        console("Config file path = '" + self.configFile + "'")

        # ---------- setup app configurations ----------
        self.__setupConfiguration()

        # ---------- initialize the grading engine ----------
        self.__agDocument = AGDocument()


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
    def __autoLocatePython3Interpreter(self):
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
    def __autoLocateCppCompiler(self):
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
    def __autoLocateShell(self):
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
        return self.__ag_config[key]


    # =======================================================================
    # public String setConfiguration(String key, String value)
    # This function returns the value for the supplied configuration key.
    # If the key is not in the configuraiton dictionary ag_config, the
    # function returns null.  All configuration keys and values are strings.
    # =======================================================================
    def setConfiguration(self,  key, value):
        # console("setting conf. for " + key)
        self.__ag_config[key] = value

    # =======================================================================
    # private void setupConfiguration()
    # This function sets up default AG2 configurations.
    # The values used for the configurations are either hardcoded defaults
    # or generated by probing the system.
    # =======================================================================
    def __setupConfiguration(self):
        # ---------- auto-locate python3 interpreter ----------
        python3Path = self.__autoLocatePython3Interpreter()
        if python3Path == '':
            console("No auto-detected python3 interpreter.")
        else:
            console("Found a Python3 interpreter at '" + python3Path + "'")

        # ---------- auto-locate c++ compiler ----------
        cppPath = self.__autoLocateCppCompiler()
        if cppPath == '':
            console("No auto-detected c++ compiler.")
        else:
            console("Found a c++ compiler at '" + cppPath + "'")

        # ---------- auto-locate shell interpreter ----------
        shellPath = self.__autoLocateShell()
        if shellPath == '':
            console("No auto-detected shell interpreter.")
        else:
            console("Found a shell interpreter at '" + shellPath + "'")

        # ---------- Generate or set the default AG options ----------
        self.__ag_config[IAGConstant.AG_CONFIG.LANGUAGE] = IAGConstant.LANGUAGE_AUTO
        self.__ag_config[IAGConstant.AG_CONFIG.MAX_RUNTIME] = "3"
        self.__ag_config[IAGConstant.AG_CONFIG.MAX_OUTPUT_LINES] = "100"
        self.__ag_config[IAGConstant.AG_CONFIG.INCLUDE_SOURCE] = IAGConstant.YES
        self.__ag_config[IAGConstant.AG_CONFIG.AUTO_UNCOMPRESS] = IAGConstant.YES
        self.__ag_config[IAGConstant.AG_CONFIG.PROCESS_RECURSIVELY] = IAGConstant.YES
        self.__ag_config[IAGConstant.AG_CONFIG.PYTHON3_INTERPRETER] = python3Path
        self.__ag_config[IAGConstant.AG_CONFIG.CPP_COMPILER] = cppPath
        self.__ag_config[IAGConstant.AG_CONFIG.SHELL] = shellPath

        # ---------- Overwrite the default AG options with data from the JSON file ----------
        self.__loadConfiguration()


    # =======================================================================
    # private void loadConfiguration()
    # This function loads the AG2 configurations from a JSON file.
    #
    # configFileName is the full path of the JSON configuration file.
    # =======================================================================
    def __loadConfiguration(self):

        console("AutoGrader3: Loading configuration from " + str(self.configFile))
        try:
            with open(self.configFile) as f:
                config = json.load(f)

            for item in config:
                self.__ag_config[item] = config[item]

        except:
            #if the file does not exist, or is otherwise inaccessible, do nothing
            console("Warning: unable to source " + self.configFile)
            return

        '''
        # read and parse the config file
        try:
            Object obj = new JSONParser().parse(new FileReader(configFileName))

            # typecasting obj to JSONObject
            JSONObject jo = (JSONObject) obj

            # getting firstName and lastName
            #String firstName = (String) jo.get("firstName")
            #String lastName = (String) jo.get("lastName")

            #read the configuration
            ag_config.put(AG_CONFIG.LANGUAGE, (String) jo.get(AG_CONFIG.LANGUAGE))
            ag_config.put(AG_CONFIG.MAX_RUNTIME, (String) jo.get(AG_CONFIG.MAX_RUNTIME))
            ag_config.put(AG_CONFIG.MAX_OUTPUT_LINES, (String) jo.get(AG_CONFIG.MAX_OUTPUT_LINES))
            ag_config.put(AG_CONFIG.INCLUDE_SOURCE, (String) jo.get(AG_CONFIG.INCLUDE_SOURCE))
            ag_config.put(AG_CONFIG.AUTO_UNCOMPRESS, (String) jo.get(AG_CONFIG.AUTO_UNCOMPRESS))
            ag_config.put(AG_CONFIG.PROCESS_RECURSIVELY, (String) jo.get(AG_CONFIG.PROCESS_RECURSIVELY))
            ag_config.put(AG_CONFIG.PYTHON3_INTERPRETER, (String) jo.get(AG_CONFIG.PYTHON3_INTERPRETER))
            ag_config.put(AG_CONFIG.CPP_COMPILER, (String) jo.get(AG_CONFIG.CPP_COMPILER))
            ag_config.put(AG_CONFIG.SHELL, (String) jo.get(AG_CONFIG.SHELL))
        }
        except:
            e = sys.exc_info()[0]
            console("loadConfiguration(): " + e.toString())
        '''


    # =======================================================================
    # public void saveConfiguration()
    # This function saves the AG2 configurations to a JSON file.
    #
    # configFileName is the full path of the JSON configuration file.
    # =======================================================================
    def saveConfiguration(self):

        console("AutoGrader3: Saving configuration to " + str(self.configFile))

        with open(self.configFile, 'w') as json_file:
            json.dump(self.__ag_config, json_file)


        '''
        console("Saving " + configFileName)
        # creating JSONObject
        JSONObject jo = new JSONObject()

       # putting data to JSONObject
        jo.put(AG_CONFIG.LANGUAGE, ag_config.get(AG_CONFIG.LANGUAGE))
        jo.put(AG_CONFIG.MAX_RUNTIME, ag_config.get(AG_CONFIG.MAX_RUNTIME))
        jo.put(AG_CONFIG.MAX_OUTPUT_LINES, ag_config.get(AG_CONFIG.MAX_OUTPUT_LINES))
        jo.put(AG_CONFIG.INCLUDE_SOURCE, ag_config.get(AG_CONFIG.INCLUDE_SOURCE))
        jo.put(AG_CONFIG.AUTO_UNCOMPRESS, ag_config.get(AG_CONFIG.AUTO_UNCOMPRESS))
        jo.put(AG_CONFIG.PROCESS_RECURSIVELY, ag_config.get(AG_CONFIG.PROCESS_RECURSIVELY))
        jo.put(AG_CONFIG.PYTHON3_INTERPRETER, ag_config.get(AG_CONFIG.PYTHON3_INTERPRETER))
        jo.put(AG_CONFIG.CPP_COMPILER, ag_config.get(AG_CONFIG.CPP_COMPILER))
        jo.put(AG_CONFIG.SHELL, ag_config.get(AG_CONFIG.SHELL))

        # writing JSON to file
        try:
            BufferedWriter bw = new BufferedWriter(new FileWriter(configFileName))
            bw.write(jo.toJSONString())
            bw.close()
        except:
            e = sys.exc_info()[0]
            console("saveConfiguration(): " +  e.toString())
        '''


    # =======================================================================
    # public AGDocument getAgDocument()
    # =======================================================================
    def getAgDocument(self):
        return self.__agDocument


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

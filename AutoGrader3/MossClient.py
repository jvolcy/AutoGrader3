import sys
import socket
from .console import console


''' ======================================================================
* This file implements a client for the Stanford MOSS (Measurement Of
* Software Similarity) based on the python client provided by
* Syed Owais Ali Chishti and available at
* https://github.com/soachishti/moss.py
*
* The MOSS homesite is
* http://theory.stanford.edu/~aiken/moss/
* or
* http://moss.stanford.edu
*
* MOSS is an online service.  You must register with the website to
* obtain a userid number (typically a 9-digit number) before you can
* use this class.
*
*
* class Usage
* -----------
* 1) You must specify the moss userid when a MossClient object is
* instantiated.
* 2) Specify all options for the code comparison.  At a minimum, you
* must specify the coding language (setLanguage()).  Use the getLanguages()
* method to retrieve a list of supported languages.
* 3) You may optionally specify other options using the
* setCommentString(), setNumberOfMatchingFiles(), setDirectoryMode()
* and setExperimentalServer() functions.
* 4) Upload any base files.  These are "starter code" files that may
* have been provided to the students.  Call the addBaseFile() method
* for each base file to be uploaded.
* 5) Upload student files to be compared.  Call the addFile() method
* for each student file to be uploaded.
* 6) Call send().  send() logs in to the server, communicates the
* selected options, transfers the base and student files and returns
* the result URL unless an error occurs.
* 7) Use the getWebPage() to download the HTML report, if desired.
* ===================================================================== '''



''' ======================================================================
* MossClient
* ===================================================================== '''
class MossClient:
    #---------- class members ----------

    __DEFAULT_MOSS_SERVER = "moss.stanford.edu"
    __DEFAULT_MOSS_PORT = 7690

    @classmethod
    def getDefaultMossServer(cls):
        return cls.__DEFAULT_MOSS_SERVER

    @classmethod
    def getDefaultMossPort(cls):
        return cls.__DEFAULT_MOSS_PORT


    ''' ======================================================================
    * General Constructor
    * Specify the userid to use this constructor.
    * default values of the MOSS server and port# are provided
    * ===================================================================== '''
    def __init__ (self, userid='', server=__DEFAULT_MOSS_SERVER, port=__DEFAULT_MOSS_PORT):
        #store the userid, server and port #
        self.__userid = userid      #moss userid
        self.__server = server      #moss server
        self.__port = port      #moss server port
        self.__socket = socket.socket()    #moss server socket object
        
        self.__languages = [        #array of valid languages MOSS can work with
            "c", "cc", "java", "ml", "pascal","ada","lisp", "scheme",
            "haskell", "fortran", "ascii","vhdl", "verilog", "perl",
            "matlab", "python", "mips","prolog",  "spice", "vb",
            "csharp", "modula2", "a8086", "javascript",  "plsql" ]

        #initialize the base file and student submission files dictionaries
        self.__files = []   #list of student files
        self.__baseFiles = []    #list of base files.  These are files provided to students as "starter code".


        self.__options = {}     #options dictionary.  These are options passed to the MOSS server

        #set the default options
        #console(userid + language)
        self.__options['l'] = ""       #selected language
        self.__options['m'] = "10"     #the maximum number of times a given passage may appear before it is ignored
        self.__options['d'] = "0"      #The -d option specifies that submissions are by directory, not by file.
                                       #That is, files in a directory are taken to be part of the same program,
        self.__options['x'] = "0"      #The -x option sends queries to the current experimental version of the server.
        self.__options['c'] = ""       #The -c option supplies a comment string that is attached to the generated report.
        self.__options['n'] = "250"    #the number of matching files to show in the results


    ''' ======================================================================
    * Sets the MOSS server
    * ===================================================================== '''
    def setServer(self, server):
        self.__server = server


    ''' ======================================================================
    * Gets the MOSS server
    * ===================================================================== '''
    def getServer(self):
        return self.__server


    ''' ======================================================================
    * Sets the MOSS server port
    * ===================================================================== '''
    def setServerPort(self, port):
        self.__port = port


    ''' ======================================================================
    * Gets the MOSS server port
    * ===================================================================== '''
    def getServerPort(self):
        return self.__port


    ''' ======================================================================
    * Sets the MOSS userID
    * ===================================================================== '''
    def setUserId(self, userid):
        self.__userid = userid


    ''' ======================================================================
    * Gets the MOSS userID
    * ===================================================================== '''
    def getUserId(self):
        return self.__userid


    ''' ======================================================================
    * Use addFile to add a student programming file to the list of files
    * to be compared.
    * ===================================================================== '''
    def addFile(self, filePath):
        console("MOSS: Adding file " + filePath)
        self.__files.append(filePath)
    

    ''' ======================================================================
    * Use addFiles to add multiple student programming files to the list of
    * files to be compared.
    * ===================================================================== '''
    def addFiles(self, filePaths):
        for filePath in filePaths:
            self.addFile(filePath)


    ''' ======================================================================
    * Moss normally reports all code
    * that matches in pairs of files.  When a base file is supplied,
    * program code that also appears in the base file is not counted in matches.
    * A typical base file will include, for example, the instructor-supplied
    * code for an assignment.  Multiple base files are allowed.  You should
    * use a base file if it is convenient; base files improve results, but
    * are not usually necessary for obtaining useful information.
    * The -b option names a "base file" when the request is sent to the server.
    * ===================================================================== '''
    def addBaseFile(self, filePath):
        console("MOSS: Adding base file " + filePath)
        self.__baseFiles.append(filePath)


    ''' ======================================================================
    * Use addBaseFiles to add multiple base files to the list of base files.
    * ===================================================================== '''
    def addBaseFiles(self, filePaths):
        for filePath in filePaths:
            self.addBaseFile(filePath)


    ''' ======================================================================
    * The -l option specifies the source language of the tested programs.
    * Moss supports many different languages; see the variable "languages" for the
    * full list.
    * ===================================================================== '''
    def setLanguage(self, language):
        #check that the language is in the list
        if language in self.__languages:
            self.__options['l'] = language
        
        else:
            self.__options['l'] = ""


    ''' ======================================================================
    * Returns the current language option.
    * ===================================================================== '''
    def getLanguage(self):
        return self.__options['l']


    ''' ======================================================================
    # The -m option sets the maximum number of times a given passage may appear
    # before it is ignored.  A passage of code that appears in many programs
    # is probably legitimate sharing and not the result of plagiarism.  With -m N,
    # any passage appearing in more than N programs is treated as if it appeared in
    # a base file (i.e., it is never reported).  Option -m can be used to control
    # moss' sensitivity.  With -m 2, moss reports only passages that appear
    # in exactly two programs.  If one expects many very similar solutions
    # (e.g., the short first assignments typical of introductory programming
    # courses) then using -m 3 or -m 4 is a good way to eliminate all but
    # truly unusual matches between programs while still being able to detect
    # 3-way or 4-way plagiarism.  With -m 1000000 (or any very
    # large number), moss reports all matches, no matter how often they appear.
    # The -m setting is most useful for large assignments where one also a base file
    # expected to hold all legitimately shared code.  The default for -m is 10.
    * ===================================================================== '''
    def setIgnoreLimit(self, limit):
        self.__options['m'] = int(limit)
    

    ''' ======================================================================
    # The -c option supplies a comment string that is attached to the generated
    # report.  This option facilitates matching queries submitted with replies
    # received, especially when several queries are submitted at once.
    * ===================================================================== '''
    def setCommentString(self, comment):
        self.__options['c'] = comment
    

    ''' ======================================================================
    # The -n option determines the number of matching files to show in the results.
    # The default is 250.
    * ===================================================================== '''
    def setNumberOfMatchingFiles(self, n):
        if n > 1:
            self.__options['n'] = int(n)


    ''' ======================================================================
    * The -d option specifies that submissions are by directory, not by file.
    * That is, files in a directory are taken to be part of the same program,
    * and reported matches are organized accordingly by directory.
    * "0" = directory mode not set
    * "1" = directory mode set
    * ===================================================================== '''
    def setDirectoryMode(self, mode):
        self.__options['d'] = mode


    ''' ======================================================================
    # The -x option sends queries to the current experimental version of the server.
    # The experimental server has the most recent Moss features and is also usually
    # less stable (read: may have more bugs).
    # "0" = do not use experimental server
    # "1" = use experimental server
    * ===================================================================== '''
    def setExperimentalServer(self, opt):
        self.__options['x'] = opt
    

    ''' ======================================================================
    * Returns the list of language with MOSS can work with.
    * ===================================================================== '''
    def getLanguages(self):
        return self.__languages
    

    ''' ======================================================================
    * open the socket connection to the moss server
    * Do not call this function directly.  It is called by the send() function.
    * ===================================================================== '''
    def __openSocket(self):
        console(f"__openSocket().  server={self.__server}, port = {self.__port}")
        self.__socket.connect((self.__server, self.__port))
    

    ''' ======================================================================
    * close the socket connection to the moss server
    * Do not call this function directly.  It is called by the send() function.
    * ===================================================================== '''
    def __closeSocket(self):
        self.__socket.close()
    

    ''' ======================================================================
    * socketWrite()
    * writes the provided string to the moss server.
    * Note that the socket must be open (see openSocket()) before
    * using this function.
    * Do not call this function directly.  It is called by the send() and
    * uploadFile() functions.
    * ===================================================================== '''
    def __socketWrite(self, data):
        self.__socket.send(data.encode())
        

    ''' ======================================================================
    * socketRead()
    * Read a string from the moss socket.
    * Note that the socket must be open (see openSocket()) before
    * using this function.
    * Do not call this function directly.  It is called by the send() function.
    * ===================================================================== '''
    def __socketRead(self, bufSize=4096):
        return self.__socket.recv(bufSize).decode()
    

    ''' ======================================================================
    * Use the uploadFile() function to upload student programming files to
    * the moss server.
    * Do not call this function directly.  It is called by the send() function.
    * ===================================================================== '''
    def __uploadFile(self, file_path, display_name, file_id):
        '''Note: socket must be open before calling this function. '''
        if display_name == '':
            #If no display name added by user,default to file path
            #Display name cannot accept \,replacing it with /
            tmp_name = file_path.replace(" ", "_").replace("\\", "/")
            split_name = tmp_name.split('/')
            if len(split_name) > 1:
                #the top level directory + filename
                display_name = split_name[-2] + '/' + split_name[-1]
            elif len(split_name) == 1:
                #only the file name
                display_name = tmp_name
            else:
                display_name = ''
        
        try:
            with open(file_path, "r") as f:
                content = f.read()
                console("sending --> <contents of" + file_path + ">")
        except:
            e = sys.exc_info()[0]
            console("MossClient::__uploadFile() " + str(e))
            return

        size = len(content)

        message = f"file {file_id} {self.__options['l']} {size} {display_name}\n"

        self.__socketWrite(message)
        self.__socketWrite(content)


    ''' ======================================================================
    * The send() function is the central function of the MossClient
    * class, from the class user's perspective.
    * send() performs all transfers to and from the server apart from
    * transferring resulting HTML from the server via the getWebPage()
    * method.
    * Call the send() function after all moss parameters have been set
    * (-l, -m, -x, etc...) and all base files and student program files
    * have been specified (addBaseFile() and addFile(), respectively.)
    * ===================================================================== '''
    def send(self):
        if self.__userid == '':
            console('No user ID set')
            return ""

        console("Opening socket...")
        self.__openSocket()
        console("Writing parameters...")

        self.__socketWrite(f"moss {self.__userid}\n")
        self.__socketWrite(f"directory {self.__options['d']}\n")
        self.__socketWrite(f"X {self.__options['x']}\n")
        self.__socketWrite(f"maxmatches {self.__options['m']}\n")
        self.__socketWrite(f"show {self.__options['n']}\n")
        self.__socketWrite(f"language {self.__options['l']}\n")
        console("Retrieving status confirmation...")
        recv = self.__socketRead()
        if recv == "no":
            self.__socketWrite("end\n")
            self.__closeSocket()
            console("MOSS: send() => Language not accepted by server")
            return ""
        
        else:
            console("MOSS: confirmation >>"+recv+"<<")
        
        console("MOSS: Uploading baseFiles...")
        for file_path in self.__baseFiles:
            console(f"sending --> {file_path} [0]")
            self.__uploadFile(file_path, "", 0)
        

        console("MOSS: Uploading Files...")
        index = 1
        for file_path in self.__files:
            console (f"sending --> {file_path} [{index}]")
            self.__uploadFile(file_path, "", index)
            index += 1


        console(f"sending --> query 0 {self.__options['c']}")
        self.__socketWrite(f"query 0 {self.__options['c']}\n")

        #console("MOSS: Retrieving response...")
        response = self.__socketRead()

        #print("sending -->:\n".format("end\n").encode())
        self.__socketWrite("end\n")

        #print('*** response=', response)
        self.__closeSocket()

        return response.replace("\n","")


    ''' ======================================================================
    * Retrieves the results page from the moss server.  Call this function
    * after a successful call to send() to download the comparison report
    * summary page.
    * ===================================================================== '''
    def getWebPage(self, url):
        pass
    



''' ======================================================================
*
* ===================================================================== '''

#----------  ----------





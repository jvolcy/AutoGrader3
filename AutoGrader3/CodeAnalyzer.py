import sys
from .console import console

class CppAnalysis (object):
    def __init__(self, numLines, numComments):
        self.numLines = numLines        # Number of lines of code
        self.numComments = numComments  # Number of comments in the code

class PythonAnalysis(object):
    def __init__(self, numLines, numComments, numDocStr, numFuncs, numClasses):
        self.numLines = numLines        # Number of lines of code
        self.numComments = numComments  # Number of comments in the code
        self.numDocStr = numDocStr      # Number of doc strings in code
        self.numFuncs = numFuncs        # Number of functions
        self.numClasses = numClasses    # Number of classes

# =======================================================================
# xxx
# ======================================================================
class CodeAnalyzer(object):

    # =======================================================================
    # public static CppAnalysis analyzeCppFile(String filepath)
    # function that counts line numbers, and estimates the # of comments
    # in the supplied C++ sourceFile.  The function returns a tuple with
    # the format (numLines, numComments).
    # ======================================================================
    @classmethod
    def analyzeCppFile(cls, filepath):
        numLines = 0
        numComments = 0

        try:
            br = open(filepath, 'rt')

            for linex in br:
                line = linex.rstrip()

                # count the number of lines in the file
                numLines += 1

                # count the number of multi-line opening comment tokens (/*) in the file
                loc = line.find("/*")
                if loc != -1:
                    numComments += 1

                # count the number of single-line comment tokens (#) in the file
                loc = line.find("//")
                if loc != -1:
                    numComments += 1

            br.close()

        except:
            e = sys.exc_info()[0]
            console("analyzeCppFile(): " + e.toString())

        return CppAnalysis(numLines, numComments)



    # =======================================================================
    # public static PythonAnalysis analyzePythonFile(String filepath)
    # function that counts line numbers, and estimates the # of comments
    # # of doc strings, # of functions and # of classes in the supplied
    # Python sourceFile.
    # ======================================================================
    @classmethod
    def analyzePythonFile(cls, filepath):
        numLines = 0       # Number of lines of code
        numDocStr = 0      # Number of doc strings in code
        numComments = 0    # Number of comments in the code
        numFuncs = 0        # Number of functions
        numClasses = 0     # Number of classes

        try:
            br = open(filepath, 'rt')

            for linex in br:
                line = linex.rstrip()
                # count the number of lines in the file
                numLines += 1

                # count the number of multi-line opening comment tokens (/*) in the file
                loc = line.find("'''")
                if loc != -1:
                    numDocStr += 1

                # count the number of multi-line opening comment tokens (/*) in the file
                loc = line.find("\"\"\"")
                if loc != -1:
                    numDocStr += 1

                # count the number of single-line comment tokens (#) in the file
                loc = line.find("#")
                if loc != -1:
                    numComments += 1

                # discount the # of times the '#' char appears as the 1st char in double quotes (skip hex constants)
                loc = line.find("\"#")
                if loc != -1:
                    numComments -= 1

                # discount the # of times the '#' char appears as the 1st char in single quotes (skip hex constants)
                loc = line.find("'#")
                if loc != -1:
                    numComments -= 1

                # look for functions
                loc = line.find("def ")
                if loc != -1:
                    numFuncs += 1

                # look for classes
                loc = line.find("class ")
                if loc != -1:
                    numClasses += 1

            br.close()

        except:
            e = sys.exc_info()[0]
            console("analyzePythonFile(): " + str(e))

        numDocStr /= 2       # assume that docString tokens appear in pairs

        return PythonAnalysis(numLines, numComments, numDocStr, numFuncs, numClasses )





# =======================================================================
# xxx
# ======================================================================

#----------  ----------
#----------  ----------
#----------  ----------
#----------  ----------

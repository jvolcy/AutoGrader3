package AutoGraderApp;

import java.io.BufferedReader;
import java.io.FileReader;
import static AutoGraderApp.Controller.console;

class CppAnalysis {
    public int numLines = 0;     //Number of lines of code
    public int numComments = 0;  //Number of comments in the code
    CppAnalysis (int numLines,int numComments) {
        this.numLines = numLines;
        this.numComments = numComments;
    }
}

class PythonAnalysis {
    public int numLines = 0;        //Number of lines of code
    public int numComments = 0;     //Number of comments in the code
    public int numDocStr = 0;       //Number of doc strings in code
    public int numFuncs = 0;        //Number of functions
    public int numClasses = 0;      //Number of classes
    PythonAnalysis (int numLines,int numComments, int numDocStr, int numFuncs, int numClasses) {
        this.numLines = numLines;
        this.numComments = numComments;
        this.numDocStr = numDocStr;
        this.numFuncs = numFuncs;
        this.numClasses = numClasses;
    }

}

/* ======================================================================
 * xxx
 * ===================================================================== */
public class CodeAnalyzer {

    /* ======================================================================
     * function that counts line numbers, and estimates the # of comments
     * in the supplied C++ sourceFile.  The function returns a tuple with
     * the format (numLines, numComments).
     * ===================================================================== */
    public static CppAnalysis analyzeCppFile(String filepath) {
        int numLines = 0;
        int numComments = 0;

        try {
            BufferedReader br = new BufferedReader(new FileReader(filepath));
            String line;

            int loc;
            while ((line = br.readLine()) != null) {
                //count the number of lines in the file
                numLines += 1;

                //count the number of multi-line opening comment tokens (/*) in the file
                loc = line.indexOf("/*");
                if (loc != -1)
                    numComments += 1;

                //count the number of single-line comment tokens (//) in the file
                loc = line.indexOf("//");
                if (loc != -1)
                    numComments += 1;
            }
        } catch (Exception e) {
            console(e.getMessage());
        }

        return new CppAnalysis(numLines, numComments);
    }


    /* ======================================================================
     * PythonAnalysis()
     * function that counts line numbers, and estimates the # of comments
     * # of doc strings, # of functions and # of classes in the supplied
     * Python sourceFile.
     * ===================================================================== */
    public static PythonAnalysis analyzePythonFile(String filepath) {
        int numLines = 0;       //Number of lines of code
        int numDocStr = 0;      //Number of doc strings in code
        int numComments = 0;    //Number of comments in the code
        int numFuncs = 0;        //Number of functions
        int numClasses = 0;     //Number of classes

        try {
            BufferedReader br = new BufferedReader(new FileReader(filepath));
            String line;

            int loc;
            while ((line = br.readLine()) != null) {
                //count the number of lines in the file
                numLines += 1;

                //count the number of multi-line opening comment tokens (/*) in the file
                loc = line.indexOf("'''");
                if (loc != -1)
                    numDocStr += 1;

                //count the number of multi-line opening comment tokens (/*) in the file
                loc = line.indexOf("\"\"\"");
                if (loc != -1)
                    numDocStr += 1;

                //count the number of single-line comment tokens (//) in the file
                loc = line.indexOf("//");
                if (loc != -1)
                    numComments += 1;

                loc = line.indexOf("#");
                if (loc != -1)
                    numComments += 1;

                //discount the # of times the '#' char appears as the 1st char in double quotes (skip hex constants)
                loc = line.indexOf("\"#");
                if (loc != -1)
                    numComments -= 1;

                //discount the # of times the '#' char appears as the 1st char in single quotes (skip hex constants)
                loc = line.indexOf("'#");
                if (loc != -1)
                    numComments -= 1;

                //look for functions
                loc = line.indexOf("def ");
                if (loc != -1)
                    numFuncs += 1;

                //look for classes
                loc = line.indexOf("class ");
                if (loc != -1)
                    numClasses += 1;
            }

        } catch (Exception e) {
            console(e.getMessage());
        }

        numDocStr /= 2;       //assume that docString tokens appear in pairs

        return new PythonAnalysis(numLines, numComments, numDocStr, numFuncs, numClasses );

    }
}



/* ======================================================================
 * xxx
 * ===================================================================== */

//----------  ----------
//----------  ----------
//----------  ----------
//----------  ----------

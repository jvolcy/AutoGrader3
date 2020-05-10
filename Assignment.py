package AutoGraderApp;

import java.io.File;
import java.util.ArrayList;

/* ======================================================================
 * Assignment
 * ===================================================================== */
public class Assignment implements java.io.Serializable {
    //---------- general members ----------
    public String studentName;
    public String assignmentDirectory;
    public ArrayList<File> assignmentFiles;
    public File primaryAssignmentFile;
    public String language;
    //---------- code analysis members ----------
    //public Integer linesOfCode;
    //public Integer numComments;
    //public Integer nunDocStrings;
    //public Integer numFunctions;
    //public Integer numClasses;
    //---------- errors ----------
    public String compilerErrors;
    public String[] runtimeErrors;     //there are as many entries as we have test cases
    //---------- processing/execution members ----------
    public String[] progOutputs;     //there are as many entries as we have test cases
    public Double[] executionTimes;      //the # of seconds required to complete execution
    //---------- grading members ----------
    public Boolean bAutoGraded;
    public Integer grade;
    public String instructorComment;
    //---------- directives ----------
    public String nameDirective;        //student name
    public String titleDirective;       //assignment title
    public String dateDirective;        //date
    public String mainDirective;        //main module
    public String dataDirective;        //misc. data

}


/* ======================================================================
 * xxx
 * ===================================================================== */

//----------  ----------
//----------  ----------
//----------  ----------
//----------  ----------

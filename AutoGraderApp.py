package AutoGraderApp;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;

import static AutoGraderApp.Controller.console;

/* ======================================================================
 * AutoGraderApp class
 * ===================================================================== */
public class AutoGraderApp extends Application implements IAGConstant {

    public static AutoGrader2 autoGrader;
    public static final String appName = "Spelman AutoGrader 2";
    public static final String version = "pre 2.0.6";
    public static final String copyrightText = "copyright 2016-2018";
    public static final String credits = "J Volcy";

    /* ======================================================================
     * start()
     * This function is automatically called after the primary stage
     * has been created.
     * This is a good place to customize the appearance of the stage.
     * ===================================================================== */
    @Override
    public void start(Stage primaryStage) throws Exception {
        console("start...");

        /* original */
        //FXMLLoader loader = new FXMLLoader(getClass().getResource("AutoGraderApp.fxml"));
        //Parent root = loader.load();
        /***********/

        Parent root = FXMLLoader.load(getClass().getResource("AutoGraderApp.fxml"));

        //Parent root = loader.load();

        // Get the Controller from the FXMLLoader
        //Controller controller = loader.getController();
        //controller.setGradingEngine(autoGrader.getGradingEngine());
        //controller.setAutoGraderRef(autoGrader);

        primaryStage.setTitle(appName);
        primaryStage.setScene(new Scene(root, MIN_STAGE_WIDTH, MIN_STAGE_HEIGHT));
        primaryStage.setMinWidth(MIN_STAGE_WIDTH);
        primaryStage.setMinHeight(MIN_STAGE_HEIGHT);

        primaryStage.getIcons().add(new Image("/ag2_icon.png"));
        primaryStage.show();
    }

    /* ======================================================================
     * main()
     * Entry point into the application.
     * ===================================================================== */
    public static void main(String[] args) {

        console("main...");
        autoGrader = new AutoGrader2();

        console("launching...");
        //---------- start the GUI ----------
        launch(args);

        //---------- Commit the AG options to the JSON file ----------
        autoGrader.saveConfiguration();

        console("Exiting main()...");
    }


    /* ======================================================================
     * Help HTML string
     * ===================================================================== */
    public static final String HelpHtml = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">" +
            "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\" lang=\"en\">" +
            "<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />" +
            "<title>AutoGrader 2 Help</title></head>" +
            "<body style=\"background: white; font-family: Cambria\">" +
            "<div class=\"WordSection1\">" +
            "<div style=\"text-align: center;\"><b>" +
            "<span style=\"font-size: 18pt; color: rgb(0, 112, 192);\">Spelman AutoGrader 2</span></b><br>" +
            "</div>&nbsp;<br>" +
            "<span style=\"font-size: 14pt; color: rgb(0, 112, 192);\"><big>Introduction</big> </span><br>" +
            "The Spelman AutoGrader 2 program is designed to help grade " +
            "Python and C++ programs submitted through Moodle.&nbsp; The program runs on macOS and Linux systems only.  " +
            "It is not Windows compatible.  To use the program, " +
            "perform a “download all submissions” of the target assignment from " +
            "Moodle. &nbsp;Extract " +
            "the downloaded zip file.&nbsp; This will create a directory on disk that holds " +
            "all student submissions.&nbsp; We will call this our “top-level " +
            "directory” (TLD).&nbsp; The TLD should contain as many sub-directories as there " +
            "are submitted assignments.&nbsp; The names of these sub-directories should be " +
            "formatted as “student name_assignment”.&nbsp; If your TLD does not contain " +
            "sub-directories, please see the section on&nbsp; " +
            "<a href=\"#moodle_download_settings\">Moodle Download Settings</a>.<br>&nbsp;<br>" +
            "The individual student directories may contain program files " +
            "(*.cpp, *.h, *.py, etc) zip files (*.zip) or subdirectories.&nbsp; The " +
            "AutoGrader first searches for zip files.&nbsp; If any are found and the " +
            "auto-uncompress option is selected, these are uncompressed into subdirectories " +
            "with the same names as the zip files.&nbsp; The AutoGrader next " +
            "searches for programming files.&nbsp; For each student submission, this " +
            "search begins in the individual submission directory and continues recursively " +
            "through sub-directories until a programming file is found.&nbsp; If a " +
            "programming language is specified, the AutoGrader looks for programming files " +
            "for that language only.&nbsp; If the programming language is set to “Auto” " +
            "(recommended), the AutoGrader searches for any programming files and attempts " +
            "to classify the submission as a Python or C++ program.<br>&nbsp;<br>" +
            "For C++, one (and only one) of the multiple source files " +
            "should contain a main().&nbsp; For Python, the top-level module must be identified " +
            "among the multiple .py files.&nbsp; By default, AutoGrader assumes that " +
            "top-level Python modules are named “main.py”.&nbsp; For this reason, it is " +
            "advisable to instruct students to name their top-level Python modules “main.py” " +
            "when submitting multi-file projects.&nbsp; If multiple Python files are " +
            "found and none are named “main.py”, the AutoGrader will prompt you to " +
            "select which of the multiple files is the top level file.<br>" +
            "<span style=\"font-size: 14pt; color: rgb(0, 112, 192);\"></span><br>The " +
            "AutoGrader UI is organized by a set of numbered buttons at the top of " +
            "the screen.&nbsp; The buttons are labeled “0-Settings”, “1-Input/Setup” " +
            "and “2-Output”.&nbsp; A 4th button labeled “Console” is for process " +
            "tracking and debugging grading mishaps.&nbsp; The numbered buttons " +
            "suggest the order of operations.&nbsp; On startup, you will be on the " +
            "“1 - Input/Setup” screen corresponding to Button 1.&nbsp; You will " +
            "probably need to use Button 0, “Settings”, only once, the first time " +
            "you launch AutoGrader 2 to configure the program.&nbsp; The " +
            "configuration options are described in the “<a href=\"#configuration_options\">Configuration Options</a>” section. <br><br><br>" +
            "<span style=\"font-size: 14pt; color: rgb(0, 112, 192);\">" +
            "<a name=\"configuration_options\"></a><big>“0 - Settings” Screen</big><br>" +
            "</span>The first time you run AutoGrader 2, you will likely want to " +
            "customize the program.&nbsp; Below is a description of the different " +
            "configuration options." +
            "<br><br><span style=\"font-size: 14pt; color: rgb(0, 112, 192);\">Configuration" +
            "Options</span>" +
            "<ul><li><span style=\"font-weight: bold;\">Language</span> - The AutoGrader can grade&nbsp; Python and C++ " +
            "code.&nbsp; You may specify the language for the programs under test or " +
            "you may let the AutoGrader automatically detect the language by " +
            "selecting “Auto”.&nbsp; This&nbsp; is the recommended setting.&nbsp; In " +
            "“Auto” mode, it is possible to have mixed-language submissions, meaning " +
            "that some students may submit their assignment in Python while others " +
            "do so in C++.</li></ul>" +
            "<ul><li><span style=\"font-weight: bold;\">Max Run Time </span>- You may specify the maximum run-time for each " +
            "submission.&nbsp; This is a safeguard against rogue programs that run " +
            "an infinite loop, for example.&nbsp; The AutoGrader will kill any " +
            "program that runs beyond the specified max run time.&nbsp; Setting this " +
            "value to 0 disables the max run time check.&nbsp; This is not " +
            "recommended.</li></ul>" +
            "<ul><li><span style=\"font-weight: bold;\">Limit Output Lines</span> - You may limit the maximum number of output " +
            "lines included in the final report for each program under test.&nbsp;" +
            "This is a safeguard against runaway programs that generate mass output " +
            "in an infinite loop.</li></ul>" +
            "<ul><li><span style=\"font-weight: bold;\">Include Source Listing in Output </span>- Specify whether or not a " +
            "listing of each source program file should be included in the final " +
            "report.</li></ul>" +
            "<ul><li><span style=\"font-weight: bold;\">Auto Uncompress</span> - Specify whether or not the AutoGrader should " +
            "uncompress zip files.&nbsp; When multiple programming files are " +
            "involved, they may be submitted as a compressed zip file. The&nbsp;" +
            "AutoGrader can automatically uncompress these.&nbsp; If unsure, select " +
            "“Yes”.</li></ul>" +
            "<ul><li><span style=\"font-weight: bold;\">Process Recursively</span> - When compressed submissions are " +
            "uncompressed, the program files may be located in a " +
            "sub-directory.&nbsp; The AutoGrader can automatically search these " +
            "subdirectories until a program file is found.&nbsp; If unsure, select " +
            "“Yes”.</li></ul>" +
            "<ul><li><span style=\"font-weight: bold;\">Python 3 Interpreter</span> - " +
            "When first run, the AutoGrader wil attempt " +
            "to automatically detect a suitable python 3 interpreter.&nbsp; If none " +
            "is found, you will have to manually enter the path to the interpreter " +
            "here.&nbsp; Also, if you have multiple Python interpreters installed, " +
            "the default interpreter is randomly selected among the possible options.&nbsp; You may " +
            "change the default interpreter here.<br>" +
            "</li></ul>" +
            "<ul><li><span style=\"font-weight: bold;\">C++ compiler </span>- When " +
            "first run, the AutoGrader will attempt to" +
            "automatically detect a suitable c++ compiler.&nbsp; If none is " +
            "found, you will have to manually enter the path to a compiler " +
            "here.&nbsp; If you do not have a c++ compiler installed and do not " +
            "intend to grade c++ programs, you may leave this field blank.<br>" +
            "</li></ul>" +
            "<ul><li><span style=\"font-weight: bold;\">Shell Interpreter " +
            "</span>- Programs are tested in a “sandbox” shell. &nbsp; By default, the shell /bin/bash is used.&nbsp; You may " +
            "specify a different shell here." +
            "</li></ul><br><br>" +
            "<span style=\"font-size: 14pt; color: rgb(0, 112, 192);\"><big>“1 - Input/Setup” Screen</big><br></span>Under " +
            "normal operations, you will spend your time on the “1 - Input/Setup” " +
            "and “2-Output” screens only.&nbsp; Starting with the “1 - Input/Setup” " +
            "screen, you must specify the TLD (top-level directory) of the " +
            "uncompressed zip file downloaded from Moodle.&nbsp; This is the minimum " +
            "requirement.&nbsp; Most likely, you will want to specify test data " +
            "files and possibly data files.&nbsp; Once these are specified, click " +
            "the “Start” button to begin autograding.&nbsp; Once the grading is " +
            "completed, you will be automatically switched to the “<a \"href=#output_screen\">2 - Output</a>” screen.<br><br>" +
            "<span style=\"font-size: 14pt; color: rgb(0, 112, 192);\">Test Data</span><br>" +
            "For programs that require keyboard input, you must specify the inputs " +
            "in a test data file.&nbsp; This file contains one line for each " +
            "required input.&nbsp; So, if a program requies the user to enter 3 " +
            "integers, your test data file should contain 3 lines, each containing 1 " +
            "integer.<br>" +
            "You may include multiple test cases in a single test data file by " +
            "separating test cases with a double @&nbsp; (“@@”)&nbsp; line.&nbsp;" +
            "Using the example of a program that requires the user to enter 3 " +
            "integers, a test data file with the following contents would test the " +
            "program using two different data sets:<br><br>" +
            "<span style=\"font-style: italic; color: rgb(102, 102, 0);\">" +
            "12<br>" +
            "72<br>" +
            "2<br>" +
            "@@<br>" +
            "103<br>" +
            "-3<br>" +
            "44</span>" +
            "<br><br>Note that in the case above, the program would be executed twice, once for each test case." +
            "<br><br>You may add comments at the end " +
            "of the file beyond the expected keyboard inputs.&nbsp; In our example, " +
            "anything beyond the 3rd integer should be ignored by the program under " +
            "test .&nbsp; However, be mindful that an ill-behaved program could interpret this as " +
            "user input.&nbsp; For a well-behaved program, the following is an " +
            "equivalent test data file:<br><br>" +
            "<span style=\"font-style: italic; color: rgb(102, 102, 0);\">" +
            "12<br>" +
            "72<br>" +
            "2<br>This is a comment.&nbsp; It should have no effect on " +
            "a program that reads only 3 integers." +
            "<br><br>" +
            "@@<br>103<br>" +
            "-3<br>44<br>" +
            "This is another comment." +
            "</span><br><br>" +
            "Note that specifying test data is optional.&nbsp; Some programs do not " +
            "require user input.&nbsp; When test data is required, but not " +
            "specified, the likely outcome is a “max execution time exceeded” error for each " +
            "submission.<br><br>" +
            "<span style=\"font-size: 14pt; color: rgb(0, 112, 192);\">Data Files</span><br>" +
            "Some programs need access to data files.&nbsp; In such cases, the " +
            "data files should be specified here.&nbsp; Each data file will be " +
            "copied to the working directory of each program when the program is " +
            "executed.&nbsp; Note that the AutoGrader assumes that the data files to " +
            "be accessed are in the same directory as the program under test.&nbsp;" +
            "It is important that submitted programs make the same assumption unless " +
            "the submitted program includes its own data files.<br><br><br>" +
            "<span style=\"font-size: 14pt; color: rgb(0, 112, 192);\"><big>" +
            "<a name=\"output_screen\"></a>“2 - Output” Screen</big><br>" +
            "</span>Upon completion of the autograding process, you will be switched " +
            "to the “2 - Output” screen.&nbsp; The main part of the screen will " +
            "display the results of the grading process.&nbsp; You can add a grade " +
            "and a comment to each submission.&nbsp; At the top of the screen, there " +
            "is a navigation bar to help with navigating to a particular student's " +
            "submission.&nbsp; At the bottom of the screen, is a button to save the " +
            "grading results as well as the instructor comments to a file.&nbsp; " +
            "AutoGrader 2 files have a “.ag2” extension.&nbsp; You may also export the " +
            "report to an HTML file.&nbsp; This is recommended as it allows you to " +
            "review the grading using any web browser.&nbsp; You cannot update the " +
            "grade in the exported HTML.&nbsp; A third button switches the main " +
            "window to display a summary of student grades and instructor " +
            "comments.&nbsp; Use this view to help with the transfer of grades back " +
            "to Moodle.<br><br><br>" +

            "<big><span style=\"font-size: 14pt; color: rgb(0, 112, 192);\">" +
            "<a name=\"moodle_download_settings\"></a><big>Moodle Download " +
            "Settings</big></span>" +
            "</big><br>If the downloaded student submissions are not in individual " +
            "folders under the top-level directory, follow the instructions below " +

            "<br><ol><li>Verify that you are using Moodle 3.1 or later</li>" +
            "<li>Go to the assignment and click on “View/grade all submissions”</li>" +
            "<li>Scroll to the very bottom of the page and verify that the “Download " +
            "submissions in folders” option is checked.&nbsp; You will only need to do " +
            "this once.&nbsp;" +
            "Moodle will remember your choice.</li>" +
            "<li>Now, under “Grading action” select “Download all submissions”.</li></ol>" +

            "<br><br><big><span style=\"font-size: 14pt; color: rgb(0, 112, 192);\">" +
            "<a name=\"acknowledgments\"></a><big>Acknowledgments</big></span>" +
            "</big><br>" +

            "<u>AutoGrader 2</u><br>" +
            "Copyright (c) 2016-2018 Jerry Volcy<br>" +
            "Department of Computer Science, Spelman College<br><br>" +

            "<u>SyntaxHighlighter 3.0.83</u><br>" +
            "Copyright (C) 2004-2010 Alex Gorbatchev<br>" +
            "http://alexgorbatchev.com/SyntaxHighlighter<br>" +
            "used under dual MIT and GPL licenses<br><br>" +

            "</div>" +
            "</body></html>";


}



/* ======================================================================
 * To Do
 * Auto version incrementing
 * copy data files to submission folders
 * make a subdirectory in the TLD for extracted test files
 * clean up data files and extracted test files
 * ===================================================================== */


/* ======================================================================
 * xxx
 * ===================================================================== */

//----------  ----------
//----------  ----------
//----------  ----------
//----------  ----------

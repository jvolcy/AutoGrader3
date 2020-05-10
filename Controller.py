package AutoGraderApp;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.concurrent.Worker;
import javafx.event.ActionEvent;
import javafx.event.Event;
import javafx.event.EventHandler;
import javafx.scene.control.*;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.AnchorPane;
import javafx.scene.paint.Paint;
import javafx.scene.web.WebView;
import javafx.stage.DirectoryChooser;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.util.Duration;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;


/* ======================================================================
 * Controller Class
 * This class is the primary store of GUI callback functions.
 * ===================================================================== */
public class Controller implements IAGConstant {
    //---------- FXML GUI control references ----------

    //---------- Misc. Controls ----------
    public TabPane tabMain;
    public AnchorPane anchorPaneMain;
    public Label lblStatus;
    public Label lblMessage;
    public Label lblLanguage;
    private static Label messagePtr;
    public MenuItem menuFileSave;
    public MenuItem menuFileSaveAs;
    public MenuItem menuFileExportHtml;
    public MenuItem menuHelpHelp;
    public MenuItem menuHelpAbout;
    public MenuItem menuFileExportConsoleLog;

    //---------- Config Tab ----------
    public ChoiceBox choiceBoxConfigLanguage;
    public Spinner<Integer> spinnerMaxRunTime;
    public Spinner<Integer> spinnerMaxLines;
    public ChoiceBox choiceBoxConfigIncludeSource;
    public ChoiceBox choiceBoxConfigAutoUncompress;
    public ChoiceBox choiceBoxConfigRecursive;
    public TextField txtPython3Interpreter;
    public TextField txtCppCompiler;
    public TextField txtShell;
    public Button btnSettings;
    public Button btnInputSetup;
    public Button btnOutput;
    public Button btnConsole;
    public Button btnSave;
    public Button btnExportHtml;
    public Button btnGradeSummary;

    //---------- Input/Setup Tab ----------
    public ListView listTestData;
    public Button btnStart;
    public Button btnAdd;
    public Button btnRemove;
    public TextField txtSourceDirectory;

    public ListView listDataFiles;
    public Button btnAddDataFiles;
    public Button btnRemoveDataFiles;

    //---------- Output Tab ----------
    public WebView wvOutput;
    public Button btnPrev;
    public Button btnNext;
    public ChoiceBox cbName;
    //public HBox hBoxWebViewTopButtons;
    //public HBox hBoxWebViewBottomButtons;

    //---------- Console Tab ----------
    public ListView listConsole;
    private static ListView consolePtr;

    //---------- Help Tab ----------
    public WebView wvHelp;

    //---------- Misc members ----------
    private Alert gradingThreadStatusAlert;     //alert box displayed while processing assignments
    private final Double GRADING_TIMELINE_PERIOD = 0.25;        //0.25 second period
    private ReportGenerator reportGenerator;
    private String documentFileName;
    private boolean bShowingSummary;
    private ArrayList<String> primaryPythonFiles;

    /* the bConfigMayHaveChanged is a boolean that is set to true whenever we
    * visit the config tab.  It is used to save the configuration when a tab
    * other than the config tab is selected. */
    private Boolean bConfigMayHaveChanged = false;


    /* ======================================================================
     * initialize()
     * Called automatically upon creation of the GUI
     * ===================================================================== */
    public void initialize() {

        //---------- set the static pointer to the console ----------
        consolePtr = listConsole;
        messagePtr = lblMessage;

        //---------- populate the different choice box configuration options ----------

        //---------- setup "language" config options ----------
        choiceBoxConfigLanguage.getItems().add(LANGUAGE_AUTO);
        choiceBoxConfigLanguage.getItems().add(LANGUAGE_PYTHON3);
        choiceBoxConfigLanguage.getItems().add(LANGUAGE_CPP);

        //---------- setup "include source" config options ----------
        choiceBoxConfigIncludeSource.getItems().add(YES);
        choiceBoxConfigIncludeSource.getItems().add(NO);

        //---------- setup "auto uncompress" config options ----------
        choiceBoxConfigAutoUncompress.getItems().add(YES);
        choiceBoxConfigAutoUncompress.getItems().add(NO);

        //---------- setup "recursive" config options ----------
        choiceBoxConfigRecursive.getItems().add(YES);
        choiceBoxConfigRecursive.getItems().add(NO);


        //---------- update the different configuration fields with the actual user-specified values ----------

        //---------- set the "language" value  ----------
        if (AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.LANGUAGE) != null)
            choiceBoxConfigLanguage.setValue(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.LANGUAGE));
        else
            choiceBoxConfigLanguage.setValue(LANGUAGE_AUTO);

        //add a listener to choiceBoxConfigLanguage to set bConfigMayHaveChanged = true indicating that a configuration has changed
        choiceBoxConfigLanguage.getSelectionModel().selectedItemProperty().addListener(new ChangeListener() {
            @Override
            public void changed(ObservableValue observable, Object oldValue, Object newValue) {
                bConfigMayHaveChanged = true;
                //console("Config may have changed [a]...");
            }
        });

        //---------- set the "max run time" value ----------
        spinnerMaxRunTime.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(0, Integer.MAX_VALUE, 0));
        if (AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.MAX_RUNTIME) != null)
            spinnerMaxRunTime.getValueFactory().setValue(Integer.valueOf(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.MAX_RUNTIME)));

        //add a listener to spinnerMaxRunTime to set bConfigMayHaveChanged = true indicating that a configuration has changed
        spinnerMaxRunTime.valueProperty().addListener(new ChangeListener() {
            @Override
            public void changed(ObservableValue observable, Object oldValue, Object newValue) {
                bConfigMayHaveChanged = true;
                //console("Config may have changed [b]...");
            }
        });

        //---------- set the "max output lines" value ----------
        spinnerMaxLines.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(0, Integer.MAX_VALUE, 0));
        if (AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.MAX_OUTPUT_LINES) != null)
            spinnerMaxLines.getValueFactory().setValue(Integer.valueOf(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.MAX_OUTPUT_LINES)));

        //add a listener to spinnerMaxLines to set bConfigMayHaveChanged = true indicating that a configuration has changed
        spinnerMaxLines.valueProperty().addListener(new ChangeListener() {
            @Override
            public void changed(ObservableValue observable, Object oldValue, Object newValue) {
                bConfigMayHaveChanged = true;
                //console("Config may have changed [c]...");
            }
        });

        //---------- set the "include source" value ----------
        if (AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.INCLUDE_SOURCE) != null)
            choiceBoxConfigIncludeSource.setValue(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.INCLUDE_SOURCE));
        else
            choiceBoxConfigIncludeSource.setValue(YES);

        //add a listener to choiceBoxConfigIncludeSource to set bConfigMayHaveChanged = true indicating that a configuration has changed
        choiceBoxConfigIncludeSource.getSelectionModel().selectedItemProperty().addListener(new ChangeListener() {
            @Override
            public void changed(ObservableValue observable, Object oldValue, Object newValue) {
                bConfigMayHaveChanged = true;
                //console("Config may have changed [d]...");
            }
        });

        //---------- set the "auto uncompress" value ----------
        if (AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.AUTO_UNCOMPRESS) != null)
            choiceBoxConfigAutoUncompress.setValue(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.AUTO_UNCOMPRESS));
        else
            choiceBoxConfigAutoUncompress.setValue(YES);

        //add a listener to choiceBoxConfigAutoUncompress to set bConfigMayHaveChanged = true indicating that a configuration has changed
        choiceBoxConfigAutoUncompress.getSelectionModel().selectedItemProperty().addListener(new ChangeListener() {
            @Override
            public void changed(ObservableValue observable, Object oldValue, Object newValue) {
                bConfigMayHaveChanged = true;
                //console("Config may have changed [e]...");
            }
        });

        //---------- set the "recursive process" value ----------
        if (AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.PROCESS_RECURSIVELY) != null)
            choiceBoxConfigRecursive.setValue(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.PROCESS_RECURSIVELY));
        else
            choiceBoxConfigRecursive.setValue(YES);

        //add a listener to choiceBoxConfigRecursive to set bConfigMayHaveChanged = true indicating that a configuration has changed
        choiceBoxConfigRecursive.getSelectionModel().selectedItemProperty().addListener(new ChangeListener() {
            @Override
            public void changed(ObservableValue observable, Object oldValue, Object newValue) {
                bConfigMayHaveChanged = true;
                //console("Config may have changed [f]...");
            }
        });


        //---------- set the python3 interpreter path value ----------
        if (AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.PYTHON3_INTERPRETER) != null)
            txtPython3Interpreter.setText(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.PYTHON3_INTERPRETER));
        else
            txtPython3Interpreter.setText("");

        //add a listener to txtPython3Interpreter to set bConfigMayHaveChanged = true indicating that a configuration has changed
        txtPython3Interpreter.textProperty().addListener(new ChangeListener<String>() {
            @Override
            public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
                bConfigMayHaveChanged = true;
                //console("Config may have changed [g]...");
            }
        });

        //---------- set the c++ compiler path value ----------
        if (AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.CPP_COMPILER) != null)
            txtCppCompiler.setText(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.CPP_COMPILER));
        else
            txtCppCompiler.setText("");

        //add a listener to txtCppCompiler to set bConfigMayHaveChanged = true indicating that a configuration has changed
        txtCppCompiler.textProperty().addListener(new ChangeListener<String>() {
            @Override
            public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
                //console("Config may have changed [h]...");
                bConfigMayHaveChanged = true;
            }
        });

        //---------- set the shell interpreter path value ----------
        if (AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.SHELL) != null)
            txtShell.setText(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.SHELL));
        else
            txtShell.setText("");

        //add a listener to txtShell to set bConfigMayHaveChanged = true indicating that a configuration has changed
        txtShell.textProperty().addListener(new ChangeListener<String>() {
            @Override
            public void changed(ObservableValue<? extends String> observable, String oldValue, String newValue) {
                bConfigMayHaveChanged = true;
                //console("Config may have changed [i]...");
            }
        });

        //---------- configure the "Test Data" and "Data Files" list view to allow multiple selections ----------
        listTestData.getSelectionModel().setSelectionMode(SelectionMode.MULTIPLE);
        listDataFiles.getSelectionModel().setSelectionMode(SelectionMode.MULTIPLE);
        //listTestData.getItems().add("/Users/jvolcy/work/Spelman/Projects/data/data.txt");  //TEMP******\n");
        //listTestData.getItems().add("/Users/jvolcy/work/Spelman/Projects/data/data2.txt");  //TEMP******\n");

        //set the main tab to the input/setup tab by invoking the btnInputSetupClick callback.
        //then, set the bConfigMayHaveChanged flag.
        bConfigMayHaveChanged = false;
        btnInputSetupClick();

        //disable the Output button
        btnOutput.setDisable(true);

        //---------- Initialize Misc. controls ----------
        lblLanguage.setText(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.LANGUAGE));

        lblMessage.setText("AutoGrader " + AutoGraderApp.version);

        //---------- Initialize web view button visibility ----------
        //hBoxWebViewTopButtons.setVisible(true);
        //hBoxWebViewBottomButtons.setVisible(true);

        //point the web engine to the html help text
        wvHelp.getEngine().loadContent(AutoGraderApp.HelpHtml);
        //wvHelp.getEngine().load("http://www.google.com");

        //************* TEMP **************
        //txtSourceDirectory.setText("/Users/jvolcy/Downloads/201709-94470-Homework 7b, P0502 - Number Pyramid, due 1021 (will count as Lab 5)-259033");
        //*********************************
        setStartButtonStatus();

        menuFileSave.setDisable(true);      //enable after successful processing
        menuFileExportHtml.setDisable(true);
        menuFileExportConsoleLog.setDisable(true);  //enable only on console tab
        setDocumentFileName(null);
        bShowingSummary = false;

        cbName.getSelectionModel().selectedItemProperty().addListener(new ChangeListener() {
            @Override
            public void changed(ObservableValue observable, Object oldValue, Object newValue) {
                cbNameClick();
            }
        });

        //---------- Configure the grading thread monitoring thread ----------
        gradingThreadMonitor.setCycleCount(Timeline.INDEFINITE);

        //---------- Configure the grading thread status alert pop-up dialog ----------
        gradingThreadStatusAlert = new Alert(Alert.AlertType.INFORMATION);
        gradingThreadStatusAlert.setTitle("Auto Grader");
        //gradingThreadStatusAlert.setHeaderText("Processing...");
        gradingThreadStatusAlert.setContentText("Click Cancel to abort.");
        gradingThreadStatusAlert.getButtonTypes().setAll(ButtonType.CANCEL);


        //---------- Configure the main WebView Listener ----------
        /* Whenever the html report is displayed in the wvOutput Web View, we have to
         * update the grade and summary fields on the HTML page.  This is done by
         * invoking the xferAGDocumentToWebView function.
         * xferAGDocumentToWebView() necessarily makes reference to the different controls on the
         * HTML page.  This function will fail if the page is not yet loaded.  Because the
         * loading is done in a separate thread, we use a listener to check for a change in
         * the page's LoadWorker status before calling xferAGDocumentToWebView(). */
        wvOutput.getEngine().getLoadWorker().stateProperty().addListener((obs, oldState, newState) -> {
            if (newState == Worker.State.SUCCEEDED) {
                // new page has loaded, call AGDocumentToWebView
                xferAGDocumentToWebView();
            }
        });

    }


    /* ======================================================================
     * configChanged()
     * function called whenever the configuration tab is selected or
     * unselected
     * The boolean bConfigMayHaveChanged is set to true whenever one of the
     * configuration parameters (combo boxes, text fields, etc.) on the
     * configuration tab is changed.  This is accomplished using change
     * listeners on each of the input controls on the configuration tab.
     * ===================================================================== */
    public void configChanged() {

        if (bConfigMayHaveChanged) {
            try {
                AutoGraderApp.autoGrader.setConfiguration(AG_CONFIG.LANGUAGE, choiceBoxConfigLanguage.getSelectionModel().getSelectedItem().toString());
                AutoGraderApp.autoGrader.setConfiguration(AG_CONFIG.MAX_RUNTIME, spinnerMaxRunTime.getValue().toString());
                AutoGraderApp.autoGrader.setConfiguration(AG_CONFIG.MAX_OUTPUT_LINES, spinnerMaxLines.getValue().toString());
                AutoGraderApp.autoGrader.setConfiguration(AG_CONFIG.INCLUDE_SOURCE, choiceBoxConfigIncludeSource.getSelectionModel().getSelectedItem().toString());
                AutoGraderApp.autoGrader.setConfiguration(AG_CONFIG.AUTO_UNCOMPRESS, choiceBoxConfigAutoUncompress.getSelectionModel().getSelectedItem().toString());
                AutoGraderApp.autoGrader.setConfiguration(AG_CONFIG.PROCESS_RECURSIVELY, choiceBoxConfigRecursive.getSelectionModel().getSelectedItem().toString());
                AutoGraderApp.autoGrader.setConfiguration(AG_CONFIG.PYTHON3_INTERPRETER, txtPython3Interpreter.getText());
                AutoGraderApp.autoGrader.setConfiguration(AG_CONFIG.CPP_COMPILER, txtCppCompiler.getText());
                AutoGraderApp.autoGrader.setConfiguration(AG_CONFIG.SHELL, txtShell.getText());

                lblLanguage.setText(AutoGraderApp.autoGrader.getConfiguration(AG_CONFIG.LANGUAGE));
                bConfigMayHaveChanged = false;
                AutoGraderApp.autoGrader.saveConfiguration();
            } catch (Exception e) {
                console("configChanged(): " + e.toString());
            }
        }
    }


    /* ======================================================================
     * console()
     * function that attempts to write the supplied formatted object
     * to the console tab.  If the console tab is not yet initialized,
     * the function outputs to stdout.
     * ===================================================================== */
    public static void console(String format, Object... arguments) {
        String formattedOutput = String.format(format, arguments);

        //if the GUI is not yet up, the consolePtr hasn't been set yet:
        //dump the output to the screen.
        try {
            consolePtr.getItems().add(formattedOutput);
            System.out.println("[c]" + formattedOutput);
        } catch (Exception e) {
            System.out.println("[x]" + formattedOutput);
        }
    }


    /* ======================================================================
     * message()
     * function that attempts to update the message lable at the bottom
     * middle of the screen.  If the lblMessage object is not yet
     * initialized, then the function outputs to stdout.
     * ===================================================================== */
    public static void message(String msg) {

        //if the GUI is not yet up, the messagePtr hasn't been set yet:
        //dump the output to the screen.
        try {
            messagePtr.setText(msg);
        } catch (Exception e) {
            console("[m]" + msg);
        }
    }


    /* ======================================================================
     * cbNameClick()
     * ===================================================================== */
    public void cbNameClick() {
        try {
            wvOutput.getEngine().executeScript("document.getElementById(\""
                    + cbName.getSelectionModel().getSelectedItem().toString()
                    + "\").scrollIntoView();");
        } catch (Exception e) {
            //trap any calls made before the wvOutput engine is assigned a document
            console(">>>" + e.toString());
        }
    }


    /* ======================================================================
     * btnPrevClick()
     * The "Prev" and "Next" buttons are on the Output tab.  These are
     * navigation buttons to move back and forth through the list of
     * graded assignments.  These buttons work in conjunction with the
     * student name drop-down list.
     * ===================================================================== */
    public void btnPrevClick() {
        cbName.getSelectionModel().selectPrevious();
    }

    /* ======================================================================
     * btnNextClick()
     * The "Prev" and "Next" buttons are on the Output tab.  These are
     * navigation buttons to move back and forth through the list of
     * graded assignments.  These buttons work in conjunction with the
     * student name drop-down list.
     * ===================================================================== */
    public void btnNextClick() {
        cbName.getSelectionModel().selectNext();
    }

    /* ======================================================================
     * menuFileOpen()
     * Callback for File->Open
     * ===================================================================== */
    public void menuFileOpen() {
        //get the app's stage
        Stage stage = (Stage) anchorPaneMain.getScene().getWindow();

        //use a select file dialog box

        //create a file chooser
        FileChooser fileChooser = new FileChooser();


        // create an extension filter
        FileChooser.ExtensionFilter extFilter =
                new FileChooser.ExtensionFilter("AutoGrader 2 file (*.ag2)", "*.ag2");
        fileChooser.getExtensionFilters().add(extFilter);

        fileChooser.setTitle("Open Assignment");
        File f = fileChooser.showOpenDialog(stage);

        //if the user cancels, do nothing
        if (f == null) return;

        //set the moodle directory to whatever the directory of the opened file is
        AutoGraderApp.autoGrader.getAgDocument().moodleDirectory = f.getParentFile();

        // Deserialization
        try {
            AutoGraderApp.autoGrader.deSerializeFromDisk(f.getAbsolutePath());
        }
        catch (Exception e) {
            //here, we won't change the current document name
            return;
        }

        //put us on the report output page, not the summary page
        if (bShowingSummary)
            btnGradeSummaryClick();

        //---------- Initialize the student name choice box ----------
        // This ChoiceBox appears on the output tab and contains student names.
        // Along with the "Prev" and "Next" buttons, t is used to navigate
        // the output HTML.
        populateStudentNameChoiceBox();

        doPostGradingProcessing();
        /* set the document filename *after* doPostGradingProcessing().  The "Save As"
        option will only be enabled if "Save" is first enabled.  That happens inside
        of doPostGradingProcessing. */
        setDocumentFileName(f.getAbsolutePath());
   }


    /* ======================================================================
     * menuFileSave()
     * Callback for File->Save
     * ===================================================================== */
    public void menuFileSave() {
        //get the app's stage
        Stage stage = (Stage) anchorPaneMain.getScene().getWindow();
        message("Saving...");

        if (getDocumentFileName() == null) {
            FileChooser fileChooser = new FileChooser();

            // create an extension filter
            FileChooser.ExtensionFilter extFilter =
                    new FileChooser.ExtensionFilter("AutoGrader 2 file (*.ag2)", "*.ag2");
            fileChooser.getExtensionFilters().add(extFilter);

            String baseDirectory = AutoGraderApp.autoGrader.getAgDocument().moodleDirectory.getParent();
            fileChooser.setInitialDirectory(new File(baseDirectory));
            fileChooser.setInitialFileName(AutoGraderApp.autoGrader.getAgDocument().moodleDirectory.getName());
            //String baseFileName = new File(documentFileName).getName();
            //baseFileName = baseFileName.substring(0, baseFileName.lastIndexOf('.'));
            //fileChooser.setInitialFileName(baseFileName);

            fileChooser.setTitle("Save Assignment");
            File f = fileChooser.showSaveDialog(stage);

            //if the user cancels, do nothing
            if (f == null) {
                message("Save Canceled.");
                return;
            }

            setDocumentFileName(f.getAbsolutePath());
        }

        //update the grading engine's assignment with the entries from the web view.
        xferWebViewToAGDocument();

        try {
            console("Writing " + documentFileName + " ...");
            AutoGraderApp.autoGrader.serializeToDisk(getDocumentFileName());
            message("Report Saved.");

        } catch (Exception e) {
            console("menuFileSave(): " + e.toString());
            message("Save Failed.");
            //the serialization process failed.  Invalidate the filename
            setDocumentFileName(null);
        }

    }


    /* ======================================================================
     * menuFileSave()
     * Callback for File->Save
     * ===================================================================== */
    public void menuFileSaveAs() {
        if (getDocumentFileName() == null) {
            /* this should never happen: the "Save As" menu option should not be enabled
            * if the document has no name. */
            console("Assertion error: documentFileName == null in call to menuFileSaveAs.");
        }

        //save the current document file name
        String oldDocumentFileName = getDocumentFileName();

        /* set the current document name to null.  This will force the fileChooser
         * dialog to open in menuFileSave(). */
        setDocumentFileName(null);
        menuFileSave();

        if (getDocumentFileName() == null) {
            /* if the user cancels the fileChooser in the call to menuFileSave,
            the document name will still be null.  In that case, re-assign the
            previous document name. */
            setDocumentFileName(oldDocumentFileName);
        }
    }


    /* ======================================================================
     * menuFileExportHtml()
     * Callback for File->Export HTML
     * ===================================================================== */
    public void menuFileExportHtml() {
        //get the app's stage
        Stage stage = (Stage) anchorPaneMain.getScene().getWindow();
        message("Export HTML...");

        FileChooser fileChooser = new FileChooser();

        // create an extension filter
        FileChooser.ExtensionFilter extFilter =
                new FileChooser.ExtensionFilter("AutoGrader 2 file (*.htm, html)", "*.html", "*.htm");
        fileChooser.getExtensionFilters().add(extFilter);

        String baseDirectory = AutoGraderApp.autoGrader.getAgDocument().moodleDirectory.getParent();
        fileChooser.setInitialDirectory(new File(baseDirectory));
        fileChooser.setInitialFileName(AutoGraderApp.autoGrader.getAgDocument().moodleDirectory.getName());

        /*
        fileChooser.setInitialDirectory(new File(documentFileName).getParentFile());
        String baseFileName = new File(documentFileName).getName();
        baseFileName = baseFileName.substring(0, baseFileName.lastIndexOf('.'));
        fileChooser.setInitialFileName(baseFileName);
        */

        fileChooser.setTitle("Export HTML");
        File f = fileChooser.showSaveDialog(stage);

        //if the user cancels, do nothing
        if (f == null) {
            message("Export HTML Canceled.");
            return;
        }

        //update the grading engine's assignment with the entries from the web view.
        xferWebViewToAGDocument();

        String annotatedReport = ReportGenerator.generateAnnotatedReport(AutoGraderApp.autoGrader.getAgDocument());

        try (BufferedWriter bw = new BufferedWriter(new FileWriter(f))) {
            bw.write(annotatedReport);
            bw.close();
            console("Writing file %s.", f.getAbsolutePath());
        } catch (IOException e) {
            console("menuFileExportHtml(): " + e.toString());
        }

        message("HTML Exported.");
    }


    /* ======================================================================
     * menuFileExportConsoleLog()
     * Callback for File->Export Console Log
     * ===================================================================== */
    public void menuFileExportConsoleLog()
    {
        //get the app's stage
        Stage stage = (Stage) anchorPaneMain.getScene().getWindow();
        message("Export Console Log...");

        FileChooser fileChooser = new FileChooser();

        // create an extension filter
        FileChooser.ExtensionFilter extFilter =
                new FileChooser.ExtensionFilter("Console log (*.log)", "*.log");
        fileChooser.getExtensionFilters().add(extFilter);

        String baseDirectory = System.getProperty("user.home") + "/Desktop";
        fileChooser.setInitialDirectory(new File(baseDirectory));
        fileChooser.setInitialFileName("ag2-console-" + java.time.LocalDate.now());


        fileChooser.setTitle("Export Console Log");
        File f = fileChooser.showSaveDialog(stage);

        //if the user cancels, do nothing
        if (f == null) {
            message("Export Console Log Canceled.");
            return;
        }

        //write all entries from the console to the file
        console("Exporting console log...");
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(f))) {
            console("Writing file %s.", f.getAbsolutePath());
            for (Object li :  listConsole.getItems()) {
                bw.write(li.toString() + "\n");
            }
            //bw.close();
        }
        catch (IOException e) {
            console("menuFileExportConsoleLog(): " + e.toString());
            message("Console Log Export Failed.");
        }

        message("Console Log Export Completed.");
    }


    /* ======================================================================
     * menuFileQuit()
     * Callback for File->Quit
     * ===================================================================== */
    public void menuFileQuit() {
        console("Good bye\n");

        /* get and close the app's stage.  This will quit the GUI and return
        control to AutoGraderApp.main(). */
        Stage stage = (Stage) anchorPaneMain.getScene().getWindow();
        stage.close();
    }


    /* ======================================================================
     * menuHelpAbout()
     * ===================================================================== */
    public void menuHelpAbout() {
        //----------  ----------
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle(AutoGraderApp.appName);
        alert.setHeaderText(AutoGraderApp.appName);
        alert.setContentText("Version " + AutoGraderApp.version + "\n" + AutoGraderApp.copyrightText);
        alert.showAndWait();
    }


    /* ======================================================================
     * menuSettingsConfig()
     * Callback for Settings->Config
     * This function sets the main tab to the CONFIGURATION_TAB.
     * ===================================================================== */
    public void menuSettingsConfig() {
        btnSettingsClick();
    }


    /* ======================================================================
     * menuHelpHelp()
     * ===================================================================== */
    public void menuHelpHelp() {
        btnSettings.setTextFill(Paint.valueOf("black"));
        btnInputSetup.setTextFill(Paint.valueOf("black"));
        btnOutput.setTextFill(Paint.valueOf("black"));
        btnConsole.setTextFill(Paint.valueOf("black"));
        tabMain.getSelectionModel().select(IAGConstant.HELP_TAB);
        menuFileExportConsoleLog.setDisable(true);  //enable only when on the console tab

        //----------  ----------
    }


    /* ======================================================================
     * btnSettingsClick()
     * Callback for Settings button.
     * This function sets the main tab to the CONFIGURATION_TAB.
     * ===================================================================== */
    public void btnSettingsClick() {
        tabMain.getSelectionModel().select(CONFIGURATION_TAB);
        btnSettings.setTextFill(Paint.valueOf("blue"));
        btnInputSetup.setTextFill(Paint.valueOf("black"));
        btnOutput.setTextFill(Paint.valueOf("black"));
        btnConsole.setTextFill(Paint.valueOf("black"));
        menuFileExportConsoleLog.setDisable(true);  //enable only when on the console tab
    }


    /* ======================================================================
     * btnInputSetupClick()
     * Callback for the Input/Setup button.
     * This function sets the main tab to the SETUP_INPUT_TAB.
     * ===================================================================== */
    public void btnInputSetupClick() {
        tabMain.getSelectionModel().select(SETUP_INPUT_TAB);
        btnSettings.setTextFill(Paint.valueOf("black"));
        btnInputSetup.setTextFill(Paint.valueOf("blue"));
        btnOutput.setTextFill(Paint.valueOf("black"));
        btnConsole.setTextFill(Paint.valueOf("black"));
        menuFileExportConsoleLog.setDisable(true);  //enable only when on the console tab
    }


    /* ======================================================================
     * btnOutputClick()
     * Callback for the Output button.
     * This function sets the main tab to the OUTPUT_TAB.
     * ===================================================================== */
    public void btnOutputClick() {
        //hBoxWebViewTopButtons.setVisible(true);
        //hBoxWebViewBottomButtons.setVisible(true);

        tabMain.getSelectionModel().select(OUTPUT_TAB);
        btnSettings.setTextFill(Paint.valueOf("black"));
        btnInputSetup.setTextFill(Paint.valueOf("black"));
        btnOutput.setTextFill(Paint.valueOf("blue"));
        btnConsole.setTextFill(Paint.valueOf("black"));
        menuFileExportConsoleLog.setDisable(true);  //enable only when on the console tab
    }


    /* ======================================================================
     * btnConsoleClick()
     * ===================================================================== */
    public void btnConsoleClick(){
        tabMain.getSelectionModel().select(CONSOLE_TAB);
        btnSettings.setTextFill(Paint.valueOf("black"));
        btnInputSetup.setTextFill(Paint.valueOf("black"));
        btnOutput.setTextFill(Paint.valueOf("black"));
        btnConsole.setTextFill(Paint.valueOf("blue"));
        menuFileExportConsoleLog.setDisable(false);  //enable only when on the console tab
    }


    /* ======================================================================
     * btnTestDataRemoveClick()
     * Callback for "Remove" button associated with the Test Data list view.
     * Clicking this button is equivalent to pressing the delete or
     * backspace key to remove selected test data files from the list.
     * ===================================================================== */
    public void btnTestDataRemoveClick() {
        /* Because we can't safely iterate through a list while we are deleting
         * items from it, we create a copy of the selected items in the list,
         * then we iterate through this non-changing list.  Note that it is
         * not possible to carry out this process using indexes instead of
         * the contents of the list because, again, the indexes would change
         * as we modify the list. */
        Object[] selectedItems = listTestData.getSelectionModel().getSelectedItems().toArray();

        //go through the list of selected items and delete each one
        for (Object selectedItem : selectedItems) {
            listTestData.getItems().remove(selectedItem);
        }

    }


    /* ======================================================================
     * btnDataFilesRemoveClick()
     * Callback for "Remove" button associated with the Data Files list view.
     * Clicking this button is equivalent to pressing the delete or
     * backspace key to remove selected data files from the list.
     * ===================================================================== */
    public void btnDataFilesRemoveClick() {
        /* Because we can't safely iterate through a list while we are deleting
         * items from it, we create a copy of the selected items in the list,
         * then we iterate through this non-changing list.  Note that it is
         * not possible to carry out this process using indexes instead of
         * the contents of the list because, again, the indexes would change
         * as we modify the list. */
        Object[] selectedItems = listDataFiles.getSelectionModel().getSelectedItems().toArray();

        //go through the list of selected items and delete each one
        for (Object selectedItem : selectedItems) {
            listDataFiles.getItems().remove(selectedItem);
        }

    }


    /* ======================================================================
     * listTestDataKeyPressed()
     * Callback for the test data list that is invoked when a key is
     * pressed.  We check for the 'delete' and 'backspace' keys and use
     * these to invoke the function that deletes selected items from the
     * list view.
     * ===================================================================== */
    public void listTestDataKeyPressed(KeyEvent e) {
        /* Check if the user pressed either delete or backspace.  If so, delete
         * all selected list entries. */
        if (e.getCode() == KeyCode.BACK_SPACE || e.getCode() == KeyCode.DELETE) {
            btnTestDataRemoveClick();
        }
    }


    /* ======================================================================
     * setStartButtonStatus()
     * This function enables and disables the "Start" button based on the
     * status of the "No Test Data" checkbox and the test data list view.
     * The button is enabled only if at least one test data file is
     * specified or the "No Test Data" checkbox is checked.  Otherwise,
     * the "Start" button should be disabled.  Call this function on
     * startup, after the checkbox's status changes and after items have
     * been removed form the list view.
     * Also, we set the background color of the list view to light red
     * or light green to indicate a missing input.
     * ===================================================================== */
    private void setStartButtonStatus() {
        //enable the start button only if the source directory is valid
        try {
            File f = new File(txtSourceDirectory.getText());
            btnStart.setDisable(!(f.isDirectory()));
        }
        catch (Exception e){
            btnStart.setDisable(true);
        }
    }


    /* ======================================================================
     * setDocumentFileName()
     * setting documentFileName to null tells us that the document has not
     * been saved (has not been named).  This will also determine the
     * enable/disable status of the "Save As" menu option.
     * Use the set/get documentFileName functions instead of directly
     * accessing the documentFileName member variable.  This allows us to
     * keep track of the enable/disable status of the "File->Save" and
     * "File-Save As" menu options.
     * ===================================================================== */
    private void setDocumentFileName(String fileName) {
        documentFileName = fileName;

        //Now, add the document file name to the App's title:

        try {
            //get the app's stage
            Stage stage = (Stage) anchorPaneMain.getScene().getWindow();

            if (documentFileName == null) {
                stage.setTitle(AutoGraderApp.appName);
            }
            else {
                stage.setTitle(AutoGraderApp.appName + " - " + documentFileName);
            }
        }
        catch (Exception e) { console("setDocumentFileName( <%s> ): No stage.", AutoGraderApp.appName+":"+fileName); }

        //enable/disable the "save" and "save as" menu options as appropriate
        if (menuFileSave.isDisable()) {
            // can't have a "Save as" without a "Save"
            menuFileSaveAs.setDisable(true);
            return;
        }

        if (documentFileName == null) {
            menuFileSaveAs.setDisable(true);
        }
        else {
            menuFileSaveAs.setDisable(false);
        }
    }


    /* ======================================================================
     * getDocumentFileName()
     * returns the document file name.
     * Use the set/get documentFileName functions instead of directly
     * accessing the documentFileName member variable.  This allows us to
     * keep track of the enable/disable status of the "File->Save" and
     * "File-Save As" menu options.
     * ===================================================================== */
    private String getDocumentFileName() { return documentFileName; }


    /* ======================================================================
     * btnAddClick()
     * Callback for the "Add" button on the Input/Setup tab.  The add button
     * is used to add test files to the test data list.
     * ===================================================================== */
    public void btnAddClick() {
        //get the app's stage
        Stage stage = (Stage) anchorPaneMain.getScene().getWindow();

        //open the file chooser dialog box
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Open Test Data File");
        List<File> files = fileChooser.showOpenMultipleDialog(stage);

        if (files == null) return;
        //save the selected file objects in the test data list view
        for (File file : files) {
            listTestData.getItems().add(file);
        }

    }


    /* ======================================================================
     * btnAddDataFilesClick()
     * Callback for the second "Add" button on the Input/Setup tab.  This
     * add button is used to add data files to the data files list.
     * ===================================================================== */
    public void btnAddDataFilesClick() {
        //get the app's stage
        Stage stage = (Stage) anchorPaneMain.getScene().getWindow();

        //open the file chooser dialog box
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Add Data Files");
        List<File> files = fileChooser.showOpenMultipleDialog(stage);

        if (files == null) return;
        //save the selected file objects in the test data list view
        for (File file : files) {
            listDataFiles.getItems().add(file);
        }

    }


    /* ======================================================================
     * btnSourceDirectoryClick()
     * Callback for "Source Director" button on Input/Setup Tab.
     * ===================================================================== */
    public void btnSourceDirectoryClick() {
        //get the app's stage
        Stage stage = (Stage) anchorPaneMain.getScene().getWindow();

        //open the file chooser dialog box
        DirectoryChooser directoryChooser = new DirectoryChooser();
        directoryChooser.setTitle("Open Assignments Directory");
        File directory = directoryChooser.showDialog(stage);
        txtSourceDirectory.setText(directory.getAbsolutePath());

        setStartButtonStatus();
    }

    /* ======================================================================
     * txtSourceDirectoryOnKeyReleased()
     * function called whenever the txtSourceDirectory text box is
     * edited.  Use this to change the status of the start button.
     * ===================================================================== */
    public void txtSourceDirectoryOnKeyReleased() {
        setStartButtonStatus();
    }

    /* ======================================================================
     * btnSaveClick()
     * ===================================================================== */
    public void btnSaveClick() {
        menuFileSave();
    }


    /* ======================================================================
     * btnExportHtmlClick()
     * ===================================================================== */
    public void btnExportHtmlClick() {
        menuFileExportHtml();
    }


    /* ======================================================================
     * btnGradeSummaryClick()
     * ===================================================================== */
    public void btnGradeSummaryClick() {

        if (bShowingSummary) {
            //we are on the summary page: switch to the report page
            /* we need to explicitly populate the grades and
             * comment fields in the report.  Any changes to the
             * report in the form of a grade or instructor comment
             * is stored in the assignments array list, not in the
             * displayed report.  It must be re-generated before
             * it is displayed again.*/

            //generate the report
            doPostGradingProcessing();

            btnGradeSummary.setText("View Summary");
            bShowingSummary = false;
        }
        else {
            //we are on the report page: switch to the summary page.
            /* transitioning from the report page to the summary page first requires
             * that any edits to the grade and comment input controls be updated in the
             * document.  The summary report must then be re-generated. */

            //update the grading engine's assignment with the entries from the web view.
            xferWebViewToAGDocument();

            //generate the summary report
            reportGenerator.generateSummary();
            wvOutput.getEngine().loadContent(reportGenerator.getSummary());
            btnGradeSummary.setText("View Report");
            bShowingSummary = true;
        }

        /* whether switching from report to summary or vice-versa, we need
         * update the scroll position on the display based on the student
         * name choice box. This function will fail if the page is not yet loaded.
         * Because the loading is done in a separate thread, we use a listener
         * to check for a change in the page's LoadWorker status before
         * calling cbNameClick(). */
        wvOutput.getEngine().getLoadWorker().stateProperty().addListener((obs, oldState, newState) -> {
            if (newState == Worker.State.SUCCEEDED) {
                // new page has loaded, call AGDocumentToWebView
                cbNameClick();
            }
        });
    }


    /* ======================================================================
     * tabMainOnKeyPressed()
     * Callback for KeyPressed event on the main tab.  We capture and
     * consume this event to eliminate keyboard navigation through the
     * tap pages.  Only the Settings/Input/Output buttons should be used
     * to navigate through he pages.
     * ===================================================================== */
    public void tabMainOnKeyPressed(Event e) {
        /* consume key press events so that they do not go on to effect
        navigation controls on the main tab. */
        e.consume();
    }


    /* ======================================================================
     * selectMainPythonFile()
     * This function creates a dialog box that permits the user to
     * select the top-level python script when multiple python files are
     * detected.  The function then populates the primaryAssignmentFile
     * member of the Assignment object accordingly.  It also allows the
     * user to store her choice for use with future submissions.
     * ===================================================================== */
    // Set the button types.
    private void selectMainPythonFile(Assignment assignment) {

        /*First, check to see if any of the files match a name on the
        * primaryPythonFiles name list.  If it does, use it and quit.*/
        for (File f : assignment.assignmentFiles) {     //go through every file in the assignment
            //compare the select filename with each filename in assignment
            if (primaryPythonFiles.contains(f.getName())){
                //if we have a match, we are done: store it in
                // primaryAssignment?File and quit the loop
                assignment.primaryAssignmentFile = f;
                console("Primary file is" + f.getAbsolutePath());
                return;
            }
        }


        /* create a list of choices that will hold the names of the multiple
        * python files. */
        List<String> choices = new ArrayList<>();;

        // add the names of each file to the list
        for (File f : assignment.assignmentFiles) {
            choices.add(f.getName());
        }

        /* Create a standard ChoiceDialog object.  We will customize this
        * dialog box by replacing its two 'Ok' and 'Cancel' buttons with
        * custom buttons. */
        ChoiceDialog<String> dialog = new ChoiceDialog<>(choices.get(0), choices);

        /* Setup the different messaging texts for the dialog box. */
        dialog.setTitle(assignment.studentName);
        dialog.setHeaderText("More than one python source was found with "
                + assignment.studentName
                + "'s submission.\nPlease select the name of the top level python file from the list below.\n"
                + "Select [Cancel] to skip this submission (not graded).");
        dialog.setContentText("Primary source:");

        /* The dialog box will offer the user 3 options when multiple python files are
        * are found.  First, the user may simply ignore the problem, in which case the
        * submission is not graded.  Second, the user can select among the different
        * files which is the primary.  Third, the user can select the primary and specify
        * that the file identified as primary will be the same for future submissions.
        * Here, we create 3 custom buttons corresponding to these 3 choices. */
        ButtonType UseSelected = new ButtonType("Applies For This Submission Only", ButtonBar.ButtonData.OK_DONE);
        ButtonType UseForAllButtonType = new ButtonType("Applies For All Submissions", ButtonBar.ButtonData.OK_DONE);
        ButtonType SkipSubmission = new ButtonType("Do Not Grade This Submission", ButtonBar.ButtonData.OK_DONE);

        //remove ok and cancel buttons
        dialog.getDialogPane().getButtonTypes().removeAll(ButtonType.OK); //remove OK button
        dialog.getDialogPane().getButtonTypes().removeAll(ButtonType.CANCEL); //remove Cancel button

        //add our 3 custom buttons
        dialog.getDialogPane().getButtonTypes().add(SkipSubmission);
        dialog.getDialogPane().getButtonTypes().add(UseSelected );
        dialog.getDialogPane().getButtonTypes().add(UseForAllButtonType );

        /* Rather than returning the selected item from the choice list, we want to
        * return the button the user selected. */
        dialog.setResultConverter(dialogButton -> {
            if (dialogButton == UseSelected) {
                //user selected "use selected file only for current submission"
                return "UseSelected";
            }

            if (dialogButton == UseForAllButtonType) {
                //user selected "use for all future submission"
                return "UseForAllButtonType";
            }

            //user opted to not grade the assignment
            return "SkipSubmission";
        });

        /* present the dialog box and wait for the user's choice
        * which will be a String assigned to result. */
        String result = dialog.showAndWait().get();

        /* We have to consider all 3 possible outcomes: User canceled,
        * user selected "for this assignment only" or user selected
        * "use for all assignments". */
        if (result.equals("SkipSubmission")) {
            //user opted to skip the assignment.  Indicate that there
            //is no primary assignment file for this submission.
            //The submission cannot be graded.
            assignment.primaryAssignmentFile = null;
            console("Skipping submission for " + assignment.studentName + ".");
        }
        else {
            /* Here, the user did NOT opt to skip the assignment.  Either
            * the primary python file was selected for the current submission
            * for for the current and all future submissions.
            * The drop-down list box on the choice dialog contains only
            * the file name of the python files, not the full path name.
            * We need to assign the full path name to the primaryAssignmentFile
            * member of 'assignment'.  We search every filename for a match,
            * then store the corresponding full pathname. */
            for (File f : assignment.assignmentFiles) {     //go through every file in the assignment
                //compare the select filename with each filename in assignment
                if (dialog.getSelectedItem().equals(f.getName())) {
                    //if we have a match, we are done: store it in
                    // primaryAssignment?File and quit the loop
                    assignment.primaryAssignmentFile = f;
                    console("Primary file is" + f.getAbsolutePath());
                    break;
                }
            }

            //now check if we should add this choice to the pythonTopLevelFilename list
            if (result.equals("UseForAllButtonType")) {
                //user has elected to apply to all: add the selection to the
                //primaryPythonFiles name list
                primaryPythonFiles.add(dialog.getSelectedItem());
                console("Apply to all!");
            }
        }

    }


    /* ======================================================================
     * populateStudentNameChoiceBox()
     * populates the cbName choice box on the output tab using the
     * student names from the grading engine assignments array list.
     * ===================================================================== */
    public void populateStudentNameChoiceBox() {

        try {
            GradingEngine gradingEngine = AutoGraderApp.autoGrader.getAgDocument().gradingEngine;

            //---------- Initialize the student name choice box ----------
            // This ChoiceBox appears on the output tab and contains student names.
            // Along with the "Prev" and "Next" buttons, t is used to navigate
            // the output HTML.

            //clear all current entries
            cbName.getItems().clear();

            for (Assignment assignment : gradingEngine.assignments) {
                //populate the names ChoiceBox with the student names
                cbName.getItems().add(assignment.studentName);
            }

            //select the first name on the student name list by default
            cbName.getSelectionModel().selectFirst();
        }
        catch (Exception e) {
            console("populateStudentNameChoiceBox(): " + e.toString());
        }
    }


    /* ======================================================================
     * readFromFile()
     * reads the entire content of the specified file and returns it as a
     * string.
     * ===================================================================== */
    private String readFromFile(String filepath) {
        try {
            String text = new String(Files.readAllBytes(Paths.get(filepath)), StandardCharsets.UTF_8);
            return text;
        } catch (Exception e) {
            console("readFromFile(): " + e.toString());
        }
        return null;
    }


    /* ======================================================================
     * writeToFile()
     * destructively writes a string to specified file
     * ===================================================================== */
    private void writeToFile(String fileName, String data) {
        // writing string to file
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(fileName))) {
            bw.write(data);
            //bw.close();
        } catch (IOException e) {
            console("writeToFile(): " + e.toString());
        }

    }


    /* ======================================================================
     * fileNameFromPathName()
     * extracts the filename given the absolute path
     * ===================================================================== */
    private String fileNameFromPathName(String pathName) {
        //extract the filename from the path name
        File f = new File(pathName);
        return f.getName();
    }


    /* ======================================================================
     * breakOutTestFiles()
     * function that returns the list of test files in the listTestData
     * list box.  If any of the files contain multiple test cases, these
     * are separated into as many test cases in the supplied output
     * directory.  Multiple test cases within a single file are separated
     * by a TEST_CASE_SEPARATOR string.
     * ===================================================================== */
    private ArrayList<File> breakOutTestFiles(File outputDirectory) {

        ArrayList<File> testFiles = new ArrayList<>();

        //go through every file in the listTestData list box
        for (Object s : listTestData.getItems()) {
            String filename = s.toString();

            //read the content of the test file
            String content = readFromFile(filename);

            //search for test case separators
            String [] subCases = content.split(IAGConstant.TEST_CASE_SEPARATOR);

            //if none are found, the length of subCases array will be 1.
            //In that case, add the test files from the 'ListTestData' to the testFiles list
            if (subCases.length == 1) {
                testFiles.add(new File(filename));
            }
            else {
                //create temporary files in the output directory for each sub-case
                for (int counter=1; counter <= subCases.length; counter++) {
                    String testDataFileName = outputDirectory.getAbsolutePath() + "/" + fileNameFromPathName(filename) + "-" + counter;
                    writeToFile(testDataFileName, subCases[counter-1]);
                    testFiles.add(new File(testDataFileName));
                    console("creating sub-test case file " + testDataFileName);
                }
            }
        }
        return testFiles;
    }


    /* ======================================================================
     * btnStart()
     * Callback for 'Start' button on Input/Setup tab
     * ===================================================================== */
    public void btnStart() {

        //---------- create aliases ----------
        // Create aliases for the autoGrader and gradingEngine members of
        // AutoGraderApp.  These are used extensively below.
        AutoGrader2 autoGrader = AutoGraderApp.autoGrader;
        GradingEngine gradingEngine = autoGrader.getAgDocument().gradingEngine;

        //---------- null the documentFileName ----------
        /* setting documentFileName to null tells us that the document has not
        * been saved (has not been named).  This will also determine the
        * enable/disable status of the "Save As" menu option. */
        setDocumentFileName(null);

        //---------- Reset the primaryPythonFile list to the default value ----------
        primaryPythonFiles = new ArrayList<>();
        primaryPythonFiles.add(IAGConstant.DEFAULT_MAIN_PYTHON_FILE);   //"main.py"

        //---------- Invoke the Moodle file pre-processor ----------
        message("Pre-processing Moodle files...");

        // The pre-processor extracts assignment files and student names
        // from the downloaded and uncompressed Moodle submissions download.
        autoGrader.getAgDocument().moodleDirectory = new File (txtSourceDirectory.getText());
        MoodlePreprocessor mpp = new MoodlePreprocessor(autoGrader.getAgDocument().moodleDirectory.getAbsolutePath(),
                autoGrader.getConfiguration(AG_CONFIG.LANGUAGE),
                autoGrader.getConfiguration(AG_CONFIG.AUTO_UNCOMPRESS).equals(YES));

        //---------- handle multiple Python files ----------
        /* for Python files, if there are more than 1 source files, the user must
        * identify the primary file.  The function selectMainPythonFile()
        * removes all python source files apart from the user-specified
        * primary file. */
        for (Assignment assignment : mpp.getAssignments()) {
            //python only: we need to check for the # of programming files found
            //only 1 can be the primary
            if (assignment.language == IAGConstant.LANGUAGE_PYTHON3) {
                if (assignment.assignmentFiles.size() > 1) {
                    selectMainPythonFile(assignment);
                } else if (assignment.assignmentFiles.size() == 1) {
                    //make the lone assignment file the primary
                    assignment.primaryAssignmentFile = assignment.assignmentFiles.get(0);
                } else {
                    /* Getting here implies that no programming files were found. */
                    console("*** Assertion failure: No programming files were found.  The" +
                            "Moodle pre-preprocessor should not be in the Assignments list. ***");
                }
            }
        }
        //---------- Xfer Assignments to the Grading Engine ----------
        /* The Moodle pre-preocessor creates the Assignments files
         * array.  It also populates the student name and possibly
         * other details of each assignment.  This array list
         * becomes the assignment list for the grading engine. */
        gradingEngine.assignments = mpp.getAssignments();

        //---------- Configure the Grading Engine ----------
        gradingEngine.setCppCompiler(autoGrader.getConfiguration(AG_CONFIG.CPP_COMPILER));
        gradingEngine.setPython3Interpreter(autoGrader.getConfiguration(AG_CONFIG.PYTHON3_INTERPRETER));
        gradingEngine.setShellInterpreter(autoGrader.getConfiguration(AG_CONFIG.SHELL));
        gradingEngine.setTempOutputDirectory(autoGrader.getAgDocument().moodleDirectory.getAbsolutePath());
        gradingEngine.setMaxOutputLines(Integer.valueOf(autoGrader.getConfiguration(AG_CONFIG.MAX_OUTPUT_LINES)));
        gradingEngine.setMaxRunTime(Integer.valueOf(autoGrader.getConfiguration(AG_CONFIG.MAX_RUNTIME)));

        //---------- generate break out test files ----------
        //first make a directory named ag_data in the moodle directory
        File testDataDirectory = new File( autoGrader.getAgDocument().moodleDirectory.getAbsolutePath() + "/.ag_data");
        testDataDirectory.mkdir();

        //now put the break out test files in the ag_data directory
        autoGrader.getAgDocument().testDataFiles = breakOutTestFiles(testDataDirectory);
        gradingEngine.testDataFiles = autoGrader.getAgDocument().testDataFiles;

        //---------- copy all data files into each submission directory ----------
        //go through every data file in the listDataFiles list box
        for (Object s : listDataFiles.getItems()) {
            String src = s.toString();

            //copy each data file to each of the assignment directories
            for (Assignment assignment : gradingEngine.assignments) {
                String dst = assignment.assignmentDirectory + "/" + (new File(src)).getName();
                try {
                    console("copying \"" + src + "\" to \"" + dst + "\"");
                    Files.copy((new File(src)).toPath(), (new File(dst)).toPath());
                }
                catch (Exception e){
                    console(e.toString());
                }
            }
        }

        //---------- indicate the current hmtlReport is invalid ----------
        //put us on the report output page, not the summary page
        if (bShowingSummary)
            btnGradeSummaryClick();

        AutoGraderApp.autoGrader.getAgDocument().htmlReport = null;

        //disable the 'Start' button
        btnStart.setDisable(true);


        //---------- invoke the grader ----------
        message("Processing assignments...");
        lblStatus.setText("Working...");

        gradingEngine.processAssignments();

        //---------- start the grading thread monitor ----------
        /* this is a periodic function that runs in the context of
        * the UI thread.  It's main purpose is to update the message
        * label as the processing progresses. The function also
        * closes out any cleanup that needs to occur
        * post-processing. */
        gradingThreadMonitor.play();

        //---------- Display the grading status alert ----------
        gradingThreadStatusAlert.setHeaderText("Processing " + gradingEngine.getProcessingStatus().progress + " assignments.");
        gradingThreadStatusAlert.showAndWait();

        //---------- Check for usr abort ----------
        /* If we are here, then the status alert has closed.  This
        would be the result of either the user closing it, or the
        grading timeline closing it programmatically.  Check to see
        if the grading process is still running.  If it is, the
        user clicked 'Cancel' and we should abort the grading process. */
        if (gradingEngine.getProcessingStatus().bRunning) {
            System.out.println("Aborting...");
            lblStatus.setText("Aborting...");
            message("Cancelling...");
            gradingEngine.abortGrading();
        }

        //reset the status (enabled/disabled) of the start button
        setStartButtonStatus();

        //---------- post-processing ----------

        /* post-processing of the auto-grading operation will be completed.
         * in the function doPostGradingProcessing().  This function
         * is called as the final operation of the gradingThreadMonitor
         * Timeline. */
    }


    /* ======================================================================
     * doPostGradingProcessing()
     * This function is called after the grading engine has completed its
     * work.  The function's primary goal is to invoke the report generator
     * and display its output.
     * ===================================================================== */
    private void doPostGradingProcessing() {

        //enable the Output button
        btnOutput.setDisable(false);

        //enable save button
        menuFileSave.setDisable(false);
        menuFileExportHtml.setDisable(false);

        /* if we are loading from file, getHtmlReport will return a non-null
        * value.  If we are processing new data, we will need to generate
        * a report.  getHmtlReport() will be null.*/
        if (AutoGraderApp.autoGrader.getAgDocument().htmlReport == null) {
            reportGenerator = new ReportGenerator("AutoGrader 2.0",         //title
                    AutoGraderApp.autoGrader.getAgDocument().moodleDirectory.getAbsolutePath(),       //header text
                    AutoGraderApp.autoGrader.getAgDocument().gradingEngine.assignments,   //assignments
                    AutoGraderApp.autoGrader.getAgDocument().testDataFiles);    //test data

            //we are processing new data so we need to generate a new report
            reportGenerator.generateReport();
            AutoGraderApp.autoGrader.getAgDocument().htmlReport = reportGenerator.getDocument();

            //point the web engine to the generated html report
            wvOutput.getEngine().loadContent(AutoGraderApp.autoGrader.getAgDocument().htmlReport);
        }
        else {
            reportGenerator = new ReportGenerator("AutoGrader 2.0",         //title
                    "",       //header text
                    AutoGraderApp.autoGrader.getAgDocument().gradingEngine.assignments,   //assignments
                    AutoGraderApp.autoGrader.getAgDocument().testDataFiles);    //test data

            //Here, we are uploading an existing report.  We do not call reportGenerator.generateReport()
            //Doing so would likely cause an error as file references are likely invalid.AutoGraderApp.autoGrader.getAgDocument().htmlReport = reportGenerator.getDocument();

            //point the web engine to the generated html report.  This will invoke the wvOutput
            //stateProperty listener which will cause the grade and summary fields of the
            //html report to be populated with the data in the AGDocument.
            wvOutput.getEngine().loadContent(AutoGraderApp.autoGrader.getAgDocument().htmlReport);

        }


        //switch to the output tab
        btnOutputClick();


        //dump the assignments to the console  ************ TEMP **************
        //AutoGraderApp.autoGrader.getAgDocument().gradingEngine.dumpAssignments();

    }


    /* ======================================================================
     * xferGradesFromWebViewToAssignmentObject()
     * retrieves the instructor-entered grades and comments for the
     * given assignment and transfers them to the Assignment object.
     * ===================================================================== */
    private void xferGradesFromWebViewToAssignmentObject(Assignment assignment) {

        //if we are on the summary page, the grades have already been transferred
        //from the web view page to the assignment object.  In that case, do nothing.
        if (bShowingSummary) return;

        String gradeId = assignment.studentName + ReportGenerator.HTML_GRADE_ID_SUFFIX;
        String commentId = assignment.studentName + ReportGenerator.HTML_COMMENT_ID_SUFFIX;

        //set the grade
        try {
            Object oGrade = wvOutput.getEngine().executeScript("document.getElementById(\"" + gradeId + "\").value");
            assignment.grade = Integer.valueOf(oGrade.toString());
        }
        catch (Exception e) {
            //if the id is not found or the conversion from str->int fails, set the grade to null
            //console(assignment.studentName + " [xfer w2a]: " + e.toString());
            assignment.grade = null;
        }

        //set the comment
        try {
            Object oComment = wvOutput.getEngine().executeScript("document.getElementById(\"" + commentId + "\").value");
            assignment.instructorComment = oComment.toString();
        }
        catch (Exception e) {
            //if the id is not found, set the comment to null
            assignment.instructorComment = null;
        }
    }


    /* ======================================================================
     * xferWebViewToAGDocument()
     * function that updates the grading engine's assignment with the
     * entries from the web view.
     *
     * ===================================================================== */
    private void xferWebViewToAGDocument() {
        for (Assignment assignment : AutoGraderApp.autoGrader.getAgDocument().gradingEngine.assignments) {
            xferGradesFromWebViewToAssignmentObject(assignment);
        }
    }


    /* ======================================================================
     * xferGradesFromAssignmentObjectToWebView()
     * transfers the grade and comment fields of the supplied assignment
     * to the corresponding fields in the web view.
     * ===================================================================== */
    private void xferGradesFromAssignmentObjectToWebView(Assignment assignment) {
        //if we are on the summary page, the grades were transferred
        //from the web view page to the assignment object.  In that case, do nothing.
        if (bShowingSummary) return;

        String gradeId = assignment.studentName + ReportGenerator.HTML_GRADE_ID_SUFFIX;
        String commentId = assignment.studentName + ReportGenerator.HTML_COMMENT_ID_SUFFIX;

        //set the grade and comment on the web view
        //v 2.0.5 - separate the xfer of grades and comments.  This way, comments will xfer even if
        //no grade is entered.  Previously, the try-catch would throw an exception if the grade was
        //missing, never having the opportunity to xfer the comment.
        try {
            wvOutput.getEngine().executeScript("document.getElementById(\"" + gradeId + "\").value =\"" + assignment.grade.toString()+"\"");
        } catch (Exception e) {
            //comment this out (too verbose in console)
            //console(assignment.studentName + " [xfer a2w]: No grade found.");
        }


        try {
            //for v 2.0.4, we replace newlines with "\n" for display on the web view.  This fixes the bug of
            //the instructor comment disappearing when switching between the report and summary.
            String s = assignment.instructorComment.replace("\n", "\\n");
            wvOutput.getEngine().executeScript("document.getElementById(\"" + commentId + "\").value = \"" + s +"\"");
        } catch (Exception e) {
            //comment this out (too verbose in console)
            //console(assignment.studentName + " [xfer a2w]: No Instructor Comment found.");
        }
    }


    /* ======================================================================
     * xferAGDocumentToWebView()
     * transfers all grades and comments from the AG Document
     * to the corresponding fields in the web view.
     * The serialized html report is the base html output from the the
     * report generator.  It does not contain grades and comments which are
     * entered by the instructor after the report is generated.  The grades
     * and comments are ultimately stored in the Assignments array list.
     * Upon de-serializing the AG document from disk, the base html document
     * must be populated with the grades and comments from the AGDocument.
     * This is the work done by the AGDocumentToWebView function.
     * ===================================================================== */
    private void xferAGDocumentToWebView() {

        //update the grading engine's assignment with the entries from the web view.
        for (Assignment assignment : AutoGraderApp.autoGrader.getAgDocument().gradingEngine.assignments) {
            xferGradesFromAssignmentObjectToWebView(assignment);
        }
    }


    /* ======================================================================
     * gradingThreadMonitor
     * This timeline is essentially a periodic function that executes with
     * a period of 0.25 sec.  The function has multiple purposes and is
     * intended to run only while the grading operation is in process.  The
     * function begins with a call to gradingThreadMonitor.start() in the
     * btnStart() handler.  It monitors the ProcessingStatus structure
     * updated by the grading engine while processing assignments.  The
     * timer auto-terminates when the processing reports to be complete.
     * That is, when ProcessingStatus.bRunning is false.  The function
     * performs a few post-processing tasks like enabling the output
     * button and switching to the output tab.
     * ===================================================================== */
    private Timeline gradingThreadMonitor = new Timeline(new KeyFrame(Duration.seconds(GRADING_TIMELINE_PERIOD), new EventHandler<ActionEvent>() {

        @Override
        public void handle(ActionEvent event) {
            //create a ProcessingStatus object to monitor the status of the grading processor
            ProcessingStatus ps = AutoGraderApp.autoGrader.getAgDocument().gradingEngine.getProcessingStatus();

            /* we will keep running so long as the grading engine is still
            * processing. This is indicated by the bRunning member of the
            * ProcessingStatus object being "true". */
            if (ps.bRunning) {
                //update the lblMessage text
                message("Processing submission for " + ps.message + "...");
                /* calculate the % complete and update the pop-up alert initiated
                * by btnClick. */
                gradingThreadStatusAlert.setHeaderText("Processing submissions..." +
                        100*(ps.progress-ps.startVal)/(ps.endVal-ps.startVal) + "%.\n[" +
                ps.message + "]");

                lblStatus.setText("Working..." + 100*(ps.progress-ps.startVal)/(ps.endVal-ps.startVal) + "%");

                /* our work is done for this invocation.  The timeline will
                * execute again in 0.25 seconds. */
                return;
            }
            else {
                /* If we are here, ps.bRunning is false, meaning that the
                * the grading engine is done.  We will self-terminate
                * the current timeline, close the status alert dialog,
                * and do other post-processing things. */
                gradingThreadMonitor.stop();        //end the current timeline
                gradingThreadStatusAlert.close();   //close the alert dialog

                message("Processing Done.");    //update the lblMessage
                lblStatus.setText("Ready.");

                //re-enable the 'Start' button
                btnStart.setDisable(false);

                //---------- To Do : clean up break out test files ----------
                //get the name of the temporary test data directory
                File testDataDirectory = new File( AutoGraderApp.autoGrader.getAgDocument().moodleDirectory.getAbsolutePath() + "/.ag_data");
                //first, remove all files in the test data directory

                // Get all files in directory
                File[] files = testDataDirectory.listFiles();
                for (File file : files) {
                    // Delete each file
                    console("deleting \"" + file + "\"");
                    if (!file.delete()) {
                        // report files we couldn't delete
                        console("Failed to delete test data file \"" + file + "\"");
                    }
                }
                //now, remove the testDataDirectory
                console ("removing temp test data directory \"" + testDataDirectory.getName() + "\"");
                testDataDirectory.delete();

                //---------- clean up data files ----------
                //go through every data file in the listDataFiles list box
                for (Object s : listDataFiles.getItems()) {
                    String src = s.toString();

                    //delete each data file to each of the assignment directories
                    for (Assignment assignment : AutoGraderApp.autoGrader.getAgDocument().gradingEngine.assignments) {
                        String dst = assignment.assignmentDirectory + "/" + (new File(src)).getName();
                        try {
                            console("deleting \"" + dst + "\"");
                            if (! ((new File(dst)).delete()) ) {
                                // report files we couldn't delete
                                console("Failed to delete test data file \"" + dst + "\"");
                            }
                        }
                        catch (Exception e){
                            console(e.toString());
                        }
                    }
                }

                //---------- Initialize the student name choice box ----------
                // This ChoiceBox appears on the output tab and contains student names.
                // Along with the "Prev" and "Next" buttons, t is used to navigate
                // the output HTML.
                populateStudentNameChoiceBox();

                //call the post-processing function
                doPostGradingProcessing();

                //dump the assignments to the console
                AutoGraderApp.autoGrader.getAgDocument().gradingEngine.dumpAssignments();

            }
        }
    }));


}



/* ======================================================================
 * xxx
 * ===================================================================== */

//----------  ----------
//----------  ----------
//----------  ----------
//----------  ----------

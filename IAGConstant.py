
# =======================================================================
# Interface of AG2 constants.
# ======================================================================
class IAGConstant(object):

    # ---------- UI Constants ----------
    MIN_STAGE_WIDTH = 600
    MIN_STAGE_HEIGHT = 440

    CONFIGURATION_TAB = 0
    SETUP_INPUT_TAB = 1
    OUTPUT_TAB = 2
    CONSOLE_TAB = 3
    HELP_TAB = 4

    YES = "Yes"
    NO = "No"

    LANGUAGE_AUTO = "Auto"
    LANGUAGE_PYTHON3 = "Python 3"
    LANGUAGE_CPP = "C++"
    LANGUAGE_UNKNOWN = "Unknown"

    PYTHON_EXTENSIONS = ["py"]
    CPP_COMPILER_EXTENSIONS = ["cpp", "c", "cc"]
    CPP_EXTENSIONS = ["cpp", "c", "cc", "h", "hpp"]
    PYTHON_AND_CPP_EXTENSIONS = ["py", "cpp", "c", "cc", "h", "hpp"]
    COMPRESSION_EXTENSIONS = ["zip"]

    # ---------- AG Options Dictionary Keys ----------
    class AG_CONFIG(object):
        LANGUAGE = "LANGUAGE"
        MAX_RUNTIME = "MAX_RUNTIME"
        MAX_OUTPUT_LINES = "MAX_OUTPUT_LINES"
        INCLUDE_SOURCE = "INCLUDE_SOURCE"
        AUTO_UNCOMPRESS = "AUTO_UNCOMPRESS"
        PROCESS_RECURSIVELY = "PROCESS_RECURSIVELY"
        PYTHON3_INTERPRETER = "PYTHON3_INTERPRETER"
        CPP_COMPILER = "CPP_COMPILER"
        SHELL = "SHELL"

    # ---------- AG Directives ----------
    NAME_DIRECTIVE  =   "@@Name"
    MAIN_DIRECTIVE =    "@@Main"
    TITLE_DIRECTIVE =   "@@Title"
    DATE_DIRECTIVE =    "@@Date"
    DATA_DIRECTIVE =    "@@Data"

    # ---------- Misc Constants ----------
    TEST_CASE_SEPARATOR = "@@\n"
    CONFIG_FILENAME = ".ag3Config.json"
    DEFAULT_MAIN_PYTHON_FILE = "main.py"




# =======================================================================
# xxx
# ======================================================================

# ----------  ----------
# ----------  ----------
# ----------  ----------
# ----------  ----------

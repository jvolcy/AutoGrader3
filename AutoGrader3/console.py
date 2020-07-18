import sys

def console(format, *args):
    Console.console(format, *args)

class Console:
    # __consoleFunc is a private pointer to a user specified function.
    # This function must accept a string argument.  The call to console()
    # redirects to this function if it is set.  Otherwise,
    # console() outputs to the screen.
    __consoleFunc = None

    @classmethod
    def console(cls, strToPrint):
        print('[c] ' + strToPrint)
        sys.stdout.flush()
        if cls.__consoleFunc is not None:
            cls.__consoleFunc(strToPrint)

    @classmethod
    def setConsole(cls, targetFunc):
        cls.__consoleFunc = targetFunc

    @classmethod
    def unSetConsole(cls):
        cls.__consoleFunc = None

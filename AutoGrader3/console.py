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
    def console(cls, fmt, *args):
        if cls.__consoleFunc == None:
            #print('fmt=', fmt, 'args=', *args)
            print('[x] ' + str(fmt) % args)
            sys.stdout.flush()
        else:
            cls.__consoleFunc('[c] ' + fmt % args)

    @classmethod
    def setConsole(cls, targetFunc):
        cls.__consoleFunc = targetFunc

    @classmethod
    def unSetConsole(cls):
        cls.__consoleFunc = None

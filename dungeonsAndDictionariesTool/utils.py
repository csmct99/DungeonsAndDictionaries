
def debug(message, debugLevel=0):
    if debugLevel == DebugLevel.NORMAL:
        print("[*]    " + str(message))
    elif debugLevel == DebugLevel.WARNING:
        print("[!]    " + str(message))
    elif debugLevel == DebugLevel.ERROR:
        print("[!!!]  " + str(message))
    elif debugLevel == DebugLevel.INFO:
        print("[-]    " + str(message))


# Setup debug enum for normal, verbose, and debug
class DebugLevel:
    NORMAL = 0
    WARNING = 1
    ERROR = 2
    INFO = 3
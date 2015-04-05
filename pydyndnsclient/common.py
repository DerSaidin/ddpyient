
enable_debug = False

def DebugEnable():
    global enable_debug
    enable_debug = True
    Debug(None, "Debug output enabled")

def DebugDisable():
    global enable_debug
    Debug(None, "Debug output disabled")
    enable_debug = False

# Debugging
def Debug(fqdn, msg):
    global enable_debug
    if enable_debug:
        if fqdn is None:
            print("Debug:   %s" % (msg))
        else:
            print("Debug:   (%s) %s" % (fqdn, msg))

# Information display
def Info(fqdn, msg):
    if fqdn is None:
        print("Note:    %s" % (msg))
    else:
        print("Note:    (%s) %s" % (fqdn, msg))

# Action taken
def Action(fqdn, msg):
    if fqdn is None:
        print("Action:  %s" % (msg))
    else:
        print("Action:  (%s) %s" % (fqdn, msg))

# Warnings
def Warning(fqdn, msg):
    if fqdn is None:
        print("Warning: %s" % (msg))
    else:
        print("Warning: (%s) %s" % (fqdn, msg))

# Errors
def Error(fqdn, msg):
    if fqdn is None:
        print("Error:   %s" % (msg))
    else:
        print("Error:   (%s) %s" % (fqdn, msg))


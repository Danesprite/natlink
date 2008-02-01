#
# Python Macro Language for Dragon NaturallySpeaking
#   (c) Copyright 1999 by Joel Gould
#   Portions (c) Copyright 1999 by Dragon Systems, Inc.
#
"""natlinkcorefunctions.py

 Quintijn Hoogenboom, January 2008:

These functions are used by natlinkstatus.py,
and can also used by all the modules,
as the core folder will be in the python path
when natlink is running.

The first function is also, hopefully identical, in
natlinkconfigfunctions, in the configurenatlinkvocolaunimacro folder

getBaseFolder: returns the folder from the calling module
getCoreDir: returns the core folder of natlink, relative to the configure directory
fatalError: raises error again, if new_raise is set, otherwise continues executing
getExtendedEnv(env): gets from os.environ, or from window system calls (CSIDL_...) the
                     environment. Take PERSONAL for HOME and ~
getAllFolderEnvironmentVariables: get a dict of all possible HOME and CSIDL variables,
           that result in a valid folder path
substituteEnvVariableAtStart: substitute back into a file/folder path an environment variable



""" 
import os, sys

def getBaseFolder(globalsDict=None):
    """get the folder of the calling module.

    either sys.argv[0] (when run direct) or
    __file__, which can be empty. In that case take the working directory
    """
    globalsDictHere = globalsDict or globals()
    baseFolder = ""
    if globalsDictHere['__name__']  == "__main__":
        baseFolder = os.path.split(sys.argv[0])[0]
        print 'baseFolder from argv: %s'% baseFolder
    elif globalsDictHere['__file__']:
        baseFolder = os.path.split(globalsDictHere['__file__'])[0]
        print 'baseFolder from __file__: %s'% baseFolder
    if not baseFolder:
        baseFolder = os.getcwd()
        print 'baseFolder was empty, take wd: %s'% baseFolder
    return baseFolder

# report function:
def fatal_error(message, new_raise=None):
    """prints a fatal error when running this module"""
    print 'natlinkconfigfunctions fails because of fatal error:'
    print message
    print
    print 'This can (hopefully) be solved by (re)installing natlink'
    print 
    if new_raise:
        raise new_raise
    else:
        raise

# helper function:
def getFromRegdict(regdict, key, fatal=None):
    """get a key from the regdict, which was collected earlier.

    if fails, do fatal error is fatal is set,
    if fatal is not set, only print warning.

    """
    value = None
    try:
        value = regnl[key]
    except KeyError:
        mess = 'cannot find key %s in registry dictionary'% key
        if fatal:
            fatal_error(mess, new_raise = Exception)
        else:
            print mess
            return ''
    else:
        return value

# keep track of found env variables, fill, if you wish, with
# getAllFolderEnvironmentVariables.
# substitute back with substituteEnvVariableAtStart.
recentEnv = {}

def getExtendedEnv(var):
    """get from environ or windows CSLID

    HOME is environ['HOME'] or CSLID_PERSONAL
    ~ is HOME

    """
    global recentEnv
    
    var = var.strip()
    var = var.strip("%")
    
    if var == "~":
        var = 'HOME'

    if var in recentEnv:
        return recentEnv[var]

    if var in os.environ:
        recentEnv[var] = os.environ[var]
        return recentEnv[var]

    # try to get from CSIDL system call:
    if var == 'HOME':
        var2 = 'PERSONAL'
    else:
        var2 = var
        
    try:
        CSIDL_variable =  'CSIDL_%s'% var2
        shellnumber = getattr(shellcon,CSIDL_variable, -1)
    except:
        raise ValueError('getExtendedEnv, cannot find in environ or CSIDL: "%s"'% var2)
    if shellnumber < 0:
        raise ValueError('getExtendedEnv, cannot find in environ or CSIDL: "%s"'% var2)
    try:
        result = shell.SHGetFolderPath (0, shellnumber, 0, 0)
    except:
        raise ValueError('getExtendedEnv, cannot find in environ or CSIDL: "%s"'% var2)

    result = str(result)
    result = os.path.normpath(result)
    recentEnv[var] = result
    return result

def getAllFolderEnvironmentVariables():
    """get all the environ AND all CSLID variables that result into a folder

    also put them in recentEnv    

    """
    global recentEnv
    D = {}

    for k in dir(shellcon):
        if k.startswith("CSIDL_"):
            kStripped = k[6:]
            try:
                v = getExtendedEnv(kStripped)
            except ValueError:
                continue
            if len(v) > 2 and os.path.isdir(v):
                D[kStripped] = v
            elif v == '.':
                D[kStripped] = os.getcwd()
    # os.environ overrules CSIDL:
    for k in os.environ:
        v = os.environ[k]
        if os.path.isdir(v):
            v = os.path.normpath(v)
            if k in D and D[k] != v:
                print 'warning, CSIDL also exists for key: %s, take os.environ value: %s'% (k, v)
            D[k] = v
            recentEnv[k] = v
    return D

def substituteEnvVariableAtStart(filepath): 
    """try to substitute back one of the (preused) environment variables back

    into the start of a filename

    if ~ (HOME) is D:\My documents,
    the path "D:\My documents\folder\file.txt" should return "~\folder\file.txt"

    

    """
    Keys = recentEnv.keys()
    # sort, longest result first, shortest keyname second:
    decorated = [(-len(recentEnv[k]), len(k), k) for k in Keys]
    decorated.sort()
    Keys = [k for (dummy1,dummy2, k) in decorated]
    for k in Keys:
        val = recentEnv[k]
        if filepath.lower().startswith(val.lower()):
            if k in ("HOME", "PERSONAL"):
                k = "~"
            else:
                k = "%" + k + "%"
            return k + filepath[len(val):]
    return filepath
       

if __name__ == "__main__":
    print 'this module is in folder: %s'% getBaseFolder(globals())
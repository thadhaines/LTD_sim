"""File to handle import of PSLF libraries
   and Creation of global PSLF object
   Replaces imports at begining of Model and init_PSLF function inside Model

   TODO: before implementation, all Model.pslf references must be corrected.
"""
import builtins

#ensure locations list exits
from __main__ import *

# load .NET dll
import clr # Common Language Runtime
clr.AddReference(locations['fullMiddlewareFilePath'])
import GE.Pslf.Middleware as mid
import GE.Pslf.Middleware.Collections as col 

builtins.mid = mid
builtins.col = col

# create pslf instance / object
global PSFL 
builtins.PSLF = mid.Pslf(locations['pslfPath'])   
# load .sav file
load_test = builtins.PSLF.LoadCase(locations['savPath'])     

if load_test == 0:
    print(locations['savPath'] + " Successfully loaded.")
else:
    print("Failure to load .sav")
    print("Error code: %d" % load_test)
    raise SystemExit(0)
    
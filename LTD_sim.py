"""Developement file that acts as main"""
"""VS may require default ironpython environment (no bit declaration)"""

import os
import __builtin__

# workaround for interactive mode runs (Use only if required)
print(os.getcwd())
os.chdir(r"C:\Users\heyth\source\repos\thadhaines\LTD_sim")
#os.chdir(r"D:\Users\jhaines\Source\Repos\thadhaines\LTD_sim")
#print(os.getcwd())

from parseDyd import *
from distPe import *
from combinedSwing import *
from findFunctions import *
from PerturbanceAgents import *

execfile('mergeDicts.py')

# Simulation Parameters
timeStep = 1.0
endTime = 20.0
slackTol = 5.0
Hsys = 0.0 # MW*sec of entire system, if !> 0.0, will be calculated in code
Dsys = 0.0 # PU; TODO: Incoroporate into simulation (probably)

# Required Paths
## full path to middleware dll
fullMiddlewareFilePath = r"C:\Program Files (x86)\GE PSLF\PslfMiddleware"  
## path to folder containing PSLF license
pslfPath = r"C:\Program Files (x86)\GE PSLF"  

# fast debug case switching
test_case = 0
if test_case == 0:
    savPath = r"C:\LTD\pslf_systems\eele554\ee554.sav"
    dydPath = r"C:\LTD\pslf_systems\eele554\ee554.dyd"
elif test_case == 1:
    savPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microBusData.sav"
    dydPath = r"C:\LTD\pslf_systems\MicroWECC_PSLF\microDynamicsData_LTD.dyd"
elif test_case == 2:
    savPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\dmini-v3c1_RJ7_working.sav"
    dydPath = r"C:\LTD\pslf_systems\MiniPSLF_PST\miniWECC_LTD.dyd"
elif test_case == 3:
    # Will no longer run due to parser errors
    savPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.sav"
    dydPath = r"C:\LTD\pslf_systems\fullWecc\fullWecc.dyd"

locations = (
    fullMiddlewareFilePath,
    pslfPath,
    savPath,
    dydPath,
    )
del fullMiddlewareFilePath, pslfPath, savPath, dydPath

simParams = (
    timeStep,
    endTime,
    slackTol,
    Hsys,
    Dsys,
    )
del timeStep, endTime, slackTol, Hsys, Dsys

# these files will change after refactor
execfile('initPSLF.py')

# imports must occur after intiPSLF.py
from CoreAgents import AreaAgent, BusAgent, GeneratorAgent, SlackAgent, LoadAgent
from Model import Model

execfile('makeGlobals.py')

# mirror arguments: locations, simParams, debug flag
mir = Model(locations, simParams, 0)

# Pertrubances configured for test case (eele)
mir.addPert('Load',[3,'2'],'Step',['St',2,1]) # step on 
mir.addPert('Load',[3,'2'],'Step',['St',12,0]) # step off 

mir.runSim()

print("Log and Step check of Load, Pacc, and sys f:")
print("Time\tSt\tPacc\tsys f\tdelta f\t\tSlackPe\tGen2Pe")
for x in range(mir.c_dp):
    print("%d\t%d\t%.2f\t%.5f\t%.6f\t%.2f\t%.2f" % (
        mir.r_t[x],
        mir.Load[0].r_St[x],
        mir.r_ss_Pacc[x],
        mir.r_f[x],
        mir.r_deltaF[x],
        mir.Slack[0].r_Pe[x],
        mir.Machines[1].r_Pe[x],))

# Testing of data export
from makeModelDictionary import makeModelDictionary
from saveModelDictionary import saveModelDictionary
dictName = 'autoMat'

D = makeModelDictionary(mir)
savedName = saveModelDictionary(D,dictName)

# use cmd to run python 3 32 bit script...
systemString = "py -3-32 makeMat.py " + savedName +" " + dictName + " 0"
# run a command prompt command
import subprocess
subprocess.Popen(systemString)

raw_input("Press <Enter> to Continue. . . . ")
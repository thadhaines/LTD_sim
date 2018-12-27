"""Parse dyd file information to python mirror
assumes each line is a separate dynamic element of the form:
genrou 12 "GRANDC-G3   " 20.00  "1 "  : #9 mva=9000.0000 6.0000 0.0250 0.0600 0.0400 5.0000 0.0000 1.2000 0.7000 0.3000 0.2300 0.2200 0.1700 0.0500 0.3000 0.0000 0.0000 0.0000 0.0000
"""

import PSLF_model_templates as pmod

def cleanDydStr(str):
    """Parse dyd string into list of more easily workable parts
    Removes any comments and casts most common parameters 
    Assumes busnum is int, all parameters after #X or mXX= are floats
    """
    clean = []
    a = str.split(":")
    b = a[0].split('"')
    c = str.split()
    d = a[1].split()
 
    clean.append(c[0])                  # model
    clean.append(int(c[1]))             # busnum
    clean.append(b[1].rstrip())         # busnam
    clean.append(float(b[2].strip()))   # base kV
    clean.append(b[3].strip())          # id?

    for n in range(len(d)):
        #set IMPORT = 0.0
        if (d[n] == 'IMPORT'):
            d[n] = 0.0
            clean.append(d[n])
            continue

        # not cast # identifier
        if '#' in d[n]:
            clean.append(d[n])
            continue

        # ignore inline comments
        if '"' in d[n]:
            continue

        # parse value from mva= 
        # funtionality removed - may cause confusion if not defined.
        if '=' in d[n]:
            #e = d[n].split('=')
            #clean.append(float(e[1]))
            clean.append(d[n])
            continue
        
        clean.append(float(d[n]))

    # debug
    #for x in range(len(clean)):
    #    print(x, clean[x], type(clean[x]))
    #print(len(clean))


    return clean

def parseDyd(m_ref,dydLoc):
    """Function that parses dyd information to mirror
    Will parse particular dyd models to intermediate classes
    these classes will be referenced by the model to populate dynamic properties
    """

    file = open(dydLoc, 'r') # open file to read
    line = next(file) # get first line of file
    foundModels = 0

    while line:
        if line[0] == '#' or line[0] =='\n':
            # line is a comment, skip
            line = next(file, None)
            continue
        
        #print(line) # Debug
        parts = line.split()
        
        if parts[0] == "genrou":
            print("testing gen %s" % parts[1])
            cleanLine = cleanDydStr(line)
            newPmod = pmod.genrou(cleanLine, m_ref)
            m_ref.PSLFdynamics.append(newPmod)
            foundModels += 1
  
        line = next(file,  None) # get next line, if there is one

    file.close() # close file
    if m_ref.debug == 1:
        print("Parsed %d models from dyd:  %s" % (foundModels, dydLoc))
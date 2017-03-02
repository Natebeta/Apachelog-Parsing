# 0: IP
# 1: Blank
# 2: Blank
# 3: Time
# 4: Command
# 5: File
# 6: HTTP-Protocol
# 7: HTTP-Code
# 8: Size

#Replacing chars
def parseLine(line):
    line = line.replace('"', "")

    line = line.replace('"', "")
    line = line.replace("[", "")
    line = line.replace("]", "")

#Convert line into list    
    splitted = line.split()

#Change ports to integer
    var = splitted[-1]
    if not var.isdecimal():
        splitted[-1] = 0
    splitted[-1] = int(splitted[-1])
    splitted[-2] = int(splitted[-2])

#Connect 3rd & 4th element for time and remove 4th element
    splitted[3] = splitted[3] + splitted[4]
    splitted.pop(4)

    return (tuple(splitted))


def parseLog(iterable, output):
    try:
        outputFile = open(output, mode="w")
    except IOError:
        print(IOError)
    # common information
    miscellaneous = {'lines': 0, 'size': 0}
    
    
    # File data
    filedata = {}
    
    # IP data
    ipfile = {}
    
    # html requests
    requests = {}
    
    # html codes
    codes = {}

    for line in iterable:
        if verboseMode == "j":
            print(line)
        miscellaneous['lines'] += 1

        para = parseLine(line)
        if not len(para) != 8:
            outputFile.write("Fehler in Zeile %d: %s" % (miscellaneous.get('lines'), line) + "\n\n")
            print("Fehler in Zeile %d: %s" % (miscellaneous.get('lines'), line) + "\n\n")
            continue
        miscellaneous['size'] += para[-1]

        if isKeyinDict(filedata, para[-4]):
            filedata[para[-4]] += 1
        else:
            filedata[para[-4]] = 1

        # html codes
        if isKeyinDict(codes, para[-2]):
            codes[para[-2]] += 1
        else:
            codes[para[-2]] = 1

        # html requests
        if isKeyinDict(requests, para[-5]):
            requests[para[-5]] += 1
        else:
            requests[para[-5]] = 1

        if not para[0] in ipfile:
            ipfile[para[0]] = []
        if not para[-4] in ipfile.get(para[0]):
            ipfile.get(para[0]).append(para[-4])

#Exchange in MB
    miscellaneous['size'] = str((miscellaneous.get('size') / 1024) // 1024) + "MB"

    # files per ip output
    outputFile.write("Dateien pro IP\n~~~~~~~~~~~~~~\n")
    for ip in sorted(ipfile):
        outputFile.write(ip + ":\n")
        print(ip + ":\n")
        for reqFile in ipfile.get(ip):
            outputFile.write("    " + reqFile + "\n")
            print("    " + reqFile + "\n")
        outputFile.write("\n")
        print("\n")

    # requests output
    outputFile.write("\nAbfragen\n~~~~~~~~\n")
    print("\nAbfragen\n~~~~~~~~\n")
    
    for req in sorted(requests, key=requests.get, reverse=True):
        outputFile.write(str(req) + ": " + str(requests.get(req)) + "\n")
        print(str(req) + ": " + str(requests.get(req)) + "\n")

    # html codes output
    outputFile.write("\nHTML Codes\n~~~~~~~~~~~\n")
    print("\nHTML Codes\n~~~~~~~~~~~\n")
    for code in sorted(codes, key=codes.get, reverse=True):
        outputFile.write(str(code) + ": " + str(codes.get(code)) + "\n")
        print(str(code) + ": " + str(codes.get(code)) + "\n")

    # miscellaneous output
    outputFile.write("\nSonstiges\n~~~~~~~~~\n")
    print("\nSonstiges\n~~~~~~~~~\n")
    for key in sorted(miscellaneous):
        outputFile.write(str(key) + ": " + str(miscellaneous.get(key)) + "\n")
        print(str(key) + ": " + str(miscellaneous.get(key)) + "\n")
    sortedfiles = sorted(filedata, key=filedata.get, reverse=True)
    outputFile.write("Häufigste Datei: " + sortedfiles[0] + " (" + str(filedata.get(sortedfiles[0])) + "x)")
    print("Häufigste Datei: " + sortedfiles[0] + " (" + str(filedata.get(sortedfiles[0])) + "x)")


def isKeyinDict(dict, entry):
    if (dict.__contains__(entry)):
        return True
    return False



from time import *

#Usermenue
t1 = clock()
#Opens logfile
logfileCheck = False
while logfileCheck == False:
    logfileName = input("Log-Datei: ")
    try:
        with open(logfileName, "r") as logfile:
            logfileCheck = True

    except OSError:
        print("Die eingegebene Logdatei wurde nicht gefunden.")


outputfilename = "parsed-" + logfileName

#Verbose Mode input check
verboseCheck = False
while verboseCheck == False:
    verboseMode = input("Verbose Modus aktivieren?(J/N): ").lower()
    if (verboseMode == "n") or (verboseMode == "j"):
        verboseCheck = True
        pass
    else:
        print("Bitte geben Sie ein J oder N ein.")

#Time input check
tInputCheck = False
while tInputCheck == False:
    timecheck = input("Möchten Sie die Zeit angezeigt bekommen?(J/N): ").lower()
    if(timecheck == "j") or (timecheck == "n"):
        tInputCheck = True
        pass
    else:
        print("Bitte geben Sie ein J oder N ein.")

#Takes time
t1 = clock()

#Start parsing
with open(logfileName, "r") as logfile:
     parseLog(logfile, outputfilename)

#Takes endtime
t2 = clock()
t = t2 - t1

#Output in programm
if timecheck=="j":
    print("Zeit: %7.2f Sekunden" % (t))
print("Fertig")

from pathlib import Path
import os

DELTA = 5/3600
# DELTA = .00001
GAIA_RA_COL = 1
GAIA_DEC_COL = 2

GALEX_RA_COL = 4
GALEX_DEC_COL = 5

# excel funtion to test output
# =IF(ABS(D2-E2) < (5/3600), 1, 0)


def getRootDir():
    rootDir = ""
    print("Path to root directory: ")
    rootDir = Path(input())
    if(rootDir.exists() == False):
        print("Invalid path")
    else:
        return str(rootDir)


def getCSVFilesInDirectory(path):
    csvFiles = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                f = path + "\\" + str(file)
                csvFiles.append(f)
    return csvFiles

def getFileNamePrefix(path):
    fileName = os.path.basename(path)
    lastUnderScoreIndex = fileName.rindex('_')
    prefix = fileName[0:lastUnderScoreIndex]
    return prefix

def getLinesFromFile(file):
    returnVal = []
    file1 = open(file, 'r')
    lines = file1.readlines()
    for line in lines:
        line = line.replace(".csv", "")
        returnVal.append(line)

    del returnVal[0] # remove the header line

    return returnVal

def AreApprox(a, b, delta):
    if (abs(a - b) < delta):
        return True
    else:
        return False

def convertListToString(list):
    result = '\n'.join(list)
    return result

def writeFile(path, contents):
    f = open(path, "w")
    f.write(contents)
    f.close()



rootDir = getRootDir()

galexPath = rootDir + "\\Galex\\"

gaiaFiles = getCSVFilesInDirectory(rootDir + "\\GAIA\\")


results = []
results.append("FILE, GAIA ROW, GALEX ROW, GAIA RA, GALEX RA, GAIA DEC, GALEX DEC")

for gaiaFile in gaiaFiles:
    # print("Processing file " + gaiaFile)
    fileNamePrefix = getFileNamePrefix(gaiaFile)

    linesFromGaia = getLinesFromFile(gaiaFile)
    linesFromGalex = getLinesFromFile(galexPath + "\\" + fileNamePrefix + "_Galex.csv")

    gaiaRow = 2 # we need to start at row 2 becaue of 0 vs 1 array and excel, plus we delete the header row
    for gaiaLine in linesFromGaia:
        galexRow = 2
        gaiaSplit = gaiaLine.split(',')
        gaia_ra = gaiaSplit[GAIA_RA_COL]
        gaia_dec = gaiaSplit[GAIA_DEC_COL]

        gaia_ra_float = float(gaia_ra)
        gaia_dec_float = float(gaia_dec)

        for galexLine in linesFromGalex:
            galexSplit = galexLine.split(',')
            galex_ra = galexSplit[GALEX_RA_COL]
            galex_dec = galexSplit[GALEX_DEC_COL]

            galex_ra_float = float(galex_ra)
            galex_dec_float = float(galex_dec)

            if(AreApprox(galex_ra_float, gaia_ra_float, DELTA) and AreApprox(galex_dec_float, gaia_dec_float, DELTA)):
                results.append(f"{fileNamePrefix},{gaiaRow},{galexRow},{gaia_ra},{galex_ra},{gaia_dec},{galex_dec}")

            galexRow = galexRow + 1

        gaiaRow = gaiaRow + 1


if (len(results) <= 0):
    print("No results found")
else:
    print("Reults")
    print("-------------------------------------")
    s = convertListToString(results)
    print(s)
    writeFile(rootDir + "\\similiar2.csv", s)





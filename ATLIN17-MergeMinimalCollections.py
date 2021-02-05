import os
import re
from datetime import datetime
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from bs4 import BeautifulSoup
# from lxml import etree
import read_ini_config
import subprocess
import shutil
import csv

# Create an application
app = QtWidgets.QApplication([])

# Create window
win = QtWidgets.QWidget()
win.setWindowTitle('ATLIN17-MergeMinimalCollection')
win.setFixedSize(500, 500)
base_path = os.getcwd()

# add application icon
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap("icons/Jommans-Ironman-Style-File-Adobe-Flash.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
win.setWindowIcon(icon)

# set windows layout
layout = QtWidgets.QGridLayout()
win.setLayout(layout)

# create widget components
browseMinimalPath = QtWidgets.QPushButton('Minimal Path')
browseFullIndexingPath = QtWidgets.QPushButton('Full Indexing Path')
browseOutputPath = QtWidgets.QPushButton('Output Path')
goMergeButton = QtWidgets.QPushButton('Merge Files')
madsModsBrowse = QtWidgets.QPushButton('MadsMods Path')   # added 10/19/2020
minimalPath = QtWidgets.QLineEdit()
minimalPath.setReadOnly(True)
fullIndexingPath = QtWidgets.QLineEdit()
fullIndexingPath.setReadOnly(True)
outputPathTextLine = QtWidgets.QLineEdit()
outputPathTextLine.setReadOnly(True)
logViewer = QtWidgets.QPlainTextEdit()
pBar = QtWidgets.QProgressBar()
madsModsBox = QtWidgets.QLineEdit()  # added 10/19/2020
madsModsBox.setReadOnly(True)  # added 10/19/2020

# set layout of each component
layout.addWidget(browseMinimalPath, 1, 1)
layout.addWidget(browseFullIndexingPath, 2, 1)
layout.addWidget(browseOutputPath, 3, 1)
layout.addWidget(minimalPath, 1, 0)
layout.addWidget(fullIndexingPath, 2, 0)
layout.addWidget(outputPathTextLine, 3, 0)
layout.addWidget(goMergeButton, 4, 1)
layout.addWidget(logViewer, 5, 0, 1, 2)
layout.addWidget(pBar, 6, 0, 1, 2)

# read config
mergePath = read_ini_config.read_config("MinimalFiles", "Path")
fullPath = read_ini_config.read_config("FullIndexing", "Path")
tempPath = read_ini_config.read_config("ApplicationPaths", "TempPath")
outputPath = read_ini_config.read_config("OutputPath", "OutputPath")
RemoveTag = read_ini_config.read_config("RemoveTag", "RemoveTag")
RemoveTagValue = read_ini_config.read_config("RemoveTag", "RemoveTagValue")
madsmodsPath = read_ini_config.read_config("MadsModsPath", "Path")  # added 10/19/2020

# set path in path text line
minimalPath.setText(mergePath)
fullIndexingPath.setText(fullPath)
outputPathTextLine.setText(outputPath)
madsModsBox.setText(madsmodsPath)  # added 10/19/2020

#create logs folder
logPath = "D:\\MergeCollections\\Logs"
if not os.path.exists(logPath):
    os.makedirs(logPath)
if os.path.exists(logPath + "\\MergeMinimalCollection.csv"):
    os.remove(logPath + "\\MergeMinimalCollection.csv")

with open(logPath + "\\MergeMinimalCollection.csv", mode='w') as csv_file:
    fieldnames = ['Tag001', 'Record Title', 'Tag=773 code=w', 'Tag=700 code=8',
                  'Tag=700 code=9']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
csv_file.close()


def checkPathExist():
    # check if folders in path or files exists
    if not os.path.exists(mergePath):
        # showDialog(mergePath + " does not exist. Check configuration file.", "Path Error")
        logViewer.appendPlainText(str(datetime.now()) + ": " + mergePath + " does not exist. Check configuration file.")
        QtGui.QGuiApplication.processEvents()
    if not os.path.exists(fullPath):
        # showDialog(fullPath + " does not exist. Check configuration file.", "Path Error")
        logViewer.appendPlainText(str(datetime.now()) + ": " + fullPath + " does not exist. Check configuration file.")
        QtGui.QGuiApplication.processEvents()
    if not os.path.exists(tempPath):
        # showDialog(tempPath + " does not exist. Check configuration file.", "Path Error")
        logViewer.appendPlainText(str(datetime.now()) + ": " + tempPath + " does not exist. Check configuration file.")
        QtGui.QGuiApplication.processEvents()
    if not os.path.exists(outputPath):
        # showDialog(outputPath + " does not exist. Check configuration file.", "Path Error")
        logViewer.appendPlainText(
            str(datetime.now()) + ": " + outputPath + " does not exist. Check configuration file.")
        QtGui.QGuiApplication.processEvents()
    if not os.path.exists(base_path + "\\icons"):
        # showDialog(base_path + "\\icons" + " does not exist. Check configuration file.", "Path Error")
        logViewer.appendPlainText(
            str(datetime.now()) + ": " + base_path + "\\icons" + " does not exist. Check configuration file.")
        QtGui.QGuiApplication.processEvents()
    if not os.path.exists(base_path + "\\ATLIN17-MergeMinimalCollection.ini"):
        # showDialog(base_path + "\\ATLIN17-MergeMinimalCollection.ini" + " does not exist. Check ini file if it exists along with the application set-up.", "Path Error")
        logViewer.appendPlainText(
            str(
                datetime.now()) + ": " + base_path + "\\ATLIN17-MergeMinimalCollection.ini" + " does not exist. Check ini file if it exists along with the application set-up.")
        QtGui.QGuiApplication.processEvents()
    if not os.path.exists(madsmodsPath):    # added 10/19/2020
        # showDialog(tempPath + " does not exist. Check configuration file.", "Path Error")
        logViewer.appendPlainText(str(datetime.now()) + ": " + madsmodsPath + " does not exist. Check configuration file.")
        QtGui.QGuiApplication.processEvents()
    return


def removeTempFiles():
    # remove temp files
    temporaryTxtPath = tempPath + "temp.txt"
    if os.path.exists(temporaryTxtPath):
        os.remove(temporaryTxtPath)
    temporaryattrPath = tempPath + "attrtag.txt"
    if os.path.exists(temporaryattrPath):
        os.remove(temporaryattrPath)
    temporaryCompiledPath = tempPath + "compiled.out"
    if os.path.exists(temporaryCompiledPath):
        os.remove(temporaryCompiledPath)
    temporaryattrvalue = tempPath + "attrvalue.txt"
    if os.path.exists(temporaryattrvalue):
        os.remove(temporaryattrvalue)
    temporaryoutput3 = tempPath + "output3.txt"
    if os.path.exists(temporaryoutput3):
        os.remove(temporaryoutput3)
    temporarytemp2 = tempPath + "temp2.txt"
    if os.path.exists(temporarytemp2):
        os.remove(temporarytemp2)
    temporaryforFinaloutput = tempPath + "forFinalOutput.txt"
    if os.path.exists(temporaryforFinaloutput):
        os.remove(temporaryforFinaloutput)
    logpath = tempPath + "MergeMinimalCollection.log"     # added 10/19/2020
    if os.path.exists(tempPath + "MergeMinimalCollection.log"):
        os.remove(logpath)


def manualBrowseMinimalPath():
    ask_path = str(QFileDialog.getExistingDirectory(None, "Browse Minimal Path"))
    minimalPath.setText("")
    minimalPath.setText(os.path.normpath(ask_path) + "\\")
    checkPathExist()


def manualBrowseFullPath():
    ask_path = str(QFileDialog.getExistingDirectory(None, "Browse Full Indexing Path"))
    fullIndexingPath.setText("")
    fullIndexingPath.setText(os.path.normpath(ask_path) + "\\")
    checkPathExist()


def manualBrowseOutputPath():
    ask_path = str(QFileDialog.getExistingDirectory(None, "Browse Output Path"))
    outputPathTextLine.setText("")
    outputPathTextLine.setText(os.path.normpath(ask_path) + "\\")
    checkPathExist()


def manualBrowseMadsModsPath():  # added 10/19/2020
    ask_path = str(QFileDialog.getExistingDirectory(None, "Browse MadsMods Path"))
    madsModsBox.setText("")
    madsModsBox.setText(os.path.normpath(ask_path) + "\\")
    checkPathExist()


def startMergingFiles():
    global tag001, tag005, tag008
    global checkifExistInMinimal
    # get string to search
    convertMadsModstoMinimal()
    pBar.setMaximum(100)
    checkPathExist()
    logViewer.appendPlainText(str(datetime.now()) + ": Starting to merge files...")
    QtGui.QGuiApplication.processEvents()
    path = fullIndexingPath.text()
    dirs = os.listdir(path)
    for file in dirs:
        progress(10)
        logViewer.appendPlainText(str(datetime.now()) + file + ": Saving each lines to temp file...")
        QtGui.QGuiApplication.processEvents()
        fileContains = re.search(r'(book|review|multimedia|authority)', file)
        if fileContains:
            continue
        readFile = open(path + file, encoding='utf-8')
        for lines in readFile:
            # getFileValue = readFile.readline()
            saveToFile(lines)
            if lines == "  </marc:record>\n" or lines == "</marc:record>\n":
                getSubField = open(tempPath + "temp.txt", "r")
                logViewer.appendPlainText(str(datetime.now()) + ": Getting the subfield...")
                QtGui.QGuiApplication.processEvents()
                with open(path + file, encoding='utf-8') as xmlFile:
                    xmlData = xmlFile.read()
                    xmlData = re.sub(r'\[', 'lbacket;', str(xmlData))
                    xmlData = re.sub(r'\]', 'rbacket;', str(xmlData))
                    xmlData = re.sub(r'\(', 'lparent;', str(xmlData))
                    xmlData = re.sub(r'\)', 'rparent;', str(xmlData))
                    xmlData = re.sub(r'\?', 'qmark;', str(xmlData))
                    getSubFieldValue = re.search(
                        r'<marc:datafield tag="245"[^>]+>[^<]*<marc:subfield code="a">([^<]+)</marc:subfield>',
                        str(xmlData))
                    if getSubFieldValue is None:
                        logViewer.appendPlainText(
                            str(datetime.now()) + ": " + file + " found no tag='245'. Please check...")
                        QtGui.QGuiApplication.processEvents()
                        return
                    fullIndexingValue = getSubFieldValue.group(1)
                    logViewer.appendPlainText(
                        str(datetime.now()) + ": SubField Value: [" + str(fullIndexingValue) + "]")
                    QtGui.QGuiApplication.processEvents()
                    fullIndexingValue = re.sub(r'lbacket;', '[', str(fullIndexingValue))
                    fullIndexingValue = re.sub(r'rbacket;', ']', str(fullIndexingValue))
                    fullIndexingValue = re.sub(r'lparent;', '(', str(fullIndexingValue))
                    fullIndexingValue = re.sub(r'rparent;', ')', str(fullIndexingValue))
                    fullIndexingValue = re.sub(r'qmark;', '?', str(fullIndexingValue))
                    findMarcSubFieldInMinimal(fullIndexingValue)  # search fullindexing value to minimal file
                    # if checkifExistInMinimal is None:
                    #  continue

                    # insert subfields to main record
                    read_ini_config.writeFile(tempPath + "attrtag.txt", "")
                    read_ini_config.writeFile(tempPath + "attrvalue.txt", "")
                    tempMainRecord = read_ini_config.readFile(tempPath + "temp.txt")
                    tempAttrRecord = read_ini_config.readFile(tempPath + "attrtag.txt")
                    # tempAttrValueRecord = read_ini_config.readFile(tempPath + "attrvalue.txt")
                    tempAttrRecord = re.sub(r'(</marc:datafield>)(<marc:datafield)', r'\1\n\2', tempAttrRecord)
                    tempAttrRecord = re.sub(r'(<marc:datafield) (ind1="[^"]+" ind2="[^"]+") (tag="[^"]+")(>)',
                                            r'\1 \3 \2\4', str(tempAttrRecord))
                    tempAttrRecord = re.sub(r'(<marc:datafield tag="[^"]+" ind1="[^"]+" ind2="[^"]+">)', r'  \1',
                                            tempAttrRecord)
                    tempAttrRecord = re.sub(r'(<marc:subfield code="[^"]+">[^<]+</marc:subfield>)', r'    \1',
                                            tempAttrRecord)
                    tempAttrRecord = re.sub(r'(</marc:datafield>)', r'  \1', tempAttrRecord)
                    xmlMainRecordSoup = BeautifulSoup(tempMainRecord, 'html.parser')
                    searchTag245 = xmlMainRecordSoup.find(tag="245")
                    searchTag245 = re.sub(r'\[', 'lbacket;', str(searchTag245))
                    searchTag245 = re.sub(r'\]', 'rbacket;', str(searchTag245))
                    searchTag245 = re.sub(r'\(', 'lparent;', str(searchTag245))
                    searchTag245 = re.sub(r'\)', 'rparent;', str(searchTag245))
                    searchTag245 = re.sub(r'\?', 'qmark;', str(searchTag245))
                    searchTag245 = re.sub(r'\"', 'quote;', str(searchTag245))
                    searchTag245 = re.sub(r'(<marc:datafield) (ind1="[^"]+" ind2="[^"]+") (tag="245")(>)',
                                          r'\1 \3 \2\4', str(searchTag245))
                    searchTag245 = re.sub(r'(<marc:datafield tag="[^"]+" ind1="[^"]+" ind2="[^"]+">)', r'  \1',
                                          searchTag245)
                    searchTag245 = re.sub(r'(<marc:subfield code="[^"]+">[^<]+</marc:subfield>)', r'    \1',
                                          searchTag245)
                    searchTag245 = re.sub(r'(</marc:datafield>)', r'  \1', searchTag245)
                    replaceOutput = re.sub(str(searchTag245), str(searchTag245) + str(tempAttrRecord),
                                           str(tempMainRecord), re.MULTILINE)
                    replaceOutput = re.sub(r'lbacket;', '[', str(replaceOutput))
                    replaceOutput = re.sub(r'rbacket;', ']', str(replaceOutput))
                    replaceOutput = re.sub(r'lparent;', '(', str(replaceOutput))
                    replaceOutput = re.sub(r'rparent;', ')', str(replaceOutput))
                    replaceOutput = re.sub(r'qmark;', '?', str(replaceOutput))
                    replaceOutput = re.sub(r'quote;', '"', str(replaceOutput))
                    replaceOutput = re.sub(r'(</marc:datafield>)(  <marc:datafield)', r'\1\n\2', str(replaceOutput))
                    replaceOutput = re.sub(r'(>)(<marc:record>)', r'\1\n\2', str(replaceOutput))
                    replaceOutput = re.sub(r'(>)(</marc:collection>)', r'\1\n\2', str(replaceOutput))

                    # xmlMainRecordSoup = BeautifulSoup(tempMainRecord, 'html.parser')
                    # searchTag001 = xmlMainRecordSoup.find(tag="001")
                    # searchTag001 = re.sub(r'<marc:controlfield tag="001">[^<]+</marc:controlfield>', str(searchTag001), str(tempMainRecord))
                    # searchTag005 = xmlMainRecordSoup.find(tag="005")
                    # searchTag005 = re.sub(r'<marc:controlfield tag="005">[^<]+</marc:controlfield>', str(searchTag005), str(tempMainRecord))
                    # searchTag008 = xmlMainRecordSoup.find(tag="008")
                    # searchTag008 = re.sub(r'<marc:controlfield tag="008">[^<]+</marc:controlfield>', str(searchTag008), str(tempMainRecord))

                    # replaceOutput = re.sub(str(searchTag001), str(searchTag001), tempMainRecord, re.MULTILINE)
                    # replaceOutput = re.sub(str(searchTag005), str(searchTag005), tempMainRecord, re.MULTILINE)
                    # replaceOutput = re.sub(str(searchTag008), str(searchTag008), tempMainRecord, re.MULTILINE)
                # append this output
                read_ini_config.writeFile(tempPath + "compiled.out", str(replaceOutput))

                # clean up temp data
                read_ini_config.writeFileWrite(tempPath + "temp.txt", "")
                read_ini_config.writeFileWrite(tempPath + "attrtag.txt", "")

                xmlFile.close()
                getSubField.close()
            # else:
            #   read_ini_config.writeFile(tempPath + "compiled.out", lines)
        readFile.close()

        progress(30)
        # save the final output
        logViewer.appendPlainText(str(datetime.now()) + file + ": Done Compiling...")
        QtGui.QGuiApplication.processEvents()
        compiledOutputFile = read_ini_config.readFile(tempPath + "compiled.out")
        outPutFile = outputPath + file
        if os.path.exists(outPutFile):
            os.remove(outputPath + file)
            read_ini_config.writeFileWrite(outputPathTextLine.text() + file,
                                           compiledOutputFile + "</marc:collection>")
        else:
            read_ini_config.writeFileWrite(outputPathTextLine.text() + file,
                                           compiledOutputFile + "</marc:collection>")

        removeTempFiles()
    # if RemoveTag:
    #   remove991DataField()
    progress(50)
    logViewer.appendPlainText(str(datetime.now()) + ": Done Processing...")
    QtGui.QGuiApplication.processEvents()
    searchGetTagInOutput()
    # remove991DataField()
    progress(100)
    showDialog("Merge Done", "Done Processing!")
    return


def convertMadsModstoMinimal():
    if not os.path.exists(madsmodsPath + "\\xmlFiles\\xmlFiles.sts"):
        f = open(madsmodsPath + "\\xmlFiles\\xmlFiles.sts", "x")
        f.close()
        g = open(madsmodsPath + "xmlFiles\\xmlFiles.sts", "w")
        g.write("For Run")
        g.close()
    g = open(madsmodsPath + "xmlFiles\\xmlFiles.sts", "w")
    g.write("For Run")
    g.close()
    subprocess.call([base_path + '\\SReplace\\SReplace.exe'])
    mads_path = madsmodsPath + "xmlFiles"
    dirs = os.listdir(mads_path)
    for f in dirs:
        if os.path.exists(mergePath + f):
            os.remove(mergePath + f)
        rightextension = f[-4:]
        if rightextension == ".sts":
            break
        shutil.move(mads_path + "\\" + f, mergePath)
    return


def checkValueinMinimal():
    pass


def remove991DataField():
    dirs991 = os.listdir(outputPath)
    for file991 in dirs991:
        logViewer.appendPlainText(str(datetime.now()) + ": Removing not needed mac:records...")
        QtGui.QGuiApplication.processEvents()
        file = read_ini_config.readFile(outputPath + str(file991))
        file = re.sub('<marc:subfield code="a">Book</marc:subfield>', '<marc:datafield>forRemove</marc:datafield>',
                      str(file))
        file = re.sub('<marc:subfield code="a">Review</marc:subfield>', '<marc:datafield>forRemove</marc:datafield>',
                      str(file))
        file = re.sub('<marc:subfield code="a">Multimedia</marc:subfield>',
                      '<marc:datafield>forRemove</marc:datafield>', str(file))
        file = re.sub(r'<marc:datafield>forRemove</marc:datafield>', '¤', str(file))
        file = re.sub(r'<marc:record>', '¥', str(file))
        file = re.sub(r'</marc:record>', '£', str(file))
        file = re.sub(r'¥[^£]*¤[^£]*£', '', file)
        file = re.sub(r'¥', '<marc:record>', file)
        file = re.sub(r'£', '</marc:record>', file)
        file = re.sub(r'</marc:record><marc:record>', '</marc:record>\n<marc:record>', file)
        file = re.sub(r'(>)(<marc:record>)', r'\1\n\2', file)
        file = re.sub(r'(>)(</marc:collection>)', r'\1\n\2', str(file))
        read_ini_config.writeFileWrite(outputPath + file991, str(file))
        searchBlankRecord = re.search(r'\n\n\n</marc:collection>', str(file))
        if searchBlankRecord:
            os.remove(outputPath + file991)
    logViewer.appendPlainText(str(datetime.now()) + ": Done removing not needed mac:records...")
    QtGui.QGuiApplication.processEvents()


def getTag010508(fromOutputValue, outputtag001):
    global mtag001, mtag005, mtag008, outputValueP, outputValueB, outputValueN, outputValue7008, outputValue7009, outputValue773w, title_counter, minimalFile
    dirs010508 = os.listdir(minimalPath.text())
    for minimalFile in dirs010508:
        fileContains = re.search(r'(book|review|multimedia|authority)', str(minimalFile))
        if fileContains:
            continue
        ## need to add error message that the Record Title is not found in the Transmitted Minimal
        readminimalFile = read_ini_config.readFile(minimalPath.text() + minimalFile)
        fromOutputValue = re.sub(r':', '', str(fromOutputValue))
        searchRecordTitleifFound = readminimalFile.rfind(fromOutputValue)
        if searchRecordTitleifFound == -1:
            title_counter = 0
            logViewer.appendPlainText(str(datetime.now()) + ": Record Title not Found... Proceeding to next file...")
            QtGui.QGuiApplication.processEvents()
            continue
        title_counter = 1
        readminimalFile = re.sub(r'\n</marc:collection>', r'</marc:collection>', str(readminimalFile))
        read_ini_config.writeFileWrite(minimalPath.text() + minimalFile, readminimalFile)
        minimalPerRecord = read_ini_config.readLinesOfFile(minimalPath.text(), minimalFile)
        logViewer.appendPlainText(str(datetime.now()) + ": Searching subfield in minimal transmitted files...")
        QtGui.QGuiApplication.processEvents()
        convertChar = re.sub(r'\[', '\[', fromOutputValue)
        convertChar = re.sub(r'\]', '\]', convertChar)
        convertChar = re.sub(r'\(', '\(', convertChar)
        convertChar = re.sub(r'\)', '\)', convertChar)
        convertChar = re.sub(r'\?', '\?', convertChar)
        convertChar = re.sub(r'\"', '\"', convertChar)
        searchSubFieldValueinFile = re.search(convertChar, readminimalFile)
        if searchSubFieldValueinFile is None:
            continue
        for line in minimalPerRecord:
            read_ini_config.writeFile(tempPath + "temp2.txt", line)
            if line == "  </marc:record>\n" or line == "</marc:record>\n" or line == "</marc:record></marc:collection>\n":
                with open(tempPath + "temp2.txt", encoding='utf-8') as xmlFile:
                    xmlData = xmlFile.read()
                    xmlData = re.sub(r'\[', 'lbacket;', str(xmlData))
                    xmlData = re.sub(r'\]', 'rbacket;', str(xmlData))
                    xmlData = re.sub(r'\(', 'lparent;', str(xmlData))
                    xmlData = re.sub(r'\)', 'rparent;', str(xmlData))
                    xmlData = re.sub(r'\?', 'qmark;', str(xmlData))
                    # current_date = f"{datetime.now():%Y%m%d}"
                    # xmlData = re.sub('&datetoday;', current_date, xmlData)
                    getSubFieldValue = re.search(
                        r'<marc:datafield tag="245"[^>]+>[^<]*<marc:subfield code="a">([^<]+)</marc:subfield>',
                        str(xmlData))
                    minimalValueP = re.search(
                        r'<marc:datafield tag="245"[^>]+>[^\*]*<marc:subfield code="p">([^<]+)</marc:subfield>',
                        str(xmlData))
                    minimalValueN = re.search(
                        r'<marc:datafield tag="245"[^>]+>[^\*]*<marc:subfield code="n">([^<]+)</marc:subfield>',
                        str(xmlData))
                    minimalValueB = re.search(
                        r'<marc:datafield tag="245"[^>]+>[^<]*<marc:subfield code="a">[^<]+</marc:subfield>[^<]+<marc:subfield code="b">([^<]+)</marc:subfield>',
                        str(xmlData))
                    minimalValue7008 = re.search(
                        r'<marc:datafield tag="700"[^>]+>[^\<]*<marc:subfield code="8">([^<]+)</marc:subfield>',
                        str(xmlData))
                    minimalValue7009 = re.search(
                        r'<marc:datafield tag="700"[^>]+>[^\*]*<marc:subfield code="9">([^<]+)</marc:subfield>',
                        str(xmlData))
                    minimalValue773w = re.search(
                        r'<marc:datafield tag="773"[^>]+>[^<]*<marc:subfield code="w">([^<]+)</marc:subfield>',
                        str(xmlData))
                    minimalValue = getSubFieldValue.group(1)
                    minimalValue = re.sub(r'lbacket;', '[', str(minimalValue))
                    minimalValue = re.sub(r'rbacket;', ']', str(minimalValue))
                    minimalValue = re.sub(r'lparent;', '(', str(minimalValue))
                    minimalValue = re.sub(r'rparent;', ')', str(minimalValue))
                    minimalValue = re.sub(r'qmark;', '?', str(minimalValue))
                    minimalValue = re.sub(r'quote;', '"', str(minimalValue))

                    if minimalValueP:
                        minimaltagValueP = minimalValueP.group(1)
                        minimaltagValueP = re.sub(r'lbacket;', '[', str(minimaltagValueP))
                        minimaltagValueP = re.sub(r'rbacket;', ']', str(minimaltagValueP))
                        minimaltagValueP = re.sub(r'lparent;', '(', str(minimaltagValueP))
                        minimaltagValueP = re.sub(r'rparent;', ')', str(minimaltagValueP))
                        minimaltagValueP = re.sub(r'qmark;', '?', str(minimaltagValueP))
                        minimaltagValueP = re.sub(r'quote;', '"', str(minimaltagValueP))
                    else:
                        minimaltagValueP = ""
                    if minimalValueN:
                        minimaltagValueN = minimalValueN.group(1)
                        minimaltagValueN = re.sub(r'lbacket;', '[', str(minimaltagValueN))
                        minimaltagValueN = re.sub(r'rbacket;', ']', str(minimaltagValueN))
                        minimaltagValueN = re.sub(r'lparent;', '(', str(minimaltagValueN))
                        minimaltagValueN = re.sub(r'rparent;', ')', str(minimaltagValueN))
                        minimaltagValueN = re.sub(r'qmark;', '?', str(minimaltagValueN))
                        minimaltagValueN = re.sub(r'quote;', '"', str(minimaltagValueN))
                    else:
                        minimaltagValueN = ""
                    if minimalValueB:
                        minimaltagValueB = minimalValueB.group(1)
                        minimaltagValueB = re.sub(r'lbacket;', '[', str(minimaltagValueB))
                        minimaltagValueB = re.sub(r'rbacket;', ']', str(minimaltagValueB))
                        minimaltagValueB = re.sub(r'lparent;', '(', str(minimaltagValueB))
                        minimaltagValueB = re.sub(r'rparent;', ')', str(minimaltagValueB))
                        minimaltagValueB = re.sub(r'qmark;', '?', str(minimaltagValueB))
                        minimaltagValueB = re.sub(r'quote;', '"', str(minimaltagValueB))
                    else:
                        minimaltagValueB = ""
                    if minimalValue7008:
                        minimaltagValue7008 = minimalValue7008.group(1)
                        minimaltagValue7008 = re.sub(r'lbacket;', '[', str(minimaltagValue7008))
                        minimaltagValue7008 = re.sub(r'rbacket;', ']', str(minimaltagValue7008))
                        minimaltagValue7008 = re.sub(r'lparent;', '(', str(minimaltagValue7008))
                        minimaltagValue7008 = re.sub(r'rparent;', ')', str(minimaltagValue7008))
                        minimaltagValue7008 = re.sub(r'qmark;', '?', str(minimaltagValue7008))
                        minimaltagValue7008 = re.sub(r'quote;', '"', str(minimaltagValue7008))
                        minimaltagValue7008 = re.sub(r' ', '', str(minimaltagValue7008))
                    else:
                        minimaltagValue7008 = ""
                    if minimalValue7009:
                        minimaltagValue7009 = minimalValue7009.group(1)
                        minimaltagValue7009 = re.sub(r'lbacket;', '[', str(minimaltagValue7009))
                        minimaltagValue7009 = re.sub(r'rbacket;', ']', str(minimaltagValue7009))
                        minimaltagValue7009 = re.sub(r'lparent;', '(', str(minimaltagValue7009))
                        minimaltagValue7009 = re.sub(r'rparent;', ')', str(minimaltagValue7009))
                        minimaltagValue7009 = re.sub(r'qmark;', '?', str(minimaltagValue7009))
                        minimaltagValue7009 = re.sub(r'quote;', '"', str(minimaltagValue7009))
                    else:
                        minimaltagValue7009 = ""
                    if minimalValue773w:
                        minimaltagValue773w = minimalValue773w.group(1)
                        minimaltagValue773w = re.sub(r'lbacket;', '[', str(minimaltagValue773w))
                        minimaltagValue773w = re.sub(r'rbacket;', ']', str(minimaltagValue773w))
                        minimaltagValue773w = re.sub(r'lparent;', '(', str(minimaltagValue773w))
                        minimaltagValue773w = re.sub(r'rparent;', ')', str(minimaltagValue773w))
                        minimaltagValue773w = re.sub(r'qmark;', '?', str(minimaltagValue773w))
                        minimaltagValue773w = re.sub(r'quote;', '"', str(minimaltagValue773w))
                    else:
                        minimaltagValue773w = ""
                    if minimaltagValue7009 == "":
                        outputValue7009 = ""
                    if fromOutputValue == minimalValue and outputValue7008 != minimaltagValue7008 and outputValue773w == minimaltagValue773w:
                        with open(logPath + "\\MergeMinimalCollection.csv", mode='a', encoding='utf-8') as csv_file2:
                            writer = csv.writer(csv_file2)
                            writer.writerow([outputtag001, fromOutputValue, outputValue773w, outputValue7008, outputValue7009])
                        csv_file2.close()
                        # ['Tag001', 'Record Title', 'Tag=773 code=w', 'Tag=700 code=8', 'Tag=700 code=9']
                        #read_ini_config.writeFile(logPath + "\\MergeMinimalCollection.log", str(
                         #  datetime.now()) + "Full Indexing: Record Title [" + fromOutputValue + "] tag=773 code=w [" + outputValue773w + "] tag=700 code=8 [" + outputValue7008 + "] has mismatch in MODS tag=700 code=8 [" + minimaltagValue7008 + "] tag=700 code=9 [" + minimaltagValue7009 + "] tag=245 code=b[" + minimaltagValueB + "] tag=245 code=p[" + minimaltagValueP + "] tag=245 code=n [" + minimaltagValueN + "] tag=245 code=p [" + minimaltagValueP + "]. Please look in Mods file[" + minimalFile + "]\r\n")
                        # remove in the selection [and outputValueB == minimaltagValueB ]
                    if fromOutputValue == minimalValue and outputValueP == minimaltagValueP: # and outputValueN == minimaltagValueN and outputValue7008 == minimaltagValue7008 and outputValue7009 == minimaltagValue7009 and outputValue773w == minimaltagValue773w:
                        mtag001 = re.search(r'<marc:controlfield tag="001">([^<]+)</marc:controlfield>', str(xmlData))
                        mtag001 = mtag001.group(1)
                        mtag005 = re.search(r'<marc:controlfield tag="005">([^<]+)</marc:controlfield>', str(xmlData))
                        mtag005 = mtag005.group(1)
                        mtag008 = re.search(r'<marc:controlfield tag="008">([^<]+)</marc:controlfield>', str(xmlData))
                        if mtag008 is None:
                            pass
                        else:
                            mtag008 = mtag008.group(1)

                        # replace output3.txt
                        outputTag010508Xml = read_ini_config.readFile(tempPath + "output3.txt")
                        ftag = re.sub(r'<marc:controlfield tag="001">([^<]+)</marc:controlfield>',
                                      r'<marc:controlfield tag="001">' + mtag001 + '</marc:controlfield>',
                                      str(outputTag010508Xml))
                        ftag = re.sub(r'<marc:controlfield tag="005">([^<]+)</marc:controlfield>',
                                      r'<marc:controlfield tag="005">' + mtag005 + '</marc:controlfield>', str(ftag))
                        ftag = re.sub(r'<marc:controlfield tag="008">([^<]+)</marc:controlfield>',
                                      r'<marc:controlfield tag="008">' + str(mtag008) + '</marc:controlfield>', str(ftag))
                        read_ini_config.writeFile(tempPath + "forFinalOutput.txt", ftag)
                        read_ini_config.writeFileWrite(tempPath + "temp2.txt", "")
                        read_ini_config.writeFileWrite(tempPath + "output3.txt", "")
                        return
                    else:
                        # continue
                        read_ini_config.writeFileWrite(tempPath + "temp2.txt", "")
                        #ftag = read_ini_config.readFile(tempPath + "output3.txt")
                        #read_ini_config.writeFile(tempPath + "forFinalOutput.txt", ftag)
                        #read_ini_config.writeFileWrite(tempPath + "temp2.txt", "")
                        #read_ini_config.writeFileWrite(tempPath + "output3.txt", "")
                        #return
                # read_ini_config.writeFileWrite(tempPath + "temp2.txt", "")
                xmlFile.close()
    if title_counter == 0:
        read_ini_config.writeFile(tempPath + "MergeMinimalCollection.log",str(datetime.now()) + ": Record Title [" + fromOutputValue + "] is not found in the Trnsmitted Minimal files\r\n")
    progress(70)
    outputTag010508XmlNo = read_ini_config.readFile(tempPath + "output3.txt")
    read_ini_config.writeFile(tempPath + "forFinalOutput.txt", outputTag010508XmlNo)
    read_ini_config.writeFileWrite(tempPath + "temp2.txt", "")
    read_ini_config.writeFileWrite(tempPath + "output3.txt", "")


def searchGetTagInOutput():
    global tag001, tag005, tag008, mtag001, mtag005, mtag008, outputValueP, outputValueB, outputValueN, outputValue7008, outputValue7009, outputValue773w
    outDirs010508 = os.listdir(outputPathTextLine.text())
    for outputFile in outDirs010508:
        isFile = os.path.isfile(outputPath + outputFile)
        if not isFile:
            continue
        outputPerRecord = read_ini_config.readLinesOfFile(outputPathTextLine.text(), outputFile)
        for outputLine in outputPerRecord:
            read_ini_config.writeFile(tempPath + "output3.txt", outputLine)
            logViewer.appendPlainText(str(datetime.now()) + ": Searching subfield in the output file...")
            QtGui.QGuiApplication.processEvents()
            if outputLine == "  </marc:record>\n" or outputLine == "</marc:record>\n":
                with open(tempPath + "output3.txt", encoding='utf-8') as outputXmlFile:
                    outputXmlFile = outputXmlFile.read()
                    outputXmlFile = re.sub(r'\[', 'lbacket;', str(outputXmlFile))
                    outputXmlFile = re.sub(r'\]', 'rbacket;', str(outputXmlFile))
                    outputXmlFile = re.sub(r'\(', 'lparent;', str(outputXmlFile))
                    outputXmlFile = re.sub(r'\)', 'rparent;', str(outputXmlFile))
                    outputXmlFile = re.sub(r'\?', 'qmark;', str(outputXmlFile))
                    tag001out = re.search(r'<marc:controlfield tag="001">([^<]+)</marc:controlfield>', str(outputXmlFile))
                    tag001valueout = tag001out.group(1)
                    getoutputSubFieldValue = re.search(
                        r'<marc:datafield tag="245"[^>]+>[^<]*<marc:subfield code="a">([^<]+)</marc:subfield>',
                        str(outputXmlFile))
                    getoutputSubFieldValueN = re.search(
                        r'<marc:datafield tag="245"[^>]+>[^\*]*<marc:subfield code="n">([^<]+)</marc:subfield>',
                        str(outputXmlFile))
                    getoutputSubFieldValueP = re.search(
                        r'<marc:datafield tag="245"[^>]+>[^\*]*<marc:subfield code="p">([^<]+)</marc:subfield>',
                        str(outputXmlFile))
                    getoutputSubFieldValueB = re.search(
                        r'<marc:datafield tag="245"[^>]+>[^<]+<marc:subfield code="a">[^<]+</marc:subfield>[^<]+<marc:subfield code="b">([^<]+)</marc:subfield>',
                        str(outputXmlFile))
                    getoutputSubFieldValue7008 = re.search(
                        r'<marc:datafield tag="700"[^>]+>[^<]*<marc:subfield code="8">([^<]+)</marc:subfield>',
                        str(outputXmlFile))
                    getoutputSubFieldValue7009 = re.search(
                        r'<marc:datafield tag="700"[^>]+>[^\*]*<marc:subfield code="9">([^<]+)</marc:subfield>',
                        str(outputXmlFile))
                    getoutputSubFieldValue773w = re.search(
                        r'<marc:datafield tag="773"[^>]+>[^<]*<marc:subfield code="w">([^<]+)</marc:subfield>',
                        str(outputXmlFile))
                    if getoutputSubFieldValue is None:
                        pass
                    else:
                        if getoutputSubFieldValueN:
                            outputValueN = getoutputSubFieldValueN.group(1)
                            outputValueN = re.sub(r'lbacket;', '[', str(outputValueN))
                            outputValueN = re.sub(r'rbacket;', ']', str(outputValueN))
                            outputValueN = re.sub(r'lparent;', '(', str(outputValueN))
                            outputValueN = re.sub(r'rparent;', ')', str(outputValueN))
                            outputValueN = re.sub(r'qmark;', '?', str(outputValueN))
                        else:
                            outputValueN = ""
                        if getoutputSubFieldValueP:
                            outputValueP = getoutputSubFieldValueP.group(1)
                            outputValueP = re.sub(r'lbacket;', '[', str(outputValueP))
                            outputValueP = re.sub(r'rbacket;', ']', str(outputValueP))
                            outputValueP = re.sub(r'lparent;', '(', str(outputValueP))
                            outputValueP = re.sub(r'rparent;', ')', str(outputValueP))
                            outputValueP = re.sub(r'qmark;', '?', str(outputValueP))
                        else:
                            outputValueP = ""
                        if getoutputSubFieldValueB:
                            outputValueB = getoutputSubFieldValueB.group(1)
                            outputValueB = re.sub(r'lbacket;', '[', str(outputValueB))
                            outputValueB = re.sub(r'rbacket;', ']', str(outputValueB))
                            outputValueB = re.sub(r'lparent;', '(', str(outputValueB))
                            outputValueB = re.sub(r'rparent;', ')', str(outputValueB))
                            outputValueB = re.sub(r'qmark;', '?', str(outputValueB))
                        else:
                            outputValueB = ""
                        if getoutputSubFieldValue7008:
                            outputValue7008 = getoutputSubFieldValue7008.group(1)
                            outputValue7008 = re.sub(r'lbacket;', '[', str(outputValue7008))
                            outputValue7008 = re.sub(r'rbacket;', ']', str(outputValue7008))
                            outputValue7008 = re.sub(r'lparent;', '(', str(outputValue7008))
                            outputValue7008 = re.sub(r'rparent;', ')', str(outputValue7008))
                            outputValue7008 = re.sub(r'qmark;', '?', str(outputValue7008))
                            outputValue7008 = re.sub(r' ', '', str(outputValue7008))
                        else:
                            outputValue7008 = ""
                        if getoutputSubFieldValue7009:
                            outputValue7009 = getoutputSubFieldValue7009.group(1)
                            outputValue7009 = re.sub(r'lbacket;', '[', str(outputValue7009))
                            outputValue7009 = re.sub(r'rbacket;', ']', str(outputValue7009))
                            outputValue7009 = re.sub(r'lparent;', '(', str(outputValue7009))
                            outputValue7009 = re.sub(r'rparent;', ')', str(outputValue7009))
                            outputValue7009 = re.sub(r'qmark;', '?', str(outputValue7009))
                        else:
                            outputValue7009 = ""
                        if getoutputSubFieldValue773w:
                            outputValue773w = getoutputSubFieldValue773w.group(1)
                            outputValue773w = re.sub(r'lbacket;', '[', str(outputValue773w))
                            outputValue773w = re.sub(r'rbacket;', ']', str(outputValue773w))
                            outputValue773w = re.sub(r'lparent;', '(', str(outputValue773w))
                            outputValue773w = re.sub(r'rparent;', ')', str(outputValue773w))
                            outputValue773w = re.sub(r'qmark;', '?', str(outputValue773w))
                        else:
                            outputValue773w = ""
                        outputValue = getoutputSubFieldValue.group(1)
                        outputValue = re.sub(r'lbacket;', '[', str(outputValue))
                        outputValue = re.sub(r'rbacket;', ']', str(outputValue))
                        outputValue = re.sub(r'lparent;', '(', str(outputValue))
                        outputValue = re.sub(r'rparent;', ')', str(outputValue))
                        outputValue = re.sub(r'qmark;', '?', str(outputValue))

                        getTag010508(outputValue, tag001valueout)
        finaloutput = read_ini_config.readFile(tempPath + "forFinalOutput.txt")
        read_ini_config.writeFileWrite(outputPathTextLine.text() + outputFile, finaloutput + "</marc:collection>")
        logViewer.appendPlainText(str(datetime.now()) + ": Saving updated output tag01, tag05 and tag08...")
        QtGui.QGuiApplication.processEvents()
        read_ini_config.writeFileWrite(tempPath + "temp2.txt", "")
        read_ini_config.writeFileWrite(tempPath + "output3.txt", "")
        read_ini_config.writeFileWrite(tempPath + "forFinalOutput.txt", "")
    progress(60)


def findMarcSubFieldInMinimal(subFieldValue):
    global checkifExistInMinimal
    logViewer.appendPlainText(str(datetime.now()) + ": Finding Sub Field Value in Minimal File...")
    QtGui.QGuiApplication.processEvents()
    mPath = minimalPath.text()
    dirs = os.listdir(mPath)
    for mFile in dirs:
        readMinimalFile = open(mPath + mFile, encoding='utf-8')
        checkifExistInMinimal = re.search(subFieldValue, str(readMinimalFile))
        if checkifExistInMinimal is None:
            return checkifExistInMinimal
        valuesFound = 0
        for mLines in readMinimalFile:
            mLines = re.sub(r'\[', 'lbacket;', str(mLines))
            mLines = re.sub(r'\]', 'rbacket;', str(mLines))
            mLines = re.sub(r'\(', 'lparent;', str(mLines))
            mLines = re.sub(r'\)', 'rparent;', str(mLines))
            mLines = re.sub(r'\?', 'qmark;', str(mLines))
            mLines = re.sub(r'\"', 'quote;', str(mLines))
            subFieldValue = re.sub(r'\[', 'lbacket;', str(subFieldValue))
            subFieldValue = re.sub(r'\]', 'rbacket;', str(subFieldValue))
            subFieldValue = re.sub(r'\(', 'lparent;', str(subFieldValue))
            subFieldValue = re.sub(r'\)', 'rparent;', str(subFieldValue))
            subFieldValue = re.sub(r'\?', 'qmark;', str(subFieldValue))
            subFieldValue = re.sub(r'\"', 'quote;', str(subFieldValue))
            mLines = re.search(subFieldValue, str(mLines))  # read sub field value
            if mLines:
                # storeMinimalFile = open(mPath + mFile, mode='r+')
                mxmlSoup = BeautifulSoup(readMinimalFile, 'html.parser')
                # mrepElemList = mxmlSoup.find_all('marc:record')
                mainTag = mxmlSoup.find('marc:subfield', {'code': 'a'})
                # tag001 = mxmlSoup.find(tag="001")
                # tag001 = re.sub(r'<marc:controlfield tag="001">([^<]+)</marc:controlfield>', r'\1', str(tag001))
                # tag005 = mxmlSoup.find(tag="005")
                # tag005 = re.sub(r'<marc:controlfield tag="005">([^<]+)</marc:controlfield>', r'\1', str(tag005))
                # tag008 = mxmlSoup.find(tag="008")
                # tag008 = re.sub(r'<marc:controlfield tag="008">([^<]+)</marc:controlfield>', r'\1', str(tag008))

                mfindAtttrTag150 = mxmlSoup.find(tag="150")
                if mfindAtttrTag150 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag150)
                    valuesFound = valuesFound + 1
                mfindAtttrTag151 = mxmlSoup.find(tag="151")
                if mfindAtttrTag151 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag151)
                    valuesFound = valuesFound + 1
                mfindAtttrTag504 = mxmlSoup.find(tag="504")
                if mfindAtttrTag504 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag504)
                    valuesFound = valuesFound + 1
                mfindAtttrTag546 = mxmlSoup.find(tag="546")
                if mfindAtttrTag546 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag546)
                    valuesFound = valuesFound + 1
                mfindAtttrTag580 = mxmlSoup.find(tag="580")
                if mfindAtttrTag580 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag580)
                    valuesFound = valuesFound + 1
                mfindAtttrTag600 = mxmlSoup.find(tag="600")
                if mfindAtttrTag600 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag600)
                    valuesFound = valuesFound + 1
                mfindAtttrTag610 = mxmlSoup.find(tag="610")
                if mfindAtttrTag610 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag610)
                    valuesFound = valuesFound + 1
                mfindAtttrTag611 = mxmlSoup.find(tag="611")
                if mfindAtttrTag611 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag611)
                    valuesFound = valuesFound + 1
                mfindAtttrTag630 = mxmlSoup.find(tag="630")
                if mfindAtttrTag630 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag630)
                    valuesFound = valuesFound + 1
                mfindAtttrTag650 = mxmlSoup.find(tag="650")
                if mfindAtttrTag650 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag650)
                    valuesFound = valuesFound + 1
                mfindAtttrTag651 = mxmlSoup.find(tag="651")
                if mfindAtttrTag651 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag651)
                    valuesFound = valuesFound + 1
                mfindAtttrTag655 = mxmlSoup.find(tag="655")
                if mfindAtttrTag655 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag655)
                    valuesFound = valuesFound + 1
                mfindAtttrTag690 = mxmlSoup.find(tag="690")
                if mfindAtttrTag690 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag690)
                    valuesFound = valuesFound + 1
                mfindAtttrTag693 = mxmlSoup.find(tag="693")
                if mfindAtttrTag693 is not None:
                    read_ini_config.writeFile(tempPath + "attrtag.txt", mfindAtttrTag693)
                    valuesFound = valuesFound + 1

                break
        logViewer.appendPlainText(str(datetime.now()) + ": 0 Values Found...")
        QtGui.QGuiApplication.processEvents()
        readMinimalFile.close()
    return


def getMinimalFullDetails(value):
    logViewer.appendPlainText(str(datetime.now()) + ": Get Minimal in Full Indexing file...")
    QtGui.QGuiApplication.processEvents()
    readTempMinimalFile = open(tempPath + "minimalText.txt", "r")
    for tempMinimalFile in readTempMinimalFile:
        saveToFileMinimal(tempMinimalFile)
        if tempMinimalFile == "</marc:record>\n":
            tempMinimalText = open(tempPath + "tempMinimal.txt", "r")
            tempMinimalTextRead = tempMinimalText.read()
            findCode = re.search(value, tempMinimalTextRead)
            if findCode:
                cont150 = 0
                for minimalItem in tempMinimalText:
                    if cont150 == 0:
                        findDataField = re.search(r'<marc:datafield tag="150"[^>]+>', str(minimalItem))
                        if findDataField:
                            read_ini_config.writeFile(tempPath + "dataFields.txt", minimalItem)
                    else:
                        read_ini_config.writeFile(tempPath + "dataFields.txt", minimalItem)
                        cont150 == 1

            else:
                read_ini_config.writeFileWrite(tempPath + "tempMinimal.txt", "r")
            tempMinimalText.close()
    readTempMinimalFile.close()
    return


def saveToFile(value):
    read_ini_config.writeFile(tempPath + "temp.txt", value)
    return


def saveToFileMinimal(value):
    read_ini_config.writeFile(tempPath + "tempMinimal.txt", value)


def saveToFileCompile(value):
    read_ini_config.writeFile(tempPath + "\\output.txt", value)
    return


def showDialog(textMessage, messageTitle):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(textMessage)
    msg.setWindowTitle(messageTitle)
    msg.setModal(True)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.exec_()
    return


def progress(completed):
    completed += 0.0001
    pBar.setValue(int(completed))
    # completed = 0
    return


# connect button
browseMinimalPath.clicked.connect(manualBrowseMinimalPath)
browseFullIndexingPath.clicked.connect(manualBrowseFullPath)
browseOutputPath.clicked.connect(manualBrowseOutputPath)
goMergeButton.clicked.connect(startMergingFiles)

# remove temp files
removeTempFiles()

# Show the window and run the app
win.show()
app.exec_()

import xml.etree.ElementTree as ET
import csv
from os import walk


#-----------------------------------------------------------------------------------------------------------------------
class folder(object):
    path = ""

    def __init__(self, p):
        self.path = p


    def getFileNames(self):
        f = []
        for (dirpath, dirnames, filenames) in walk(self.path):
            f.extend(filenames)
            break
        return f


    def getFilesByExtension(self, extensions):
        flist = []
        files = self.getFileNames()
        for f in files:
            for ext in extensions:
                if (f.endswith(ext)):
                    flist.append(f)
        return flist


    def getXMLFiles(self):
        return self.getFilesByExtension(["xml"])


    def getDITAFiles(self):
        return self.getFilesByExtension(["dita"])
#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------
def loadXML(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root


def printAttribute(elem, a):
    return a + "=" + elem.attrib[a]


def getAttributes(e):
    attributes = ""
    for a in e.attrib:
        attributes = attributes + printAttribute(e,a) + ":"
    return attributes.rstrip(":")


def stripNewLine(s):
    if (s == None):
        return ""
    return s.replace("\n","")


def isEmpty(t):
    if(t == None):
        return True
    return stripNewLine(t).strip() == ""


def hasText(e):
    if(isEmpty(e.text)):
        return False
    return True


def getInnerText(e):
    # t = ET.tostring(e, "us-ascii", "text").decode()
    return "".join(e.itertext())


def getCleanText(e):
    t = ""
    if(hasText(e)):
        t = getInnerText(e)
    return stripNewLine(t)


def getEntry(tag,text,attributes):
    entry = ",".join([tag,text,attributes])
    return entry


def printElement(o, e):
    tag = stripNewLine(e.tag)
    text = getCleanText(e)
    attrib = getAttributes(e)
    printRow(o, getEntry(tag,text,attrib))


def getHeaders():
    return ",".join(["TAG","TEXT","ATTRIBUTES"])


def iterateElements(o, r):
    for e in r.iter():
        if(hasText(e)):
            printElement(o, e)


def traverseElem(e):
    printElement(e)
    for subElem in e:
        traverseElem(subElem)


def writeln(file, string):
    file.write(string)
    file.write('\n')


def printRow(output, row):
    print(row)
    if (output != None):
        writeln(output,row)


def xml2csv(xml, csv):
    #Open output file
    f = open(csv, 'wt')

    #Load input file
    root = loadXML(xml)

    try:
        #Write headers
        printRow(f,getHeaders())

        #Traverse XML tree
        iterateElements(f, root)

    except Exception as err:
        print(err)
    finally:
        f.close()
#-----------------------------------------------------------------------------------------------------------------------

#Convert all xml / dita files in local folder
def run():
    files = folder(".").getDITAFiles()
    print(files)
    for f in files:
        xml2csv(f,f+".csv")


def main():
    run()
    #xml2csv("CalculatingTime.dita","CalculatingTime.csv")


main()


#-----------------------------------------------------------------------------------------------------------------------
class myString(object):
    s = ""

    def __init__(self, s):
        self.s = s


    @staticmethod
    def stripNewLine(s):
        if (s == None):
            return ""
        return s.replace("\n", "")

    @staticmethod
    def isEmpty(t):
        if (t == None):
            return True
        return stripNewLine(t).strip() == ""

    @staticmethod
    def hasText(e):
        if (isEmpty(e.text)):
            return False
        return True



#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------
class xmlFile(object):
    inputFile = ""
    output = None
    root = None


    def __init__(self, filename):
        self.inputFile = filename
        self.load()


    @staticmethod
    def loadXML(filename):
        return ET.parse(filename).getroot()


    def load(self):
        self.root = loadXML(self.inputFile)


    @staticmethod
    def xml2csv(xml, csv):
        # Open output file
        f = open(csv, 'wt')

        # Load input file
        root = loadXML(xml)

        try:
            # Write headers
            printRow(f, getHeaders())

            # Traverse XML tree
            iterateElements(f, root)

        except Exception as err:
            print(err)
        finally:
            f.close()


    def toCSV(self):
        # Open output file
        outputFile = self.inputFile + ".csv"
        self.output = open(outputFile, 'wt')

        try:
            # Write headers
            printRow(self.output, getHeaders())

            # Traverse XML tree
            iterateElements(self.output, self.root)

        except Exception as err:
            print(err)
            self.output = None
        finally:
            self.output.close()
            self.output = None


    def printAttribute(elem, a):
        return a + "=" + elem.attrib[a]

    def getAttributes(e):
        attributes = ""
        for a in e.attrib:
            attributes = attributes + printAttribute(e, a) + ":"
        return attributes.rstrip(":")



    def getInnerText(e):
        # t = ET.tostring(e, "us-ascii", "text").decode()
        return "".join(e.itertext())

    def getCleanText(e):
        t = ""
        if (hasText(e)):
            t = getInnerText(e)
        return stripNewLine(t)

    def getEntry(tag, text, attributes):
        entry = ",".join([tag, text, attributes])
        return entry

    def printElement(o, e):
        tag = stripNewLine(e.tag)
        text = getCleanText(e)
        attrib = getAttributes(e)
        printRow(o, getEntry(tag, text, attrib))


    @staticmethod
    def getHeaders():
        return ",".join(["TAG", "TEXT", "ATTRIBUTES"])


    def iterateElements(o, r):
        for e in r.iter():
            if (hasText(e)):
                printElement(o, e)


    @staticmethod
    def writeln(file, string):
        file.write(string)
        file.write('\n')


    def printRow(self, row):
        print(row)
        if (self.output != None):
            writeln(self.output, row)

#-----------------------------------------------------------------------------------------------------------------------


#TODO
#1. XML 2 CSV with console printout -- done
#2. convert all files in folder -- done
#3. uses classes to encapsulate
#4. refactor printAttributes
#4. documentation + README to share on github
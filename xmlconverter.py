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
class myString(object):
    s = ""

    def __init__(self, s):
        self.s = s

    def get(self):
        return self.s


    def stripNewLine(self):
        if (self.s == None):
            return ""
        return self.s.replace("\n", "")

    def isEmpty(self):
        if (self.s == None):
            return True
        return self.stripNewLine().strip() == ""

#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------
class myElement(object):
    e= None

    def __init__(self,e):
        self.e = e

    def get(self):
        return self.e


    # -------------------- end --------------------

    def hasText(self):
        if(myString(self.e.text).isEmpty()):
            return False
        return True

    def getInnerText(self):
        # t = ET.tostring(e, "us-ascii", "text").decode()
        return "".join(self.e.itertext())

    def getCleanText(self):
        t = ""
        if(self.hasText()):
            t = self.getInnerText()
        return myString(t).stripNewLine()


    def getKeyValuePair(self,a):
        return "=".join([a,self.e.attrib[a]])


    def getAttributes(self):
        attributes = []
        for a in self.e.attrib:
            attributes.append(self.getKeyValuePair(a))
        return ":".join(attributes)


    def getEntry(self):
        tag = myString(self.e.tag).stripNewLine()
        text = self.getCleanText()
        attrib = self.getAttributes()
        return ",".join([tag,text,attrib])


#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------
class xmlFile(object):
    inputFile = ""
    output = None
    root = None


    def __init__(self, filename):
        self.inputFile = filename
        self.load()


    def load(self):
        self.root = self.loadXML(self.inputFile)


    @staticmethod
    def loadXML(filename):
        return ET.parse(filename).getroot()


    @staticmethod
    def writeln(file, string):
        file.write(string)
        file.write('\n')


    @staticmethod
    def getHeaders():
        return ",".join(["TAG", "TEXT", "ATTRIBUTES"])


    def printRow(self, row):
        print(row)
        if (self.output != None):
            self.writeln(self.output, row)


    def iterateElements(self):
        for e in self.root.iter():
            me = myElement(e)
            if (me.hasText()):
                self.printRow(me.getEntry())


    def toCSV(self):
        # Open output file
        outputFile = self.inputFile + ".csv"
        self.output = open(outputFile, 'wt')

        try:

            print("==> open " + outputFile)

            # Write headers
            self.printRow(self.getHeaders())

            # Traverse XML tree
            self.iterateElements()

            print("==> close " + outputFile)

        except Exception as err:
            print(err)
        finally:
            self.output.close()
            self.output = None

#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------

#Convert all xml / dita files in local folder
def convertFolder(path):
    files = folder(path).getDITAFiles()
    print(files)
    for f in files:
        xmlFile(f).toCSV()


def main():
    convertFolder(".")


main()



#TODO
#4. documentation + README to share on github
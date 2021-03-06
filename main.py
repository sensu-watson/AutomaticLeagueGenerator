#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import re
import copy
import json
import csv


class Compornent:
    filename = ''
    itemname = []
    items = {}
    itemcounter = {}
    itemlength = {}
    replacer = {}
    roopcounter = 1
    
    def __init__(self, filename):
        self.filename = filename
        self.itemname = []
        self.items = {}
        self.itemcounter = {}
        self.itemlength = {}
        self.replacer = {}
        self.roopcounter = 1

    def appenditem(self, itemname, itemlist):
        self.itemname.append(itemname)
        self.items[itemname] = itemlist
        self.itemcounter[itemname] = 0
        self.itemlength[itemname] = len(itemlist)

    def appendreplace(self, itemname, replacelist):
        self.replacer[itemname] = replacelist
        
    def getitem(self, itemname):
        i = self.itemcounter[itemname]
        length = self.itemlength[itemname]
        if i >= length:
            return ''
        self.itemcounter[itemname] += 1
        retitem = self.items[itemname][i]
        if itemname in self.replacer:
            for t in self.replacer[itemname]:
                retitem = retitem.replace(t[0], t[1])
        return retitem

    def resetalliterator(self, itemname):
        for item in self.itemname:
            self.itemcounter[item] = 0
        self.roopcounter = 0

    def getroop(self):
        ret = self.roopcounter
        self.roopcounter += 1
        return str(ret)

    def isallitemoutput(self):
        isdone = True
        for item in self.itemname:
            counter = self.itemcounter[item]
            length = self.itemlength[item]
            if counter < length:
                isdone = False
                break
        return isdone

            
class Token:
    isString = False
    isTag = False
    isGeneral = False
    isNormal = False
    isRoopStart = False
    isRoopStop = False
    string = ''
    tagname = ''
    csvfile = ''
    csvtag = ''

    def __init__(self, tokentype, tokenstring):
        string = tokenstring.replace('[', '').replace(']', '')
        self.string = string
        
        if tokentype == 'roopstarttag':
            self.isRoopStart = True
            self.isTag = True
            temp = string.split(' ')
            self.csvfile = temp[1].replace("'", '')
        elif tokentype == 'roopstoptag':
            self.isRoopStop = True
            self.isTag = True
        elif tokentype == 'normaltag':
            self.isTag = True
            self.isNormal = True
            temp = string.split('.')
            self.csvfile = temp[0] + '.csv'
            self.csvtag = temp[1]
        elif tokentype == 'generaltag':
            self.isTag = True
            self.isGeneral = True
            self.csvfile = '__general.csv'
            self.csvtag = string
        else:
            self.isString = True
            
    def tokenprint(self):
        print(self.string, end="")
        
    def gettokenstring(self):
        return self.string

    def getcsvfileandtag(self):
        return self.csvfile, self.csvtag
        
def getListFromCSV(csvfilename):
    """Get list from csvfile."""

    csvlist = []
    with codecs.open(csvfilename, 'r', 'cp932') as f:
        reader = csv.reader(f)
        for row in reader:
            csvlist.append(row)
    #f.close
    return csvlist

def getDictionaryFromCSVInTopTitle(csvfilename):
    """Get dictionary from csvfile."""
    
    csvlist = getListFromCSV(csvfilename)
    csvdic  = csvlist2csvdicInTopTitle(csvlist)
    return csvdic

def getDictionaryFromCSVInSideTitle(csvfilename):
    """Get dictionary from csvfile."""
    
    csvlist = getListFromCSV(csvfilename)
    csvdic  = csvlist2csvdicInSideTitle(csvlist)
    return csvdic

def csvlist2csvdicInTopTitle(beforelist):
    csvtitle = []
    csvdictionary = {}
    
    for title in beforelist[0]:
        csvtitle.append(title)
        csvdictionary[title] = []

    for row in beforelist[1:]:
        for i, cell in enumerate(row):
            csvdictionary[csvtitle[i]].append(cell)
    

    return csvdictionary

def csvlist2csvdicInSideTitle(beforelist):
    csvtitle = []
    csvdictionary   = {}
    titledictionary = {}
    beforelist.pop(0)
    
    for row in beforelist:
        title = row.pop(0)
        data = row.pop(0)
        csvdictionary[title] = data
    return csvdictionary

def removeStartPeriodFileFromList(filelist):
    returnlist = []
    for filename in filelist:
        if not (filename.startswith('.') or filename.startswith('_')):
            returnlist.append(filename)
    return returnlist

def getCsvData(inputdir, replacedir):
    filelist = os.listdir(inputdir)
    filelist = removeStartPeriodFileFromList(filelist)
    generalDicts = getDictionaryFromCSVInSideTitle(inputdir + '__general.csv')
    
    compornents = {}
    for filename in filelist:
        csv = getDictionaryFromCSVInTopTitle(inputdir + filename)
        compornent = Compornent(filename)
        for k, v in csv.items():
            compornent.appenditem(k, v)
        compornents[filename] = compornent

    filelist = os.listdir(replacedir)
    filelist = removeStartPeriodFileFromList(filelist)
    for filename in filelist:
        csv = getDictionaryFromCSVInSideTitle(replacedir + filename)
        temp = filename.split('.')
        compornentfile = temp[0] + '.csv'
        compornentitem = temp[1]
        appendlist = []
        for k,v in csv.items():
            appendlist.append((k,v))
        compornents[compornentfile].appendreplace(compornentitem, appendlist)
    
    return generalDicts, compornents

def getHtmlData(htmlfile):
    f = codecs.open(htmlfile, 'r', 'shift_jis')
    html = f.read()
    f.close()

    tagnamelist = []
    tagpositionlist = []
    StartPattern = r"\[\[([^]]*)]\]"
    reStartPattern = re.compile(StartPattern)
    matchStart = re.finditer(reStartPattern,html)
    for match in matchStart:
        tagnamelist.append(match.group(1))
        tagpositionlist.append(match.span())
    
    
    tokenlist = []
    
    len(html)
    point = 0
    for tagposition in tagpositionlist:
        string = html[point:tagposition[0]]
        tokenlist.append(Token('string', string))
        
        string = html[tagposition[0]:tagposition[1]]
        if re.match('\[\[ROOP', string):
            tokenlist.append(Token('roopstarttag', string))
        elif re.match('\[\[/ROOP', string):
            tokenlist.append(Token('roopstoptag', string))
        elif string.find('.') == -1:
            tokenlist.append(Token('generaltag', string))
        else:
            tokenlist.append(Token('normaltag', string))
        
        point = tagposition[1]
    tokenlist.append(Token('string', html[point:len(html)]))

    return tokenlist

def buildstructure(i, end, tokenlist, h):
    buildlist = []
    while True:
        if tokenlist[i].isRoopStop:
            if h == 0:
                print('error1')
            i+=1
            break
        elif tokenlist[i].isRoopStart:
            buildlist.append(tokenlist[i])
            i+=1
            buildtemplist, i = buildstructure(i, end, tokenlist, h + 1)
            buildlist.append(buildtemplist)
        else:
            buildlist.append(tokenlist[i])
            i+=1
        if i >= end:
            if h != 0:
                print('error2')
            break
    return buildlist, i

def generatestring(tokenstructure, generalDicts, compornents, h, rooptagname):
    i = 0
    end = len(tokenstructure)
    genstring = ''
    while True:
        token = tokenstructure[i]
        if token.isString:
            genstring += token.gettokenstring()
            i+=1
        elif token.isGeneral:
            filename, tagname = token.getcsvfileandtag()
            genstring += generalDicts[tagname]
            i+=1
        elif token.isNormal:
            filename, tagname = token.getcsvfileandtag()
            #print(tagname)
            if tagname == '__roopcount':
                appendstring = compornents[filename].getroop()
            else:
                appendstring = compornents[filename].getitem(tagname)
            genstring += appendstring
            i+=1
        elif token.isRoopStart:
            i+=1
            roopstructure = tokenstructure[i]
            genstring += generatestring(roopstructure, generalDicts, compornents, h + 1, token.csvfile)
            i+=1
        elif token.isRoopStop:
            i+=1
            break
        else:
            print('error3')
            break
        if i >= end:
            if rooptagname is None:
                break
            else:
                if compornents[rooptagname].isallitemoutput():
                    break
                else:
                    i = 0
    return genstring

def outputtofile(outputfile, outputstring):
    f = codecs.open(outputfile, 'w', 'shift_jis')
    f.write(outputstring)
    f.close()

def selecttemplate(sourcehtml_dir):
    source_list = os.listdir(sourcehtml_dir)

    if len(source_list) == 0:
        print('テンプレートがありません．')
        forcedtermination()

    if len(source_list) == 1:
        return sourcehtml_dir + source_list[0]
    
    print('テンプレートファイルが複数あります．\n利用するテンプレートの番号を入力してください．')
    for i, filename in enumerate(source_list):
        print(str(i) + ' : ' + filename)
        
    num = int(input('番号 : '))

    if num < 0 or len(source_list) <= num:
        print('該当番号のテンプレートはありません．')
        forcedtermination()

    return sourcehtml_dir + source_list[num]

def forcedtermination():
    print('強制終了します．')
    sys.exit()

if __name__ == '__main__':
    inputdir = 'input_csv/'
    replacedir = 'tag_replace_csv/'
    sourcehtml_dir = 'source/'
    outputfile = 'generate/generate.html'

    sourcehtml = selecttemplate(sourcehtml_dir)

    generalDicts, compornents = getCsvData(inputdir, replacedir)
    tokenlist = getHtmlData(sourcehtml)

    i = 0
    h = 0
    end = len(tokenlist)
    tokenstructure, i = buildstructure(i, end, tokenlist, h)
    
    h = 0
    genstring = generatestring(tokenstructure, generalDicts, compornents, h, None)
    outputtofile(outputfile, genstring)

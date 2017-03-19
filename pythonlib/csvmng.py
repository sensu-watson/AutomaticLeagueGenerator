#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import csv
import codecs

def getListFromCSV(csvfilename):
    """Get list from csvfile."""

    csvlist = []
    with codecs.open(csvfilename, 'r', 'shift_jis') as f:
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

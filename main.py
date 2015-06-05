__author__ = 'neocaine'
#!/usr/bin/env python2.7

# -*- coding: utf-8 -*-
import os
import pymssql
import logging
from datetime import datetime, tzinfo, timedelta
import shutil, zipfile
from rtf import Rtf2Txt




# ...
# Started on: 2015.01.01
# Authors: Filatov Vladimir Olegovich
#          Konyaev Sergey Sergeevich
# =================================================
# Copyright 2015 Filatov Vladimir Olegovich
#                Konyaev Sergey Sergeevich
#
# This file is part of LyncLogsParser.
#
# ==================================================
#
# You can contact me at: neocaine@amneziainc.ru
# -----
# Description:
# 1
# 2
# 3
#
# ...
# =================================================

# ChangeLogs
# + Today Folder Deletion on every start
# + All except Today Folder Archiving to archive folder
# + RTF String Encoding (There is little bug with windows-1252 encoding)
#
# TODO Conferences Logs
# TODO Folders By Message Date not by Today date
#
#
# INSTALL
# Requirements
# http://sourceforge.net/projects/pyrtflib/ - For Lync 2013 RTF To PlainText Convertion
# https://github.com/pymssql/pymssql - For Working With MsSQL Database

#CONSTANTS
MSSQLHOST = "mssql"
MSSQLUSER = "pycharm"
MSSQLPASSWORD = "herePasswordToMSSQL"
MSSQLDATABASE = "LcsLog"
LOGSFOLDER = 'c:\LogsLync\\'
LOGGINGLEVEL = 10  # 'CRITICAL' : 50, 'ERROR' : 40, 'WARNING' : 30, 'INFO' : 20, 'DEBUG' : 10
ARCHIVEPATH= 'c:\LogsLync\\archive\\'
ARCHIVEFOLDERNAME = 'archive'

def rtfStringConvert(string):
    converter = Rtf2Txt
    resultString = converter.getTxt(string)
    return resultString


def zipdir(path, zip):
    logging.debug('_Function Called zipdir(path = %s, zip = %s)' % (path,zip))
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))


def ArchiveAllPreviousDates():
    logging.debug('_Function Called ArchiveAllPreviusDates()')
    try:
        os.stat(LOGSFOLDER)
    except:
        mkdir(LOGSFOLDER)

    sub = os.listdir(LOGSFOLDER)

    for i in range(len(sub)):
        if os.path.exists(ARCHIVEPATH + sub[i] + '.zip') \
                or sub[i] == ARCHIVEFOLDERNAME \
                or sub[i] == "%d.%d.%d" % (datenow.day, datenow.month, datenow.year):
            logging.warn(ARCHIVEPATH + sub[i] + '.zip' + " file Exists or filename is in exception")
        else:
            try:
                os.stat(ARCHIVEPATH)
            except:
                os.makedirs(ARCHIVEPATH)

            zipf = zipfile.ZipFile(ARCHIVEPATH + sub[i] + '.zip', 'w')
            zipdir(LOGSFOLDER + sub[i], zipf)
            zipf.close()


class Zone(tzinfo):

    def __init__(self, offset, isdst, name):
        self.offset = offset
        self.isdst = isdst
        self.name = name

    def utcoffset(self, dt):
            return timedelta(hours=self.offset) + self.dst(dt)

    def dst(self, dt):
            return timedelta(hours=1) if self.isdst else timedelta(0)

    def tzname(self, dt):
            return self.name

# GMT = Zone(0, False, 'GMT')
# GMT5 = Zone(+5, False, 'GMT')
# EST = Zone(-5, False, 'EST')


# print datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S %Z')
# print datetime.now(GMT).strftime('%m/%d/%Y %H:%M:%S %Z')
# print datetime.now(EST).strftime('%m/%d/%Y %H:%M:%S %Z')

# t = datetime.strptime('2011-01-21 02:37:21','%Y-%m-%d %H:%M:%S')
# t = t.replace(tzinfo=GMT)
# print t
# print t.astimezone(EST)


def setup_custom_logger(name):

    formatter = logging.basicConfig(format=u'%(filename)s '
                                     u'[LINE:%(lineno)d]# '
                                        u'%(levelname)-8s '
                                          u'[%(asctime)s] '
                                             u'%(message)s', level=LOGGINGLEVEL)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


def deleteAllFolderSetExceptToday():
    logging.debug('_Function Called deleteAllFolderSetExceptToday')
    try:
        sub = os.listdir(LOGSFOLDER)
        for i in range(len(sub)):
            if sub[i] == ARCHIVEFOLDERNAME or sub[i] == "%d.%d.%d" % (datenow.day, datenow.month, datenow.year):
                logging.warn('Cant Delete This Folder = %s' % sub[i])
            else:
                logging.debug(sub[i]," ", ARCHIVEFOLDERNAME)
                shutil.rmtree(LOGSFOLDER + sub[i])
    except:
        logging.warn('Cant Delete This Folder = %s with unknown reason' % sub[i])


def deleteTodayFolderSet(dateString):
    logging.debug('_Function Called deleteTodayFolderSet')
    try:

        dateString = LOGSFOLDER + '%d.%d.%d' % (datenow.day, datenow.month, datenow.year)
        logging.debug("Deleting Folder Tree at %s" % dateString)
        shutil.rmtree(dateString)
    except:
        logging.warn("Cant Delete Folder Tree at %s" % dateString)


#SetHTMLFormatWithTitle
def setHTMLHeaders(title):
    HTMLHEAD = """

    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>%s</title>
    </head>
    <body style="font-family: sans-serif; font-size: 11pt">
    <div style="margin-bottom: 1em;">
    """ % title
    return HTMLHEAD


#MakeDirsFullPath Recursive
def setDirNameAndCreate(name):
    logging.debug("_Function Called setDirNameAndCreate(name = %s)" % name)
    dir = os.path.dirname(LOGSFOLDER +"%d.%d.%d\%s\\" % ((datenow.day, datenow.month, datenow.year, name)))
    mkdir(dir)


#TouchFile Function
def touch(HTMLtitle,fname,ftext):
    logging.debug("_Function Called touch(HTMLtitle = %s, fname = %s, ftext = %s)" %  (HTMLtitle, fname, "()"))
    if os.path.exists(fname):
        os.utime(fname, None)
        with open(fname, 'a') as logfile:
            logfile.seek(0)
            logfile.write(ftext)
            logfile.close()
    else:
        open(fname, 'a').close()
        with open(fname, 'a') as logfile:
            logfile.seek(0)
            logfile.write(setHTMLHeaders(HTMLtitle))
            logfile.write(ftext)
            logfile.close()


#MakeDir Function
def mkdir(dir):
    logging.debug('_Function Called mkdir (dir = %s)' % dir)
    try:
        os.stat(dir)
    except:
        os.makedirs(dir)



logger = setup_custom_logger('root')
GMT = Zone(0, False, 'GMT')
GMT5 = Zone(+5, False, 'GMT')
EST = Zone(-5, False, 'EST')
datenow = datetime.now()
ArchiveAllPreviousDates()
deleteAllFolderSetExceptToday()
deleteTodayFolderSet("")

#print(MSSQLDATABASE)
GetAllUsersIDConnector=pymssql.connect(host=MSSQLHOST,
                                       user=MSSQLUSER,
                                       password=MSSQLPASSWORD,
                                       database=MSSQLDATABASE)

GetMessagesConnector=pymssql.connect(host=MSSQLHOST,
                                     user=MSSQLUSER,
                                     password=MSSQLPASSWORD,
                                     database=MSSQLDATABASE)

GetUserNameByIDConnector=pymssql.connect(host=MSSQLHOST,
                                         user=MSSQLUSER,
                                         password=MSSQLPASSWORD,
                                         database=MSSQLDATABASE)

GetAllUsersIDCursor   =  GetAllUsersIDConnector.cursor()
GetMessagesCursor     =  GetMessagesConnector.cursor()
GetUserNameByIDCursor =  GetUserNameByIDConnector.cursor()

GetAllUsersIDCursor.execute('Select FromId, ToId '
                            'from LcsLog.dbo.Messages '
                            'where MessageIdTime >= CAST(CURRENT_TIMESTAMP AS DATE) '
                            'order by MessageIdTime desc')

GetAllUsersIDCursorResult = GetAllUsersIDCursor.fetchall()

usersIDToNameDictionary = {}
usersDialogsDictionary  = {}

for i in range(len(GetAllUsersIDCursorResult)):

    GetUserNameByIDCursor.execute('Select UserUri '
                                  'from LcsLog.dbo.Users '
                                  'where UserId= %d',GetAllUsersIDCursorResult[i][0])

    usersIDToNameDictionary[GetAllUsersIDCursorResult[i][0]] = GetUserNameByIDCursor.fetchone()

    GetUserNameByIDCursor.execute('Select UserUri '
                                  'from LcsLog.dbo.Users '
                                  'where UserId= %d',GetAllUsersIDCursorResult[i][1])

    usersIDToNameDictionary[GetAllUsersIDCursorResult[i][1]] = GetUserNameByIDCursor.fetchone()

    usersDialogsDictionary[GetAllUsersIDCursorResult[i]] = str(usersIDToNameDictionary.get(GetAllUsersIDCursorResult[i][0]))
    #print(users1DoubleDictionary)
    setDirNameAndCreate(str(usersIDToNameDictionary.get(GetAllUsersIDCursorResult[i][0]))[3:-3])
    setDirNameAndCreate(str(usersIDToNameDictionary.get(GetAllUsersIDCursorResult[i][1]))[3:-3])

usersDialogsDictionaryCompleted = {}
logging.debug('Length of usersDialogsDictionary.keys() = %s' % len(usersDialogsDictionary.keys()))

for j in range(len(usersDialogsDictionary.keys())):
    logging.debug('J = %s From %s of usersDialogsDictionary.keys' %(j,len(usersDialogsDictionary.keys())))
    GetMessagesCursor.execute('Select MessageIdTime, FromId, ToId, Body, ContentTypeId '
                              'from LcsLog.dbo.Messages '
                              'where MessageIdTime >= CAST(CURRENT_TIMESTAMP AS DATE) '
                              'and FromId = %s '
                              'and ToId = %s '
                              'OR MessageIdTime >= CAST(CURRENT_TIMESTAMP AS DATE) '
                              'and ToId = %s '
                              'and FromId = %s '
                              'order by MessageIdTime asc' % (usersDialogsDictionary.keys()[j][0],
                                                              usersDialogsDictionary.keys()[j][1],
                                                              usersDialogsDictionary.keys()[j][0],
                                                              usersDialogsDictionary.keys()[j][1]))

    GetMessagesCursorResult = GetMessagesCursor.fetchall()
    logging.debug('Length of GetMessagesCursorResult = %s' % len(GetMessagesCursorResult))
    for i in range(len(GetMessagesCursorResult)):
        messageTimeConverted = GetMessagesCursorResult[i][0]
        messageTimeConverted = messageTimeConverted.replace(tzinfo=GMT)

        stringFromCursor = GetMessagesCursorResult[i][3]

        if (GetMessagesCursorResult[i][4] == 2):
            stringFromCursor = rtfStringConvert(stringFromCursor)
            print(stringFromCursor)

        #stringFromCursor = stringFromCursor.encode('windows-1251')

        stringForWritening = str(messageTimeConverted.astimezone(GMT5))[:-13] + \
                             " <strong>From: </strong>" + \
                             str(usersIDToNameDictionary.get(GetMessagesCursorResult[i][1]))[3:-18] + \
                             "<strong>To: </strong>" + \
                             str(usersIDToNameDictionary.get(GetMessagesCursorResult[i][2]))[3:-18] + \
                             "<br>" + \
                             stringFromCursor + \
                             "<br>"

        stringForMessageListWriteng = stringForWritening.encode('utf-8')

        TitleForFile = str(usersIDToNameDictionary.get(GetMessagesCursorResult[i][2]))[3:-18] + \
                       " to " + \
                       str(usersIDToNameDictionary.get(GetMessagesCursorResult[i][1]))[3:-18]

        if usersDialogsDictionaryCompleted.get(str(usersDialogsDictionary.keys()[j][0]) +
                str(usersDialogsDictionary.keys()[j][1])) or\
            usersDialogsDictionaryCompleted.get(str(usersDialogsDictionary.keys()[j][1]) +
                str(usersDialogsDictionary.keys()[j][0])):


            logging.debug("There are all messages for users = %s & %s skipping" %
                          (str(usersDialogsDictionary.keys()[j][0]),
                           str(usersDialogsDictionary.keys()[j][1])))
            break
            pass

        else:

            touch(TitleForFile, LOGSFOLDER + "%d.%d.%d\%s\\%s.html" % (datenow.day,
                                                                     datenow.month,
                                                                     datenow.year,
                                                                     str(usersIDToNameDictionary.get(GetMessagesCursorResult[i][1]))[3:-3],
                                                                     str(usersIDToNameDictionary.get(GetMessagesCursorResult[i][2]))[3:-3] ),
                                                                     stringForMessageListWriteng)

            touch(TitleForFile, LOGSFOLDER + "%d.%d.%d\%s\\%s.html" % (datenow.day,
                                                                     datenow.month,
                                                                     datenow.year,
                                                                     str(usersIDToNameDictionary.get(GetMessagesCursorResult[i][2]))[3:-3],
                                                                     str(usersIDToNameDictionary.get(GetMessagesCursorResult[i][1]))[3:-3] ),
                                                                     stringForMessageListWriteng)

    usersDialogsDictionaryCompleted[str(usersDialogsDictionary.keys()[j][0]) + str(usersDialogsDictionary.keys()[j][1])] = True

#!/usr/bin/env python3

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

file1 = drive.CreateFile()
file1.SetContentFile('test1.doc')
file1.Upload()
print('title: %s, filetype: %s' % (file1['title'], file1['mimeType']))

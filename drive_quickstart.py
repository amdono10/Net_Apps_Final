#!/usr/bin/env python3

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Test_Upload.txt'})
file1.SetContentString('We are putting in some text!')
file1.Upload()
print('title: %s, id: %s' % (file1['title'], file1['id']))

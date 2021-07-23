
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


import os

def drive_launch(): 
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive



def drive_upload(path, drive): 
    folder = drive.ListFile({'q': "title = 'San Jose' and trashed=false"}).GetList()[0]
    # this is set only for San Jose for now, but we will need to make it dynamic for other cities in the future
    for x in os.listdir(path):
        f = drive.CreateFile({'title': x, 'parents': [{'id': folder['id']}]})
        f.SetContentFile(os.path.join(path, x))
        f.Upload()
    f = None

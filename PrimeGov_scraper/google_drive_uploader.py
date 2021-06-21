from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

""" CAUTION:
Due to the nature of Google drive files, duplicate files will not be over-written but instead will be duplicated.
"""

local_path = './data'  # Path to local files to be uploaded.

# Path to remote G-Drive directory to upload files. Special note. this is a tag not a directory
g_path = 'PrimeGov.data'
file_list = os.listdir(local_path)

# Initiation
gauth = GoogleAuth()
# gauth.SaveCredentialsFile("mycreds.txt")  # use this to save a temporary credential for re-running
gauth.LoadCredentialsFile('mycreds.txt')
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

folder = drive.ListFile({'q': f"title = '{g_path}' and trashed=false"}).GetList()[0]  # find ID for g_path folder
print('Uploading file(s)')
for file in file_list:
    g_file = drive.CreateFile({'title': file, 'parents': [{'id': folder['id']}]})
    g_file.SetContentFile(os.path.join(local_path, file))
    g_file.Upload()
    g_file = None  # re-initialize variable to prevent known pydrive memory leak
    print('.', end='')
print()
print(f'{len(file_list)} file(s) uploaded.')

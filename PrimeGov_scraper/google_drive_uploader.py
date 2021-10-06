from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

""" CAUTION:
Due to the nature of Google drive files, duplicate files will not be over-written but instead will be duplicated.
"""


def uploader(path_to_files, google_drive_path, local_file_list):
    try:
        # Initiation
        gauth = GoogleAuth()
        # gauth.SaveCredentialsFile("mycreds.txt")  # use this to save a temporary credential for re-running
        gauth.LoadCredentialsFile()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        # find ID for g_path folder
        folder = drive.ListFile({'q': f"title = '{google_drive_path}' and trashed=false"}).GetList()[0]
        print('Uploading file(s)')
        for file in local_file_list:
            g_file = drive.CreateFile({'title': file, 'parents': [{'id': folder['id']}]})
            g_file.SetContentFile(os.path.join(path_to_files, file))
            g_file.Upload()
            g_file = None  # re-initialize variable to prevent known pydrive memory leak
            print('.', end='')
        print()
        print(f'{len(local_file_list)} file(s) uploaded.')
        return True

    except Exception:
        print('Upload failed')
        return False


from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


import os

def drive_launch(): 
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive



def get_city_folder(drive, current_city='sanjose'):
    """Creates a city folder if one does not exist and returns a city folder
    under the shared drive 'Cities'
    returns: GoogleDriveFile object """

    SHARED_FOLDER_NAME = 'Cities'
    shared_query = "title = '{}' and sharedWithMe and trashed=false".format(SHARED_FOLDER_NAME)

    # List the (shared) Cities folder
    shared_folder_list = drive.ListFile({'q': shared_query}).GetList()

    # Next - list all files under the shared Cities folder
    # Build a new querry for the same
    folder_query = "'{}' in parents and trashed=false".format(shared_folder_list[0]['id'])
    city_list = drive.ListFile({'q': folder_query}).GetList()

    # city_list above now contains a list of GoogleDriveFile objects
    # Iterate through the city list to see if the folder for current_city exists.
    # If not - first create the folder
    # Subsequently - the folder now exists - tiehr it already existed - or a folder by that name was just created
    # either ways - the folder now exists
    # Upload to the folder

    folder = None
    for index, a_city in enumerate(city_list):
        if a_city['title'] == current_city:
            folder = city_list[index]
            break

    # Create the city if it does not exist
    if folder is None:
        # No city by the name exists
        folder_query = "title = '{}' and trashed=false".format(SHARED_FOLDER_NAME)
        parent_folder = drive.ListFile({'q': folder_query}).GetList()

        folder_name = current_city
        folder = drive.CreateFile({'title' : folder_name, 
                               'mimeType' : 'application/vnd.google-apps.folder',
                               'parents': [{'id': parent_folder[0]['id']}]})
        folder.Upload()

    # A folder now exists - upload the csv
    return folder


def upload_files(folder, full_path, drive):
    """Upload all files in the folder indicated by full_path (on the workstation)
    to the Google Drive folder identified by folder. Note that the files in full_path
    likely should be deleted - or moved out - so that the same files are not uploaded
    subsequently"""
    for x in os.listdir(full_path):
        f = drive.CreateFile({'title': x, 'parents': [{'id': folder['id']}]})
        f.SetContentFile(os.path.join(full_path, x))
        f.Upload()





def drive_upload(full_path, drive, current_city = 'sanjose'):

    # The Cities folder is shared with the account that was chosen when the script is run
    # NOTE: This login required that you choose your google account that has the Cities folder shared
    # In other words, the code below as is will likely not work if you are logged in to the
    # agendascraper@gmail.com directly. If we do need to support that scenario - that of having
    # logged directly into agendascraper@gmail.com account, then the logic below will need to be
    # enhanced. 
    # 
    folder = get_city_folder(drive, current_city)

    # Upload the csv. The below may need to be revised/refactoed as once the fiels are uploaded, maybe the
    # files in the fodler hshould be deleted? Tat way - at the next run - the same files are not uploaded
    # again
    upload_files(folder, full_path, drive)

d = drive_launch()
full_path = 'C:\\Users\\m_noa\\Documents\\GitHub\\city-agenda-scraper\\Legistar_scraper\\agenda_tables\\'
drive_upload(full_path, d, 'sanjose')

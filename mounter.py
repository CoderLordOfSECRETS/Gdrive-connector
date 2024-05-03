import os
import subprocess
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

# Path to the credentials JSON file you downloaded
CREDS_FILE = 'desktopcode.json'

# Path where you want to mount your Google Drive
MOUNT_PATH = '/global'

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def main():
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    # Replace the folder ID with your Google Drive folder ID
    folder_id = '1dtr1hjA8ui1NtBTk86vpuSStgC6POJr2'

    results = service.files().list(q=f"'{folder_id}' in parents", fields="files(name, id)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found in the specified folder.')
    else:
        for item in items:
            print(f"Found file: {item['name']} ({item['id']})")

    # Mount the Google Drive folder using FUSE
    mount_command = f'google-drive-ocamlfuse -headless -label label_name -id client_id -secret client_secret'
    subprocess.run(mount_command, shell=True)
    
    # Create the mount directory if it doesn't exist
    os.makedirs(MOUNT_PATH, exist_ok=True)
    
    # Mount the Google Drive folder
    mount_command = f'google-drive-ocamlfuse {MOUNT_PATH}'
    subprocess.run(mount_command, shell=True)
    
    print("Google Drive folder mounted successfully.")

if __name__ == '__main__':
    main()

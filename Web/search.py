import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port = 0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials = creds)
    return service


def find_top_folder(service, test):
    page_token = None
    q_rules = "mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q = f"{q_rules}",
                                   spaces = 'drive',
                                   fields = 'nextPageToken, '
                                            'files(id, name, parents)',
                                   pageToken = page_token).execute()
    items = results.get('files', [])
    data = {}
    if not items:
        print('No files found.')
    else:
        for item in items:
            try:
                parents = item["parents"]
            except:
                parents = "N/A"
            data[item['id']] = {"Name": item['name'], "Parents": parents}
    return data


def find_file(service, site, data_type, year):
    # Call the Drive v3 API
    page_token = None
    q_rules = [f"name contains '{site}'",
               "mimeType != 'application/vnd.google-apps.folder'"]
    fields_rules = ", ".join(['id', 'name', 'parents', 'webContentLink'])
    results = service.files().list(q = " and ".join(q_rules),
                                   spaces = 'drive',
                                   fields = 'nextPageToken, '
                                            f'files({fields_rules})',
                                   pageToken = page_token).execute()
    items = results.get('files', [])
    data = {}
    if not items:
        print('No files found.')
    else:
        for item in items:
            try:
                parents = item["parents"]
            except:
                parents = "N/A"
            try:
                link = item['webContentLink']
            except:
                link = "N/A"
            file_info_l = [str(item['name']), str(item['id']), str(parents),
                           str(link)]
            file_info = '\t'.join(file_info_l)
            print(f"Found file: {file_info}")
            if data_type in item['name']:
                if year in item['name']:
                    data[item['id']] = {"Name": item['name'],
                                        "Parents": parents,
                                        "Link": link}
    print(data)
    return data

from apiclient import errors
import sys
# ...

def print_files_in_folder(service, folder_id):
  """Print files belonging to a folder.

  Args:
    service: Drive API service instance.
    folder_id: ID of the folder to print files from.
  """
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      children = service.children().list(folderId=folder_id, **param).execute()

      for child in children.get('items', []):
        print('File Id: %s' % child['id'])
      page_token = children.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError:
      print('An error occurred: %s' % sys.exc_info()[0])
      break

service_instance = "https://www.googleapis.com/auth/drive"
file_id = "1N3tUkV558C9GZtj9ju6r4VqL6u1xk12B"
print_files_in_folder(service_instance, file_id)
# https://dropbox-sdk-python.readthedocs.io/en/latest/api/dropbox.html#dropbox.dropbox_client.Dropbox.files_upload
# https://www.dropbox.com/developers/documentation/python#tutorial
# https://github.com/dropbox/dropbox-sdk-python

import dropbox
import json
import requests
import os

DROPBOX_SECOND_HALF_TOKEN_URL = 'https://raw.githubusercontent.com/v-popov/window-collage/main/dropbox_half_token.json'

if __name__ == '__main__':
    resp = requests.get(DROPBOX_SECOND_HALF_TOKEN_URL)
    data = json.loads(resp.text)

    dbx = dropbox.Dropbox(f"{first_half_token}{data['half-token']}")

    organized_photos_existing_folders = dbx.files_list_folder('/organized_photos/').entries
    organized_photos_existing_folders = [content.name for content in organized_photos_existing_folders]
    print(f'organized_photos_existing_folders={organized_photos_existing_folders}')

    raw_photos_contents = dbx.files_list_folder('/raw_photos/').entries
    raw_photos_filenames = [content.name for content in raw_photos_contents]
    print(f'raw_photos_filenames={raw_photos_filenames}')

    raw_photos_dates = [filename.split('_')[0] for filename in raw_photos_filenames]
    raw_photos_unique_dates = set(raw_photos_dates)
    print(f'raw_photos_unique_dates={raw_photos_unique_dates}')

    organized_photos_missing_dates_folders = raw_photos_unique_dates - set(organized_photos_existing_folders)
    print(f'organized_photos_missing_dates_folders={organized_photos_missing_dates_folders}')
    for organized_photos_missing_date_folder in organized_photos_missing_dates_folders:
        dbx.files_create_folder_v2(path=f'/organized_photos/{organized_photos_missing_date_folder}')

    for i, raw_photos_filename in enumerate(raw_photos_filenames):
        print(f'moving raw file {raw_photos_filename} to {raw_photos_dates[i]} folder')
        dbx.files_move_v2(from_path=f'/raw_photos/{raw_photos_filename}',
                          to_path=f'/organized_photos/{raw_photos_dates[i]}/{raw_photos_filename}')

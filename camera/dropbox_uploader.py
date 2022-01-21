import dropbox
import json
import requests
import os

DROPBOX_SECOND_HALF_TOKEN_URL = 'https://raw.githubusercontent.com/v-popov/window-collage/main/dropbox_half_token.json'

if __name__ == '__main__':
    resp = requests.get(DROPBOX_SECOND_HALF_TOKEN_URL)
    data = json.loads(resp.text)
    dbx = dropbox.Dropbox(f"{os.environ['DROPBOX_FIRST_HALF_TOKEN']}{data['half-token']}")

    project_abs_path = os.environ['CAMERA_DIR']
    photos_filenames = os.listdir(f"{project_abs_path}/photos/")

    # upload files to dropbox
    for photo_filename in photos_filenames:
        with open(f'{project_abs_path}/photos/{photo_filename}', "rb") as image:
            f = image.read()
            dbx.files_upload(f, f'/raw_photos/{photo_filename}')
            os.remove(f'{project_abs_path}/photos/{photo_filename}')

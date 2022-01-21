import argparse
import dropbox
import json
import requests
import os

parser = argparse.ArgumentParser(description='''Dropbox Uploader Script Arguments''', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-fhdt', '--first_half_dropbox_token', default='', type=str, help='''First Half Dropbox Token''')
parser.add_argument('-cam_dir', '--camera_directory', default='', type=str, help='''Camera Directory''')

DROPBOX_SECOND_HALF_TOKEN_URL = 'https://raw.githubusercontent.com/v-popov/window-collage/main/dropbox_half_token.json'

if __name__ == '__main__':
    args = parser.parse_args()
    first_half_token = args.first_half_dropbox_token

    resp = requests.get(DROPBOX_SECOND_HALF_TOKEN_URL)
    data = json.loads(resp.text)
    dbx = dropbox.Dropbox(f"{first_half_token}{data['half-token']}")

    project_abs_path = args.camera_directory

    photos_filenames = os.listdir(f"{project_abs_path}/photos/")

    # upload files to dropbox
    for photo_filename in photos_filenames:
        with open(f'{project_abs_path}/photos/{photo_filename}', "rb") as image:
            f = image.read()
            dbx.files_upload(f, f'/raw_photos/{photo_filename}')
            os.remove(f'{project_abs_path}/photos/{photo_filename}')

import dropbox
import argparse
import json
import requests
import os
from datetime import datetime, timedelta
import subprocess

DROPBOX_SECOND_HALF_TOKEN_URL = 'https://raw.githubusercontent.com/v-popov/window-collage/main/dropbox_half_token.json'

parser = argparse.ArgumentParser(description='''Dropbox Uploader Script Arguments''', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-fhdt', '--first_half_dropbox_token', default='', type=str, help='''First Half Dropbox Token''')
parser.add_argument('-sd', '--server_directory', default='', type=str, help='''Server Directory''')


if __name__ == '__main__':
    args = parser.parse_args()
    first_half_token = args.first_half_dropbox_token

    resp = requests.get(DROPBOX_SECOND_HALF_TOKEN_URL)
    data = json.loads(resp.text)

    dbx = dropbox.Dropbox(f"{first_half_token}{data['half-token']}")

    organized_photos_existing_folders = dbx.files_list_folder('/organized_photos/').entries
    organized_photos_existing_folders = [content.name for content in organized_photos_existing_folders]

    end_date = datetime.now()
    project_abs_path = args.server_directory
    for delta_days in range(7, 0, -1):
        print(f'Processing T-{delta_days} day')
        date = (end_date - timedelta(days=delta_days)).strftime('%Y-%m-%d')
        if date in organized_photos_existing_folders:
            photos_names = dbx.files_list_folder(f'/organized_photos/{date}').entries
            photos_names = [content.name for content in photos_names]
            for photo_name in photos_names:
                local_name = photo_name.replace(':','-')
                downloaded_file = dbx.files_download_to_file(f'{project_abs_path}/photos/{local_name}', f'/organized_photos/{date}/{photo_name}')

    #filenames_to_gif = os.listdir(f'{project_abs_path}/photos/')
    gif_name = f"{end_date.strftime('%Y-%m-%d')}-collage.gif"

    s = subprocess.getstatusoutput(f"ffmpeg -framerate 30 -pattern_type glob -i '{project_abs_path}/photos/*.jpg' -vf scale=512:-1 {project_abs_path}/{gif_name = f"{end_date.strftime('%Y-%m-%d')}-collage.gif"
    gif_path}")
    # with imageio.get_writer(gif_path, mode='I') as writer:
    #     for i, filename in enumerate(filenames_to_gif, start=1):
    #         print(f'Gif creation: Processed {i}/{len(filenames_to_gif)} photos')
    #         image = imageio.imread(f'{project_abs_path}/photos/{filename}')
    #         writer.append_data(image)
    # print('Optimizing the GIF')
    # optimize(gif_path)

    with open(gif_path, "rb") as gif:
        file = gif.read()
        dbx.files_upload(file, f'/gifs/{gif_name}')


# user_input = '20210115 20210119'

# def safe_str_to_date(s):
#     try:
#         return 'OK', datetime.strptime(s, '%Y%m%d')
#     except:
#         return 'INCORRECT FORMAT; Please specify dates in the YYYYMMDD format', None
#
#     user_input_parsed = user_input.split(' ')
#     print(user_input_parsed)
#     status, start_date = safe_str_to_date(user_input_parsed[0])
#     if status != 'OK':
#         print(status)
#     else:
#         if len(user_input_parsed) == 2:
#             status, end_date = safe_str_to_date(user_input_parsed[1])
#             if status != 'OK':
#                 print(status)
#         elif len(user_input_parsed) == 1:
#             end_date = start_date + timedelta(days=7)
#         else:
#             end_date = None
#             print('Incorrect message format - use either a single date with no spaces, or two dates separated by one space')
#
#         if end_date is not None:
#             print(f'start_date={start_date}; end_date={end_date}; delta={(end_date-start_date).days} days')
#             delta_days = (end_date-start_date).days + 1
#             dates = [datetime.strftime(start_date + timedelta(days=delta), '%Y-%m-%d') for delta in range(delta_days)]
#             print(dates)

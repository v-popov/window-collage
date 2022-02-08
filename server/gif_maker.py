import dropbox
import argparse
import json
import requests
import os
import imageio
from datetime import datetime, timedelta
# pip install pygifsicle
from pygifsicle import optimize
DROPBOX_SECOND_HALF_TOKEN_URL = 'https://raw.githubusercontent.com/v-popov/window-collage/main/dropbox_half_token.json'

parser = argparse.ArgumentParser(description='''Dropbox Uploader Script Arguments''', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-fhdt', '--first_half_dropbox_token', default='', type=str, help='''First Half Dropbox Token''')
parser.add_argument('-sd', '--server_directory', default='', type=str, help='''Server Directory''')


if __name__ == '__main__':
    dbx = dropbox.Dropbox(f"DM89k7WB5lIAAAAAAAAAARh4mBK_-89GUqiQ9GQf-CJPUHmLq7BYT6SZdMDHwyBY")

    organized_photos_existing_folders = dbx.files_list_folder('/organized_photos/').entries
    organized_photos_existing_folders = [content.name for content in organized_photos_existing_folders]

    end_date = datetime.now()
    for delta_days in range(7, 0, -1):
        date = (end_date - timedelta(days=delta_days)).strftime('%Y-%m-%d')
        if date in organized_photos_existing_folders:
            photos_names = dbx.files_list_folder(f'/organized_photos/{date}').entries
            photos_names = [content.name for content in photos_names]
            for photo_name in photos_names:
                local_name = photo_name.replace(':','-')
                downloaded_file = dbx.files_download_to_file(f'./photos/{local_name}', f'/organized_photos/{date}/{photo_name}')

    filenames_to_gif = os.listdir('./photos/')
    print(filenames_to_gif)
    gif_path = f"./{end_date.strftime('%Y-%m-%d')}-collage.gif"
    with imageio.get_writer(gif_path, mode='I') as writer:
        for filename in filenames_to_gif:
            image = imageio.imread(f'./photos/{filename}')
            writer.append_data(image)
    optimize(gif_path)


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

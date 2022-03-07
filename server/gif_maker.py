import dropbox
import argparse
import json
import requests
import os, shutil
from datetime import datetime, timedelta
import imageio
from skimage.transform import resize

DROPBOX_SECOND_HALF_TOKEN_URL = 'https://raw.githubusercontent.com/v-popov/window-collage/main/dropbox_half_token.json'

parser = argparse.ArgumentParser(description='''Dropbox Uploader Script Arguments''', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-fhdt', '--first_half_dropbox_token', default='', type=str, help='''First Half Dropbox Token''')
parser.add_argument('-sd', '--server_directory', default='', type=str, help='''Server Directory''')

DEFAULT_PARAMS = {
        'duration_': 0.1,
        'image_length_': 512,
        'image_width_': 512,
        'num_days_per_gif_': 7
    }


def clean_dir_contents(dir):
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


def get_service_params(service_info, param_name):
    matched_params = [info for info in service_info if param_name in info]
    if len(matched_params) > 0:
        return matched_params[0].replace('.txt','').replace(param_name, '')
    else:
        return DEFAULT_PARAMS[param_name]


def get_latest_gif_date(dbx):
    gif_dates_str = dbx.files_list_folder(f'/gifs').entries
    gif_dates_str = [content.name for content in gif_dates_str]
    last_gif_date = '2021-01-01'
    for gif_date_str in gif_dates_str:
        if ('-collage.gif' in gif_date_str) and (gif_date_str.replace('-collage.gif', '') > last_gif_date):
            last_gif_date = gif_date_str.replace('-collage.gif', '')
    print(f'last_gif_date={last_gif_date}')
    last_gif_date = datetime.strptime(last_gif_date, '%Y-%m-%d')
    return last_gif_date


def get_photos_folder_names(dbx):
    organized_photos_existing_folders = dbx.files_list_folder('/organized_photos/').entries
    organized_photos_existing_folders = [content.name for content in organized_photos_existing_folders]
    #print(f'organized_photos_existing_folders: {organized_photos_existing_folders}')
    organized_photos_existing_folders_dates = []
    for folder_name in organized_photos_existing_folders:
        try:
            organized_photos_existing_folders_dates.append(datetime.strptime(folder_name, '%Y-%m-%d'))
        except:
            print(f'Cannot convert to date value: {folder_name}')
    organized_photos_existing_folders_dates.sort()
    #print(f'organized_photos_existing_folders_dates: {organized_photos_existing_folders_dates}')
    return organized_photos_existing_folders_dates


if __name__ == '__main__':
    args = parser.parse_args()
    first_half_token = args.first_half_dropbox_token

    resp = requests.get(DROPBOX_SECOND_HALF_TOKEN_URL)
    data = json.loads(resp.text)

    dbx = dropbox.Dropbox(f"{first_half_token}{data['half-token']}")

    organized_photos_existing_folders_dates = get_photos_folder_names(dbx)

    last_gif_date = get_latest_gif_date(dbx)

    service_info = dbx.files_list_folder(f'/service').entries
    service_info = [content.name for content in service_info]
    print(f'service_info: {service_info}')
    duration = float(get_service_params(service_info, 'duration_'))
    image_length = int(get_service_params(service_info, 'image_length_'))
    image_width = int(get_service_params(service_info, 'image_width_'))
    num_days_per_gif = int(get_service_params(service_info, 'num_days_per_gif_'))
    print(f'Service Parameters: duration={duration}; image_length={image_length}; image_width={image_width}; num_days_per_gif={num_days_per_gif}')

    start_folder_num = 0
    not_all_folders_processed = True
    while not_all_folders_processed:
        while (start_folder_num < len(organized_photos_existing_folders_dates)) and (last_gif_date > organized_photos_existing_folders_dates[start_folder_num]):
            start_folder_num += 1
            print(f'start_folder_num = {start_folder_num}')
        print(f'Starting making gifs from date: {organized_photos_existing_folders_dates[start_folder_num]}')

        end_date = datetime.now()
        project_abs_path = args.server_directory
        for delta_days in range(num_days_per_gif):
            print(f'Processing T+{delta_days} day')
            if start_folder_num + delta_days < len(organized_photos_existing_folders_dates):
                current_folder = organized_photos_existing_folders_dates[start_folder_num+delta_days]
                print(f'current_folder: {current_folder}')
                current_folder_str = datetime.strftime(current_folder, '%Y-%m-%d')
                photos_names = dbx.files_list_folder(f"/organized_photos/{current_folder_str}").entries
                photos_names = [content.name for content in photos_names]
                for photo_name in photos_names:
                    local_name = photo_name.replace(':','-')
                    downloaded_file = dbx.files_download_to_file(f'{project_abs_path}/photos/{local_name}', f'/organized_photos/{current_folder_str}/{photo_name}')
                last_gif_date = current_folder
            else:
                not_all_folders_processed = False
        start_folder_num += delta_days + 1
        filenames_to_gif = os.listdir(f'{project_abs_path}/photos/')
        filenames_to_gif = sorted(filenames_to_gif)
        gif_name = f"{last_gif_date.strftime('%Y-%m-%d')}-collage.gif"
        gif_path = f"{project_abs_path}/{gif_name}"

        with imageio.get_writer(gif_path, mode='I', duration=duration) as writer:
            for i, filename in enumerate(filenames_to_gif, start=1):
                print(f'Gif creation: Processed {i}/{len(filenames_to_gif)} photos')
                image = imageio.imread(f'{project_abs_path}/photos/{filename}')
                image = resize(image, (image_width, image_length))
                writer.append_data(image)

        with open(gif_path, "rb") as gif:
            file = gif.read()
            dbx.files_upload(file, f'/gifs/{gif_name}')

        clean_dir_contents(f'{project_abs_path}/photos/')
        os.remove(gif_path)


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

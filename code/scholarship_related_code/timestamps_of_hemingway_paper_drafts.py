import os
import datetime

def get_creation_date(path):
    creation_time = os.path.getctime(path)
    return datetime.datetime.fromtimestamp(creation_time)

def list_files_with_creation_dates(folder_path):
    file_list = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            creation_date = get_creation_date(file_path)
            file_list.append((file_name, creation_date))

    file_list.sort(key=lambda x: x[1])

    for file_info in file_list:
        file_name, creation_date = file_info
        print(f'{file_name} --- {creation_date}')

folder_path = r'G:\My Drive\william_stuff\current_writing_projects\hemingway\drafts'
list_files_with_creation_dates(folder_path)
import pandas as pd
from pandas.errors import EmptyDataError
import os
from sys import exit

def read_txt(file_name, data_format='list'):
    data = []
    file_dir = os.path.join(os.getcwd(), file_name)
    try:
        with open(file_dir, "r", encoding="utf8", errors="surrogateescape") as file:
            str_data = file.read().strip()
            
            if data_format == 'str':
                return str_data
            elif data_format == 'list':
                if str_data:
                    lines = str_data.split('\n')
                    [data.append(line.strip()) for line in lines]   
            else:
                raise ValueError(f'data_format must be either list or str, You have given "{data_format}"')
    except FileNotFoundError:
        print(f'File "{file_name}" not found in path "{file_dir}"')
        exit()
    
    return data
    # data = ['a', 'b', 'c', 'd']

def write_to_txt(data, file_name='output.txt', lablel=False):
    file_dir = os.path.join(os.getcwd(), file_name)

    with open(file_dir, "w") as file:
        # data = ['a', 'b', 'c', 'd']
        if lablel:
            file.write(f'{lablel}\n')
        for line in data:
            file.write(f'{line}\n')

def read_txt_in_dict(file_name, split_by=':'):
    data = dict()
    inputs = read_txt(file_name)
    
    for line in inputs:
        try:
            parts = line.split(split_by)
            key = parts[0].strip()
            value = parts[1].strip()
        
            data[key] = value
        except IndexError:
            pass
    
    return data

def read_csv(file_name, data_format='list', exit_on_missing_file=True):
    file_dir = os.path.join(os.getcwd(), file_name)
    data = []
    try:
        df = pd.read_csv(file_dir)
        if data_format == 'dict':
            data = df.to_dict('records')
        else:
            data = df.values.tolist()
    except EmptyDataError:
        data = []
    except FileNotFoundError:
        if exit_on_missing_file:
            print(f'File "{file_name}" not found in path "{file_dir}"')
            exit()
        
    # Returning data as a list
    return data

def write_to_csv(data, labels=None, file_name = 'output.csv', excel_file = False):
    file_dir = os.path.join(os.getcwd(), file_name)
        
    header = True if labels else False
    
    try:
        df = pd.DataFrame(data, columns=labels)
        if excel_file:
            df.to_excel(file_dir, index=False, header=header)
        else:
            df.to_csv(file_dir, index=False, header=header)
    except PermissionError:
        print(f"PermissionError: Your file {file_name} is open with another application, Close the file first.")
        input('Then press Anykey to continue execution...')
        write_to_csv(data, labels, file_name, excel_file)

def read_executable_path_info(file_name='inputs/settings.txt', split_by='='):
    settings = dict()
    inputs = read_txt(file_name)
    settings = {}
    
    for line in inputs:
        try:
            parts = line.split(split_by)
            key = parts[0].strip()
            value = parts[1].strip()
            
            if value:
                if key in ['browser', 'driver', 'chrome_version', 'proxy', 'on_failure']:
                    settings[key] = value
                elif key in ['headless', 'captcha_extension']:
                    settings[key] = True if value.lower() in ['true', 'yes'] else False
                else:
                    settings[key] = value
        except:
            pass
        
    # print(settings)    
    return settings
import os
import json
import csv
from tqdm import tqdm

dataset_header = ['title', 'text']


def write_data_to_datasetfile(data: []):
    print('Сохраняем денные в dataset файл ...')
    with open('dataset/dataset.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=dataset_header)
        writer.writeheader()
        writer.writerows(data)

    print('Данные успешно сохранены!')


def read_file_data(full_file_name):
    with open(full_file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data


def walk_files_dataset(dir_path):
    res = []
    for path in tqdm(os.listdir(dir_path)):
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(read_file_data(dir_path + '/' + path))

    return res


if __name__ == '__main__':
    write_data_to_datasetfile(walk_files_dataset('dataset-archives/dataset/ruwiki'))

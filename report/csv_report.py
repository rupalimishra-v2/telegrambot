import csv
from utils import constants


def csv_file_generator(data, file_name):
    header = ['Group Name', 'Date', 'Time (in UTC)', 'Shilling Text']
    csv_file = file_name + '.csv'

    with open(csv_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)

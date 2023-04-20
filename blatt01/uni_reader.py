import datetime
import os
import csv

import numpy as np

BASE_DIR: str = os.getcwd()
CSV_DIR: str = os.path.join(BASE_DIR, 'csv')


def read_student_results(file_name: str) -> any:
    csv_data: list = []

    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)

    if file_name.endswith('.csv'):
        with open(file=file_name, mode='r') as csv_file:
            csv_in = csv.reader(csv_file, quotechar='"', delimiter=";")
            for row in csv_in:
                csv_data.append(row)
    else:
        raise Exception("Path given doesn't point to a .csv file")

    return csv_data


def analyze_student_results(csv_data: list):
    csv_processed: list = []

    for idx, row in enumerate(csv_data):
        if idx == 0:
            csv_processed.append(row + ['G_MAX', 'G_MEAN'])

        else:
            grades = [int(row[30]),
                      int(row[31]),
                      int(row[32])]

            g_max = np.max(grades)
            g_mean = round(np.average(grades), 2)
            csv_processed.append(row + [str(g_max), str(g_mean)])
    return csv_processed


def write_student_results(csv_data: list, file_name: str):
    if os.path.exists(file_name):
        os.remove(file_name)

    with open(file=file_name, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, quotechar='"', delimiter=";")
        for row in csv_data:
            csv_writer.writerow(row)


file_in = os.path.join(CSV_DIR, 'student-mat.csv')
file_out = os.path.join(CSV_DIR, f'student-mat-{datetime.date.today()}.csv')

csv_data = read_student_results(file_name=file_in)
csv_data_processed = analyze_student_results(csv_data=csv_data)
write_student_results(csv_data=csv_data, file_name=file_out)
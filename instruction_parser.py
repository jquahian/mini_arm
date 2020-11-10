import csv
import os

path = 'data'

instruction_set = []

# read data (points/angles/whatever) from csv
# store data in an array
def parse_csv(file_name):
    instruct = os.path.join(path, file_name)

    with open(instruct) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            instruction_set.append(row)
        
        print(f'{len(instruction_set)} instructions to process')
        
        return instruction_set

# # for testing
# parse_csv('test_test.txt')

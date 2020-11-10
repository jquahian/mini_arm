import csv
import os

path = 'data'

# read data (points/angles/whatever) from csv
# store data in an array
def parse_csv(file_name):
    instruction_set = []

    instruct = os.path.join(path, file_name)

    with open(instruct) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            instruction_set.append(row)
            
        # convert values to float since reading from csv returns strings.
        
        for i in range(len(instruction_set)):
            for j in range(len(instruction_set[i])):
                instruction_set[i][j] = float(instruction_set[i][j])

        print(f'{len(instruction_set)} instructions to process')
        
        return instruction_set

# # uncomment for testing
# parse_csv('test_test.txt')

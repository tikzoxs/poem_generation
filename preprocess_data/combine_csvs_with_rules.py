import csv
import numpy as np
import os
import random
import re
from operator import itemgetter 


read_folder = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/poems/processed_seperate'
train_filename = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/poems/processed_final/train.csv'
valid_filename = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/poems/processed_final/valid.csv'
max_in_length = 0
max_out_length = 0
validation_size = 15000

def process_input(input_text, output_text):
	global max_in_length, max_out_length
	in_length = len(input_text)
	out_length = len(output_text)
	print(in_length, out_length)
	new_in_length = min(out_length//5 + 1, in_length)
	index_list = random.sample(range(max(in_length, 1)), new_in_length)
	if(new_in_length > max_in_length):
		max_in_length = new_in_length
	if(out_length > max_out_length):
		max_out_length = out_length	
	if(in_length == new_in_length):
		return input_text
	else:
		return list(itemgetter(*index_list)(input_text))

def read_file_and_process(read_folder, write_filename):
	with open(train_filename, 'w') as train_file:
		train_writer = csv.writer(train_file, delimiter=',')
	# with open(valid_filename, 'w') as valid_file:
		# valid_writer = csv.writer(valid_file, delimiter=',')
		write_line_count = 0
		train_writer.writerow(['text', 'summary'])
		# valid_writer.writerow(['text', 'summary'])
		csv_list = os.listdir(read_folder)
		for file in csv_list:
			read_filename = read_folder + '/' + file
			with open(read_filename, 'r') as data:
				poem_reader = csv.reader(data, delimiter=',')
				read_line_count = 0
				for row in poem_reader:
					# if(write_line_count == 10000):
						# break
					read_line_count += 1
					[input_data, output_data] = row
					input_text = input_data.split(' ')
					output_text = output_data.split(' ')
					input_segment = process_input(input_text, output_text)
					spaced_input = [word + ' ' for word in input_segment]
					# if(validation_size < 1)
					# if(len(spaced_input)>0 and output_data is not None):
					source = str(''.join(spaced_input))
					target = str(output_data)
					if(len(re.findall(r'[A-Za-z]', source)) > 0):
						train_writer.writerow([source, target])
					write_line_count += 1 
					print(read_line_count, '\t\t', write_line_count)


read_file_and_process(read_folder, train_filename)
print('max in: ' + str(max_in_length) + '\tmax out: ' + str(max_out_length))
# print(process_input(['ber','fde','asd','asdf'],['ber','fde','asd','asdf','ber','fde','asd','asdf','ber','fde','asd','asdf','ber','fde','asd','asdf','ber','fde','asd','asdf']))




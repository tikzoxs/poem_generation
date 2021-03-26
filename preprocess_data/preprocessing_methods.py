import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv

ideal_poem_length = 25
low_buffer = 10
max_buffer = 20
max_poem_length = ideal_poem_length + max_buffer
poem_column = 4 #all = 1, kaggle = 4
read_filename = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/poems/kaggle.csv'
write_filename = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/poems/poems2.csv'

def split_poem_by_size(long_poem_segment):
	length = len(word_tokenize(long_poem_segment))
	if length > ideal_poem_length - low_buffer and length < ideal_poem_length + low_buffer :
		return [long_poem_segment]
	sentences = long_poem_segment.split('.')
	correct_sized_poems_list = []
	correct_sized_segment = ''
	for sentence in sentences:
		correct_sized_segment = correct_sized_segment + sentence + '.'
		if correct_sized_segment == '.':
			return correct_sized_poems_list
		correct_sized_segment_as_list = correct_sized_segment.split(' ')
		if(abs(len(correct_sized_segment_as_list) - ideal_poem_length) < low_buffer):
			correct_sized_poems_list.append(correct_sized_segment)
			correct_sized_segment = ''
		elif(len(correct_sized_segment_as_list) - ideal_poem_length > max_buffer):
			seg = ''
			for word in correct_sized_segment_as_list[0:max_poem_length]:
				if word != '':
					seg = seg + ' ' + word
			correct_sized_poems_list.append(seg)
			correct_sized_segment = ''
	return correct_sized_poems_list

def adjust_poem_size(poems_split_by_new_lines): 
	correct_sized_poems_list = [split_poem_by_size(segment) for segment in poems_split_by_new_lines]
	correct_sized_poems = [poem for item in correct_sized_poems_list for poem in item]
	return correct_sized_poems

def process_poems(poem_segment):
	poems_split_by_new_lines = poem_segment.lower().split("\n\n")
	correct_sized_poems= adjust_poem_size(poems_split_by_new_lines)
	new_lines_removed = [re.sub(r'[\n]', ' ', segment) for segment in correct_sized_poems if len(word_tokenize(segment)) > 5]
	tabs_removed = [re.sub(r'[\t]', '', segment) for segment in new_lines_removed]
	wierd_tuff_removed = [re.sub(r'[\xa0]', '', segment) for segment in tabs_removed]
	unwanted_chatacters_removed = [re.sub(r'[^0-9A-Za-z ;:\'.,]+', '', segment) for segment in wierd_tuff_removed]
	extra_spaces_removed = [re.sub(' +', ' ', segment) for segment in unwanted_chatacters_removed]
	stop_words = set(stopwords.words('english')) 
	stop_words_removed = [[word for word in poem.split(" ") if not word in stop_words] for poem in extra_spaces_removed]  
	return stop_words_removed, extra_spaces_removed

def read_file_and_process(read_filename, write_filename):
	with open(read_filename, 'r') as data:
		poem_reader = csv.reader(data, delimiter=',')
		with open(write_filename, 'w') as output:
			poem_writer = csv.writer(output, delimiter=',')
			read_line_count = 0
			write_line_count = 0
			for row in poem_reader:
				read_line_count += 1
				input_sequence, output_sequence = process_poems(row[poem_column])
				for input_segment, poem_segment in zip(input_sequence,output_sequence):
					spaced_input = [word + ' ' for word in input_segment]
					if(len(poem_segment) > 0):
						if(spaced_input[0][0] == ' '):
							spaced_input[0] = spaced_input[0].split(' ')[1]
						if(poem_segment[0] == ' '):
							poem_segment = str(poem_segment[1:])
						poem_writer.writerow([''.join(spaced_input), poem_segment])
						write_line_count += 1 
						print(read_line_count, '\t\t', write_line_count)
					else:
						print("NONE")
				# if(read_line_count > 50): break



read_file_and_process(read_filename, write_filename)


# test, poem = process_poems("this is a poem\n        blaaaa,\nkadda        there\nsaalsdkfj      alsdk\n\nflas     dd")
# print(poem,test)

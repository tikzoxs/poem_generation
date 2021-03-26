import re
import nltk
import csv
import random
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from operator import itemgetter 
from better_profanity import profanity


ideal_poem_length = 25
min_poem_length = 10
low_buffer = 10
max_buffer = 75
max_poem_length = ideal_poem_length + max_buffer
min_words_for_input = 5
max_words_for_input = 10
poem_column_kaggle = 4 #all = 1, kaggle = 4
poem_column_all = 1


read_kaggle_filename = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/poems/original/kaggle.csv'
read_all_filename = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/poems/original/all.csv'
write_kaggle_filename = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/poems/poems_kaggle.csv'
write_all_filename = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/poems/poems_all.csv'
combined_filename = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/poems/poems_final_processed.csv'
dics_folder = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/dictionaries/'
good_words_dict_filename = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/dictionaries/good_words_dict.csv'


dynamic_good_words_dict = {'love':0}


def load_or_save_dics(operation, write_dict=None):
	if(operation == 'load'):
		with open(good_words_dict_filename, 'r') as poem_word_doc:
			poem_word_reader = csv.reader(poem_word_doc, delimiter=',')
			good_words_dict = {rows[0]:int(rows[1]) for rows in poem_word_reader}
		return good_words_dict
	elif(operation == 'save'):
		sorted_dict = {k: v for k, v in sorted(write_dict.items(), key=lambda item: item[1])}
		with open(good_words_dict_filename, 'w') as poem_word_doc:
			poem_word_writer = csv.writer(poem_word_doc, delimiter=',')
			for key,value in sorted_dict.items():
				poem_word_writer.writerow([key, value])


def preprocess_poem_string(poem_string):
	poem_string = re.sub("i'm", 'i am', poem_string)
	poem_string = re.sub("'re", ' are', poem_string)
	poem_string = re.sub("'d", ' would', poem_string)
	poem_string = re.sub("'ll", ' will', poem_string)
	poem_string = re.sub("n't", ' not', poem_string)
	poem_string = re.sub("'ve", ' have', poem_string)
	poem_string = re.sub(r'[\n]', ', ', poem_string)
	poem_string = re.sub(r'[-]', ' ', poem_string)
	poem_string = re.sub(r'[—]', ', ', poem_string)
	poem_string = re.sub(r'[!;?]', '.', poem_string)
	poem_string = re.sub(r'[^a-z0-9\.:—\ ,-]', '', poem_string)
	poem_string = re.sub(r'(\ \.)', ',', poem_string)
	poem_string = re.sub(r'(\.\,)', '.', poem_string)
	poem_string = re.sub(r'(\,\.)', ',', poem_string)
	poem_string = re.sub(r'(\.)\1*', '.', poem_string)
	poem_string = re.sub(r'(\ )\1*', ' ', poem_string)
	poem_string = re.sub(r'(\,)\1*', ',', poem_string)
	poem_string = re.sub(' im ', ' i am ', poem_string)
	poem_string = re.sub('youre', 'you are', poem_string)
	poem_string = re.sub('theyre', 'they are', poem_string)
	if(poem_string[-1] != '.'):
		poem_string = poem_string + '.'
	poem_string = re.sub(r'(\,\.)', '.', poem_string)
	return(poem_string)


def get_random_word(stop_words_removed):
	word_list = list(dynamic_good_words_dict.keys())
	dict_size = len(word_list)
	random_word = word_list[random.randint(0,dict_size-1)] 
	while(random_word in stop_words_removed):
		random_word = word_list[random.randint(0,dict_size-1)] 
	return [random_word]


def generate_input(poem_segment):
	global dynamic_good_words_dict
	stop_words = set(stopwords.words('english') + ['.', ':', ' ', ',']) 
	# print(stop_words)
	tokenized_poem = word_tokenize(poem_segment)
	stop_words_removed = [word for word in tokenized_poem if word not in stop_words and len(re.findall(r'[0-9]',word)) == 0] 
	if(len(stop_words_removed)>0):
		num_words_for_input = min(min(max(len(stop_words_removed)//3, 5), 10), len(stop_words_removed))
		selected_indexes = random.sample(range(len(stop_words_removed)), num_words_for_input)
		selected_words = list(itemgetter(*selected_indexes)(stop_words_removed)) 
	else:
		selected_words = get_random_word(stop_words_removed)
	selected_words_for_dict = set(selected_words)
	random_word_added = selected_words + get_random_word(stop_words_removed)
	random.shuffle(random_word_added)
	input_set = set(random_word_added)
	for word in selected_words_for_dict:
		dynamic_good_words_dict[word] = dynamic_good_words_dict.get(word,0) + 1
	return input_set


def split_long_poems(raw_poem_outputs):
	short_poems = []
	for poem in raw_poem_outputs:
		if(len(poem.split(' ')) < max_poem_length):
			short_poems.append(poem)
		else:
			senteces = poem.split('.')
			short_poem = ''
			for sentece in senteces:
				if(len(short_poem.split(' ')) < max_poem_length):
					short_poem = short_poem + sentece + '.'
				else:
					short_poems.append(short_poem)
					short_poem = ''
	return short_poems


def process_poems(poem_segment):
	segmented_poem = poem_segment.lower().split("\n\n")
	raw_poem_outputs = [preprocess_poem_string(segment) for segment in segmented_poem if len(segment.split(' ')) >= min_poem_length] 
	# and profanity.contains_profanity(poem_segment) == False
	poem_outputs = split_long_poems(raw_poem_outputs)
	poem_inputs = [generate_input(segment) for segment in poem_outputs]
	return poem_inputs, poem_outputs


def read_file_and_process(read_filename, write_filename, poem_column):
	with open(read_filename, 'r') as data:
		poem_reader = csv.reader(data, delimiter=',')
		with open(write_filename, 'a') as output:
			poem_writer = csv.writer(output, delimiter=',')
			poem_writer.writerow(['source', 'target'])
			read_line_count = 0
			write_line_count = 0
			for row in poem_reader:
				read_line_count += 1
				poem_inputs, poem_outputs = process_poems(row[poem_column])
				for input_segment, output_segment in zip(poem_inputs, poem_outputs):
					poem_writer.writerow([input_segment, output_segment])
					write_line_count += 1 
					print(read_line_count, '\t\t', write_line_count)
				# if(write_line_count > 50): break


read_file_and_process(read_kaggle_filename, combined_filename, poem_column_kaggle)
read_file_and_process(read_all_filename, combined_filename, poem_column_all)

load_or_save_dics('save', dynamic_good_words_dict)
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig
import random
import re
from operator import itemgetter 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

word_embeddings_file = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/word_embedding/glove.6B/glove.6B.' + str(glove_embedding_dimensions) + 'd.txt'

glove_embedding_dimensions = 100

good_words_old = ['trees', 'love', 'flower', 'house', 'world', 'peace', 'mind', 'hero', 'beaches', 'beach', 'picture', 'victim', 'person', 'happy', 'angry', 'lake', 'grave', 'life', 'death', 'children', 'sweet', 'lane', 'nice', 'sorrow', 'exicted', 'forest', 'road']
good_words = ['happy', 'love', 'lane', 'unsure', 'anger', 'angry', 'happiness', 'joy', 'caring', 'care', 'loving']

embeddings_dict = {}

def load_word_embeddings():
	global embeddings_dict
	with open(word_embeddings_file) as f:
		for line in f:
			word, coefs = line.split(maxsplit=1)
			coefs = np.fromstring(coefs, "f", sep=" ")
			embeddings_dict[word] = coefs

def process_input(in_text):
	global good_words
	word_list = in_text.split(' ')
	stop_words = set(stopwords.words('english') + ['always', 'into', 'can\'t', 'don\'t']) 
	stop_words_removed = [word + ' ' for word in word_list if not word in stop_words]
	in_length = len(stop_words_removed)
	index_list = random.sample(range(max(in_length, 1)), in_length//2)
	good_index_list = random.sample(range(len(good_words)), min(in_length//3,2))
	if(in_length>4):
		selected_words = list(itemgetter(*index_list)(stop_words_removed))
	else:
		selected_words = []
	good_words_list = list(itemgetter(*good_index_list)(good_words))
	selected_good_words = [word + ' ' for word in good_words_list]
	# print(selected_words)
	# print(selected_good_words)
	all_selected_words = selected_words #+ selected_good_words
	random.shuffle(all_selected_words)
	processed_in_text = ''.join(all_selected_words)
	# print(processed_in_text)
	return processed_in_text

def process_output(out_text):
	if(len(re.findall(r'[.]', out_text)) > 0):
		sections = out_text.split('.')[:-1]
		return(''.join(sections))
	else:
		return out_text

model = BartForConditionalGeneration.from_pretrained('/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/BART/checkpoint-68500')
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

while(True):
	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	in_text = input("Tell Something: ")
	if(in_text == 'q'):
		break
	ARTICLE_TO_SUMMARIZE = process_input(in_text)
	inputs = tokenizer([ARTICLE_TO_SUMMARIZE], return_tensors='pt')

	# Generate Summary
	summary_ids = model.generate(inputs['input_ids'], num_beams=4, min_length=30, max_length=100, early_stopping=True)
	whole_out_text = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
	# print(whole_out_text)
	raw_out_text = ''.join(whole_out_text)
	# print(raw_out_text)
	print("Emotional Pavilion: ", process_output(raw_out_text))
	print("***************************************************************************************************")

	#yesterday was quite hectic. never had a chance to get a good sleep
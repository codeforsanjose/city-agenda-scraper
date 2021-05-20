import pickle
import os
import pandas as pd
import re
import string
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from gensim import matutils, models
import scipy.sparse
import logging
import sys

#logging.basicConfig(stream=sys.stdout, level=logging.INFO)
#logger = logging.getLogger(__name__)

path = r"..\Agenda_samples\text_files"
output_dir = r"..\output"
#print(os.getcwd())
#print(os.listdir(path))
agenda_folder = os.listdir(path)

def combine_text(list_of_text):
	combined_text = ' '.join(list_of_text)
	return combined_text

def clean_text_round1(text):
	#lower case, remove punctuation, remove stop words
	#for numbers, keep the word before them OR just remove single digit numbers
	text = text.lower()
	text = re.sub("\d+", "", text)
	text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
	text = re.sub('[‘’“”…]', '', text)
	text = re.sub('\n', '', text)
	text = re.sub(r'(?i)\b[a-z]\b','',text)
	text = ' '.join(text.split())
	return text

def process_and_clean_data(text):
	combine = combine_text(text)
	clean1 = clean_text_round1(combine)
	return clean1

def load_files_in_dir(directory):
	out_dict = {}
	for file in os.listdir(directory):
		with open(os.path.join(directory, file), "r") as input_file: #  added encoding="Windows-1252" to make it work on colab Notebooks
			a = input_file.readlines()
			if a:
				out_dict[file] = [process_and_clean_data(a)]
	return out_dict

def create_pandas(input_dict):
	#load data into Pandas dataframe
	pd.set_option("max_colwidth", 100)
	data_df = pd.DataFrame.from_dict(input_dict).transpose()
	data_df.columns = ['agenda_transcript']
	return data_df

#remove stop words with CountVectorizer
#create Document Term Matrix & pickle

def create_cv(df):
	cv = CountVectorizer(stop_words='english', ngram_range=(1,1), min_df=.01)
	#print(cv.get_stop_words())
	data_cv = cv.fit_transform(df.agenda_transcript)
	#rint(data_cv.toarray())
	data_dtm = pd.DataFrame(data_cv.toarray(), index=data_clean.index, columns=cv.get_feature_names())
	#print(data_dtm)
	data_dtm.index = data_clean.index
	return data_dtm

def get_top_words(count_vect):
	r = pd.DataFrame(count_vect.loc[i])
	filtered = r[r[r.columns[0]] > 0]
	sorted_filtered = filtered.sort_values(by=filtered.columns[0], ascending=False).head(10)
	return sorted_filtered, filtered

def get_topic_models(d,filtered):
		cv = CountVectorizer(stop_words='english', ngram_range=(1,1), min_df=.01)
		data_cv = cv.fit_transform(d[i])
		sparse_counts = scipy.sparse.csr_matrix(filtered)
		corpus=matutils.Sparse2Corpus(sparse_counts)
		id2word = dict((v,k) for k,v in cv.vocabulary_.items())
		lda = models.LdaModel(corpus=corpus,id2word=id2word,num_topics=3, passes=50)
		lda2 = lda.show_topics(num_topics=3,num_words=10,formatted=False)
		topic_words = [(tp[0], [wd[0] for wd in tp[1]]) for tp in lda2]
		for topic,words in topic_words:
			print(str(topic)+ "::"+ str(words))
		return lda.show_topics(num_topics=3, num_words=5, log=False, formatted=True)

data_dict = load_files_in_dir(path)
data_clean = create_pandas(data_dict)

for i in data_clean.index:
	cv = create_cv(data_clean)
	sf,f=get_top_words(cv)
	print("\n")
	print("Top Words: ")
	print(sf)
	get_topic_models(data_dict,f)

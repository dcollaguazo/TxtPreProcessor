import csv
import pandas as pd
import langdetect as ld
import numpy as np
import nltk
import re

class Cleaner:
	def __init__(self, file_path:str):
		self.df = pd.read_csv(file_path, header=None, names = ["Blog Content"])

	def strip_language(self, foreign_language: str = 'all'):
		indices_to_be_dropped = []
		if foreign_language == 'all':
			for index, row in self.df.iterrows():
				for value in row.values:
					try:
						if ld.detect(value) != 'es':
							indices_to_be_dropped.append(index)
					except Exception as e:
						print(e)
		self.df.drop(list(set(indices_to_be_dropped)), inplace = True)
		
	def to_lower(self):
		self.df['Blog Content'] = self.df['Blog Content'].str.lower()		

	def remove_punctuation(self):
		self.df['Blog Content'] = self.df['Blog Content'].str.replace(r'[^\w\s]','')
		
	def handle_strs(self, char, replacement):
		self.df['Blog Content'] = self.df['Blog Content'].str.replace(char, replacement)

	def handle_nulls(self):
		self.df.replace(np.nan, '', regex=True)

	def remove_numbers(self):
		self.df['Blog Content'] = self.df['Blog Content'].str.replace(r'[\d]','')

	def remove_stopwords(self):
		stop_words = set(nltk.corpus.stopwords.words('spanish'))
		self.df['Blog Content'] = self.df['Blog Content'].str.split()
		self.df['Blog Content'] = self.df['Blog Content'].apply(lambda x:[item for item in x if item not in stop_words])

	def stem_words(self):
		snowball = nltk.stem.SnowballStemmer('spanish')
		self.df['Blog Content'] = self.df['Blog Content'].apply(lambda x: [snowball.stem(t) for t in x])
		
	def clean(self, file_path:str):
		self.strip_language()

		self.to_lower()
		
		#removing some other customized content
		self.handle_strs(r'\[comma\]',' ')

		self.remove_punctuation()

		#remove other weird remaining strings that you might find 
		self.handle_strs('var dd_offset_from_content  40var dd_top_offset_from_content  0var dd_override_start_anchor_id  var dd_override_top_offset', '')

		#converting unicode to characters we might miss some but thats ok
		#here a helpful source:http://www.fileformat.info/info/unicode/char/search.htm
		self.handle_strs('u00e1','a')
		self.handle_strs('u00e0','a')
		self.handle_strs('u00c1','a')
		self.handle_strs('u00e3','a')
		self.handle_strs('u00e9','e')
		self.handle_strs('u00c9','e')
		self.handle_strs('u00ea','e')
		self.handle_strs('u0113','e')
		self.handle_strs('u00ed','i')
		self.handle_strs('u00cd','i')
		self.handle_strs('u00ce','i')
		self.handle_strs('u00f3','o')
		self.handle_strs('u00d3','o')
		self.handle_strs('u00f4','o')
		self.handle_strs('u00f5','o')
		self.handle_strs('u00f2','o')
		self.handle_strs('u00fa','u')
		self.handle_strs('u00fc','u')
		self.handle_strs('u00da','u')
		self.handle_strs('u00f1','n')
		self.handle_strs('u00d1','n')
		self.handle_strs('u00e7','c')
		self.handle_strs('u00fa','')
		self.handle_strs('u201d','')
		self.handle_strs('u201c','')
		self.handle_strs('u00bf','')
		self.handle_strs('u00a1','')
		self.handle_strs('ufffc','')
		self.handle_strs('u00a8','')
		self.handle_strs('u00ab','')
		self.handle_strs('u00bb','')
		self.handle_strs('u0301','')
		self.handle_strs('u0300','')
		self.handle_strs('u00b4','')
		self.handle_strs('u00b0','')
		self.handle_strs('u00aa','')
		self.handle_strs('u00ba','')
		self.handle_strs('u00bd','')
		self.handle_strs('u00a9','')
		self.handle_strs('u00b3','')
		self.handle_strs('u2018','')
		self.handle_strs('u2019','')
		self.handle_strs('u2033','')
		self.handle_strs('u2022','')
		self.handle_strs('u200b','')
		self.handle_strs('u200a','')
		self.handle_strs('u200f','')
		self.handle_strs('u202f',' ')
		self.handle_strs('u2014',' ')
		self.handle_strs('u2026',' ')
		self.handle_strs('u2010',' ')
		self.handle_strs('u00a0',' ')
		self.handle_strs('u2013',' ')

		#remove numbers
		self.remove_numbers()

		#remove stopwords
		self.remove_stopwords()

		#word stemming and lemmatization
		self.stem_words()

		#export cleaned dataframe to csv
		self.df.to_csv(file_path, encoding='utf-8', index=False)
		

	

if __name__ == "__main__":
	input_path = "C:/Users/DANIELACO/blog_abierto_al_publico/blog_abierto_al_publico/input/blog_content.csv"
	output_path = "C:/Users/DANIELACO/blog_abierto_al_publico/blog_abierto_al_publico/output/blog_content_cleaned.csv"
	clean = Cleaner(input_path).clean(output_path)
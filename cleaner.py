import pandas as pd
import langdetect as ld
import numpy as np
import nltk

class Cleaner:
	def __init__(self, file_path:str):
		self.df = pd.read_csv(file_path, header=0)

	#funcion que separa el contenido en español del resto
	def strip_language(self, col_idx:int, lang_to_keep:str):
		indices_to_be_kept = []
		for index, row in self.df.iterrows():
			try:
				if ld.detect(row[col_idx])== lang_to_keep:
					indices_to_be_kept.append(index)

			except Exception as e:
				print(e)
		self.df = self.df.iloc[indices_to_be_kept]

	def to_lower(self, col_idx:int):
		self.df.iloc[:,col_idx] = self.df.iloc[:,col_idx].str.lower()

	def remove_punctuation(self, col_idx:int):
		self.df.iloc[:,col_idx] = self.df.iloc[:,col_idx].str.replace(r'[^\w\s]','')
		print(self.df)
		
	def handle_strs(self, char:str, replacement:str, col_idx:int):
		self.df.iloc[:,col_idx] = self.df.iloc[:,col_idx].str.replace(char, replacement)

	# def handle_nulls(self):
	# 	self.df.replace(np.nan, '', regex=True)

	def remove_numbers(self, col_idx:int):
		self.df.iloc[:,col_idx] = self.df.iloc[:,col_idx].str.replace(r'[\d]','')

	def remove_stopwords(self, col_idx:int, lang_to_keep:str):
		stop_words = set()
		if(lang_to_keep == 'es'):
			stop_words = set(nltk.corpus.stopwords.words('spanish'))
		elif (lang_to_keep == 'en'):
			stop_words = set(nltk.corpus.stopwords.words('english'))
		self.df.iloc[:,col_idx] = self.df.iloc[:,col_idx].str.split()
		self.df.iloc[:,col_idx] = self.df.iloc[:,col_idx].apply(lambda x:[item for item in x if item not in stop_words])

	def stem_words(self, col_idx:int, lang_to_keep:str):
		if(lang_to_keep == 'es'):
			snowball = nltk.stem.SnowballStemmer('spanish')
			self.df.iloc[:,col_idx] = self.df.iloc[:,col_idx].apply(lambda x: [snowball.stem(t) for t in x])
		elif(lang_to_keep == 'en'):
			snowball = nltk.stem.SnowballStemmer('english')
			self.df.iloc[:,col_idx] = self.df.iloc[:,col_idx].apply(lambda x: [snowball.stem(t) for t in x])

	def clean(self, file_path:str, col_idx:int, lang_to_keep:str):
		self.strip_language(col_idx, lang_to_keep)

		self.to_lower(col_idx)

		self.remove_punctuation(col_idx)

		self.handle_strs('xa0',' ', col_idx)
		self.handle_strs('var dd_offset_from_content  40var dd_top_offset_from_content  0var dd_override_start_anchor_id  var dd_override_top_offset','',col_idx)

		#Se remueven los números
		self.remove_numbers(col_idx)

		#Se quitan las palabras comunes
		self.remove_stopwords(col_idx, lang_to_keep)

		#Se transforman las palabras a su raíz
		self.stem_words(col_idx, lang_to_keep)

		#Se exporta el texto limpio a un csv
		self.df = self.df.reset_index()
		self.df.index.names = ['Topic Modeling Id - New Index']
		self.df = self.df.drop(self.df.columns[1], axis = 1)
		# print(self.df)
		self.df.to_csv(file_path, encoding='utf-8', index=True)


if __name__ == "__main__":
	raw_data = "raw_data/blog_content_raw.csv"
	cleaned_data = "cleaned_data/blog_content_cleaned_es.csv"
	#clean(file_to_be_processed, index of the column with thhe content, language) takes three parameters
	clean = Cleaner(raw_data).clean(cleaned_data,2,'es')
import pandas as pd
import langdetect as ld
import numpy as np
import nltk


class Cleaner:
	def __init__(self, file_path:str):
		self.df = pd.read_csv(file_path, header=0, names=['Id','Author', 'Blog Content', 'Blog URL', 'Publication Date', 'Summary', 'Title'])

	#funcion que separa el contenido en español del resto
	def strip_language(self, foreign_language: str = 'all'):
		indices_to_be_dropped = []
		if foreign_language == 'all':
			for index, row in self.df.iterrows():
				try:
					if ld.detect(row['Blog Content'])  != 'es':
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

		self.remove_punctuation()

		self.handle_strs('xa0',' ')
		self.handle_strs('var dd_offset_from_content  40var dd_top_offset_from_content  0var dd_override_start_anchor_id  var dd_override_top_offset','')

		#Se remueven los números
		self.remove_numbers()

		#Se quitan las palabras comunes
		self.remove_stopwords()

		#Se transforman las palabras a su raíz
		self.stem_words()

		#Se exporta el texto limpio a un csv
		self.df[['Id','Blog URL','Blog Content']].to_csv(file_path, encoding='utf-8', index=False)

if __name__ == "__main__":
	raw_data = "raw_data/blog_content_raw.csv"
	cleaned_data = "cleaned_data/blog_content_cleaned.csv"
	clean = Cleaner(raw_data).clean(cleaned_data)


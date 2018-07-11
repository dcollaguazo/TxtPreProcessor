import pandas as pd
import json

class JsonToCSV:
	def __init__(self, filepath:str):
		with open(filepath) as f:
			self.data_json = json.load(f)
			self.df_json = pd.DataFrame.from_dict(self.data_json, orient='columns')
			
	def transform_to_csv(self, filepath:str):
		self.df_json.to_csv(filepath, encoding='utf-8', index=False)

if __name__ == "__main__":
	raw_data = "raw_data/raw_data.json"
	cleaned_data = "output/blog_content_raw.csv"
	json_to_csv = JsonToCSV(raw_data).transform_to_csv(cleaned_data)

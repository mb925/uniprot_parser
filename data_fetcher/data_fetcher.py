import requests


class DataFetcher(object):

	def __init__(self, log_path='./datafetcher_log.txt'):

		self.log_file = open(log_path, 'w')
		self.json = None

	def __del__(self):

		self.log_file.close()

	def get_json(self, url):
		r = requests.get(url)
		if not r.status_code == 200:
			self.json = None
		else:
			self.json = r.json()

	def get_uniprot_list(self):

		schema = 'http://'
		domain = 'repeatsdb.bio.unipd.it'
		subfolders = '/ws/search'
		params = 'query=average_unit:1TO9999999999&collection=uniprot_protein&show=uniprotid'
		self.get_json('%s%s%s?%s' % (schema, domain, subfolders, params))

		if not self.json:
			self.log_file.write('RepeatsDB: error fetching uniprot list')
			self.log_file.flush()
			return None

		if not type(self.json) == list:
			self.log_file.write('RepeatsDB: wrong uniprot list format')
			self.log_file.flush()
			return None

		return self.json

	def get_ebi_sequence(self, uniprot_id):

		schema = 'https://'
		domain = 'www.ebi.ac.uk'
		subfolders = '/proteins/api/proteins/'
		self.get_json('%s%s%s%s' % (schema, domain, subfolders, uniprot_id))

		if not self.json:
			self.log_file.write('EBI: error fetching uniprot info -> %s' % uniprot_id)
			self.log_file.flush()
			return None

		if not type(self.json) == dict:
			self.log_file.write('EBI: wrong uniprot info format -> %s' % uniprot_id)
			self.log_file.flush()
			return None

		return self.json

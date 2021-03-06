import requests


class DataFetcher(object):

	def __init__(self, log_path='./datafetcher_log.txt'):

		self.log_file = open(log_path, 'w')
		self.json = None

	def __del__(self):

		self.log_file.close()

	def get_json(self, url):
		try:
			r = requests.get(url)
		except:
			self.json = None
			return

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
			self.log_file.write('RepeatsDB: error fetching uniprot list\n')
			self.log_file.flush()
			return []

		if not type(self.json) == list:
			self.log_file.write('RepeatsDB: wrong uniprot list format\n')
			self.log_file.flush()
			return []

		res = []
		for elem in self.json:

			if not type(elem) == dict:
				self.log_file.write('%s: not a dict\n' % str(elem))
				self.log_file.flush()

			elif 'uniprotid' not in elem:
				self.log_file.write('%s: missing uniprot id\n' % str(elem))
				self.log_file.flush()

			else:
				if 'id' not in elem:
					self.log_file.write('%s: missing id\n' % str(elem))
					self.log_file.flush()
				res.append(elem)

		self.json = res
		return self.json

	def get_ebi_sequence(self, uniprot_id):

		schema = 'https://'
		domain = 'www.ebi.ac.uk'
		subfolders = '/proteins/api/proteins/'
		self.get_json('%s%s%s%s' % (schema, domain, subfolders, uniprot_id))

		if not self.json:
			self.log_file.write('EBI: error fetching uniprot info -> %s\n' % uniprot_id)
			self.log_file.flush()
			return None

		if not type(self.json) == dict:
			self.log_file.write('EBI: wrong uniprot info format -> %s\n' % uniprot_id)
			self.log_file.flush()
			return None

		return self.json

	def get_ebi_mapping(self, uniprot_id):

		schema = 'https://'
		domain = 'www.ebi.ac.uk'
		subfolders = '/pdbe/api/mappings/'
		self.get_json('%s%s%s%s' % (schema, domain, subfolders, uniprot_id))

		if not self.json:
			self.log_file.write('EBI: error fetching uniprot mapping -> %s\n' % uniprot_id)
			self.log_file.flush()
			return None

		if not type(self.json) == dict:
			self.log_file.write('EBI: wrong uniprot mapping format -> %s\n' % uniprot_id)
			self.log_file.flush()
			return None

		return self.json

	def get_ebi_listing(self, pdb_id):

		schema = 'https://'
		domain = 'www.ebi.ac.uk'
		subfolders = '/pdbe/api/pdb/entry/residue_listing/'
		self.get_json('%s%s%s%s' % (schema, domain, subfolders, pdb_id))

		if not self.json:
			self.log_file.write('EBI: error fetching pdb listing -> %s\n' % pdb_id)
			self.log_file.flush()
			return None

		if not type(self.json) == dict:
			self.log_file.write('EBI: wrong pdb listing format -> %s\n' % pdb_id)
			self.log_file.flush()
			return None

		return self.json

	def get_repeats_entities(self, pdb, chain):

		schema = 'http://'
		domain = 'repeatsdb.bio.unipd.it'
		subfolders = '/ws/search'
		params = 'entry_type=repeat_region&id=%s%s&collection=repeat_region&show=ALL' % (pdb, chain)
		self.get_json('%s%s%s?%s' % (schema, domain, subfolders, params))

		if not self.json:
			self.log_file.write('RepeatsDB: error fetching entity -> %s, %s\n' % (pdb, chain))
			self.log_file.flush()
			return None

		if not type(self.json) == list:
			self.log_file.write('RepeatsDB: wrong entity format -> %s, %s\n' % (pdb, chain))
			self.log_file.flush()
			return None

		return self.json

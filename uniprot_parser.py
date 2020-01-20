import sys

from data_fetcher.data_fetcher import DataFetcher
from json_parser.json_parser import JsonParser


class UniprotParser(object):

	def __init__(self, log_path='./uniprotparser_log.txt'):

		self.log_file = open(log_path, 'w')
		self.data_fetcher = DataFetcher()
		self.uniprot_parser = JsonParser(out_path='./uniprot.json')

		self.mapping_parser = JsonParser(
			out_path='./mapping.json',
			aggregators=[
				'ROOT._aggr',
				'ROOT._aggr.PDB._aggr'
			]
		)

		self.listing_parser = JsonParser(out_path='./listing.json')
		self.entities_parser = JsonParser(out_path='./entities.json')

	def __del__(self):

		self.log_file.close()

	def start(self):

		print('Downloading uniprot list...')
		ulist = self.data_fetcher.get_uniprot_list()
		if not ulist:
			return

		print('Collecting %d uniprots...\n\n' % len(ulist))
		for i in range(0, len(ulist)):

			elem = ulist[i]

			if not self.check_uniprot_entry(elem):
				return

			unp_id = elem['uniprotid']
			print('#%d: %s' % (i, unp_id))
			print('Uniprot:')
			self.fetch_uniprot(unp_id)
			print('Mapping:')
			self.fetch_mapping(unp_id)

			print('\n')



	def check_uniprot_entry(self, elem):

		if not type(elem) == dict:
			self.log_file.write('%s: not a dict\n' % str(elem))
			self.log_file.flush()
			print('%s: not a dict\n\n' % str(elem))
			return False

		if 'uniprotid' not in elem:
			self.log_file.write('%s: missing uniprot id\n' % str(elem))
			self.log_file.flush()
			print('%s: missing uniprot id\n\n' % str(elem))
			return False

		if 'id' not in elem:
			self.log_file.write('%s: missing id\n' % str(elem))
			self.log_file.flush()
			print('%s: missing id\n' % str(elem))

		return True

	def fetch_uniprot(self, id):

		self.parse_and_restructure(self.data_fetcher.get_ebi_sequence, self.uniprot_parser, id)

	def fetch_mapping(self, id):

		self.parse_and_restructure(self.data_fetcher.get_ebi_mapping, self.mapping_parser, id)

	def parse_and_restructure(self, fetcher, parser, code):

		print('- Fetching %s...' % code)
		json_data = fetcher(code)
		if not json_data:
			return

		print('-- Parsing %s...' % code)
		parser.parse(json_data)

		print('--- Restructuring %s...' % code)
		parser.restructure()

		print('---- Done')


if __name__ == '__main__':

	uniprot_parser = UniprotParser()
	uniprot_parser.start()

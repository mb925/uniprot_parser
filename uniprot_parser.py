from data_fetcher.data_fetcher import DataFetcher
from json_parser.json_parser import JsonTree


class UniprotParser(object):

	def __init__(self):
		self.df = DataFetcher()
		# uniprot tree
		self.utree = JsonTree('./uniprot.txt')
		# mapping tree
		self.mtree = JsonTree('./mapping.txt')
		# listing tree
		# self.ltree = JsonTree('./listing.txt')
		# entity tree
		# self.etree = JsonTree('./entity.txt')

	def start(self):

		print('Downloading uniprot list...')
		ulist = self.df.get_uniprot_list()
		print('Collecting %d uniprots...\n\n' % len(ulist))
		i = 0
		j = 0
		for elem in ulist:

			# get elements
			unp_id = elem['uniprotid']

			i += 1
			print('>>>>>>>>>>')
			print('#%d: %s' % (i, unp_id))

			print('---> Uniprot...')
			self.utree.acquire(
				self.df.get_ebi_sequence(unp_id))

			print('---> Mapping...')
			self.mtree.acquire(
				self.df.get_ebi_mapping(unp_id))

			print('---> Listing...')
			for pdb in elem['id']:
				j += 1
				print('--- #%d: %s' % (j, pdb))

			print('<<<<<<<<<<\n')

			# update state
			self.utree.save()
			self.mtree.save()

			if i == 50:
				break

	# def save_listing(self):
	# 	update_file(UniprotParser.listing_path, ...)
	#
	# def save_entity(self):
	# 	update_file(UniprotParser.entity_path, ...)


if __name__ == '__main__':
	uparser = UniprotParser()
	uparser.start()

from data_fetcher.data_fetcher import DataFetcher
from json_parser.json_parser import JsonTree


class UniprotParser(object):

	def __init__(self):
		self.df = DataFetcher()
		# uniprot tree
		self.utree = JsonTree('./uniprot.txt')
		# mapping tree
		self.mtree = JsonTree(
			'./mapping.txt',
			{
				'',
				'.__dict.PDB'
			})
		# listing tree
		self.ltree = JsonTree(
			'./listing.txt',
			{
				''
			}
		)
		# entity tree
		self.etree = JsonTree('./entity.txt')

	def start(self):

		print('Downloading uniprot list...')
		ulist = self.df.get_uniprot_list()
		print('Collecting %d uniprots...\n\n' % len(ulist))
		i = 0
		j = 0
		k = 0
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

			pdbs = {}
			for pdb in elem['id']:
				pdb_id = pdb[:-1]
				chain_id = pdb[-1]

				if pdb_id not in pdbs:
					pdbs[pdb_id] = set()
				pdbs[pdb_id].add(chain_id)

			for pdb in pdbs:
				j += 1
				print('--- #%d: %s' % (j, pdb))

				print('---> Listing...')
				self.ltree.acquire(
					self.df.get_ebi_listing(pdb))

				print('---> Entities...')
				for chain in pdbs[pdb]:
					k += 1
					print('--- #%d: %s, %s' % (k, pdb, chain))
					self.etree.acquire(
						self.df.get_repeats_entities(pdb, chain))

			print('<<<<<<<<<<\n')

			# update state
			self.utree.save()
			self.mtree.save()
			self.ltree.save()
			self.etree.save()


if __name__ == '__main__':
	uparser = UniprotParser()
	uparser.start()

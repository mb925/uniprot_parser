import sys

from data_fetcher.data_fetcher import DataFetcher
from json_parser.json_parser import JsonParser

class UniprotParser(object):

if __name__ == '__main__':

	data_fetcher = DataFetcher()

	print('Downloading uniprot list...')
	ulist = data_fetcher.get_uniprot_list()
	if not ulist:
		sys.exit()

	# init JsonParser
	parser = JsonParser()
	print('Starting fetch of %d uniprots...\n\n' % len(ulist))
	for i in range(0, len(ulist)):

		elem = ulist[i]

		# check list formatting
		if not type(elem) == dict:
			print('%s: not a dict\n' % str(elem))
			continue

		if not 'id' in elem:
			print('%s: missing id\n' % str(elem))

		if not 'uniprotid' in elem:
			print('%s: missing uniprot id\n' % str(elem))
			continue

		print('Fetching %s...' % str(elem['uniprotid']))
		uinfo = data_fetcher.get_ebi_sequence(elem['uniprotid'])
		if not uinfo:
			continue

		print('- Parsing %s...' % str(elem['uniprotid']))
		parser.parse(uinfo)

		print('-- Restructuring %s...' % str(elem['uniprotid']))
		parser.restructure()

		print('--- Done #%d!\n\n' % i)

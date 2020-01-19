import json

from json_parser.json_dict import JsonDict
from json_parser.json_type import JsonType


class JsonParser(object):

	def __init__(self):

		self.parsed = None
		self.paths = {}
		self.restructured = {}

	def parse(self, json_data, out_path='./paths.json', log_path='./paths_log.txt'):

		# reset paths
		self.paths = {}

		# open info files
		log_file = open(log_path, 'w')
		out_file = open(out_path, 'w')

		# parse input json
		self.parsed = JsonDict(json_data, 'ROOT', 0, self.paths, log_file)

		# save results
		json.dump(self.paths, out_file, indent=2)
		log_file.close()
		out_file.close()

	def restructure(self, out_path='./restructured.json', log_path='./restructured_log.txt'):

		for key in self.paths:
			# set pointer to start position
			ptr = self.restructured
			for node in str(key).split(JsonType.sep):
				if node not in ptr:
					ptr[node] = {'__count': 0, '__values': {}}
				ptr = ptr[node]

			ptr['__count'] += self.paths[key]['count']
			for value in self.paths[key]['values']:
				if len(ptr['__values']) > 25:
					value = '...'
				if value not in ptr['__values']:
					ptr['__values'][value] = 1
				else:
					ptr['__values'][value] += 1

		# save result
		restructured_file = open(out_path, 'w')
		json.dump(self.restructured, restructured_file, indent=2)
		restructured_file.close()

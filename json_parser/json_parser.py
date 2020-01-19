import json

from json_parser.json_dict import JsonDict
from json_parser.json_type import JsonType


class JsonParser(object):

	def __init__(self, out_path='./paths.json'):

		self.parsed = None
		self.paths = {}
		self.restructured = {}
		self.out_path = out_path

	def parse(self, json_data, out_path=None, log_path='./paths_log.txt'):

		# reset paths
		self.paths = {}

		# open info files
		log_file = open(log_path, 'w')
		out_file = None
		if out_path:
			out_file = open(out_path, 'w')

		# parse input json
		self.parsed = JsonDict(json_data, 'ROOT', 0, self.paths, log_file)

		# save results
		log_file.close()
		if out_file:
			json.dump(self.paths, out_file, indent=2)
			out_file.close()

	def restructure(self):

		for key in self.paths:
			# set pointer to start position
			ptr = self.restructured
			for node in str(key).split(JsonType.sep):
				if node not in ptr:
					ptr[node] = {'__count': 0, '__values': {}}
				ptr = ptr[node]

			ptr['__count'] += self.paths[key]['count']
			for value in self.paths[key]['values']:
				if value not in ptr['__values']:
					if len(ptr['__values']) > 25:
						if not '...' in ptr['__values']:
							ptr['__values']['...'] = 1
						else:
							ptr['__values']['...'] += 1
					else:
						ptr['__values'][value] = 1
				else:
					ptr['__values'][value] += 1

		# save result
		restructured_file = open(self.out_path, 'w')
		json.dump(self.restructured, restructured_file, indent=2)
		restructured_file.close()

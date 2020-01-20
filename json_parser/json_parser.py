from json_parser.json_node import JsonNode


class JsonTree:

	def __init__(self, out_path='./tree.txt', aggregators=None):
		self.root = JsonNode()
		self.out_path = out_path
		self.aggregators = aggregators

	def acquire(self, json):
		self.root.acquire(json)

	def save(self):
		file = open(self.out_path, 'w')
		file.write(self.root.__str__())
		file.close()

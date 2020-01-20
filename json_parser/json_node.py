import json_parser.json_const as JC


class JsonNode:

	def __init__(self, parent=None, name=''):

		# check parent type
		if parent is not None and not type(parent) == JsonNode:
			raise TypeError('wrong parent type')
		# set parent node
		self.parent = parent
		# set name
		self.name = str(name)
		# set path
		self.path = ''
		if self.parent is not None:
			self.path = '%s%s%s' % (self.parent.get_path(), JC.sep, self.name)
		# set depth from root
		self.depth = len(self.path.split(JC.sep)) - 1
		# set tabs char
		self.tabs = ''.join([JC.tab for i in range(0, self.depth)])

		# init counter
		self.counter = 0
		# init children
		self.children = {}
		# init values storage
		self.types = {}

	def __str__(self):
		res = '%s-%s(%d):' % (self.tabs, self.name, self.counter)
		if len(self.types) > 0:
			typ = '('
			for key in self.types:
				typ += '%s:%d,' % (key, len(self.types[key]))
			res += typ + ')'
		res += '\n'

		for key in self.children:
			res += self.children[key].__str__()
		return res

	def get_name(self):
		return self.name

	def get_path(self):
		return self.path

	def add(self, json):
		try:
			float(json)
			atype = 'num'

		except (ValueError, TypeError):
			atype = str(type(json).__name__)

		if atype not in self.types:
			self.types[atype] = set()

		if len(self.types[atype]) < JC.num:
			value = str(json)
			if len(value) > JC.lng:
				value = '%s...' % value[:JC.lng]
			self.types[atype].add(value)

	def acquire(self, json):

		self.counter += 1

		if type(json) == dict:
			for prop in json:
				if prop not in self.children:
					self.children[prop] = JsonNode(self, prop)
				self.children[prop].acquire(json[prop])

		elif type(json) == list:
			if JC.lst not in self.children:
				self.children[JC.lst] = JsonNode(self, JC.lst)
			for element in json:
				self.children[JC.lst].acquire(element)

		else:
			if JC.val not in self.children:
				self.children[JC.val] = JsonNode(self, JC.val)
			self.children[JC.val].add(json)

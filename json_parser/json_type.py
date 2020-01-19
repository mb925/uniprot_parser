class JsonType:

	sep = '.'
	tab = '  '
	types = ['list', 'dict', 'string', 'number']

	def __init__(self, atype, name, depth, paths):
		# check type
		if atype not in JsonType.types:
			raise ValueError('unexpected value: %s' % atype)
		self.type = atype
		# init object name
		self.name = name
		# init depth level
		self.depth = depth
		# insert path
		self.paths = paths
		self.increment_path(name)

	def get_type(self):
		return self.type

	def get_name(self):
		return self.name

	def get_depth(self):
		return self.depth

	def get_tabs(self):
		tmp = [JsonType.tab for x in range(0, self.depth)]
		return ''.join(tmp)

	def increment_path(self, path):
		if path not in self.paths:
			self.paths[path] = {'count': 1, 'values': []}
		else:
			self.paths[path]['count'] += 1

	def add_value(self, path, value):

		# convert to string
		value = str(value)

		# max number of char to store
		if len(value) > 10:
			value = '%s...' % value[:10]

		# create if not exists
		if path not in self.paths:
			self.paths[path] = {'count': 1, 'values': [value]}

		else:
			# max number of values to store
			if len(self.paths[path]['values']) > 25:
				value = '...'
			# store if not saved yet
			if value not in self.paths[path]['values']:
				self.paths[path]['values'].append(value)

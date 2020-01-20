class JsonType:

	sep = '.'
	tab = '  '
	types = ['list', 'dict', 'string', 'number']

	def __init__(self, atype, name, depth, paths, aggregators):
		# check type
		if atype not in JsonType.types:
			raise ValueError('unexpected value: %s' % atype)
		self.type = atype
		# init name
		self.name = name
		# aggregate name if needed
		name_split = name.split('.')
		tmp = None
		for aggregator in aggregators:
			if not len(name_split) == len(aggregator):
				continue
			if name_split[:-1] == aggregator[:-1]:
				tmp = name_split[-1]
				self.name = '%s_aggr' % name[:-len(tmp)]
				break
		# init depth level
		self.depth = depth
		# insert path
		self.paths = paths
		self.increment_path(self.name, tmp)

	def get_type(self):
		return self.type

	def get_name(self):
		return self.name

	def get_depth(self):
		return self.depth

	def get_tabs(self):
		tmp = [JsonType.tab for x in range(0, self.depth)]
		return ''.join(tmp)

	def increment_path(self, path, aggr):
		if path not in self.paths:
			self.paths[path] = {'count': 0, 'values': [], 'aggr': []}

		self.paths[path]['count'] += 1
		if aggr is not None and not aggr in self.paths[path]['aggr']:
			self.paths[path]['aggr'].append(aggr)

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

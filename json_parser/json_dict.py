from json_parser.json_type import JsonType


class JsonDict(JsonType):

	def __init__(self, adict, name, depth, paths, aggregators, log_file):

		# avoid recursive import problem
		from json_parser.json_list import JsonList
		from json_parser.json_simple import JsonSimple

		# init parent class
		super().__init__('dict', name, depth, paths, aggregators)

		# init children
		self.values = {}
		for k in adict:
			val = adict[k]

			# check collision with separator
			k = str(k)
			if JsonType.sep in k:
				raise ValueError('%s: path with separator in node -> %s' % (name, k))

			name = '%s.%s' % (super().get_name(), k)
			if type(val) == dict:
				self.values[k] = JsonDict(val, name, depth+1, paths, aggregators, log_file)
			elif type(val) == list:
				self.values[k] = JsonList(val, name, depth+1, paths, aggregators, log_file)
			else:
				self.values[k] = JsonSimple(val, name, depth+1, paths, aggregators, log_file)

	def __str__(self):

		tabs = super().get_tabs()
		res = '{\n'
		for k in self.values:
			res += '%s%s%s: %s,\n' % (tabs, JsonType.tab, str(k), self.values[k].__str__())
		return res + '%s}' % tabs

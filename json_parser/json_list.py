from json_parser.json_type import JsonType


class JsonList(JsonType):

	def __init__(self, alist, name, depth, paths, aggregators, log_file):

		# avoid recursive import problem
		from json_parser.json_dict import JsonDict
		from json_parser.json_simple import JsonSimple

		# init parent class
		super().__init__('list', name, depth, paths, aggregators)

		# init children
		name = '%s._arr' % super().get_name()
		self.values = []
		for e in alist:
			if type(e) == dict:
				self.values.append(JsonDict(e, name, depth+1, paths, aggregators, log_file))
			elif type(e) == list:
				self.values.append(JsonList(e, name, depth+1, paths, aggregators, log_file))
			else:
				self.values.append(JsonSimple(e, name, depth+1, paths, aggregators, log_file))

	def __str__(self):

		tabs = super().get_tabs()
		res = '[\n'
		for e in self.values:
			res += '%s%s%s,\n' % (tabs, JsonType.tab, e.__str__())
		return res + '%s]' % tabs

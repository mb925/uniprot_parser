import sys

from json_parser.json_type import JsonType


class JsonSimple(JsonType):

	def __init__(self, value, name, depth, paths, aggregators, log_file):

		self.depth = depth
		if value is None:
			self.value = 'none'
		else:
			self.value = value

		try:
			float(self.value)
			super().__init__('number', name, depth, paths, aggregators)
			name = '%s%snumber' % (super().get_name(), JsonType.sep)

		except ValueError:
			if not isinstance(value, str):
				log_file.write('%s: invalid simple object -> %s' % (name, value))
				return
			super().__init__('string', name, depth, paths, aggregators)
			name = '%s%sstring' % (super().get_name(), JsonType.sep)

		super().increment_path(name, None)
		super().add_value(name, value)

	def __str__(self):
		return super().get_type()

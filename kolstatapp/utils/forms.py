import re

def underscore_delim(s):
	return re.sub('[A-Z]', lambda x: '_' + x.group(0).lower(), s)[1:]


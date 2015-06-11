'''
Parsely
A toy command line option parser
Author: gmareske
Email: gmareske@gmail.com
'''
import os
import sys
import string

__all__ = ['CLParser']


# basic data storage classes
class Option(object):
	def __init__(self,name,label,help,arg_type):
		self.name = name
		self.label = label
		self.help = help
		self.arg_type = arg_type

class Argument(object):
	def __init__(self,name,label,help,num_args,arg_type,required=False):
		self.name = name
		self.label = label
		self.help = help
		self.num_args = num_args
		self.arg_type = arg_type
		self.required = required

# parser class
class CLParser(object):

	def __init__(self,program_name=sys.argv[0],description='',post_description='',option_prefix='-'):
		self.name = program_name
		self.desc = description
		self.post_desc = post_description
		self.prefix = option_prefix
		self._arguments = []
		self._options = []
		self.values = {}

	def _exit():
		sys.exit()

	def add_argument(self,name,label=None,help='',num_args=1,arg_type=None,required=False):
		# name begins with self.prefix
		# thus, it's an option
		if name[0] == self.prefix:
			self.add_option(name,label,help,arg_type)
		else:
			self.add_positional_argument(name,label,help,num_args,arg_type,required)

	def add_option(self,name,label,help,arg_type):
		self._options.append(Option(name,label,help,arg_type))

	def add_positional_argument(self,name,label,help,num_args,arg_type,required):
		self._arguments.append(Argument(name,label,help,num_args,arg_type,required))

	def parse_args(self,args=sys.argv[1:]):
		for index, arg in enumerate(args):
			print('parsing: {}'.format(arg))
			if arg[0] == '-':
				print('{} is an option...'.format(arg))
				if arg[1] == '-':
					self._set(arg)
				else:
					for char in arg[1:]:
						self._set(self.prefix + char)

			else:
				for pos_arg in self._arguments:
					if pos_arg.num_args == '+':
						self._set(pos_arg.name, val=args[index:], others=pos_arg.label, dest_type = pos_arg.arg_type)
						return # break every loop, this is the end
					else:
						self._set(pos_arg.name,val=args[index:index+pos_arg.num_args], others=pos_arg.label, dest_type = pos_arg.arg_type)

		self._check_required()

	def _set(self,name,val=True, others=None, dest_type=bool, alt=None):
		print('Trying to set {0} to {1}'.format(name,val))
		def cast(item):
			return dest_type(item)

		if type(val) == bool:
			self.values[name] = val
			self.values[others] = val
		else:
			if type(val) == list:
				val = list(map(cast,val))
			else:
				val = cast(val)
			# get rid of any list if the length is 1
			if len(val) == 1:
				val = val[0]

			self.values[name] = val
			self.values[others] = val

	def _check_required(self):
		for pos_arg in self._arguments:
			if pos_arg.required:
				if self.get(pos_arg.name) == None and self.get(pos_arg.label) == None:
					raise Exception # TODO implement better exceptions

	def get(self,query):
		return self.values.get(query)


parser = CLParser(description='This is a program that takes strings and does things with them')
parser.add_argument('-s',label='sum',help='Sum the strings')
parser.add_argument('-l',label='list',help='List the strings')
parser.add_argument('string',label='S',help='the strings to use in the program',num_args='+',arg_type=str,required=True)
parser.parse_args(['-f','-s','ayy', 'lmao'])
print(parser.values)
parser.parse_args(['-sl','decent'])
print(parser.values)
parser.parse_args(['-s'])
print(parser.values)


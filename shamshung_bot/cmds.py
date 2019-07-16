import traceback
from tabulate import tabulate


class CmdSet:
	
	def __init__(self):
		self.cmds = {}
	
	def __getitem__(self, key):
		return self.cmds[key]
	
	def new(self, *args, **kwargs):
		def decor(f):
			self.cmds[f.__name__] = Cmd(name=f.__name__, func=f, *args, **kwargs)
			return f
		return decor


class ArgError(Exception):
	def __init__(self, message='Invalid paramaters given'):
		super().__init__(message)
		self.message = message


class Cmd:
	def __init__(self, name, func, desc='No description', usage=None):
		if usage == None:
			usage = name
		self.name = name
		self.func = func
		self.desc = desc
		self.usage = usage
	
	def __call__(self, args):
		try:
			return self.func(args)
		except ArgError as e:
			return f'Error: {e.message}\nUsage: {self.usage}'
		except Exception as e:
			tb = traceback.format_exc()
			return f'Unexpected error:\n```{tb}```'
	

cmds = CmdSet()


@cmds.new(desc='Sends text from bot', usage='say <message>')
def say(args):
	try:
		return args[1]
	except IndexError:
		raise ArgError('No message given')


@cmds.new(desc='Displays info about all commands')
def help(args):
	table = []
	for cmd in cmds.cmds:
		table.append([cmd.name, cmd.usage, cmd.desc])
	text = tabulate(table, headers=['Name', 'Usage', 'Description'], tablefmt='fancy_grid')
	return f'```{text}```'

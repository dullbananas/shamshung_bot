import traceback
import random
from tabulate import tabulate
from . import utils


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
	for cmd in cmds.cmds.values():
		table.append([cmd.usage, cmd.desc])
	text = tabulate(table, headers=['Command', 'Description'], tablefmt='fancy_grid')
	footer = 'Made by Dull Bananas - https://dull.pythonanywhere.com\nGitHub repository: https://github.com/dullbananas/shamshung_bot'
	return f'```{text}```\n{footer}'


@cmds.new(desc='Displays a random recently posted meme on cleanmemes.com')
def meme(args):
	wp = utils.read_webpage('https://cleanmemes.com')
	parser = utils.ImageExtractor()
	parser.feed(str(wp))
	urls = filter((lambda x: 'gravatar' not in x), parser.urls)
	return random.choice(urls)

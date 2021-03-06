import traceback
import inspect
import random
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

	def _filter_args(self, args, func):
		sig = inspect.signature(func)
		filter_keys = [param.name for param in sig.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD]
		filtered_args = {key:args[key] for key in filter_keys}
		return filtered_args

	def __call__(self, kwargs):
		try:
			return self.func(**self._filter_args(kwargs, self.func))
		except ArgError as e:
			return Result(f'Error: {e.message}\nUsage: {self.usage}')
		except Exception:
			tb = traceback.format_exc()
			return Result(f'Unexpected error:\n```{tb}```')


class Result:
	def __init__(self, text=None, **kwargs):
		self.text = text
		self.kwargs = kwargs

	def get_dict(self):
		d = self.kwargs
		d['content'] = self.text
		return d


cmds = CmdSet()


@cmds.new(desc='Sends text from bot', usage='say <message>')
def say(args):
	try:
		return Result(args[1])
	except IndexError:
		raise ArgError('No message given')


@cmds.new(desc='Displays info about all commands')
def help(args):
	if len(args) > 1:
		try:
			cmd = cmds.cmds[args[1]]
		except KeyError:
			return 'Command not found'
		text = f'**{cmd.name}**\nUsage: `{cmd.usage}`\nDescription: {cmd.desc}'
	else:
		text = '**Shamshung Bot Commands**\n'
		names = [f' - {cmd.name}' for cmd in cmds.cmds.values()]
		text += '\n'.join(sorted(names))
		text += '\n\nTo give a parameter with spaces to a command, put it in quotes: shamshung.say "FBI OPEN UP!!!!!"'

	footer = 'Made by Dull Bananas - https://dull.pythonanywhere.com\nGitHub repository: https://github.com/dullbananas/shamshung_bot' if not len(args) > 1 else ''
	return Result(f'{text}\n\n{footer}')


@cmds.new(desc='Displays either a random recently posted meme on cleanmemes.com, or a meme created my the creators of this bot')
def meme():
	wp = utils.read_webpage('https://cleanmemes.com')
	parser = utils.ImageExtractor()
	parser.feed(str(wp))
	urls = list(filter((lambda x: 'gravatar' not in x), parser.urls)) + [
		# Sam sung his last song
		'https://doc-0g-60-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/fjbrofpv1ilind9qnuejm3s3j0msmjpa/1563292800000/00697965516584679432/*/1aFvFNjHpN4pVLax3KB-HWNRN7hVRFqdB?e=download',
		# Cupcake
		'https://doc-00-7s-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/pvlb13585lfho7cqrvmpvgf6juuh6la6/1563292800000/05448460070245808790/*/1yqoto8VYH5Dwvlu1W4GNgwSTmELjT11R?e=download',
	]
	return Result(random.choice(urls))


@cmds.new(desc='Sorts the given parameters in alphabetical order', usage='sort <text>...')
def sort(args):
	return Result('\n'.join(sorted(args[1:])))


@cmds.new(desc='Shows a random color')
def randcolor(msg):
	from PIL import Image
	import discord

	img = Image.new('RGB', (64,64), (random.randrange(256), random.randrange(256), random.randrange(256)))
	msg_id = str(msg.id)
	filename = f'temp/rand_color_{msg_id}.png'

	img.save(filename)
	fp = open(filename, 'rb')
	return Result(file=discord.File(fp))


@cmds.new(desc='Generates an insult')
def insult():
	import random
	ADJECTIVES = [
		'fat',
		'obese',
		'stupid',
	]
	NOUNS = [
		'failure',
		'idiot',
	]
	POOP = [
		'you get run over by a truck',
		'your mom spanks you 69 times',
	]
	adj = random.choice(ADJECTIVES)
	noun = random.choice(NOUNS)
	poop = random.choice(POOP)
	return Result(f'You are a {adj} {noun}. I hope {poop}.')

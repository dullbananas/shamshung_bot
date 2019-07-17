import discord
import logging
import shlex
from . import db
from .cmds import cmds
from .swears import swears

logging.basicConfig(level=logging.INFO)



class ShamshungBot(discord.Client):
	
	
	async def on_ready(self):
		print(f'Bot is ready as {self.user}')
	
	
	async def on_message(self, msg):
		if msg.author.id == self.user.id:
			return
		
		logging.info(f'Message from {msg.author}: {msg.content}')
		session = db.Session()
		prefix = 'shamshung.'
		for i in session.query(db.Prefix).filter(db.Prefix.server_id == msg.guild.id):
			prefix = i.prefix
		
		if msg.content.startswith(prefix):
			try:
				try:
					args = shlex.split(msg.content[len(prefix):])
				except ValueError as e:
					emsg = str(e)
					await msg.channel.send(f'Error: {emsg}')
				output = cmds.cmds[args[0]]({
					'args': args,
					'msg': msg,
					'prefix': prefix,
					'session': session,
				})
			except KeyError:
				output = 'Invalid command'
			except IndexError:
				output = 'No command given'
			
			for swear in swears:
				if swear.lower() in output.lower():
					await msg.channel.send('STOP MAKIN\' ME SWEAR')
					return
			
			await msg.channel.send(output)

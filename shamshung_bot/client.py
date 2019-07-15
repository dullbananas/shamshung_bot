import discord
import logging
import shlex
from . import db, cmds

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
		for i in session.query(db.Prefix).filter(Prefix.server_id == msg.guild.id):
			prefix = i.prefix
		
		if msg.content.startswith(prefix):
			args = shlex.split(msg.content[len(prefix):])
			await msg.channel.send(repr(args))

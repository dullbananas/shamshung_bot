import discord



class ShamshungBot(discord.Client):
	
	
	async def on_ready(self):
		print(f'Bot is ready as {self.user}')
	
	
	async def on_message(self, msg):
		print(f'Message from {msg.author}: {msg.content}')

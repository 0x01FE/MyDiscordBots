import asyncio, discord
from discord.ext import commands

bot = commands.Bot("%%%")
bot.remove_command('help')
incorrect_channel = None
message_id = None

@bot.event
async def on_ready():
	global incorrect_channel
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	incorrect_channel = bot.get_channel(838255076606083103)

@bot.event
async def on_message(message):
	global message_id
	await update_message_id()
	if str(message.channel) == 'secret-channel':
		if "i don't know" in message.content.lower() or "i don’t know" in message.content.lower():
			temp = await message.channel.send('correct')
			roles = message.guild.get_role(838158542245855232)
			await message.author.add_roles(roles,reason='they gave the correct password')
			await message.delete()
			await asyncio.sleep(5)
			await temp.delete()
		else:
			if not message.author.bot:
				temp = await message.channel.send('incorrect')
				try:
					old_message = await incorrect_channel.fetch_message(int(message_id.replace('\n','')))
				except:
					old_message = None
				if old_message:
					if len(old_message.content) + len(message.content) >= 2000:
						last_message = await incorrect_channel.send(message.content)
						with open('message_id.txt','w') as f:
							f.write(str(last_message.id))
					else:
						await old_message.edit(content=old_message.content+'\n'+message.content,suppress=True)
				else:
					last_message = await incorrect_channel.send(message.content)
					with open('message_id.txt','w') as f:
						f.write(str(last_message.id))
				await message.delete()
				await asyncio.sleep(5)
				await temp.delete()
	else:
		await bot.process_commands(message)
		

async def update_message_id():
	global message_id
	with open('message_id.txt','r') as f:
		message_id = f.read()

		
bot.run('')

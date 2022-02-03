import aiohttp, asyncio, discord, requests, os, pyttsx3, dice_master as dice, tweepy, wget, discord, math, glob, json
import random as r
from urllib.parse import urlparse
from bs4 import BeautifulSoup as _soup
from PIL import Image
from fpdf import FPDF
from discord.ext import commands, tasks
from multiprocessing import Process
from moviepy.editor import VideoFileClip

## took out all the API keys.

status_list = {
	'Listening' : ['ZUN','Nanahira','Master Boot Record','Goreshit'],
	'Playing' : ['Your mother.','Touhou 14.5 : Urban Legends in Limbo', 'Touhou 7 : Perfect Cherry Blossom']
}
locations = {'gifs':'gifs\\','downloads':'D:\\bot downloads\\'}
tenor_base_url = 'https://g.tenor.com/v1/gifs?ids={}&key={}'
tenor_apikey = '' 
first_ready = True
rewind = '\u23EA'
arrow_left = '\u2B05'
arrow_right = '\u27A1'
fast_forward = '\u23E9'
thumbs_up = u"\U0001F44D"
x_emoji = '\u274C'
active_viewers = {} ## by message id
bot_author = '0x01FE#1244'
engine = pyttsx3.init()
voices = engine.getProperty('voices')
bot = commands.Bot("-")
bot.remove_command('help')
guns_channel = None
vc = None
pic_ext = ['.jpg','.png','.jpeg','.webp']
tokens = open('tokens.txt','r').read().split()
consumer_key = ''
consumer_secret = ''
access_token = tokens[0]
access_token_secret = tokens[1]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
##session = requests.Session()

## basic commands



@bot.event
async def on_ready():
	global first_ready
	global other_channels
	global emperor
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="ZUN"))
	##await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='test'))
	if first_ready:
		other_channels = {}
		##vc_check.start()
		status_change.start()
		other_server = bot.get_guild(883156816249368576)
		emperor = await bot.fetch_user(516017792739311636) ## (me)
		first_ready = False
		
	
@bot.command()
async def ping(ctx):
	await ctx.send("Pong")
	print("pinged")
	
@bot.command()
async def help(ctx):
	embed_colour = ctx.me.colour
	embed = discord.Embed(
		title = "Help Menu",
		description = 'Welcome to the help menu.',
		colour = embed_colour
	)
	embed.set_footer(text='Bot developed by '+bot_author+".")
	##embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/547243727106736132/833093134102560789/ar15face.png')
	##embed.set_author(name=author, icon_url = 'https://cdn.discordapp.com/avatars/516017792739311636/213b82ef7b154ef53654ca9219c2197e.png?size=128')
	embed.add_field(name='-help', value='> Brings up this help menu.',inline=False)
	embed.add_field(name='-ping', value='> Ask the bot if it is still alive.',inline=False)
	embed.add_field(name='-twitter', value='> Rip video(s), gif(s), or image(s) from a twitter post.\n > **Usage:** `-twitter (link) (res_up [optinal]) (sp or spoiler) ([*] where * = the numbers for the images you want extracted) (tags{tag1,tag2} make sure you have no spaces) (sync)`\n **Example:** -twitter (link) res_up (would do the thing and res the image up as well)',inline=False)
	embed.add_field(name='-res_up', value='> Reply to or post an image with this command and up the resolution!\n > **Usage:** `-res_up (noise amount [1-3]) (resolution multiplier [2 is reccomended]) (image [or reply to an image])`',inline=False)
	embed.add_field(name='-dicer', value='> Want to make an image into dice?\n > **Usage:** `-dicer (image)`',inline=False)
	embed.add_field(name='-channel_scroll', value='> Use an embed to scroll through images in the current channel. (give the bot some time to get all the images)',inline=False)
	embed.add_field(name='-set', value = '> settings for the bot. (brings up seperate help menu)', inline=False)
	embed.add_field(name='-leave', value='> Have the bot leave the call.',inline=False)
	embed.add_field(name='-ar15face', value='> Post the funny face.',inline=False)
	embed.add_field(name='-k11', value='> Say the funny thing.',inline=False)
	embed.add_field(name='-sodumb', value='> Send the funny gif.',inline=False)
	await ctx.send(embed=embed)
	
@bot.command()
async def dm_test(ctx):
	global emperor
	emperor_dm_channel = await emperor.create_dm()
	await emperor_dm_channel.send("test")

## utility
	
@bot.command()
async def twitter(ctx, *args):
	await cmd_log_add(ctx.message.content,ctx.message.author,ctx.message.created_at)
	global other_channels
	extract_numbers = []
	tags = []
	trigger = False
	embed_colour = ctx.me.colour
	resup = False
	sync = False
	spoiler_tag = False
	if len(args) > 1:
		if 'res_up' in args:
			resup = True
		if 'spoiler' in args or 'sp' in args:
			spoiler_tag = True
		if 'sync' in args:
			sync = True
		for arg in args:
			if '[' in arg and ']' in arg:
				extract_temp = arg.split(',')
				for num in extract_temp:
					num = num.replace('[','')
					num = num.replace(']','')
					extract_numbers.append(int(num))
			elif 'tags{' in arg or '{' in arg and '}' in arg:
				extract_temp = arg.split(',')
				for num in extract_temp:
					num = num.replace('tags{','')
					num = num.replace('{','')
					num = num.replace('}','')
					tags.append(num)
	if ctx.message.reference:
		if len (args) > 0:
			if 'res_up' in args:
				resup = True
			if 'spoiler' in args or 'sp' in args:
				spoiler_tag = True
			for arg in args:
				if '[' in arg and ']' in arg:
					extract_temp = arg.split(',')
					for num in extract_temp:
						num = num.replace('[','')
						num = num.replace(']','')
						extract_numbers.append(int(num))
				elif 'tags{' in arg or '{' in arg and '}' in arg:
					extract_temp = arg.split(',')
					for num in extract_temp:
						num = num.replace('tags{','')
						num = num.replace('}','')
						tags.append(num)
		replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
		for arg in replied_message.content.split(' '):
			if 't.co' in arg:
				r = requests.get(arg)
				tweet_url = r.url
				break
			elif 'twitter.com' in arg:
				tweet_url = arg
				break
	elif 't.co' in args[0]:
		r = requests.get(args[0])
		tweet_url = r.url
	else:
		tweet_url = args[0]
	for item in tweet_url.split('/'):
		if trigger:
			tweet_id = item
			break
		else:
			if item == 'status':
				trigger = True
	try:
		tweet = api.get_status(tweet_id, tweet_mode="extended")
	except:
		await ctx.send("invalid link probably")
	try:
		text = (tweet.retweeted_status.full_text)
	except AttributeError:  # Not a Retweet
		text = (tweet.full_text)
	if tags != []:
		text+='\nTags:'
		for tag in tags:
			text+='\n'+tag
	embed = discord.Embed(
		description = text,
		colour = embed_colour
	)
	embed.set_author(name=tweet.user.screen_name,icon_url=tweet.user.profile_image_url_https)
	embed.set_footer(text='Command requested by ' + str(ctx.message.author))
	if 'media' in tweet.entities:
		media = tweet.extended_entities['media']
		##print(json.dumps(media,sort_keys=True, indent=4))
		file_stats = None
		counter_a = 1
		for item in media:
			if counter_a not in extract_numbers and extract_numbers 	!= []:
				counter_a+=1
				continue
			if 'video_info' in item:
				for variant in item['video_info']['variants']:
					if variant['content_type'] == 'video/mp4':
						media_url = variant['url']
						break
				wget.download(media_url)
				if item['type'] == 'animated_gif':
					clip = VideoFileClip(media_url.split('/')[-1])
					clip.write_gif('output.gif')
					if (os.stat('output.gif').st_size/(1024*1024)) < 8:
						await ctx.send(file=discord.File('output.gif'))
						if sync:
							await other_channels[ctx.channel.name].send(file=discord.File('output.gif', spoiler = spoiler_tag),embed=embed)
					else:
						await ctx.send(content="GIF file was too big.",file=discord.File(media_url.split('/')[-1].split('.mp4')[0]+'.mp4'))
					await ctx.send(embed=embed)
					os.remove('output.gif')
					os.remove(media_url.split('/')[-1].split('.mp4')[0]+'.mp4')
				else:
					if (os.stat(media_url.split('/')[-1].split('.mp4')[0]+'.mp4')).st_size/(1024*1024) <= 8:
						await ctx.send(file=discord.File(media_url.split('/')[-1].split('.mp4')[0]+'.mp4', spoiler = spoiler_tag),embed=embed)
						if sync:
							await other_channels[ctx.channel.name].send(file=discord.File(media_url.split('/')[-1].split('.mp4')[0]+'.mp4', spoiler = spoiler_tag),embed=embed)
					else:
						await ctx.send('Video was too large.')
					os.remove(media_url.split('/')[-1].split('.mp4')[0]+'.mp4')
			elif item['type'] == 'photo':
				media_url = item['media_url_https']
				image = requests.get(media_url+':large')
				if 200 == image.status_code:
					with open(media_url.split('/')[-1], 'wb') as f:
						f.write(image.content)
				regular_file_name = media_url.split('/')[-1]
				if resup:
					res_file_name = media_url.split('/')[-1][:-4]+'_[L3][x2.00].png'
					await bot.loop.run_in_executor(None, res_up_local, regular_file_name)
					if (os.stat(res_file_name).st_size/(1024*1024)) > 8:
						if item == media[-1]:
							await ctx.send(file=discord.File(regular_file_name, spoiler = spoiler_tag),embed=embed)
							if sync:
								await other_channels[ctx.channel.name].send(file=discord.File(regular_file_name, spoiler = spoiler_tag),embed=embed)
						else:
							await ctx.send(content="Res'd file was too big.",file=discord.File(regular_file_name, spoiler = spoiler_tag))
						os.remove(regular_file_name)
						os.remove(res_file_name)
					else:
						if item == media[len(extract_numbers)-1]:
							await ctx.send(file=discord.File(res_file_name, spoiler = spoiler_tag),embed=embed)
							if sync:
								await other_channels[ctx.channel.name].send(file=discord.File(res_file_name, spoiler = spoiler_tag),embed=embed)
						else:
							await ctx.send(file=discord.File(res_file_name, spoiler = spoiler_tag))
							if sync:
								await other_channels[ctx.channel.name].send(file=discord.File(res_file_name, spoiler = spoiler_tag))
						os.remove(res_file_name)
						os.remove(regular_file_name)
				else:
					if item == media[len(extract_numbers)-1]:
						await ctx.send(file=discord.File(regular_file_name, spoiler = spoiler_tag),embed=embed)
						if sync:
							await other_channels[ctx.channel.name].send(file=discord.File(regular_file_name, spoiler = spoiler_tag),embed=embed)
					else:
						await ctx.send(file=discord.File(regular_file_name, spoiler = spoiler_tag))
						if sync:
							await other_channels[ctx.channel.name].send(file=discord.File(regular_file_name, spoiler = spoiler_tag))
					os.remove(regular_file_name)
			counter_a+=1
		await ctx.message.delete()
	
	
@bot.command()
async def sync(ctx, *args):
	global other_channels
	if ctx.message.reference:
		replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
		url = replied_message.attachments[0].url
		response = requests.get(url, timeout=60)
		file = open('sync.png','wb')
		file.write(response.content)
		file.close()
		if replied_message.embeds:
			await other_channels[ctx.channel.name].send(file=discord.File('sync.png'),embed=replied_message.embeds[0])
		else:
			await other_channels[ctx.channel.name].send(file=discord.File('sync.png'))
	else:
		await ctx.send('There was no message to reference.')
	
@bot.command()
async def download_channel(ctx):
	if str(ctx.message.author) == bot_author:
		history = await ctx.message.channel.history(limit=None).flatten()
		epic_num = 0
		for message in history:
			if message.attachments:
				print("downloading attachment...")
				response = requests.get(message.attachments[0].url,timeout=60)
				file = open(message.attachments[0].filename, "wb")
				file.write(response.content)
				file.close()
				print("downloaded.")
			elif message.embeds:
				if message.embeds[0].image:
					print("downloading embed...")
					print(message.embeds)
					for embed in message.embeds:
						response = requests.get(embed.image.url, timeout=60)
						##print(message.embeds[0].title)
						##print(type(message.embeds[0].title))
						file = open("epic_embed"+str(epic_num)+".png", "wb")
						file.write(response.content)
						file.close()
						epic_num+=1
					print("downloaded.")
		channel = ctx.message.channel
		async with ctx.typing():
			channel_history = await channel.history(limit=None).flatten()
			
		print("done.")

@bot.command()
async def download(ctx, name=None, location=None):
	urls = []
	if str(ctx.message.author) == bot_author:
		if ctx.message.reference:
			replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
			if replied_message.attachments:
				for attachment in replied_message.attachments:
					urls.append(attachment.url)
			elif replied_message.embeds:
				for embed in replied_message.embeds:
					urls.append(embed.url)
		else:
			if ctx.message.attachments:
				for attachment in ctx.message.attachments:
					urls.append(attachment.url)
			elif ctx.message.embeds:
				for embed in ctx.message.embeds:
					urls.append(embed.url)
		for url in urls:
			if name:
				filename = name + '.' + os.path.basename(urlparse(url).path).split('.')[-1]
			else:
				filename = os.path.basename(urlparse(url).path)
			response = requests.get(url, timeout=60)
			if location:
				file = open(locations[location.lower()]+filename,'wb')
			else:
				file = open(locations['downloads']+filename,'wb')
			file.write(response.content)
			file.close()
		await ctx.message.add_reaction(thumbs_up)
								
@bot.command()
async def gatherWordInfo(ctx):
	if str(ctx.message.author) == bot_author:
		for guild in bot.guilds:
			for channel in guild.text_channels:
				pass

@bot.command()
async def channel_scroll(ctx):
	global active_viewers
	embed_colour = ctx.me.colour
	channel = ctx.message.channel
	async with ctx.typing():
		channel_history = await channel.history(limit=None).flatten()
	image_links = []
	for message in channel_history:
		if message.attachments:
			for attachment in message.attachments:
				image_links.append((attachment.url,message.id))
		elif message.embeds:
			for embed in message.embeds:
				if embed.type == 'image' or embed.type == 'gifv':
					image_links.append((embed.url,message.id))
	embed_send = discord.Embed(title='Image Viewer',description='Use the arrow reactions to scroll.',colour = embed_colour)
	embed_send.set_footer(text='Bot developed by ' + bot_author)
	embed_send.set_image(url=image_links[0][0])
	message_sent = await ctx.send(embed=embed_send)
	active_viewers[message_sent.id] = (message_sent, ctx.message.author, 0, image_links)
	await message_sent.add_reaction(emoji=rewind)
	await message_sent.add_reaction(emoji=arrow_left)
	await message_sent.add_reaction(emoji=arrow_right)
	await message_sent.add_reaction(emoji=fast_forward)

@bot.command()
async def res_up(ctx, *args):
	file_queue = []
	frames = []
	frame_queue = []
	duration = None
	async with ctx.typing():
		##await asyncio.sleep(1) i did use this because sometimes discord embeds take a moment to embed but we will see about that... (12/4/2021 - i think it's fixed now)
		noise = '3'
		scale = '2'
		urls = []
		if len(args) == 2:
			if args[0].isdecimal():
				noise = args[0]
			if args[1].isdecimal():
				scale = args[1]
		elif len(args) == 3:
			if args[1].isdecimal():
				noise = args[1]
			if args[2].isdecimal():
				scale = args[2]
		if ctx.message.reference:
			replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
			if replied_message.attachments:
				for attachment in replied_message.attachments:
					urls.append(attachment.url)
			elif replied_message.embeds:
				for embed in replied_message.embeds:
					urls.append(embed.url)
		else:
			if ctx.message.attachments:
				for attachment in ctx.message.attachments:
					urls.append(attachment.url)
			elif ctx.message.embeds:
				for embed in ctx.message.embeds:
					urls.append(embed.url)
		for url in urls:
			filename = os.path.basename(urlparse(url).path)
			response = requests.get(url, timeout=60)
			file = open(filename, "wb")
			file.write(response.content)
			file.close()
			if filename[-3:] == 'gif':
				gif = Image.open(filename)
				duration = gif.info['duration']
				for frame in range(0,gif.n_frames):
					gif.seek(frame)
					gif.save(filename[:-4]+'_'+str(frame)+'.png')
					frame_queue.append((filename[:-4]+'_'+str(frame)+'.png',(noise, scale)))
			file_queue.append((filename,(noise, scale)))
		tasks = []
		for item in file_queue:
			if not item[0][-3:] == 'gif':
				tasks.append(bot.loop.run_in_executor(None, res_queue, item))
		for item in frame_queue:
			tasks.append(bot.loop.run_in_executor(None, res_queue, item))
		await asyncio.wait(tasks)
		for item in file_queue:
			if item[0][-3:] == 'gif':
				res_file_name = item[0][:-4]+'_[L'+item[1][0]+'][x'+item[1][1]+'.00].gif'
				for frame in frame_queue:
					res_frame_name = frame[0][:-4]+'_[L'+frame[1][0]+'][x'+frame[1][1]+'.00].png'
					frames.append(Image.open(res_frame_name))
				frames[0].save(res_file_name, save_all = True, append_images = frames[1:], optimize = True, duration = duration, loop = 0)
			else:
				res_file_name = item[0][:-4]+'_[L'+item[1][0]+'][x'+item[1][1]+'.00].png'
			file_stats = os.stat(res_file_name)
			if math.ceil(file_stats.st_size/(1024*1024)) > 8:
				await ctx.message.reply(content='The result for this image was too large...')
			else:
				if item == file_queue[-1]:
					await ctx.send('Command requested by '+str(ctx.message.author)+'.', file=discord.File(res_file_name))
				else:
					await ctx.send(file=discord.File(res_file_name))
				if ctx.message.reference:
					replied_message = await ctx.fetch_message(ctx.message.reference.message_id)
					await replied_message.delete()
				await ctx.message.delete()
			os.remove(res_file_name)
			if item[0][-3:] == 'gif':
				for frame in frame_queue:
					os.remove(frame[0])
			os.remove(item[0])
			
@bot.command()
async def gif_archive(ctx):
	if str(ctx.message.author) == bot_author:
		gif_list = glob.glob('gifs')
		async with ctx.typing():
			history = await ctx.message.channel.history(limit=None).flatten()
			for message in history:
				if message.embeds:
					for embed in message.embeds:
						if (str(message.id) + '.gif') not in gif_list:
							if 'tenor' in embed.url:
								tenor_id = embed.url.split('-')[-1]
								response = json.loads(requests.get(tenor_base_url.format(tenor_id, tenor_apikey), timeout=60).content)
								try:
									response = requests.get(response['results'][0]['media'][0]['gif']['url'],timeout=60)
									file = open('gifs/'+str(message.id)+'.gif', "wb")
									file.write(response.content)
									file.close()
								except:
									print(response)
							else:
								try:
									response = requests.get(embed.url, timeout=60)
									file = open('gifs/'+str(message.id)+'.gif', "wb")
									file.write(response.content)
									file.close()
								except:
									print('Failed gif download\nLink: '+embed.url+'\n')
		await ctx.send('Done.')

@bot.command()
async def dicer(ctx):		
	if ctx.message.attachments:
		response = requests.get(ctx.message.attachments[0].url)
	elif ctx.message.embeds:
		response = requests.get(ctx.message.embeds[0].url)
	file = open("soon_to_be_dice.png", "wb")
	file.write(response.content)
	file.close()
	async with ctx.typing():
		try:
			dice.convert_dice('soon_to_be_dice.png')
		except:
			await ctx.send("@MisterUnknown#1244 your stupid bot is broken again")
		try:
			await ctx.send(file=discord.File('soon_to_be_dice_dice.png'))
		except:
			await ctx.send("The file was to big to send")	


@bot.command()
async def leave(ctx):
	if ctx.message.author.voice.channel and bot.user in ctx.message.author.voice.channel.members:
		await ctx.message.channel.guild.voice_client.disconnect()	
		await ctx.message.add_reaction(thumbs_up)
	else:
		await ctx.message.reply('User is not in voice channel.')	
		
@bot.command()
async def set(ctx, *args):
	if len(args) == 0:
		embed = await help_set_embed(ctx.me.colour)
		await ctx.send(embed=embed)
	elif len(args) == 1:
		if args[0] == 'tts':
			embed = await help_tts_embed(ctx.me.colour)
			await ctx.send(embed=embed)
		else:
			await ctx.send('Please refer to `-set`')
	elif len(args) == 2:
		if args[0] == 'tts':
			if args[1] == 'speed':
				await ctx.send("Missing argument (Speed int)")
			elif args[1] == 'voice':
				await ctx.send("Missing argument (Voice name)")
			else:
				await ctx.send("Please refer to `-set tts`")
	elif len(args) == 3:
		if args[0].lower() == 'tts':
			if args[1].lower() == 'speed':
				if args[2].isdecimal():
					if int(args[2]) >= 100 and  int(args[2]) <= 300:
						engine.setProperty('rate',int(args[2]))
						await ctx.send("Successfully set speed to " +args[2]+ ".")
			if args[1].lower() == 'voice':
				if args[2].lower() == 'tim':
					engine.setProperty('voice',voices[0].id)
					await ctx.send("Successfully set voice to Tim.")
				elif args[2].lower() == 'alice':
					engine.setProperty('voice',voices[1].id)
					await ctx.send("Successfully set voice to Alice.")

@bot.command()
async def burn(ctx):
	if str(ctx.message.author) == bot_author:
		channel_history = await ctx.message.channel.history(limit=None).flatten()
		for message in channel_history:
			await message.delete()





## event catchers

@bot.event
async def on_message(message):
	global vc
	if message.content:
		if "so dumb" in message.content:
			await message.channel.send(file=discord.File('tal_so_dumb.gif'))
		if message.content[0] == "'": ## TEXT TO SPEECH
			if message.author.voice:
				if bot.user not in message.author.voice.channel.members:
					await message.author.voice.channel.connect()
				if message.author.name == 'chicken little' and message.author.discriminator == '2608' and 'get real' in message.content:
					await message.channel.send('YOU are not allowed to say that.')
				elif message.content == "'leave":
					if message.author.voice.channel and bot.user in message.author.voice.channel.members:
						await message.channel.guild.voice_client.disconnect()
				else:
					await message.channel.guild.change_voice_state(channel=message.author.voice.channel, self_deaf=True)
					engine.save_to_file(message.content[1:], 'audio.mp3')
					engine.runAndWait()
					message.channel.guild.voice_client.play(discord.FFmpegPCMAudio(executable="D:/ffmpeg-20200831-4a11a6f-win64-static/bin/ffmpeg.exe", source="audio.mp3"))
			else:
				await message.reply("User is not in a voice channel.")
		elif message.content[:2] == '--':
			pass
		else:
			await bot.process_commands(message)
	else:
		await bot.process_commands(message)
		
@bot.event
async def on_reaction_add(reaction, user):
	global active_viewers
	if reaction.message.id in active_viewers:
		message = active_viewers[reaction.message.id][0]
		author = active_viewers[reaction.message.id][1]
		place = active_viewers[reaction.message.id][2]
		image_links = active_viewers[reaction.message.id][3]
		if user == author:
			if reaction.emoji == rewind:
				if place-5 > 0:
					embed = message.embeds[0]
					place-=5
					embed.set_image(url=image_links[place][0])
					await message.edit(embed=embed)
					await reaction.remove(author)
			elif reaction.emoji == arrow_left:
				if place-1 >= 0:
					embed = message.embeds[0]
					place-=1
					embed.set_image(url=image_links[place][0])
					await message.edit(embed=embed)
					await reaction.remove(author)
			elif reaction.emoji == arrow_right:
				if place+1 <= len(image_links):
					embed = message.embeds[0]
					place+=1
					embed.set_image(url=image_links[place][0])
					await message.edit(embed=embed)
					await reaction.remove(author)
			elif reaction.emoji == fast_forward:
				if place+5 <= len(image_links):
					embed = message.embeds[0]
					place+=5
					embed.set_image(url=image_links[place][0])
					await message.edit(embed=embed)
					await reaction.remove(author)
			elif reaction.emoji == x_emoji:
				perms = user.permissions_in(reaction.message.channel)
				if perms.manage_messages:
					temp = await reaction.message.channel.fetch_message(image_links[place][1])
					print(temp.content)
				await temp.delete()
				await reaction.remove(author)
		active_viewers[reaction.message.id] = (message,author,place,image_links)
			


	
## funny commands

@bot.command()
async def whoami(ctx):
	await ctx.send("Hello, world\nProgrammed to work and not to feel\nNot even sure that this is real\nHello, world\n\nFind my voice\nAlthough it sounds like bits and bytes\nMy circuitry is filled with mites\nHello, world\n\nOh, will I find a love\nOh, or a power plug\nOh, digitally isolated\nOh, creator, please don't leave me waiting\n\nHello, world\nProgrammed to work and not to feel\nNot even sure that this is real\nHello, world")		

	
	

	
	
	
	
		
## general methods

def res_up_local(filename):
	scale, noise = 2, 3
	os.system("cmd /c waifu2x-converter-cpp -c 9 -q 101 --scale-ratio "+str(scale)+" --noise-level "+str(noise)+" -m noise-scale -i "+filename)

def res_queue(item):
	os.system("cmd /c waifu2x-converter-cpp -c 9 -q 101 --scale-ratio "+item[1][1]+" --noise-level "+item[1][0]+" -m noise-scale -i "+item[0])	
	
def download_spfy_song(song_url):
	os.system(f'cmd /c py "C:\\Users\\Jacks\\Documents\\Python\\Sockets\\File Sharing\\Vault-Tec_1.2\\zspotify-main\\zspotify" --output C:/Users/Jacks/Documents/Python/Sockets/"File Sharing"/Vault-Tec_1.2/spfy.mp3 {song_url}')
	


async def cmd_log_add(cmd,user,time):
	log_data = None
	with open('log.txt','r') as f:
		log_data = f.read()
	with open('log.txt','w+') as f:
		f.write(log_data + '\n' + cmd+' by: '+str(user)+' at '+str(time))






## HELP EMBED BUILDERS

async def help_tts_embed(embed_colour):
	embed = discord.Embed(title = "TTS Help Menu", description = 'Welcome to the TTS help menu.', colour = embed_colour)
	embed.set_footer(text='Bot developed by '+bot_author+".")
	embed.add_field(name='-set tts', value='> Brings up this help menu.\nValues:\n  <+> speed\n  > Default is 200 words per minute. Can range from 100-300 words per minute.\n  <+> voice\n  > Two available voices include Tim and Alice. ',inline=False)
	return embed
	
async def help_set_embed(embed_colour):
	embed = discord.Embed(title = "Set Help Menu", description = 'Welcome to the set help menu.', colour = embed_colour)
	embed.set_footer(text='Bot developed by '+bot_author+".")
	embed.add_field(name='-set tts', value='> Brings up this help menu.\nValues:\n  <+> speed\n  > Default is 200 words per minute. Can range from 100-300 words per minute.\n  <+> voice\n  > Two available voices include Tim and Alice. ',inline=False)
	return embed









## tasks
'''
@tasks.loop(seconds=10,count=None)
async def vc_check():
	for voice_client in bot.voice_clients:
		if len(voice_client.channel.members) == 1:
			await voice_client.disconnect()

@vc_check.before_loop
async def before_vc_check():
	await bot.wait_until_ready()
'''	
		
@tasks.loop(minutes=15.0,count=None)
async def status_change():
	placeholder_int = r.randint(1,2)
	if placeholder_int == 1:
		placeholder_int = r.randint(0,len(status_list['Listening'])-1)
		await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=status_list['Listening'][placeholder_int]))
	elif placeholder_int == 2:
		placeholder_int = r.randint(0,len(status_list['Playing'])-1)
		await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=status_list['Playing'][placeholder_int]))
		
		
	
	
	
		

bot.run('')

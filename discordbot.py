import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import discord.ext

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name="ping", description="Pong!", guild = discord.Object(id=835654071351377930))
async def ping(int : discord.Interaction):
    await int.response.send_message('pong')

@client.event
async def member_join(member : discord.Member):
	await member.send(embed=discord.Embed(title='Welcome to the PixelPlace Logs server!', description="This server is for logging the activity of and datamining PixelPlace.io. If you have any questions, please contact a staff member. Thank you for joining!", color=0x00ff00))
	#send a modal
	await member.send(embed=discord.Embed(title='Subscribe to Logs+', description="Want to be notified when a new guild war starts, or when your coin island is captured, or even when your guild is attacked? Get Logs+ today! Logs+ is available (for free) to members of the idehanix discord and for server boosters.", color=0x00ff00), components=[Button(style=ButtonStyle.link, label="Join idehanix today!", url="https://discord.gg/idehanix")])

@tree.command(name="testmodal", description="Test the join modal", guild = discord.Object(id=835654071351377930))
async def test_modal(int : discord.Interaction):
	#await int.response(embed=discord.Embed(title='Welcome to the PixelPlace Logs server!', description="This server is for logging the activity of and datamining PixelPlace.io. If you have any questions, please contact a staff member. Thank you for joining!", color=0x00ff00))
	await int.response.send_message(embed=discord.Embed(title='Subscribe to Logs+', description="Want to be notified when a new guild war starts, or when your coin island is captured, or even when your guild is attacked? Get Logs+ today! Logs+ is available (for free) to members of the idehanix discord and for server boosters.", color=0x00ff00), components=[Button(style=ButtonStyle.link, label="Join idehanix today!", url="https://discord.gg/idehanix")])
#ill run it locally. makes things faster for me
@client.event
async def on_ready():
	await tree.sync(guild=discord.Object(id=835654071351377930))
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="PixelPlace.io"))
	print('Discord bot is ready.')
#fixed also you can like use a diff console for running hawkeye  pls restart bot danke should be good n
client.run('MTA2OTY3NjI3Nzk1MjQzMDE5NQ.G99vYl.T4NvJ6hg_oEFuAXTSm6Ndby4V386iE6ZvDOlmE')

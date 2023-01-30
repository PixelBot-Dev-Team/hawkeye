import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import discord.ext
from discord.ui import View
from discord.ext import tasks

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(name="ping", description="Pong!", guild = discord.Object(id=835654071351377930))
async def ping(int : discord.Interaction):
    await int.response.send_message('pong')

@client.event
async def on_member_join(member : discord.Member):
	if member.guild.id == 835654071351377930: 
		#use purple color
		await member.send(embed=discord.Embed(title='Welcome to the PixelPlace Logs server!', description="This server is for logging the activity of and datamining PixelPlace.io. If you have any questions, please contact a staff member. Thank you for joining!", color=0xFFC965C9))
		#send a modal
		await member.send(embed=discord.Embed(title='Subscribe to Logs+', description="Want to be notified when a new guild war starts, or when your coin island is captured, or even when your guild is attacked? Get Logs+ today! Logs+ is available (for free) to members of the idehanix discord and for server boosters.", color=0x00ff00), view = discord.ui.View().add_item(discord.ui.Button(style=ButtonStyle.link, label="Join idehanix today!", url="https://discord.gg/23vYtDfxzc")))

@tree.command(name="logsplus", description="Find out more about Logs+.", guild = discord.Object(id=835654071351377930))
async def test_modal(int : discord.Interaction):
	#await int.response(embed=discord.Embed(title='Welcome to the PixelPlace Logs server!', description="This server is for logging the activity of and datamining PixelPlace.io. If you have any questions, please contact a staff member. Thank you for joining!", color=0x00ff00))
	await int.response.send_message(embed=discord.Embed(title='Subscribe to Logs+', description="Want to be notified when a new guild war starts, or when your coin island is captured, or even when your guild is attacked? Get Logs+ today! Logs+ is available (for free) to members of the idehanix discord and for server boosters.", color=0x00ff00), view=discord.ui.View().add_item(discord.ui.Button(style=ButtonStyle.link, label="Join idehanix today!", url="https://discord.gg/23vYtDfxzc")))

@client.event
async def on_ready():
	await tree.sync(guild=discord.Object(id=835654071351377930))
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="PixelPlace.io"))
	print('Discord bot is ready.')
	update_users_roles.start()

@tasks.loop(seconds=60)
async def update_users_roles():
	print('Updating users roles...')
	#if the user is in both the idehanix (ID: 1008042737142091887) AND the logs (ID: 835654071351377930) guilds, give them the Logs+ role (ID: 1069689780432015471)
	idehanix = client.get_guild(1008042737142091887)
	logs = client.get_guild(835654071351377930)

	#loop through all members in the logs guild
	for member in logs.members:
		try:
			#check if they are in the idehanix guild
			if idehanix.get_member(member.id):
				#if they dont have the Logs+ role, give it to them
				if not logs.get_role(1069689780432015471) in member.roles:
					#they are in both guilds, give them the Logs+ role in the logs discord
					await member.add_roles(logs.get_role(1069689780432015471))
					#send them a modal thanking them for subscribing to Logs+
					await member.send(embed=discord.Embed(title='Thank you for subscribing to Logs+!', description="You have been automatically subscribed for free thanks to your membership in idehanix. Thank you for subscribing!", color=0x00ff00), view=discord.ui.View().add_item(discord.ui.Button(style=ButtonStyle.link, label="Check out our notification roles", url="https://discordapp.com/channels/835654071351377930/1069692057419010169/1069692212897665034")))
					print(f'Added Logs+ role to {member} ({member.id})')

			else:
				#they are not in both guilds, remove the Logs+ role
				#check if they have the Logs+ role
				if logs.get_role(1069689780432015471) in member.roles:
					await member.remove_roles(logs.get_role(1069689780432015471))
					await member.send(embed=discord.Embed(title='You have been unsubscribed from Logs+', description="You have been unsubscribed from Logs+ because you are no longer a member of idehanix. You can re-subscribe by joining idehanix today!", color=0xff0000), view=discord.ui.View().add_item(discord.ui.Button(style=ButtonStyle.link, label="Join idehanix today!", url="https://discord.gg/23vYtDfxzc")))
					print(f'Removed Logs+ role from {member} ({member.id})')
				#else:
					#send a one time ad to join idehanix
					#await member.send(embed=discord.Embed(title='Subscribe to Logs+', description="Want to be notified when a new guild war starts, or when your coin island is captured, or even when your guild is attacked? Get Logs+ today! Logs+ is available (for free) to members of the idehanix discord and for server boosters.", color=0x00ff00).set_footer("This is a one time message sent because you are a member of the PixelPlace Logs discord, but don't have Logs+. You will not recieve any more messages unless you subcribe."), view=discord.ui.View().add_item(discord.ui.Button(style=ButtonStyle.link, label="Join idehanix today!", url="https://discord.gg/23vYtDfxzc")))
		except:
			print(f'Failed to update {member} ({member.id})')


#fixed also you can like use a diff console for running hawkeye  pls restart bot danke should be good n
client.run('MTA2OTY3NjI3Nzk1MjQzMDE5NQ.G99vYl.T4NvJ6hg_oEFuAXTSm6Ndby4V386iE6ZvDOlmE')

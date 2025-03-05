import configs.DefaultConfig as defaultConfig
import utils.DiscordUtil as discordUtil

import discord
from discord.ext import commands
from cogs.GeminiCog import GeminiAgent
from cogs.MusicCog import MusicCog
from cogs.ReminderCog import ReminderCog
from cogs.PollsCog import PollsCog  # ✅ Import PollsCog

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="pook ", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print("Bot is online..")
    await bot.add_cog(GeminiAgent(bot))
    await bot.add_cog(MusicCog(bot))
    await bot.add_cog(ReminderCog(bot))
    await bot.add_cog(PollsCog(bot))  # ✅ Load PollsCog

@bot.event
async def on_member_join(member):
    print("New member is joining")
    guild = member.guild
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"Welcome to {guildname}! Feel free to ask me questions here. Type pook help to learn my commands in the server!")

@bot.command(aliases=["about"])
async def help(ctx):
    MyEmbed = discord.Embed(
        title="Commands",
        description="These are the Commands you can use.",
        color=discord.Color.dark_purple(),
    )
    MyEmbed.set_thumbnail(url="https://th.bing.com/th/id/OIG.UmTcTiD5tJbm7V26YTp.?w=270&h=270&c=6&r=0&o=5&pid=ImgGn")
    
    MyEmbed.add_field(name="pook q", value="Chat with Gemini AI.", inline=False)
    MyEmbed.add_field(name="pook dm", value="Private message the Gemini AI Bot.", inline=False)
    MyEmbed.add_field(name="pook play", value="Play a song.", inline=False)
    MyEmbed.add_field(name="pook queue", value="Lists upcoming songs.", inline=False)
    MyEmbed.add_field(name="pook skip", value="Skips the current song.", inline=False)
    MyEmbed.add_field(name="pook pause", value="Pauses the song.", inline=False)
    MyEmbed.add_field(name="pook resume", value="Resumes the song.", inline=False)
    MyEmbed.add_field(name="pook remind <date> <time> <message>", value="Set a reminder.", inline=False)
    MyEmbed.add_field(name="pook list_reminders", value="List all reminders.", inline=False)
    MyEmbed.add_field(name="pook delete_reminder <id>", value="Delete a reminder.", inline=False)
    MyEmbed.add_field(name="pook modify_reminder <id> <new_date> <new_time>", value="Modify a reminder.", inline=False)
    MyEmbed.add_field(name="pook poll \"Question\" \"Option1\" \"Option2\" ...", value="Create a poll.", inline=False)
    MyEmbed.add_field(name="pook poll_results <message_id>", value="Show poll results.", inline=False)

    await ctx.send(embed=MyEmbed)

@bot.command()
@commands.check(discordUtil.is_me)
async def unloadGemini(ctx):
    bot.remove_cog("GeminiAgent")
    await ctx.send("GeminiAgent unloaded!")

@bot.command()
@commands.check(discordUtil.is_me)
async def reloadGemini(ctx):
    await bot.add_cog(GeminiAgent(bot))
    await ctx.send("GeminiAgent reloaded!")

bot.run(defaultConfig.DISCORD_SDK)

import discord
from discord.ext import commands
import asyncio

class PollsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = {}  # Dictionary to store active polls

    @commands.command()
    async def poll(self, ctx, question: str, *options):
        """Starts a poll with up to 10 options. Usage: pook poll "Question" "Option1" "Option2" ..."""
        if len(options) < 2:
            await ctx.send("You need at least two options to create a poll!")
            return
        if len(options) > 10:
            await ctx.send("You can have a maximum of 10 options.")
            return

        embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.blue())
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        poll_message = ""
        for i, option in enumerate(options):
            poll_message += f"{reactions[i]} {option}\n"

        embed.add_field(name="Options", value=poll_message, inline=False)
        embed.set_footer(text="React to vote!")

        message = await ctx.send(embed=embed)
        self.polls[message.id] = {"question": question, "options": options, "votes": {}, "message": message}

        for i in range(len(options)):
            await message.add_reaction(reactions[i])

    @commands.command()
    async def poll_results(self, ctx, message_id: int):
        """Displays the results of a poll given its message ID. Usage: pook poll_results <message_id>"""
        try:
            poll = self.polls.get(message_id)
            if not poll:
                await ctx.send("Poll not found!")
                return
            
            message = poll["message"]
            message = await ctx.channel.fetch_message(message_id)

            reactions = message.reactions
            results = {}

            for reaction in reactions:
                results[reaction.emoji] = reaction.count - 1  # Subtract bot's reaction

            embed = discord.Embed(title="📊 Poll Results", description=poll["question"], color=discord.Color.green())

            reactions_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            result_message = ""

            for i, option in enumerate(poll["options"]):
                emoji = reactions_list[i]
                votes = results.get(emoji, 0)
                result_message += f"{emoji} {option}: **{votes} votes**\n"

            embed.add_field(name="Results", value=result_message, inline=False)
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Error retrieving poll results: {str(e)}")

async def setup(bot):
    await bot.add_cog(PollsCog(bot))

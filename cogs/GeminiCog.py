import configs.DefaultConfig as defaultConfig
from discord.ext import commands
import google.generativeai as genai

genai.configure(api_key=defaultConfig.GEMINI_SDK)
DISCORD_MAX_MESSAGE_LENGTH = 2000
PLEASE_TRY_AGAIN_ERROR_MESSAGE = 'There was an issue with your question, please try again.'

class GeminiAgent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    @commands.Cog.listener()
    async def on_message(self, msg):
        try:
            if msg.content == "ping gemini-agent":
                await msg.channel.send("Agent is connected..")
            elif 'Direct Message' in str(msg.channel) and not msg.author.bot:
                response = self.gemini_generate_content(msg.content)
                dmchannel = await msg.author.create_dm()
                await self.send_message_in_chunks(dmchannel, response)
        except Exception as e:
            await msg.channel.send(PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e))

    @commands.command()
    async def q(self, ctx, *, question):
        """Handles general queries using Gemini AI."""
        try:
            response = self.gemini_generate_content(question)
            await self.send_message_in_chunks(ctx, response)
        except Exception as e:
            await ctx.send(PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e))

    @commands.command()
    async def dm(self, ctx):
        """Allows users to start a direct conversation with the bot."""
        try:
            dmchannel = await ctx.author.create_dm()
            await dmchannel.send('Hi, how can I help you today?')
            await ctx.send(f"Yup! Check your DMs, {ctx.author.name}!")
        except Exception as e:
            await ctx.send(PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e))


    @commands.command()
    async def summary(self, ctx):
        """Summarizes the message that the user replied to."""
        if ctx.message.reference:
            try:
                original_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                summary_prompt = f"Summarize this in a few sentences:\n\n{original_message.content}"
                response = self.gemini_generate_content(summary_prompt)
                await self.send_message_in_chunks(ctx, response)
            except Exception as e:
                await ctx.send(f"Failed to summarize: {str(e)}")
        else:
            await ctx.send("Please reply to a message with `pook summary` to summarize it.")

    def gemini_generate_content(self, content):
        """Generates content using Gemini AI."""
        try:
            response = self.model.generate_content(content)
            return response.text
        except Exception as e:
            return PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e)

    async def send_message_in_chunks(self, ctx, response):
        """Sends long messages in chunks to avoid Discord's message limit."""
        message = response

        while len(message) > DISCORD_MAX_MESSAGE_LENGTH:
            await ctx.send(message[:DISCORD_MAX_MESSAGE_LENGTH])
            message = message[DISCORD_MAX_MESSAGE_LENGTH:]

        if message:
            await ctx.send(message)

async def setup(bot):
    await bot.add_cog(GeminiAgent(bot))

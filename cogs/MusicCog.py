import discord
from discord.ext import commands
import asyncio
import yt_dlp

FFMPEG_PATH = "C:/ffmpeg/ffmpeg.exe"

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}

    async def ensure_voice(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You must be in a voice channel to use this command.")
            return None
        voice_channel = ctx.author.voice.channel
        vc = ctx.voice_client
        if vc is None:
            return await voice_channel.connect()
        elif vc.channel != voice_channel:
            await vc.move_to(voice_channel)
        return vc

    def search_youtube(self, query):
        """Searches YouTube for the first video matching the query and returns the URL and title."""
        ydl_opts = {"quiet": True, "format": "bestaudio/best"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                if info["entries"]:
                    entry = info["entries"][0]
                    return entry["url"], entry["title"]
            except Exception as e:
                print(f"Error fetching YouTube URL: {e}")
        return None, None

    @commands.command(name="play")
    async def play(self, ctx, *search):
        """Plays a song from YouTube by searching its name."""
        query = " ".join(search)  # Joins the words into a single string
        if not query:
            await ctx.send("Please provide a song name.")
            return
        
        vc = await self.ensure_voice(ctx)
        if vc is None:
            return

        url, title = self.search_youtube(query)
        if not url:
            await ctx.send("Couldn't find the song on YouTube.")
            return

        guild_id = ctx.guild.id
        if guild_id not in self.queue:
            self.queue[guild_id] = []

        self.queue[guild_id].append((url, title))

        if not vc.is_playing():
            await self.play_next(ctx)
        else:
            await ctx.send(f"🎶 Added to queue: {title}")

    async def play_next(self, ctx):
        vc = ctx.voice_client
        guild_id = ctx.guild.id

        if guild_id not in self.queue or len(self.queue[guild_id]) == 0:
            await ctx.send("Queue is empty, disconnecting.")
            await vc.disconnect()
            return

        url, title = self.queue[guild_id].pop(0)

        try:
            source = discord.FFmpegOpusAudio(url, executable=FFMPEG_PATH, options="-vn")
            vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
            await ctx.send(f"🎶 Now playing: {title}")
        except discord.errors.ClientException as e:
            await ctx.send(f"Error: {str(e)} - Check if ffmpeg is installed correctly.")
        except Exception as e:
            await ctx.send(f"Unexpected error: {str(e)}")

    @commands.command(name="skip")
    async def skip(self, ctx):
        """Skips the currently playing song."""
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await ctx.send("⏩ Skipped the current song.")
        else:
            await ctx.send("There's no song playing right now.")

    @commands.command(name="pause")
    async def pause(self, ctx):
        """Pauses the current song."""
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("⏸️ Paused the song.")
        else:
            await ctx.send("There's no song playing to pause.")

    @commands.command(name="resume")
    async def resume(self, ctx):
        """Resumes a paused song."""
        vc = ctx.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("▶️ Resumed the song.")
        else:
            await ctx.send("There's no paused song to resume.")

    @commands.command(name="queue")
    async def show_queue(self, ctx):
        """Displays the current song queue."""
        guild_id = ctx.guild.id
        if guild_id not in self.queue or len(self.queue[guild_id]) == 0:
            await ctx.send("The queue is empty.")
            return
        queue_list = "\n".join([f"{i+1}. {title}" for i, (url, title) in enumerate(self.queue[guild_id])])
        await ctx.send(f"🎵 Current queue:\n{queue_list}")

    @commands.command(name="stop")
    async def stop(self, ctx):
        """Stops playing and clears the queue."""
        vc = ctx.voice_client
        if vc:
            vc.stop()
            self.queue[ctx.guild.id] = []
            await vc.disconnect()
            await ctx.send("⏹️ Stopped playing and cleared the queue.")
        else:
            await ctx.send("The bot is not connected to a voice channel.")

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
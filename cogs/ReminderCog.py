import discord
from discord.ext import commands, tasks
import asyncio
import datetime

class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []  # Stores reminders as (user, datetime, message)
        self.check_reminders.start()

    def cog_unload(self):
        self.check_reminders.cancel()

    @commands.command(name="remind")
    async def set_reminder(self, ctx, date: str, time: str, *, message: str):
        """Set a reminder with format: pook remind DD-MM-YYYY HH:MM Your message"""
        try:
            reminder_time = datetime.datetime.strptime(f"{date} {time}", "%d-%m-%Y %H:%M")
            self.reminders.append((ctx.author, reminder_time, message))
            await ctx.send(f"✅ Reminder set for {date} at {time}.")
        except ValueError:
            await ctx.send("❌ Invalid format! Use: pook remind DD-MM-YYYY HH:MM Your message")

    @commands.command(name="list_reminders")
    async def list_reminders(self, ctx):
        """Lists all active reminders."""
        if not self.reminders:
            await ctx.send("📌 No reminders set.")
            return
        
        response = "**Your Reminders:**\n"
        for idx, (user, time, msg) in enumerate(self.reminders):
            if user == ctx.author:
                response += f"`{idx}` ➝ {time.strftime('%d-%m-%Y %H:%M')} → {msg}\n"
        
        await ctx.send(response if response != "**Your Reminders:**\n" else "📌 No reminders found.")

    @commands.command(name="delete_reminder")
    async def delete_reminder(self, ctx, reminder_index: int):
        """Deletes a reminder by index."""
        if 0 <= reminder_index < len(self.reminders):
            user, _, _ = self.reminders[reminder_index]
            if user == ctx.author:
                self.reminders.pop(reminder_index)
                await ctx.send("🗑 Reminder deleted.")
            else:
                await ctx.send("❌ You can only delete your own reminders.")
        else:
            await ctx.send("❌ Invalid index.")

    @commands.command(name="modify_reminder")
    async def modify_reminder(self, ctx, reminder_index: int, new_date: str, new_time: str, *, new_message: str):
        """Modifies an existing reminder."""
        if 0 <= reminder_index < len(self.reminders):
            user, _, _ = self.reminders[reminder_index]
            if user == ctx.author:
                try:
                    new_time_obj = datetime.datetime.strptime(f"{new_date} {new_time}", "%d-%m-%Y %H:%M")
                    self.reminders[reminder_index] = (ctx.author, new_time_obj, new_message)
                    await ctx.send("✅ Reminder updated.")
                except ValueError:
                    await ctx.send("❌ Invalid format! Use: pook modify_reminder <index> DD-MM-YYYY HH:MM New message")
            else:
                await ctx.send("❌ You can only modify your own reminders.")
        else:
            await ctx.send("❌ Invalid index.")

    @tasks.loop(seconds=60)
    async def check_reminders(self):
        """Checks if any reminder is due and sends a DM."""
        now = datetime.datetime.now()
        to_remove = []
        for i, (user, time, message) in enumerate(self.reminders):
            if now >= time:
                try:
                    dm_channel = await user.create_dm()
                    await dm_channel.send(f"🔔 Reminder: {message}")
                    to_remove.append(i)
                except:
                    pass
        for index in sorted(to_remove, reverse=True):
            del self.reminders[index]

async def setup(bot):
    await bot.add_cog(ReminderCog(bot))

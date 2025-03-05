# Pookie - A Discord Bot

Pookie is a Discord bot that provides multiple functionalities, including AI chat, music playback, reminders, polls, and welcome messages. It is built using Discord.py and follows a modular cog-based structure for maintainability and extensibility.

## Features
- **AI Chat**: Chat with Gemini AI using `pook q`.
- **Music Player**: Play, pause, resume, skip, and queue songs.
- **Reminders**: Set, list, delete, and modify reminders.
- **Polls**: Create polls and view poll results.
- **Welcome Messages**: Sends a DM or channel message to new members.
- **Modular Cogs**: Easy-to-maintain and extend functionality.

## Modules Used

### 1. `GeminiCog.py` (AI Chat)
- Uses Gemini AI to provide intelligent chat responses.
- Handles queries sent via `pook q`.
- Uses APIs to interact with Gemini AI and return responses.

### 2. `MusicCog.py` (Music Player)
- Integrates with FFMPEG for high-performance music playback.
- Commands like `pook play`, `pook pause`, `pook resume`, `pook skip`, and `pook queue`.
- Handles voice channel interactions to stream audio.

### 3. `ReminderCog.py` (Reminders)
- Implements `pook remind` to set reminders.
- Provides commands to list, delete, and modify reminders.

### 4. `PollsCog.py` (Polls)
- Allows users to create and manage polls using `pook poll`.
- Uses message reactions for voting.
- Displays poll results using `pook poll_results`.

### 5. `on_member_join` Event (Welcome Messages)
- Listens for new member joins.
- Sends a DM with an introduction and command help.

### 6. `DiscordUtil.py`
- Utility functions for common Discord interactions.
- Includes permission checks like `discordUtil.is_me`.

### 7. `DefaultConfig.py`
- Stores configuration values like `DISCORD_SDK` token and other settings.

### `NOTE`:
If I had more time to improve Pookie, I would focus on:

  Make Gemini AI remember previous messages in a conversation for better replies.

  Allow server admins to tweak the AI’s personality and response style.

  Allow users to self-assign roles via reactions

  Detect and delete spam or inappropriate messages

  Scale across multiple servers without performance drops

  Translate AI and command responses into different languages.


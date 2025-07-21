# Discord Music Bot

A Discord music bot with modern slash commands, YouTube search, and voice playback.

## Features

- Join and leave voice channels
- Play music from YouTube by title or URL
- Pause, resume, and stop playback
- Easy-to-use slash commands

## Setup

### Prerequisites

- Python 3.8+
- FFmpeg installed and added to your PATH ([Download FFmpeg](https://ffmpeg.org/download.html))
- A Discord bot token ([How to create a bot](https://discord.com/developers/applications))

### Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/mintcodec/music-bot.git
   cd music-bot
   ```

2. **Install dependencies:**
   ```
   pip install discord.py yt-dlp python-dotenv pynacl
   ```

3. **Create a `.env` file in the project folder:**
   ```
   DISCORD_TOKEN=your-bot-token-here
   ```

4. **Run the bot:**
   ```
   python bot.py
   ```

## Usage

Invite your bot to your server with the `applications.commands` and `bot` scopes.

Use these slash commands in Discord:
- `/join` — Bot joins your voice channel
- `/leave` — Bot leaves the voice channel
- `/play <title or URL>` — Play a song by title or YouTube URL
- `/pause` — Pause playback
- `/resume` — Resume playback
- `/stop` — Stop playback

## Notes

- Make sure FFmpeg is installed and accessible from your command line.
- Never share your bot token publicly.

---

Enjoy your

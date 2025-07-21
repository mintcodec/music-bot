import discord
from discord.ext import commands
import yt_dlp
import os
import re
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  

@bot.event
async def on_ready():
    print(f"🎵 Logged in as {bot.user}")
    print("✨ Music Bot is online and ready to groove!")
    await tree.sync()  

@tree.command(name="join", description="Join your voice channel")
async def join(interaction: discord.Interaction):
    print(f"🔗 {interaction.user} requested to join a voice channel.")
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        await channel.connect()
        print(f"✅ Joined voice channel: {channel}")
        await interaction.response.send_message(f"✅ Joined {channel}")
    else:
        print("❌ Join failed: User not in a voice channel.")
        await interaction.response.send_message("❌ You must be in a voice channel.", ephemeral=True)

@tree.command(name="leave", description="Leave the voice channel")
async def leave(interaction: discord.Interaction):
    print(f"👋 {interaction.user} requested to leave the voice channel.")
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        print("👋 Left the voice channel.")
        await interaction.response.send_message("👋 Left the voice channel.")
    else:
        print("❌ Leave failed: Not connected to any voice channel.")
        await interaction.response.send_message("❌ Not connected to any voice channel.", ephemeral=True)

@tree.command(name="play", description="Play a song by title or URL")
async def play(interaction: discord.Interaction, query: str):
    print(f"🎶 {interaction.user} requested to play: {query}")
    if not interaction.guild.voice_client:
        print("❌ Play failed: Bot not in a voice channel.")
        await interaction.response.send_message("❌ I'm not in a voice channel. Use `/join` first.", ephemeral=True)
        return

    await interaction.response.send_message("🎶 Searching for your song...")

    url_pattern = re.compile(r'^(https?://)')
    if url_pattern.match(query):
        search_term = query
    else:
        search_term = f"ytsearch:{query}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': 'song.%(ext)s',
        'noplaylist': True,
        'default_search': 'ytsearch'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_term, download=False)
            if 'entries' in info:
                if not info['entries']:
                    print("❌ No results found for play command.")
                    await interaction.followup.send("❌ No results found!")
                    return
                info = info['entries'][0]
            stream_url = info['url']
    except Exception:
        print("❌ Not a valid URL or no results found for play command!")
        await interaction.followup.send("❌ Not a valid URL or no results found!")
        return

    interaction.guild.voice_client.stop()
    interaction.guild.voice_client.play(
        discord.FFmpegPCMAudio(stream_url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'),
        after=lambda e: print('Player error: %s' % e) if e else None
    )

    print(f"▶️ Now playing: {info['title']}")
    await interaction.followup.send(f"▶️ Now playing: **{info['title']}**")

@tree.command(name="stop", description="Stop the music")
async def stop(interaction: discord.Interaction):
    print(f"⏹ {interaction.user} requested to stop the music.")
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.stop()
        print("⏹ Music stopped.")
        await interaction.response.send_message("⏹ Music stopped.")
    else:
        print("❌ Stop failed: Nothing is playing.")
        await interaction.response.send_message("❌ Nothing is playing.", ephemeral=True)

@tree.command(name="pause", description="Pause the music")
async def pause(interaction: discord.Interaction):
    print(f"⏸ {interaction.user} requested to pause the music.")
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.pause()
        print("⏸ Music paused.")
        await interaction.response.send_message("⏸ Music paused.")
    else:
        print("❌ Pause failed: Nothing is playing.")
        await interaction.response.send_message("❌ Nothing is playing.", ephemeral=True)

@tree.command(name="resume", description="Resume the music")
async def resume(interaction: discord.Interaction):
    print(f"▶️ {interaction.user} requested to resume the music.")
    vc = interaction.guild.voice_client
    if vc and vc.is_paused():
        vc.resume()
        print("▶️ Resuming music.")
        await interaction.response.send_message("▶️ Resuming music.")
    else:
        print("❌ Resume failed: Nothing is paused.")
        await interaction.response.send_message("❌ Nothing is paused.", ephemeral=True)

bot.run(TOKEN)

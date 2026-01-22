import discord
from discord.ext import commands
import wavelink
from config import *
from controls import MusicControls

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.start_node())

    async def start_node(self):
        await self.bot.wait_until_ready()
        if not wavelink.NodePool.nodes:
            await wavelink.NodePool.create_node(
                bot=self.bot,
                host=LAVALINK_HOST,
                port=LAVALINK_PORT,
                password=LAVALINK_PASSWORD
            )
            print("🎶 Lavalink connected")

    @commands.slash_command()
    async def join(self, ctx):
        if not ctx.author.voice:
            return await ctx.respond("❌ VC তে ঢুক আগে")

        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect(cls=wavelink.Player)

        await ctx.respond(f"🎧 Joined **{channel.name}**")

    @commands.slash_command()
    async def play(self, ctx, *, song: str):
        if not ctx.voice_client:
            await ctx.invoke(self.join)

        player: wavelink.Player = ctx.voice_client
        tracks = await wavelink.YouTubeTrack.search(song)
        if not tracks:
            return await ctx.respond("❌ Kichu pawa jai nai")

        track = tracks[0]

        if not player.is_playing():
            await player.play(track)
            await ctx.respond(
                content=f"🔍 Searching for **{song}**\n🎵 Now Playing: **{track.title}**",
                view=MusicControls(player)
            )
        else:
            await player.queue.put_wait(track)
            await ctx.respond(f"➕ Queue তে add: **{track.title}**")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player, track):
        vc = player.channel
        await vc.edit(status=f"🎵 {track.title}")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player, track, reason):
        if not player.queue.is_empty:
            next_track = await player.queue.get_wait()
            await player.play(next_track)
        # ❌ disconnect নাই

    @commands.slash_command()
    async def skip(self, ctx):
        await ctx.voice_client.stop()
        await ctx.respond("⏭️ Skipped")

    @commands.slash_command()
    async def stop(self, ctx):
        await ctx.voice_client.stop()
        await ctx.respond("⏹️ Playback stopped (bot VC তে থাকবে)")

    @commands.slash_command()
    async def queue(self, ctx):
        player = ctx.voice_client
        if not player or player.queue.is_empty:
            return await ctx.respond("📭 Queue empty")

        desc = "\n".join(
            f"{i+1}. {t.title}" for i, t in enumerate(player.queue)
        )
        embed = discord.Embed(title="🎶 Queue", description=desc)
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def nowplaying(self, ctx):
        player = ctx.voice_client
        if not player or not player.is_playing():
            return await ctx.respond("❌ Kono gaan cholche na")

        await ctx.respond(f"🎵 Now Playing: **{player.current.title}**")

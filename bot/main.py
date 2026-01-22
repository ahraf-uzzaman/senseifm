import discord
from discord.ext import commands
from config import TOKEN
from music import Music
from help import Help

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"🔥 {bot.user} is LIVE for SeNSEi Arena")

bot.add_cog(Music(bot))
bot.add_cog(Help(bot))

bot.run(TOKEN)

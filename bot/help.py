import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="🎧 SeNSEiFM Help",
            description="""
**/join** – Bot কে তোমার VC তে আনে  
**/play song** – গান চালাও  
**/skip** – গান skip  
**/stop** – গান বন্ধ  
**/queue** – Queue দেখো  
**/nowplaying** – বর্তমান গান  

🎵 গান শেষ হলেও bot disconnect হবে না  
🎧 তুমি VC ছাড়লেও bot থাকবে  
🎛️ Buttons দিয়ে control করা যাবে
""",
            color=0x00ffcc
        )
        await ctx.respond(embed=embed)

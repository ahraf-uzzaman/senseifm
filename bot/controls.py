import discord

class MusicControls(discord.ui.View):
    def __init__(self, player):
        super().__init__(timeout=None)
        self.player = player

    @discord.ui.button(label="⏸️ Pause")
    async def pause(self, interaction, button):
        await self.player.pause()
        await interaction.response.send_message("⏸️ Paused", ephemeral=True)

    @discord.ui.button(label="▶️ Resume")
    async def resume(self, interaction, button):
        await self.player.resume()
        await interaction.response.send_message("▶️ Resumed", ephemeral=True)

    @discord.ui.button(label="⏭️ Skip")
    async def skip(self, interaction, button):
        await self.player.stop()
        await interaction.response.send_message("⏭️ Skipped", ephemeral=True)

    @discord.ui.button(label="⏹️ Stop")
    async def stop(self, interaction, button):
        await self.player.stop()
        await interaction.response.send_message("⏹️ Stopped", ephemeral=True)
        
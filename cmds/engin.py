import discord
from discord.ext import commands
from discord import app_commands
from core.classes import Cog_Extension
from botcore import auth_check,descrip

class engin(Cog_Extension):

    @commands.hybrid_command(name = "delmsg", with_app_command = True, description = descrip.delmsg)
    @app_commands.guilds(discord.Object(id = 496446747628011550))
    async def delmsg(self,ctx: commands.Context, channel: str, msg_id: str):
        await ctx.defer(ephemeral = True)
        guild = ctx.guild
        channel=int(channel.strip('<#').strip('>'))
        chat=guild.get_channel(channel)
        if auth_check.check(ctx, auth_check.LOW):
            try:
                msg = await chat.fetch_message(msg_id)
                await msg.delete()
                await ctx.reply('刪除成功')
            except:
                await ctx.reply('查無訊息')

    @commands.hybrid_command(name = "get_vip_permission", with_app_command = True, description = descrip.get_vip_permission)
    @app_commands.guilds(discord.Object(id = 496446747628011550))
    async def get_vip_permission(self,ctx):
        await ctx.defer(ephemeral = True)
        if auth_check.check(ctx, auth_check.ENGIN):
            guild = ctx.guild
            vip_cat = discord.utils.get(guild.categories, id=821040748232179772)
            sunny = guild.get_member(389053471560695808)
            for chat in vip_cat.channels:
                await chat.set_permissions(sunny, manage_permissions=True, manage_channels=True, view_channel=True)
            await ctx.reply('成功新增權限')
        
async def setup(bot):
    await bot.add_cog(engin(bot))
import discord
from discord.ext import commands
from discord import app_commands
from core.classes import Cog_Extension
from botcore import auth_check,descrip
import asyncio
import random

unable_channel={496446747628011552, 500600084644364289, 500600433723572225
                , 577038463115853824, 500598264249188353,  547804836943364112}
        
class 其他(Cog_Extension):

    @commands.hybrid_command(name = "ping", with_app_command = True, description = descrip.ping)
    @app_commands.guilds(discord.Object(id = 496446747628011550))
    async def ping(self, ctx: commands.Context):
        await ctx.defer(ephemeral = True)
        await ctx.reply(f'延遲時間：{round(self.bot.latency*1000)} 毫秒')

    @commands.hybrid_command(name = "gay", with_app_command = True, description = descrip.gay)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @app_commands.guilds(discord.Object(id = 496446747628011550))
    async def gay(self, ctx: commands.Context):
        await ctx.defer()
        if ctx.channel.id not in unable_channel:
            guild = ctx.guild
            chat = guild.get_channel(854891494849380353)
            messages = [message async for message in chat.history(limit=200)]
            msg=random.choice(messages)
            text=msg.embeds[0]
            await ctx.reply(embed=text)
        else:
            delmsg = await ctx.reply("您無法在這個頻道使用此指令！", ephemeral = True)
            await asyncio.sleep(2)
            try:
                await ctx.message.delete()
                await delmsg.delete()
            except:
                pass
        
    @commands.hybrid_command(name = "help", with_app_command = True, description = descrip.help_embed)
    @app_commands.guilds(discord.Object(id = 496446747628011550))
    async def help(self, ctx: commands.Context):
        await ctx.defer(ephemeral = True)
        arrow_emoji='<:arrow:854291847052525568>'
        embed=discord.Embed(title="指令列表", color=0xb300a4)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/853812014765178950/879793352260874300/wynnbot.png")
        embed.add_field(name="⭐新功能⭐", value="現在可以使用 / 指令囉！")        
        embed.add_field(name="\n機器人系統指令", value=
        f"""__工程師指令__
        －w!load [指令集名稱]   {arrow_emoji} 安裝指令集（all為全部指令集）
        －w!unload [指令集名稱] {arrow_emoji} 卸載指令集（all為全部指令集）
        －w!reload [指令集名稱] {arrow_emoji} 重載指令集（all為全部指令集）

        __工作人員指令__
        －w!delmsg [#頻道] [訊息ID]  {arrow_emoji} 刪除指定訊息
        """, inline=False)

        embed.add_field(name="*\n連結防護系統指令", value=
        f"""__工作人員指令__
        －w!add_safe [網址]    {arrow_emoji} 將網址列入白命單
        －w!add_warn [網址]    {arrow_emoji} 將網址列入黑命單
        """, inline=False)
        
        embed.add_field(name="＊\n活躍系統", value=
        f"""__普通指令__ 
        －w!active_rank {arrow_emoji} 顯示活躍排行資訊
        －w!rank_logs [年] [月] {arrow_emoji} 顯示活躍排行資訊""", inline=False)
        

        embed.add_field(name="＊\n其他指令", value=
        f"""__普通指令__ 
        －w!gay {arrow_emoji} 隨機發送經典語錄
        －w!help {arrow_emoji} 顯示指令列表""", inline=False)
        await ctx.reply(embed=embed)
        
async def setup(bot):
    await bot.add_cog(其他(bot))
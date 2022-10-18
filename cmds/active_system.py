import discord
from discord.ext import commands
from discord import app_commands
from core.classes import Cog_Extension
import botcore.mainDB as mdb
from botcore import descrip

class active_system(Cog_Extension):
    
    @commands.hybrid_command(name = "active_rank", with_app_command = True, description = descrip.active_rank)
    @app_commands.guilds(discord.Object(id = 496446747628011550))
    async def active_rank(self, ctx: commands.Context):
        await ctx.defer()        
        userid = str(ctx.author.id)
        adict = mdb.get_active_point()
        if len(adict) == 0:
            await ctx.reply("尚無任何排名")
            return 0
        rankinfo = ""
        guild = ctx.guild
        explorer_role = guild.get_role(760757024324976650)
            
        embed = discord.Embed(title="≺Active Rank≻", color=0x54e6f5)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/853812014765178950/879793352260874300/wynnbot.png")
        t = 1
        for k, v in adict.items():
            member = guild.get_member(int(k))
            rankinfo += f"{str(t)+'.':<2} {str(member)}－{v} ACT Points\n"
            t += 1
            if t > 10:
                break

        embed.add_field(name="Top 10", value=rankinfo, inline=False)

        if str(ctx.author.id) in adict.keys():
            rank = list(adict.keys()).index(userid) + 1
            embed.set_footer(text=f"{ctx.author.name} 的排名 #{rank}－{adict[str(ctx.author.id)]} ACT Points",
                             icon_url=ctx.author.display_avatar)
        elif explorer_role in ctx.author.roles:
            embed.set_footer(text=f"{ctx.author.name} 您現在已經沒有資格獲取 ACT Points 了",
                             icon_url=ctx.author.display_avatar)
        else:
            embed.set_footer(text=f"{ctx.author.name} 您目前沒有任何的 ACT Points",
                             icon_url=ctx.author.display_avatar)
        
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name = "rank_logs", with_app_command = True, description = descrip.rank_logs)
    @app_commands.guilds(discord.Object(id = 496446747628011550))
    async def rank_logs(self, ctx: commands.Context, year: str, month: str):
        await ctx.defer(ephemeral = True)
        month = month.lstrip('0')
        rank_logs = mdb.get_rank_logs()
        if year not in rank_logs.keys():
            await ctx.reply("此年分不在記錄內")
        elif month not in rank_logs[year].keys():
            await ctx.reply("此月分不在記錄內")
        else:
            embed = discord.Embed(title=f"≺{year}/{month.zfill(2)} Logs≻", color=0x54e6f5)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/853812014765178950/879793352260874300/wynnbot.png")
            logs_info = ""

            for k, v in rank_logs[year][month].items():
                logs_info += f"－第{k}周 活躍之星：{v}"
    
            embed.add_field(name=f"Active Star", value=logs_info, inline=False)
            await ctx.reply(embed=embed)
        
async def setup(bot):
    await bot.add_cog(active_system(bot))

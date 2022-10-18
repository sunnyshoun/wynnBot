import keep_alive
import discord
from discord.ext import commands
from discord import app_commands
from urllib.parse import urlparse
from datetime import datetime
import asyncio
import pytz
import os
import sys
import botcore.mainDB as mdb
from botcore import url_check,auth_check,descrip

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix = "w!",
                         intents = intents,
                         help_command=None,
                         activity=discord.Game(name="指令前綴：w!"))
    
    async def setup_hook(self) -> None:
        await start_cog()
        await self.tree.sync(guild = discord.Object(id = 496446747628011550))
        print(f"Now login user: {self.user}.")
        self.bg_task = self.loop.create_task(self.bg_loop())

    async def bg_loop(self):
        await bot.wait_until_ready()
        tw = pytz.timezone('Asia/Taipei')
        guild = bot.get_guild(496446747628011550)
        active_role = guild.get_role(1022137844904513639)
        
        while not self.is_closed():
            now = datetime.now()
            twdt = now.astimezone(tw)
            if twdt.weekday() == 0 and mdb.get_reset_num() == 0:
                user_ids = list(mdb.get_active_point().keys())
                last_id = mdb.get_last_member()
                first_date = datetime(twdt.year,twdt.month,1).astimezone(tw)
                if len(user_ids) != 0:
                    first_id = int(user_ids[0])
                    if first_id != last_id:
                        first_member = guild.get_member(first_id)
                        await first_member.add_roles(active_role)
                        
                        if last_id != "-1":
                            last_member = guild.get_member(last_id)
                            await last_member.remove_roles(active_role)

                        month_week = str(((twdt - first_date).days // 7) + 1)
                        mdb.set_last_member(first_id)
                        mdb.add_rank_logs(str(first_member),str(twdt.year),str(twdt.month),month_week)               
                else:
                    if last_id != "-1":
                        last_member = guild.get_member(last_id)
                        await last_member.remove_roles(active_role)
                        mdb.set_last_member("-1")
                
                mdb.reset_member_active_point()
                mdb.set_reset_num(1)
            if twdt.weekday() != 0 and mdb.get_reset_num() != 0:
                mdb.set_reset_num(0)
            await asyncio.sleep(10)
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            delmsg = await ctx.reply(f"Cooldown（冷卻中）：{round(error.retry_after, 2)}s", ephemeral = True)
        elif isinstance(error, commands.CommandNotFound):
            delmsg = await ctx.reply('Command Not Found（查無此指令）！', ephemeral = True)
        else:
            delmsg = await ctx.reply(error, ephemeral = True)
        await asyncio.sleep(3)
        try:
            await ctx.message.delete()
            await delmsg.delete()
        except:
            pass


async def start_cog():
    for filename in os.listdir('./cmds'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cmds.{filename[:-3]}')

async def add_vip(member):
    guild = member.guild
    chat_dict, boost_member_list, boost_channel_list = mdb.get_vipdatas()
    if member.id not in boost_member_list:
        log_chat = guild.get_channel(853812014765178950)
        mail_chat = guild.get_channel(835378855933771798)
        vip_cat = discord.utils.get(guild.categories, id=821040748232179772)
        chat_name = f"{member.id}-channel"
        chat = await guild.create_text_channel(chat_name, category=vip_cat)
        print(f'Add boost channel {member.name}')
        await chat.set_permissions(guild.default_role, view_channel=False)
        await chat.set_permissions(member,
                                   manage_permissions=True,
                                   manage_channels=True,
                                   view_channel=True,
                                   mention_everyone=False)
        mdb.add_vipdata(member.id, chat.id)
        await chat.send(f"""{member.mention} 您的私人頻道建立好囉！ 首先謝謝您給本伺服器加成！ 
您會有這個頻道的所有權限，包含訊息管理及可以加入的成員等等...
您可以親自設定。有什麼問題再到 {mail_chat.mention} 詢問就好囉！☺️
        
另外私人頻道是您為伺服器加成所獲得的獎勵，所以如果加成停止沒有繼續，頻道也會隨之消失喔! """)

        embed_member = discord.Embed(
            title="⭐您的私人頻道已創建⭐",
            description=f"感謝您的加成，我們為準備了您的專屬頻道，您可以在這個頻道做任何事！",
            color=0xea7aef)
        try:
            await member.send(embed=embed_member)
        except:
            pass

        embed = discord.Embed(
            title="Boost Channel Created",
            description=f"Created {member}'s' boost channel！",
            color=0xfe71fa)
        embed.set_author(name=member)
        await log_chat.send(embed=embed)

async def del_vip(member):
    guild = member.guild
    log_chat = guild.get_channel(853812014765178950)
    vip_cat = discord.utils.get(guild.categories, id=821040748232179772)
    chat_dict, boost_member_list, boost_channel_list = mdb.get_vipdatas()
    if member.id in boost_member_list:
        del_id = chat_dict[member.id]
        print(f'Del boost channel {member}')
        mdb.del_vipdata(member.id)
        try:
            chat = discord.utils.get(vip_cat.channels, id=del_id)
            await chat.delete()
            embed_member = discord.Embed(
                title="⭐您的私人頻道已收回⭐",
                description=f'您的加成時效已過，我們將收回您的私人頻道，感謝您對本伺服器的支持！',
                color=0x00ffbf)
            try:
                await member.send(embed=embed_member)
            except:
                pass

            embed = discord.Embed(
                title="Boost Channel Deleted",
                description=f"Deleted {member}'s' boost channel！",
                color=0xea7aef)
            embed.set_author(name=member)
            await log_chat.send(embed=embed)
        except:
            print(f"{member}'s channel is already delete！")

bot = Bot()
malicious, safe = mdb.refresh_urls()
active_channel = {
    496446747628011552,500600433723572225,532952619422056470,500598264249188353,
    547804836943364112,500598817054523403,832604056803213322,547788416906166272,
    1005008130293379132
}

guild = ""
boost_role = ""
punish = ""
data_chat = ""
senior_role = ""
muted_role = ""
music_role = ""
explorer_role= ""

@bot.event
async def on_ready():
    global guild,boost_role,punish,data_chat,senior_role,muted_role,music_role,explorer_role
    guild = bot.get_guild(496446747628011550)
    boost_role = guild.get_role(652287715538108448)
    punish = guild.get_channel(532322683992670208)
    data_chat = guild.get_channel(853812014765178950)
    senior_role = guild.get_role(761262272186155078)
    muted_role = guild.get_role(621679294069866506)
    music_role = guild.get_role(829217647785672754)
    explorer_role = guild.get_role(760757024324976650)

    restart_context, edit_msg_id = mdb.is_restart()
    if restart_context != False:
        restart_chat = guild.get_channel(restart_context)
        edit_msg = await restart_chat.fetch_message(edit_msg_id)
        await edit_msg.edit(content='bot restarted successfully!')
        mdb.set_restart('NO')

    boost_member_set = set(mdb.get_vipmembers())
    for ids in boost_member_set:
        member = guild.get_member(ids)
        if boost_role not in member.roles and ids != 389053471560695808:
            await del_vip(member)

    for member in guild.members:
        if boost_role in member.roles:
            if member.id not in boost_member_set:
                await add_vip(member)

    print('>>>wynnbot is ready<<<')

@bot.event
async def on_member_update(before, after):
    if boost_role not in before.roles and boost_role in after.roles:
        await add_vip(after)
    elif boost_role in before.roles and boost_role not in after.roles:
        await del_vip(after)
        
@bot.event
async def on_message_delete(msg):
    await bot.wait_until_ready()
    if msg.channel.id in active_channel:
        mdb.remove_active_point(msg.author.id)

@bot.event
async def on_message(msg):
    while guild == "":
        await asyncio.sleep(1)
        
    if msg.author == bot.user or isinstance(msg.channel, discord.channel.DMChannel):
        return 0
    
    member = guild.get_member(msg.author.id)
    text = msg.content
    
    if member != None and msg.author.bot == False:
        if senior_role not in member.roles:
            for role in member.roles:
                if '| 資深成員' in str(role):
                    await member.add_roles(senior_role)
                    break
        if msg.channel.id in active_channel and text.startswith('w!') == False:
            if explorer_role not in msg.author.roles:
                mdb.add_active_point(msg.author.id)
    
    if text.startswith('w!add_safe') or text.startswith('w!add_warn'):
        urls = None
    else:
        urls = url_check.search_url(text)
    if urls != None:
        tt = 0
        for url in urls:
            if 'https://' not in url and 'http://' not in url:
                url = 'https://' + url
            domain = url[0:url.find('/') + 2] + urlparse(url).netloc
            print(domain)
            t = 0
            if url in malicious:
                t = 1
            elif domain in safe:
                t = 0
            elif url_check.check_url_google(url):
                mdb.add_malicious(url)
                malicious.add(url)
                t = 1
            else:
                result = url_check.check_url(url)
                if result == 'warning':
                    mdb.add_malicious(url)
                    malicious.add(url)
                    t = 1
                elif result == 'safe':
                    mdb.add_safe(domain)
                    safe.add(domain)
            if t == 1 and tt == 0:
                tt = 1
                await msg.delete()
                await member.add_roles(muted_role)
                now = datetime.now()
                tw = pytz.timezone('Asia/Taipei')
                twdt = now.astimezone(tw)
                embed = discord.Embed()
                embed = discord.Embed(timestamp=twdt)
                embed.set_author(name="⚠️Malicious Link⚠️",
                                 icon_url=member.avatar_url)
                embed.set_footer(text=f"ID:{member.id}")
                embed.add_field(name="**User**",
                                value=f'{member.mention}\n{str(member)}',
                                inline=True)
                await punish.send(embed=embed)
                embed.add_field(name="**url**", value=url, inline=True)
                embed.add_field(name="**content**",
                                value=msg.content,
                                inline=False)
                await data_chat.send(embed=embed)
    await bot.process_commands(msg)

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel == None and after.channel != None:
        if after.channel.id == 500603591116062720:
            await member.add_roles(music_role)
    elif before.channel != None and after.channel == None:
        if before.channel.id == 500603591116062720:
            await member.remove_roles(music_role)

@bot.hybrid_command(name = "add_safe", with_app_command = True, description = descrip.add_safe)
@app_commands.guilds(discord.Object(id = 496446747628011550))
async def add_safe(ctx: commands.Context, url: str):
    await ctx.defer(ephemeral = True)
    try:
        await ctx.message.delete()
    except:
        pass
    if auth_check.check(ctx, auth_check.TOP):
        global malicious, safe
        domain = url[0:url.find('/') + 2] + urlparse(url).netloc
        mdb.add_safe(domain)
        mdb.del_malicious(url)
        malicious, safe = mdb.refresh_urls()
        await ctx.send(f'{ctx.author.mention} 成功新增連結至白名單')
    else:
        await ctx.send(f'{ctx.author.mention} 您沒有此權限')


@bot.hybrid_command(name = "add_warn", with_app_command = True, description = descrip.add_warn)
@app_commands.guilds(discord.Object(id = 496446747628011550))
async def add_warn(ctx: commands.Context, url: str):
    await ctx.defer(ephemeral = True)
    try:
        await ctx.message.delete()
    except:
        pass
    if auth_check.check(ctx, auth_check.TOP):
        global malicious, safe
        domain = url[0:url.find('/') + 2] + urlparse(url).netloc
        mdb.add_malicious(url)
        mdb.del_safe(domain)
        malicious, safe = mdb.refresh_urls()
        await ctx.send(f'{ctx.author.mention} 成功新增連結至黑名單')
    else:
        await ctx.send(f'{ctx.author.mention} 您沒有此權限')


@bot.hybrid_command(name = "load", with_app_command = True, description = descrip.load)
@app_commands.guilds(discord.Object(id = 496446747628011550))
async def load(ctx: commands.Context, extention: str):
    await ctx.defer(ephemeral = True)
    if auth_check.check(ctx, auth_check.ENGIN):
        if extention.lower() == 'all':
            for filename in os.listdir('./cmds'):
                if filename.endswith('.py'):
                    extention = filename[:-3]
                    await bot.load_extension(f'cmds.{extention}')
            await ctx.reply('所有檔案讀取完成')
        else:
            await bot.load_extension(f'cmds.{extention}')
            await ctx.reply(f'[{extention}] 讀取完成')
    else:
        await ctx.reply(f'{ctx.author.mention} 您沒有此權限')


@bot.hybrid_command(name = "unload", with_app_command = True, description = descrip.unload)
@app_commands.guilds(discord.Object(id = 496446747628011550))
async def unload(ctx: commands.Context, extention: str):
    await ctx.defer(ephemeral = True)
    if auth_check.check(ctx, auth_check.ENGIN):
        if extention.lower() == 'all':
            for filename in os.listdir('./cmds'):
                if filename.endswith('.py'):
                    extention = filename[:-3]
                    await bot.unload_extension(f'cmds.{extention}')
            await ctx.reply('所有檔案卸載完成')
        else:
            await bot.unload_extension(f'cmds.{extention}')
            await ctx.reply(f'[{extention}] 卸載完成')
    else:
        await ctx.reply(f'{ctx.author.mention} 您沒有此權限')


@bot.hybrid_command(name = "reload", with_app_command = True, description = descrip.reload)
@app_commands.guilds(discord.Object(id = 496446747628011550))
async def reload(ctx: commands.Context, extention: str):
    await ctx.defer(ephemeral = True)
    if auth_check.check(ctx, auth_check.ENGIN):
        if extention.lower() == 'all':
            for filename in os.listdir('./cmds'):
                if filename.endswith('.py'):
                    extention = filename[:-3]
                    await bot.reload_extension(f'cmds.{extention}')
            await ctx.reply('所有檔案重載完成')
        else:
            await bot.reload_extension(f'cmds.{extention}')
            await ctx.reply(f'[{extention}] 重載完成')
    else:
        await ctx.reply(f'{ctx.author.mention} 您沒有此權限', ephemeral = True)
    
@bot.hybrid_command(name = "restart", with_app_command = True, description = descrip.restart)
@app_commands.guilds(discord.Object(id = 496446747628011550))
async def restart(ctx: commands.Context):
    await ctx.defer()
    if auth_check.check(ctx, auth_check.ENGIN):
        restart_msg = await ctx.reply("Restarting bot...")
        mdb.set_restart(restart_msg.channel.id, restart_msg.id)
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        await ctx.reply(f'{ctx.author.mention} 您沒有此權限', ephemeral = True)
        

token = os.environ.get('bot_token')
keep_alive.keep_alive()
if __name__ == '__main__':
    try:
        bot.run(token)
    except discord.errors.HTTPException:
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        os.system("python3 restart.py")
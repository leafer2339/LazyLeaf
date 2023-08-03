import discord
from discord.ext import commands
import re
import random
import json
import requests
import time

async def setup(bot):
    await bot.add_cog(TextCommand(bot))

class TextCommand(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.last_api_time = time.time()

    @classmethod
    def getChannelId(cls,s):
        channel = re.compile(r'<#(\d+)>')
        channelMatch = channel.search(s)
        if(channelMatch==None):
            return None
        else:
            return int(channelMatch.groups()[0])

    @commands.command()
    async def send(self,context:commands.Context,channel:discord.TextChannel, *args):
        #if len(arg) < 1:
        #    await context.send('Lệnh trống')
        #    return
        #cId = TextCommand.getChannelId(arg[0])
        #if (cId == None):
        #    await context.send('Không thấy tên kênh')
        #    return
        #else:
        #    if len(arg) >= 2:
        #        targetChannel = self.bot.get_channel(cId)
        #        if(targetChannel != None):
        #            await targetChannel.send(' '.join(arg[1:]))
        #        else:
        #            await context.send('Tin nhắn trống')
        if(len(args) < 1):
            await context.send('Không có tin nhắn')
        else:
            await channel.send(' '.join(args))


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delete(self,context,*arg):
        amount = 2
        try:
            amount = int(arg[0]) + 1
        except ValueError as ve:
            await context.send('Lỗi: {}'.format( ve));
        else:
            await context.channel.purge(limit=amount)
            await context.send("Xóa {} tin nhắn theo lệnh của {}".format(amount-1,context.author.mention))

    @commands.command()
    async def selfdelete(self,context,*arg):
        await context.channel.purge(limit=2,check=lambda msg: msg.author == context.author)
        await context.send("{} đã thu hồi một tin nhắn".format(context.author.nick))

    async def cog_command_error(self, context, error: Exception) -> None:
        #return await super().cog_command_error(ctx, error)
        if(isinstance(error,commands.MissingPermissions)):
            await context.send("Bạn không có quyền làm vậy. Lỗi: {}".format(error))


    @commands.command()
    async def quote(self,context):
        if((time.time() - self.last_api_time) < 6):
            await context.send("Bạn phải chờ {:.2f} giây nữa mới được lấy quote".format(6 - (time.time() - self.last_api_time )))
        else:
            async with context.typing():
                rquote = requests.get("https://zenquotes.io/api/random")
                self.last_api_time = time.time()
                jquote = json.loads(rquote.text)[0]
                quote = jquote['q']
                author = jquote['a']
                await context.send("\"{}\" - {}".format(quote,author))

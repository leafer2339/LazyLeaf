import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import os

load_dotenv()



token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?',intents=intents)
# hmm


@bot.event
async def setup_hook() -> None:
    await bot.load_extension('cogs.text')
    await bot.load_extension('cogs.voice')

@bot.event
async def on_ready():
    if(bot.user != None):
        print(f'Launched as {bot.user.name}')
    #bot.currentVoice = None
    #await bot.load_extension('cogs.text')

@bot.command()
async def hello(context, *arg):
    if(len(arg)>0):
        await context.send(' '.join(arg))

def getCoinflip(times : int) -> list[str]:
    flips = []
    for i in range(0,times):
        num = random.randint(1,100)
        if num % 2 == 0:
            flips.append('N')
        else:
            flips.append('S')
    return flips

@bot.command()
async def coinflip(context,*arg):
    times = 1
    option = ''
    if len(arg) > 2:
        await context.send('Thừa tham số')
        return
    elif len(arg) == 2:
        times = int(arg[0])
        option = arg[1]
        if(times <1): 
            await context.send('Tham số times không hợp lệ, vui lòng nhập một số nguyên dương')
            return
    else:
        await context.send('Thiếu tham số')

    flips = getCoinflip(times)
    if(option == 'show'):
        await context.send('Kết quả tung đồng xu: ' + ' '.join(flips))
    elif(option == 'count'):
        numHead = flips.count('N')
        numTail = flips.count('S')
        await context.send('Kết quả: {} ngửa, {} sấp'.format(numHead,numTail))
    else:
        await context.send('Tham số option không hợp lệ, vui lòng lựa chọn show hoặc count')




@bot.command()
async def newthread(context,*arg):
    threadname = ' '.join(arg)
    nthread = await context.channel.create_thread(name=threadname,type=discord.ChannelType.public_thread)
    await nthread.send("Chào mừng đến thread, {}".format(context.author.mention))

if(token is None):
    print("Error: token is None")
else:
    bot.run(token)


import discord
from discord.ext import commands
from pytube import YouTube

async def setup(bot:commands.Bot):
    await bot.add_cog(VoiceCommand(bot))

class VoiceCommand(commands.Cog):
    def __init__(self,bot:commands.Bot) -> None:
        self.bot = bot
        self.currentVoice = None
        self.volume = 100
        self.currentStream = None

    @commands.command()
    async def join(self,context:commands.Context):
        targetChannel = None
        if(isinstance(context.author,discord.Member) and context.author.voice != None):
            targetChannel = context.author.voice.channel
        if(targetChannel == None):
            await context.send("Bạn không nằm trong kênh thoại nào")
        else:
            if(self.currentVoice == None):
                if(targetChannel != None):
                    self.currentVoice = await targetChannel.connect()
                    await context.send("Đã kết nối đến kênh thoại {}".format(targetChannel.mention))
            else:
                if(self.currentVoice == targetChannel):
                    await context.send("Tôi đã trong kênh thoại này rồi")
                else:
                    await self.currentVoice.disconnect()
                    self.currentVoice = await targetChannel.connect()
                    await context.send("Đã chuyển sang kênh thoại {}".format(targetChannel.mention))

    @commands.command()
    async def leave(self,context):
        if(self.currentVoice == None):
            await context.send("Hiện tôi không nằm trong kênh thoại nào")
        else:
            await self.currentVoice.disconnect()
            self.currentVoice = None
        await context.send("Đã ngắt kết nối")

    @commands.command()
    async def play(self,context,targetURL:str):
        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        async with context.typing():
            if(self.currentVoice == None):
                await self.join(context)
                #await context.send("Gửi lại lệnh nào")
            if(self.currentVoice is not None):
                yt = YouTube(targetURL)
                stream = yt.streams.filter(adaptive=True,file_extension='mp4',type='audio')[0].url
            
                audio = discord.FFmpegPCMAudio(source=stream,executable='ffmpeg',before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',options='-vn')
                audio = discord.PCMVolumeTransformer(audio,volume=self.getVolume())
                self.currentStream = audio
                # audio.volume = self.volume
                self.currentVoice.play(audio,after=self.resetAudio)
                await context.send("Đang phát {} bởi {}, âm lượng hiện tại là {}%".format(yt.title,yt.author,self.volume))
                #await context.send("Done playing")

    
    def resetAudio(self,e):
        self.currentStream = None
        print("LazyLeaf: Đã phát nhạc xong")

    @commands.command()
    async def volumeinc(self,context,amount:int):
        self.volume += amount
        if(self.volume > 100):
            self.volume = 100
        await self.volumeget(context)
        if(self.currentStream is not None):
            self.currentStream.volume = self.getVolume()

    @commands.command()
    async def volumedec(self,context,amount:int):
        self.volume -= amount
        if(self.volume<0):
            self.volume = 0
        await self.volumeget(context)
        if(self.currentStream is not None):
            self.currentStream.volume = self.getVolume()
    
    @commands.command()
    async def volumeget(self,context):
        await context.send("Âm lượng hiện tại là {}%".format(self.volume))
    
    @commands.command()
    async def pause(self,context):
        if(self.currentVoice is not None and self.currentVoice.is_playing()):
            self.currentVoice.pause()
            await context.send("Đã tạm dừng phát nhạc")
        else:
            await context.send("Hiện tôi không phát nhạc")
    
    @commands.command()
    async def resume(self,context):
        if(self.currentVoice is not None and self.currentVoice.is_paused()):
            self.currentVoice.resume()
            await context.send("Quẩy tiếp nào")
        else:
            await context.send("Không thể tiếp tục bản nhạc không tồn tại :v")
    
    @commands.command()
    async def stop(self,context):
        if(self.currentVoice is not None):
            self.currentVoice.stop()
            await context.send("Đã dừng nhạc")
        else:
            await context.send("Tôi hiện không phát bản nhạc nào")

    @commands.command()
    async def comp(self,context):
        audio = discord.FFmpegPCMAudio(source='/home/luong/audio/music/songs/Understand.mp4',options='-vn')
        if(self.currentVoice is not None):
            self.currentVoice.play(audio)

    def getVolume(self):
        return self.volume/100.0
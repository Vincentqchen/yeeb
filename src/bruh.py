import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import random
from dateutil.relativedelta import relativedelta
from apex_legends import ApexLegends

def user_is_me(ctx):
    return ctx.author.id == 228017779511394304

class Bruh(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def apex(self, ctx, player:str):
        if ctx.invoked_subcommand is None:
            apex = ApexLegends("af6873a1-ef18-4ea4-aced-143ba5b6eb5d")
            try:
                player = apex.player(player)
            except:
                await ctx.send('Player not found')
                return
            embed = discord.Embed(
                 colour = discord.Colour.blue()
                 )
            embed.set_footer(text='the stat tracking right now is ass so I can only show damage and kills if you have the banner')
            embed.set_thumbnail(url=player.legends[0].icon)
            embed.set_author(name=player.username + ' | ' + player.legends[0].legend_name, icon_url='https://cdn.gearnuke.com/wp-content/uploads/2019/02/apex-legends-logo-768x432.jpg')
            embed.add_field(name='Level:', value=player.level, inline=False)
            # for legend in player.legends:
            #   embed.add_field(name=legend.legend_name, value='Stats:', inline=False)
            for a in dir(player.legends[0]):
                if a == 'damage' or 'kills' in a:
                    name = a + ':'
                    embed.add_field(name=name.capitalize(), value=player.legends[0].__dict__[a], inline=True)
            await ctx.send(embed=embed)

    @apex.command()
    async def xbox(self, ctx, *args):
        apex = ApexLegends("af6873a1-ef18-4ea4-aced-143ba5b6eb5d")
        try:
            name = ''
            for word in args:
                name += word + ' '
            player = apex.player(name, plat=1)
        except:
            await ctx.send('Player not found')
            return
        embed = discord.Embed(
             colour = discord.Colour.blue()
             )
        embed.set_footer(text='the stat tracking right now is ass so I can only show damage and kills if you have the banner')
        embed.set_thumbnail(url=player.legends[0].icon)
        embed.set_author(name=player.username + ' | ' + player.legends[0].legend_name, icon_url='https://cdn.gearnuke.com/wp-content/uploads/2019/02/apex-legends-logo-768x432.jpg')
        embed.add_field(name='Level:', value=player.level, inline=False)
        # for legend in player.legends:
        #   embed.add_field(name=legend.legend_name, value='Stats:', inline=False)
        for a in dir(player.legends[0]):
            if a == 'damage' or 'kills' in a:
                name = a + ':'
                embed.add_field(name=name.capitalize(), value=player.legends[0].__dict__[a], inline=True)
        await ctx.send(embed=embed)

    @apex.command()
    async def psn(self, ctx, player:str):
        apex = ApexLegends("af6873a1-ef18-4ea4-aced-143ba5b6eb5d")
        try:
            player = apex.player(player, plat=2)
        except:
            await ctx.send('Player not found')
            return
        embed = discord.Embed(
             colour = discord.Colour.blue()
             )
        embed.set_footer(text='the stat tracking right now is ass so I can only show damage and kills if you have the banner')
        embed.set_thumbnail(url=player.legends[0].icon)
        embed.set_author(name=player.username + ' | ' + player.legends[0].legend_name, icon_url='https://cdn.gearnuke.com/wp-content/uploads/2019/02/apex-legends-logo-768x432.jpg')
        embed.add_field(name='Level:', value=player.level, inline=False)
        # for legend in player.legends:
        #   embed.add_field(name=legend.legend_name, value='Stats:', inline=False)
        for a in dir(player.legends[0]):
            if a == 'damage' or 'kills' in a:
                name = a + ':'
                embed.add_field(name=name.capitalize(), value=player.legends[0].__dict__[a], inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        await ctx.author.send('bet')
        await asyncio.sleep(5)
        await ctx.author.send('https://github.com/sirmammingtonham/yeeb')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=100):
        channel = ctx.message.channel
        def is_pinned(m):
            return not m.pinned
        await channel.purge(limit=amount, check=is_pinned)
        await ctx.send('I\'m still logging all your data lol', delete_after=10)

    @clear.error
    async def clear_error(error, ctx):
        if isinstance(error, MissingPermissions):
            await ctx.send('You don\'t have the power, peasant.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def snap(self, ctx):
        channel = ctx.message.channel
        messages = []
        async for message in ctx.channel.history(after=datetime.now() - timedelta(days=14)):
            if not message.pinned:
                messages.append(message)
        random.shuffle(messages)
        await ctx.channel.delete_messages(messages[:len(messages)//2])
        await ctx.send('perfectly balanced\nhttps://media1.tenor.com/images/d89ba4e965cb9144c82348a1c234d425/tenor.gif?itemid=11793362', delete_after=30)

    @snap.error
    async def snap_error(error, ctx):
        if isinstance(error, MissingPermissions):
            await ctx.send('You don\'t have the power, peasant.')

    @commands.command()
    async def spam(self, ctx, *args):
        if user_is_me(ctx):
            for _ in range(int(args[-1])):
                output = ''
                for word in args[:-1]:
                    output += word + ' '
                await ctx.send(output)
        else:
            await ctx.send('You don\'t have the power, peasant.')

    @commands.command(name='thatsprettycringe', aliases=['that\'sprettycringe', 'naenaebaby', 'cringe'])
    async def thatsprettycringe(self, ctx):
        if random.randint(0,1) == 0:
            await ctx.send('https://scontent-dfw5-1.cdninstagram.com/vp/c282a44720c779936cf34c43152ef8ae/5DED2138/t51.2885-15/e35/66229303_174304563604647_4383371938153947034_n.jpg?_nc_ht=scontent-dfw5-1.cdninstagram.com')
        else:
            await ctx.send('https://pbs.twimg.com/media/EBOgkoXXUAEf7hx.jpg')

    @commands.command(name='howlong', aliases=['schmurda'])
    async def howlong(self, ctx):
        td = relativedelta(datetime(2020, 12, 11), datetime.now())
        await ctx.send(f'Bobby Shmurda will be released in {td.years} years, {td.months} months, {td.days} days, {td.hours} hours, {td.minutes} minutes, and {td.seconds} seconds.')

    @commands.command()
    async def code(self, ctx):
        await ctx.send('https://github.com/sirmammingtonham/yeeb')

    @commands.command()
    async def censor(self, ctx, *args, time:int=1):
        channel = ctx.message.channel
        if args is not None:
            user = ''
            for word in args:
                user += word
        elif args.isdigit():
            time = int(args)

        if time > 5:
            await ctx.send('nah')
            return

        end = datetime.now() + timedelta(minutes=time)

        if user in [str(member) for member in ctx.message.guild.members]:
            def check(message):
                return str(message.author) == user and message.channel == channel

            while datetime.now() < end:
                message = await self.bot.wait_for('message', check=check)
                await message.delete()
                await ctx.send(f'||{message.content}||')

        else:
            while datetime.now() < end:
                message = await self.bot.wait_for('message', check=lambda m: m.channel==channel)
                await message.delete()
                await ctx.send(f'||{message.content}||')

    @commands.command()
    async def invite(self, ctx):
        await ctx.send('https://discordapp.com/oauth2/authorize?client_id=547156702626185230&scope=bot&permissions=8')

    @commands.command()
    async def die(self, ctx):
        if user_is_me(ctx):
            await self.bot.logout()
        else:
            await ctx.send('You cannot kill me, peasant.')
            
    @commands.command()
    async def swear(self, ctx):
        words = open("swearwords.txt").readlines()
        word = words[random.randrange(165)][:-2]
        await ctx.send(word)

def setup(bot):
    bot.add_cog(Bruh(bot))
    print('Miscellaneous module loaded.')

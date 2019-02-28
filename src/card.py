import os, sys
sys.path.append(os.path.join(os.getcwd(), "../hearthstone"))
from Game import YEET
import asyncio
import discord
from discord.ext import commands
from fireplace.exceptions import InvalidAction

class Hearthstone:
    ICONS = {'Rexxar': 'https://i.imgur.com/b3MUi1H.png',
             'Malfurion Stormrage': 'https://i.imgur.com/PNWNZG0.png',
             'Jaina Proudmoore': 'https://i.imgur.com/gi4HWzG.png',
             'Uther Lightbringer': 'https://i.imgur.com/tQt6q5y.png',
             'Anduin Wrynn': 'https://i.imgur.com/QA5C4jg.png',
             'Valeera Sanguinar': 'https://i.imgur.com/k5OEewr.png',
             'Thrall': 'https://i.imgur.com/7xiRyiI.png',
             'Gul\'dan': 'https://i.imgur.com/6VFRzA8.png',
             'Garrosh Hellscream': 'https://i.imgur.com/HUltfT7.png',
            }
    def __init__(self, bot):
        self.bot = bot
        self.game_active = False
        self.p1, self.p2 = '', ''
        self.players = {}

    @commands.group(pass_context=True, invoke_without_command=True)
    async def shitty(self, ctx, *args):
        check = ''
        for word in args:
            check += word
        if check == 'hearthstone' and not self.game_active:
            self.g = YEET()
            self.game_active = True
            await self.bot.say('Created a new shitty hearthstone game... Type ```css\nbruh hearthstone join\n``` to join')
        elif not self.game_active:
            await self.bot.say('Game not active... Type ```css\nbruh shitty hearthstone\n``` to start a game')
        else:
            await self.bot.say('the command is ```css\nbruh shitty hearthstone\n``` you nonce')

    @commands.group(pass_context=True, invoke_without_command=True)
    async def hearthstone(self, ctx):
        if ctx.invoked_subcommand is None and self.game_active:
            await self.bot.say('Game active! Type ```css\nbruh hearthstone join\n``` to join')
        elif ctx.invoked_subcommand is None:
            await self.bot.say('Game not yet created. Type ```css\nbruh shitty hearthstone\n``` to start one.')

    @hearthstone.command(pass_context=True, no_pm=False)
    async def join(self, ctx):
        if not self.game_active:
            await self.bot.say('Game not yet created. Type ```css\nbruh shitty hearthstone\n``` to start one.')
            return
        if not self.p1:
            self.p1 = ctx.message.author
            await self.bot.say('anyone else?')
        elif self.p1 and not self.p2:
            self.p2 = ctx.message.author
            await self.bot.say(f'Congrats, you\'ve joined along with {self.p1}')
            await self.bot.say('To get started, one of you need to type ```css\nbruh hearthstone itstimetoduel\n```')
        else:
            await self.bot.say('Too late, two ppl already joined')

    @hearthstone.command(pass_context=True, no_pm=False)
    async def reset(self, ctx):
        self.p1, self.p2 = '', ''
        self.game_active = False

    @hearthstone.command(pass_context=True, no_pm=False)
    async def itstimetoduel(self, ctx):
        if ctx.message.author == self.p1 or ctx.message.author == self.p2:
            await self.bot.say('Game starting... (it might take a while and has a 1/5 chance of breaking)')
            try:
                game_instance = self.g.getInitGame()
            except KeyError:
                await self.bot.say('Goddammit your terrible rng broke it. Run ```bruh hearthstone itstimetoduel``` to try again')
                return
            curPlayer = 0 #useless, just need it because i haven't cleaned up the other functions
            self.players[game_instance.players[0].name] = self.p1
            self.players[game_instance.players[1].name] = self.p2

            def check(message):
                return message.content.isdigit() or message.content == '-1'

            while not game_instance.ended or game_instance.turn > 180:
                embed, embed_hand, embed_field, embed_oppfield, embed_other = self.create_action_embed(game_instance, ctx)
                async with ctx.typing():
                    await self.bot.say(embed=embed)
                    await self.bot.say(embed=embed_hand)
                    await self.bot.say(embed=embed_field)
                    await self.bot.say(embed=embed_oppfield)
                    await self.bot.say(embed=embed_other)

                while True:
                    try:
                        action = await self.bot.wait_for_message(author=self.players[game_instance.current_player.name], channel=ctx.message.channel, check=check)
                        embed_target = self.create_target_embed(int(action.content), game_instance, ctx)

                        if embed_target.fields:
                            await self.bot.say(embed=embed_target)
                            target = await self.bot.wait_for_message(author=self.players[game_instance.current_player.name], channel=ctx.message.channel, check=check)
                            target = int(target.content)
                        else:
                            target = 0

                        if int(action.content) == -1:
                            action.content = 19

                        _, curPlayer = self.g.getNextState(curPlayer, (int(action.content), target), game_instance)

                    except IndexError:
                        await self.bot.say('Invalid action you absolute melon, try again')
                        continue
                    except InvalidAction as e:
                        await self.bot.say(f'Invalid action you absolute melon, try again\n{e}')
                        continue
                    except:
                        await self.bot.say('BRUH, you broke something that i havent checked for... fix it yourself\nhttps://github.com/sirmammingtonham/yeeb')
                        await self.bot.say('If you want to try again type ```css\nbruh hearthstone reset\n```')
                        return
                    break

            if self.g.getGameEnded(curPlayer, game_instance) == 1:
                await self.bot.say(f'gg you\'re both garbage\n@{self.players[game_instance.player_to_start.name]} won')
            if self.g.getGameEnded(curPlayer, game_instance) == -1:
                await self.bot.say(f'gg you\'re both garbage\n@{self.players[game_instance.player_to_start.name]} lost')
            else:
                await self.bot.say('gg you\'re both garbage... how the hell do you even tie??')
        else:
            await bot.say('Who do you think you are?? You\'re not even in the game, peasant')

    def create_action_embed(self, game_instance, ctx):
        you = game_instance.current_player
        if self.players[you.name] == self.p1:
            color = discord.Colour.blue()
        else:
            color = discord.Colour.red()
        embed = discord.Embed(colour = color)
        embed.set_author(name=self.players[game_instance.current_player.name])
        embed.set_footer(text='please type [action index] to input your action (-1 is concede)')
        embed.set_thumbnail(url=Hearthstone.ICONS[str(you.hero)])
        embed.add_field(name=f'{you.hero}', value=f'Health: {you.hero.health}', inline=True)
        embed.add_field(name=f'Opponent', value=f'Health: {you.opponent.hero.health}', inline=True)
        embed.add_field(name='Mana:', value=you.mana, inline=False)

        embed_hand = discord.Embed(colour = color)
        embed_hand.set_author(name='Hand:')
        for idx, card in enumerate(you.hand):
            embed_hand.add_field(name=f'{card}, Index: {idx}', value=f'Cost: {card.cost}, Is Playable? {card.is_playable()}')
            if card.type == 4:
                embed_hand.set_field_at(-1, name=f'{card}', value=f'Index: {idx}, Cost: {card.cost}, Is Playable? {card.is_playable()}, Attack: {card.atk}, Health: {card.health}', inline=False)

        embed_field = discord.Embed(colour = color)
        embed_field.set_author(name='Field:')
        for idx, card in enumerate(you.field):
            embed_field.add_field(name=f'{card}, Index: {idx+10}', value=f'Can Attack? {card.can_attack()}', inline=False)

        embed_oppfield = discord.Embed(colour = color)
        embed_oppfield.set_author(name='Opponent\'s field:')
        for idx, card in enumerate(you.opponent.field):
            embed_oppfield.add_field(name=f'{card}:', value=f'Attack: {card.atk}, Health: {card.health}', inline=False)

        embed_other = discord.Embed(colour = color)
        embed_other.set_author(name='Other options:')
        if you.hero.power.is_usable():
            embed_other.add_field(name='Hero Power Available', value='Index: 17')
        if you.hero.can_attack():
            embed_other.add_field(name='Attack with Weapon', value='Index: 18')
        embed_other.add_field(name='End Turn', value='Index: 19')

        return embed, embed_hand, embed_field, embed_oppfield, embed_other

    def create_target_embed(self, actionid, game_instance, ctx):
        you = game_instance.current_player
        if self.players[you.name] == self.p1:
            color = discord.Colour.blue()
        else:
            color = discord.Colour.red()
        embed = discord.Embed(colour = color)
        embed.set_author(name='Choose a target')
        embed.set_footer(text='please type [target index] to input your target')
        embed.set_thumbnail(url='http://www.usdn.ca/humour/Thumb-Hearthstone.png')
        if 0 <= actionid <= 9:
            if you.hand[actionid].requires_target():
                # embed.add_field(name='Choose a target:', value=' ', inline=False)
                for idx, target in enumerate(you.hand[actionid].targets):
                    embed.add_field(name=f'{target}', value=f'Index: {idx}')
            elif you.hand[actionid].must_choose_one:
                embed.add_field(name='Choose 1:', value='-', inline=False)
                for idx, choose in enumerate(you.hand[actionid].choose_cards):
                    embed.add_field(name=f'{choose}', value=f'Index: {idx}')

        elif 10 <= actionid <= 16:
            for idx, target in enumerate(you.field[actionid - 10].attack_targets):
                embed.add_field(name=f'{target}', value=f'Index: {idx}')

        elif actionid == 17:
            if you.hero.power.requires_target():
                for idx, target in enumerate(you.hero.power.targets):
                    embed.add_field(name=f'{target}', value=f'Index: {idx}')

        elif actionid == 18:
            for idx, target in enumerate(you.hero.attack_targets):
                embed.add_field(name=f'{target}', value=f'Index: {idx}')

        elif actionid == -1:
            you.hero.to_be_destroyed = True

        return embed

def setup(bot):
    bot.add_cog(Hearthstone(bot))
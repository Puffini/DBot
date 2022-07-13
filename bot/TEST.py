import discord
    
from discord import utils
from discord.ext import commands, tasks

import config

bot = commands.Bot(command_prefix='1', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('verification_mod logged on as {0}!'.format(bot.user))
    
@tasks.loop(minutes=2) #ПОДСЧЕТ УЧАСТНИКОВ
async def number_of_users():
    guilds = bot.guild.members
    channelmembers = bot.get_channel(933108290638970981)
    await channelmembers.edit(name = f'Members: {guilds}')
    print('[SUCCESS] Количество пользователей обновилось')

@bot.event #ПРИСВОЕНИЕ РОЛИ
async def on_raw_reaction_add(payload):
    #ВЫБОР ЯЗЫКА
    if payload.message_id == config.POST_ID_LANG:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members,
                           id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES_LANG[emoji])

            if(len([i for i in member.roles if i and i.id not in config.EXCROLES])<= config.MAX_ROLES_PER_USER):
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
            else:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))

    #ВЕРИФИКАЦИЯ
    if payload.message_id == config.POST_ID_VERIF:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members,
                           id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES_VERIF[emoji])

            if(len([i for i in member.roles if i and i.id not in config.EXCROLES])):
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
            else:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))

@bot.event #ОТМЕНА РОЛИ    
async def on_raw_reaction_remove(payload):
    #ОТМЕНА ЯЗЫКА
    if payload.message_id == config.POST_ID_LANG:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members,
                           id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES_LANG[emoji])

            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
    await bot.process_commands(member)

bot.run(config.TOKEN)
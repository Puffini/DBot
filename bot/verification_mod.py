import discord
    
from discord import utils
    
import config
    
intents = discord.Intents.all()
intents.members = True

class MyClient(discord.Client):
    async def on_ready(self):
        print('verification_mod logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID_VERIF: # ID сообщения
            channel = self.get_channel(payload.channel_id)  # получаем объект канала
            message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
            member = utils.get(message.guild.members,
                               id=payload.user_id)  # получаем объект пользователя который поставил реакцию
    
            try:
                emoji = str(payload.emoji)  # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=config.ROLES_VERIF[emoji])  # объект выбранной роли (если есть)
    
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
    
    client = discord.Client(intents=intents)
    
    
    
client = MyClient(intents = discord.Intents.all())
client.run(config.TOKEN)
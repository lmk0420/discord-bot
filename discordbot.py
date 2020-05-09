import sys
import discord
import random


def random_katoru():
    katoru_vocabulary = ['四天より至る雫は激情の涙。',
                         'その様は、終末の予兆！',
                         '調子に乗ってんじゃねえぞ、ゴミ虫が！',
                         'このクソボケが、細切れに切り刻んでやるよ！']
    return ''.join(katoru_vocabulary[random.randint(0, 3)] for i in range(5))


client = discord.Client()

@client.event
async def on_ready():
    print('login successful')


@client.event
async def on_message(message):
    if message.content.startswith('/katoru'):
        await message.channel.send(random_katoru())

    elif message.content.startswith('/help'):
        m = '\t\t・/katoru\n' \
            '\t\t\t 最終カトルの４アビが発動します。\n' \
            '\n・ユーザのボイスチャンネルへの入室・退室・移動を通知します。\n' \
            '\n※ご要望, 追加して欲しい機能などあれば マコト#7215 までお気軽にどうぞ。\n'
        await message.channel.send(m)


@client.event
async def on_voice_state_update(member, before, after):
    # fixme サーバーを動的に変えられるようにしたい
    text_channels = [channel for channel in member.guild.channels if isinstance(channel, discord.TextChannel)]
    channel_to_send_meesage = [text_channel for text_channel in text_channels if text_channel.name == 'bot_notification'][0]
    if before.channel is None and after.channel is not None:
        try:
            await channel_to_send_meesage.send(f'{member.name}さんが{after.channel.name}に入室しました')
        except:
            await channel_to_send_meesage.send('エラーが発生しました')
            with open('error.txt', mode='a', encoding='utf-8') as err:
                err.write(sys.exc_info() + '\n')

    elif before.channel is not None and after.channel is None:
        try:
            await channel_to_send_meesage.send(f'{member.name}さんが退室しました')
        except:
            await channel_to_send_meesage.send('エラーが発生しました')
            with open('error.txt', mode='a', encoding='utf-8') as err:
                err.write(sys.exc_info() + '\n')

    elif before.channel and after.channel and before.channel != after.channel:
        try:
            await channel_to_send_meesage.send(f'{member.name}さんが{before.channel.name}から{after.channel.name}に移動しました')
        except:
            await channel_to_send_meesage.send('エラーが発生しました')
            with open('error.txt', mode='a', encoding='utf-8') as err:
                err.write(sys.exc_info() + '\n')


with open('token.txt', mode='r', encoding='utf-8') as f:
    token = f.readline()

client.run(token)

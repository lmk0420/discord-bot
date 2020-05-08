import sys
import discord
import random


client = discord.Client()


def pick_channel(channel_list, server_name, channel_name):
    for channel_gen in channel_list:
        if (channel_gen.server.name == server_name) and (channel_gen.name == channel_name):
            channel = channel_gen
    return channel


def random_katoru():
    katoru_vocabulary = ['四天より至る雫は激情の涙。',
                         'その様は、終末の予兆！',
                         '調子に乗ってんじゃねえぞ、ゴミ虫が！',
                         'このクソボケが、細切れに切り刻んでやるよ！']
    return ''.join(katoru_vocabulary[random.randint(0, 3)] for i in range(5))


@client.event
async def on_ready():
    print('login successful')


@client.event
async def on_message(message):
    split_message = message.content.split(' ')
    channel_map = {channel.name: channel for channel in client.get_all_channels()}

    if message.content.startswith('/katoru'):
        await client.send_message(message.channel, random_katoru())

    elif message.content.startswith('/help'):
        m = '\t\t・/katoru\n' \
            '\t\t\t 最終カトルの４アビが発動します。\n' \
            '\n・ユーザのボイスチャンネルへの入室・退室・移動を通知します。\n' \
            '\n※ご要望, 追加して欲しい機能などあれば マコト#7215 までお気軽にどうぞ。\n'
        await client.send_message(message.channel, m)


@client.event
async def on_voice_state_update(before, after):
    channel_list = [channel for channel in client.get_all_channels()]
    # fixme サーバーを動的に変えられるようにしたい
    channel = pick_channel(channel_list, 'smart_I/O', 'bot_notification')
    if before.voice_channel is None:
        try:
            await client.send_message(channel, str(before) + 'さんが入室しました')
        except:
            await client.send_message(channel, 'エラーが発生しました')
            with open('error.txt', mode='a', encoding='utf-8') as err:
                err.write(sys.exc_info() + '\n')

    elif after.voice_channel is None:
        try:
            await client.send_message(channel, str(after) + 'さんが退室しました')
        except:
            await client.send_message(channel, 'エラーが発生しました')
            with open('error.txt', mode='a', encoding='utf-8') as err:
                err.write(sys.exc_info() + '\n')

    elif before.voice_channel and after.voice_channel and before.self_mute == after.self_mute and before.self_deaf == after.self_deaf:
        try:
            await client.send_message(channel, '{name}さんが{before}から{after}に移動しました'
                                      .format(name=before, before=before.voice_channel, after=after.voice_channel))
        except:
            await client.send_message(channel, 'エラーが発生しました')
            with open('error.txt', mode='a', encoding='utf-8') as err:
                err.write(sys.exc_info() + '\n')


with open('token.txt', mode='r', encoding='utf-8') as f:
    token = f.readline()

client.run(token)

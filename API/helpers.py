import json
import disnake
import io

from typing import List
from datetime import datetime, timedelta

def get_guild_id():
    with open('./json_files/config.json','r',encoding='utf-8-sig') as f:
        data = json.load(f)

    return data["guild_id"]


def delete_messages_log(messages: List[disnake.Message], reason) -> disnake.File:
    '''Converts the list of deleted messages to a log.txt and returns the File object ready to be sent'''
    _file = io.StringIO()
    _file.write("Reason: " + reason + '\n')

    for i, message in enumerate(messages):
        line = {
            str(i): {
                'author': message.author.name,
                'timestamp': str(message.created_at),
                'content': message.content
            }
        }
        _file.write("="*30 + '\n')
        _file.write(f'{json.dumps(line, indent=2)}\n')

    _file.seek(0)
    return disnake.File(_file, filename=f"Deleted_{datetime.now()}.txt")

def get_restricted_channels():
    channel_ids = []

    with open('./json_files/setup.json','r',encoding='utf-8-sig') as f:
        data = json.load(f)

        for guild in data["guilds"]:
            for channel in data["guilds"][guild]["restricted_channels"]:
                channel_ids.append(data["guilds"][guild]["restricted_channels"][channel])

    return channel_ids
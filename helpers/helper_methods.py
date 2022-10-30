import json

def get_guild_id():
    with open('config.json','r',encoding='utf-8-sig') as f:
        data = json.load(f)

    return data["guild_id"]
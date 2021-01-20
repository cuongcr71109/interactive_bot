from telethon import TelegramClient
from time import sleep
from db import *

insertUsers()
insertGroups()
insertDialog()
users = getUser()
groups = getGroup()
dialogue = getDialogue()



async def interact(client, group_id, content):
    me = await client.get_me()
    await client.send_message(group_id, content)
    sleep(1)
    print(me.phone, 'sent to {}'.format(group_id))


for dial in dialogue:
    group_id = int(dial[3])
    content = dial[2]
    query = 'SELECT api_id, api_hash, phone FROM users WHERE id = {}'.format(dial[1])
    cursor.execute(query)
    user = cursor.fetchall()

    client = TelegramClient(session='{}'.format(user[0][2]), api_id = int(user[0][0]), api_hash = user[0][1])
    with client:
        print('sent')
        # client.loop.run_until_complete(interact(client, group_id, content))
from jinja2.utils import internal_code
from telethon.sync import TelegramClient, events, types
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from time import sleep

from db import *
from app import *

# send message
async def interact(client, group_id, content):
    me = await client.get_me()
    await client.send_message(group_id, content)
    print(me.phone, 'sent to {} -->'.format(group_id), content)
    sleep(1)

# check user in group or not
def checkin_group(client, group_id):
    dialog_id = []
    for dialog in client.iter_dialogs():
        dialog_id.append(dialog.id)
    return group_id in dialog_id

# join group if user is not in group
def join_group(client, group_type, group_link):
    if group_type == 'private':
        join = client(ImportChatInviteRequest(hash=group_link))
        print('Join to private')

    elif group_type == 'public':
        join = client(JoinChannelRequest(channel=group_link))
        print('Join to public')

# function to interact
def main_function(dialogue):
    for dial in dialogue:
        group_id = int(dial['group_id'])
        content = dial['content']

        # get api_id and api_hash to create Client
        query = 'SELECT api_id, api_hash, phone FROM users WHERE id = {}'.format(dial['user_id'])
        cursor.execute(query)
        user = cursor.fetchone()
        # user [{'api_id': 2484767, 'api_hash': 'df8557fedd7d125f1128eec0fb021f27', 'phone': '84856852624'}]

        # get group_type and group_link to join
        query = 'SELECT group_type, group_link FROM groups WHERE group_id = {}'.format(group_id)
        cursor.execute(query)
        gr_typelink = cursor.fetchone()
        # gr_typelink [('private', 'https://t.me/joinchat/HZesgX2L5zcpKvq0')]

        client = TelegramClient(session='{}'.format(user['phone']), api_id = int(user['api_id']), api_hash = user['api_hash'])
        with client:
            if not checkin_group(client, group_id):
                join_group(client, gr_typelink['group_type'], gr_typelink['group_link'])
                client.loop.run_until_complete(interact(client, group_id, content))
            else:
                client.loop.run_until_complete(interact(client, group_id, content))

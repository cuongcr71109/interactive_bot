from telethon.sync import TelegramClient, events, types
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from time import sleep

from telethon.client import updates
from db import *


# users = getUser()
# users [(id, user_id, api_id, api_hash, username, phone)]
# users [(1, 784093829, 2484767, 'df8557fedd7d125f1128eec0fb021f27', 'quannmUET', '84856852624')]

# groups = getGroup()
# groups [(id, group_id, group_title, group_type, group_link)]
# groups [(1, '-1001158850531', 'Test BOT', 'private', 'https://t.me/joinchat/HZesgX2L5zcpKvq0')]

dialogue = getDialogue()
# dialogue [(id, user_id, content, group)]
# dialogue [(1, 1, 'Hello.', '-1001158850531')]



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
def interact_tool(dialogue):
    for dial in dialogue:
        group_id = int(dial[3])
        content = dial[2]


        print('ok1')
        # get api_id and api_hash to create Client
        query = 'SELECT api_id, api_hash, phone FROM users WHERE id = {}'.format(dial[1])
        cursor.execute(query)
        user = cursor.fetchall()
        print(user, 'ok2')
        # user [(2484767, 'df8557fedd7d125f1128eec0fb021f27', '84856852624')]

        # get group_type and group_link to join
        query = 'SELECT group_type, group_link FROM groups WHERE group_id = {}'.format(group_id)
        cursor.execute(query)
        gr_typelink = cursor.fetchall()
        print(gr_typelink, 'ok3')
        # gr_typelink [('private', 'https://t.me/joinchat/HZesgX2L5zcpKvq0')]

        client = TelegramClient(session='{}'.format(user[0][2]), api_id = int(user[0][0]), api_hash = user[0][1])
        print('ok4')
        with client:
            print('ok5')
            if not checkin_group(client, group_id):
                print('ok6')
                join_group(client, gr_typelink[0][0], gr_typelink[0][1])
                client.loop.run_until_complete(interact(client, group_id, content))
            else:
                print('sent')
                client.loop.run_until_complete(interact(client, group_id, content))
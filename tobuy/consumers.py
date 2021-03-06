import json
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user

from .models import Item

# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    print('in ws_add')
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the users group
    Group("users").add(message.reply_channel)

@channel_session_user
def ws_receive(message):
    print('in ws_receive')
    Group('users').add(message.reply_channel)
    msg = message.content.get('text')
    msg_content = json.loads(msg)
    print(msg_content.get('action'))
    mydict = {'item_id': msg_content.get('item_id'),
            'sender_id': message.user.id,}
    if msg_content.get('action') == "additem":
        user_active_list = message.user.profile.active_list
        item_name = msg_content.get('item_name')
        item = Item.objects.create(name=item_name, items_list=user_active_list)
        # create new html li element to be inserted into list
        mydict['new_li'] = item.name
        mydict['new_item_id'] = item.id
        mydict['action'] = 'add_new_item'
    if msg_content.get('action') == "delete":
        item_id = msg_content.get('item_id')
        item = Item.objects.get(pk=item_id)
        item.delete()
        mydict['action'] = 'delete_item'
    if msg_content.get('action') == 'switch':
        item_id = msg_content.get('item_id')
        item = Item.objects.get(pk=item_id)
        item.active = not item.active
        item.save()
        mydict['action'] = 'switch_status'
    Group('users').send({
        'text': json.dumps(mydict)
    })

def ws_disconnect(message):
    print('in ws_disconnect')
    Group("users").discard(message.reply_channel)

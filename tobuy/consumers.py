import json
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user

# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    print('jestem w ws_add')
    print(message.user.id)
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the users group
    Group("users").add(message.reply_channel)

@channel_session_user
def ws_receive(message):
    print('jestem w rec')
    print(message.user.id)
    Group('users').add(message.reply_channel)
    item_id = message.content.get('text')
    print(item_id)    
    Group('users').send({
        'text': json.dumps({
            'item_id': item_id,
            'sender_id': message.user.id,
        })
    })

def ws_disconnect(message):
    Group("users").discard(message.reply_channel)

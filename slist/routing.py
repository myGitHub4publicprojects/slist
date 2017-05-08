from channels.routing import route
from tobuy.consumers import ws_add, ws_receive, ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_receive),
    route("websocket.disconnect", ws_disconnect),
]
import os
import sys
import channels.asgi

print 'jestem w asgi'
sys.stdout.flush()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "slist.settings")
channel_layer = channels.asgi.get_channel_layer()
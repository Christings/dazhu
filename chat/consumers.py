import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
from models import Message

log = logging.getLogger(__name__)
from tools.secu import encodeHtml

@channel_session
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    try:
        prefix, label = message['path'].decode('ascii').strip('/').split('/')
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
    except:
        log.debug('invalid ws path=%s', message['path'])
        return
        
    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('chat', channel_layer=message.channel_layer).add(message.reply_channel)


@channel_session
def ws_receive(message):
   
    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])        
        
        log.debug("receive chat data,",data)
    except ValueError:
        log.debug("ws message isn't json text=%s", message)
        return
    
    if set(data.keys()) != set(('handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        if '##clean' in data['message']:
            Message.objects.all().delete()
        else:            
            data['handle']=encodeHtml(data['handle'])
            data['message']=encodeHtml(data['message'])        
            m = Message.objects.create(**data)        
            # See above for the note about Group
            Group('chat', channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})

@channel_session
def ws_disconnect(message):
    try:
        Group('chat', channel_layer=message.channel_layer).discard(message.reply_channel)
    except :
        pass
    
    
    
    
    
    
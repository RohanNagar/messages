import json
import datetime

# Constants
path = 'raw_messages.json'
first_author_id = 'fbid:609628589'
first_author_name = 'Stephanie Tran'
second_author_id = 'fbid:1399342159'
second_author_name = 'Rohan Nagar'


# Get the appropriate URL of the attachment
def get_url_from_attachment(attachment):
    if attachment['url'] is None:
        return attachment['share']['uri']
    elif '/ajax/' in attachment['url']:
        return attachment['hires_url']
    else:
        return attachment['url']


# Parses any attachments for each message
def get_attachments(message):
    result = []
    if 'attachments' in message and len(message['attachments']) != 0:
        for attachment in message['attachments']:
            atchmnt = {
                'type': attachment['attach_type'],
                'url': get_url_from_attachment(attachment)
            }

            result.append(atchmnt)
    
    return result


# Loads all messages from a JSON file given in filename.
# Default filename is the `path` variable defined above.
def get_all_messages(filename=path):
    with open(filename) as f:
        messages = json.load(f)

        # Sort by date
        messages.sort(key=lambda d: d['timestamp'])

        # Get only the needed information
        result = []
        for message in messages:
            msg = {
                'text': message['body'] if 'body' in message else '',
                'name': first_author_name if message['author'] == first_author_id else second_author_name,
                'timestamp': message['timestamp'],
                'date': datetime.datetime.fromtimestamp(float(message['timestamp'] / 1000)).strftime('%B %d, %Y %-I:%M %p'),
                'attachments': get_attachments(message)
            }

            # Update body text with attachment links
            for attachment in msg['attachments']:
                if attachment['type'] == 'sticker':
                    msg['text'] = '<img src=' + attachment['url'] + ' width="50" height="50">'
                elif attachment['type'] == 'file':
                    msg['text'] = 'Audio Message'
                elif attachment['type'] == 'photo':
                    msg['text'] = msg['text'] + ' <a href=' + attachment['url'] + ' target="_blank">Link to Attached Photo (May be Expired)</a>'
                elif attachment['type'] == 'animated_image':
                    msg['text'] = msg['text'] + ' <a href=' + attachment['url'] + ' target="_blank">Link to Attached GIF (May be Expired)</a>'
                elif attachment['type'] == 'video':
                    msg['text'] = msg['text'] + ' <a href=' + attachment['url'] + ' target="_blank">Link to Attached Video (May be Expired)</a>'
                elif attachment['type'] == 'share':
                    if attachment['url'] is None:
                        msg['text'] = msg['text'] + ' Unavailable Attachment'
                    else:
                        msg['text'] = msg['text'] + ' <a href=' + attachment['url'] + ' target="_blank">Attached Link</a>'

            # If there is still an empty body, then the message was a chat log
            if msg['text'] == '' and 'log_message_body' in message:
                msg['text'] = message['log_message_body']

            result.append(msg)

        return result


# START EXECUTION #
print('Converting messages found in {}'.format(path))
messages = get_all_messages()

print('Writing results to file.')
with open('messages.json', 'w') as f:
    json.dump(messages, f)


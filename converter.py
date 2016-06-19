import json
import datetime

# Constants
path = 'Messages/609628589/complete.json'
first_author_id = 'fbid:609628589'
first_author_name = 'Stephanie Tran'
second_author_id = 'fbid:1399342159'
second_author_name = 'Rohan Nagar'


# Retrieves the link to any attachments for each message
def get_attachments(message):
    if 'attachments' in message and len(message['attachments']) != 0:
        for attachment in message['attachments']:
            if attachment['url'] is None:
                return attachment['share']['uri']
            elif '/ajax/' in attachment['url']:
                return attachment['hires_url']
            else:
                return attachment['url']
    else:
        return None


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
                'link': get_attachments(message)
            }

            if msg['text'] == '' and msg['link'] is not None:
                if msg['link'].endswith('.png'):
                    msg['text'] = '<img src=' + msg['link'] + ' width="50" height="50">'
                else:
                    msg['text'] = '<a href=' + msg['link'] + '>Link to Attachment (May be Expired)</a>'

            result.append(msg)

        return result


# START EXECUTION #
print('Converting messages found in {}'.format(path))
messages = get_all_messages()

print('Writing results to file.')
with open('messages.json', 'w') as f:
    json.dump(messages, f)


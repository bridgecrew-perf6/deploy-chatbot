import os
import urllib.request
import urllib.parse
import json

def hello(event, context):
    # body = {
    #     "message": "Go Serverless v3.0! Your function executed successfully!",
    #     "input": event,
    # }

    slack_event = json.loads(event['body']) # python dict
    # print('Printing slack event:', slack_event)
    
    send_response(slack_event)
    
    return {
        'statusCode': 200,
        'body': 'OK'
    }

def send_response(event): # slack event
    SLACK_URL = 'https://slack.com/api/chat.postMessage'
    
    bot_token = os.environ['BOT_TOKEN']
    channel_id = event['event']['channel']
    slack_message = event['event']['text']
    message_ts = event['event']['ts']
    
    slack_message = "Hi! I'm the MassMutual bot. You're request is: " + '"' + slack_message + '"' + '\n\nHere are some relevant links to help with your request: ' + 'https://api.slack.com/ (just an example)'
    
    try:
        event['event']['thread_ts'] # message is a reply --> exit
        return
    except KeyError: # message is not a reply --> proceed
        pass
    
    data = urllib.parse.urlencode({
        'token': bot_token,
        'channel': channel_id,
        'text': slack_message,
        'thread_ts': message_ts
    })
    
    data = data.encode('ascii')
    request = urllib.request.Request(SLACK_URL, data=data, method='POST')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    res = urllib.request.urlopen(request).read()
    print('res:', res)

    # return {"statusCode": 200, "body": json.dumps(body)}

import re
import xlwt
import json
from datetime import datetime

def format_message(msg):
    msg = msg.replace(u'\u200e', '')
    regex = '(\[\d{2}\/\d{2}\/\d{2}, \d{1,2}:\d{2}:\d{2} [AP][M]\])([^:]*):?((.|\n)*)'
    match = re.search(regex, msg)
    
    try:
        date = match.group(1).strip()
        date = datetime.strptime(date, "[%d/%m/%y, %I:%M:%S %p]")
        sender = match.group(2).strip()
        message = match.group(3).strip()
    except:
        return 'error'

    return refine_message( { 'date': date.isoformat(),
            'sender': sender,
            'message':message})

def match_regex(reg, text):
    if re.match(reg, text):
        match = re.search(reg, text)
        return [match.group(1).strip(), match.group(3).strip(), match.group(2).strip()]

def refine_message(message):
    returnMsg = message
    regex1 = '(' + "|".join(senders_list) + ').*(added|removed|left).*(' + "|".join(senders_list) + ')?'
    regex2 = '(' +  "|".join(senders_list) + ') (changed) the (subject to .*)'
    regex3 = '(' +  "|".join(senders_list) + ') (changed) this (group\'s icon)'

    try:
        if re.match(regex1, message['sender']):
            match = re.search(regex1, message['sender'])
            returnMsg['sender'] = match.group(1).strip()
            returnMsg['message'] = match.group(3).strip()
            returnMsg['type'] = match.group(2).strip()
        elif re.match(regex2, message['sender']):
            match = re.search(regex2, message['sender'])
            returnMsg['sender'] = match.group(1).strip()
            returnMsg['message'] = match.group(3).strip()
            returnMsg['type'] = match.group(2).strip()
        elif re.match(regex3, message['sender']):
            match = re.search(regex3, message['sender'])
            returnMsg['sender'] = match.group(1).strip()
            returnMsg['message'] = match.group(3).strip()
            returnMsg['type'] = match.group(2).strip()
        elif message['message'] == 'image omitted':
            returnMsg['type'] = 'image'
        elif message['message'] == 'video omitted':
            returnMsg['type'] = 'video'
        elif message['message'] == 'audio omitted':
            returnMsg['type'] = 'audio'
        elif message['message'] == 'Contact card omitted':
            returnMsg['type'] = 'contact'
        else:
            returnMsg['type'] = 'text'
    except:
        return 'error'
    return returnMsg

senders_list = ['Suyash Shetty',
                'Pratik Kapoor',
                'Abhishek Rastogi',
                'Nabil Silva',
                'Bhavarth Chauhan',
                'Rajat Tripathi',
                'Rohit Malhotra',
                'Arpan Mishra',
                'Abhishek Bhatnagar',
                'Ashish Kona',
                'Rijul Rastogi Cse',
                'Manish Verma',
                'Code.Clean.Do',
                'Sailesh Shriram',
                'You'
                ]
messages = list()
with open('_chat.txt', 'r') as ccd_chat:
    content = ccd_chat.readlines()
    msg = str()
    for line in content:
        line = line.decode('utf-8')
        if re.search('(\[\d{2}\/\d{2}\/\d{2}, \d{1,2}:\d{2}:\d{2} [AP][M]\])', line) and msg:
            messages.append(format_message(msg))
            msg = ""
        msg = msg + line

with open('chat.json', 'w') as outfile:
    outfile.write(json.dumps(messages, indent=4))
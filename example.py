#!/usr/bin/env python3

# First, call fb_chat_parse.py on the command line to generate the parsed pickle file.
# Usage: fb_chat_parse.py [loation of messages.htm file] [name to save parsed file]

from fb_chat_parse import *

d = load_data()

if d:
    print(sum(len(message) for message in d.get_all_messages())) #print the total number of characters
    print(sum(1 for message in d.get_my_messages() if datetime(2015, 1, 1) < message.time)) #get the total number of messages you sent after Jan 1, 2015


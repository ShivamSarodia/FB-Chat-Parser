#!/usr/bin/env python3

from fb_chat_parse import *
import pickle

d = Data() #create an empty Data object
d.parse("messages.htm") #fill up the Data object with messages--can take a while

with open("parsed.p", "wb") as f:
    pickle.dump(d, f) #pickle the data object so you don't have to run d.parse every time

    #to unpickle, just use d = pickle.load(f)
    
print(sum(len(message) for message in d.get_all_messages())) #print the total number of characters
print(sum(1 for message in d.get_my_messages() if datetime(2015, 1, 1) < message.time)) #get the total number of messages you sent after Jan 1, 2015


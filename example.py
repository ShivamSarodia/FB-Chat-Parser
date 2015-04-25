#!/usr/bin/env python3

from fb_chat_parse import *
import pickle

d = Data("Shivam Sarodia") #create an empty Data object
d.parse("messages.htm") #fill up the Data object with messages--can take a while

with open("parsed.p", "wb") as f:
    pickle.dump(d, f) #pickle the data object so you don't have to run d.parse every time

    #to unpickle, just use d = pickle.load(f)

print(sum(len(message) for message in d.get_total_message_list())) #print the total number of characters


#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pickle

class Data:
    """Class to store all imported data. Pickle this class to speed up future use."""
    
    def __init__(self, _me = "",  _threads = []):
        self.me = _me #The name of the person whose messages are being analyzed
        self.threads = _threads

    def __setitem__(self, key, item):
        self.threads[key] = item

    def __getitem__(self, key):
        return self.threads[key]
        
    def add_thread(self, thread):
        """Add thread to data structure"""
        thread.flip()
        self.threads.append(thread)

    def get_threads(self, people):
        """Returns list of all threads of specified people."""
        return [i for i in self.threads if i.people == people]

    def get_indie_threads(self, person):
        """Returns all threads of individual chat with a person"""
        return self.get_threads({self.me, person})
        
    def get_messages(self, people):
        """Returns list of all messages in threads of specified people"""
        return sum([thread.messages for thread in self.get_threads(people)], [])

    def get_indie_messages(self, person):
        """Returns list of all messages in individual chat with a person"""
        return self.get_messages({self.me, person})

    def get_all_messages(self):
        """Returns list of all messages sent and received"""
        return sum([thread.messages for thread in self.threads], [])

    def get_messages_by(self, person):
        """Returns list of all messages sent by a particular person"""
        return [message for message in self.get_all_messages() if message.sender == person]
        
    def get_my_messages(self):
        """Return list of all messages sent by me"""
        return self.get_messages_by(self.me)
        
class Thread:
    def __init__(self, _people = set([]), _messages = []):
        self.messages = _messages
        self.people = _people #note that people includes the user himself
    def flip(self):
        self.messages = self.messages[::-1]
    def add_message(self, message):
        self.messages.append(message)
    def __iter__(self):
        return iter(self.messages)
    def __getitem__(self, key):
        return self.messages[key]
    def __setitem__(self, key, item):
        self.messages[key] = item
    def __len__(self):
        return len(self.messages)
    def __repr__(self):
        return "<Thread of " + str(self.people) + ">"
        
class Message:
    def __init__(self, _sender = None, _time = None, _content = ""):
        self.sender = _sender
        self.time = _time
        self.content = _content
    def __repr__(self):
        return "(" + str(self.time) + ") " + self.sender + ": " + self.content
    def __len__(self):
        return len(self.content)

def load_data(file_name = "messages.p"):
    try:
        f = open(file_name, "rb")
    except:
        print("Could not open pickled messages at " + file_name + ". Have you generated it?")
        return False
    else:
        return pickle.load(open(file_name, "rb"))

if __name__ == "__main__":
    messages_html = "messages.htm" if len(sys.argv) <= 1 else sys.argv[1]
    pickled = "messages.p" if len(sys.argv) <= 2 else sys.argv[2]

    d = Data()

    try:
        html_doc = open(messages_html, "rb")
    except IOError:
        print("Could not find messages.htm file")
    else:
        print("Beginning BeautifulSoup parse...")

        soup = BeautifulSoup(html_doc)
        print("Parse done.")
        print("Loading into thread...")

        d.me = str(soup.find_all("h1")[0].string)

        thread_iter = soup.find_all("div", class_ = "thread")
        for tel in thread_iter:
            try:
                thread = Thread(set(tel.contents[0].split(", ")), []) #create a new thread to populate
                
                message = Message() #create the first message to populate
                for mel in tel.children:
                    if mel.name == None:
                        pass #should only happen once, for the list of participants
                    elif mel.name == "div":
                        try:
                            message.sender = str(mel.find_all("span", class_ = "user")[0].string)
                            timestr = str(mel.find_all("span", class_ = "meta")[0].string[0:-4])
                            message.time = datetime.strptime(timestr, "%A, %B %d, %Y at %I:%M%p")
                        except IndexError:
                            pass
                    elif mel.name == "p":
                        if mel.string == None: #this happens if there's no text in the message
                            message.content = ""
                        else:
                            message.content = str(mel.string)
                            thread.add_message(message) #add the current message to the string
                            message = Message() #create a new message to populate
                    else:
                        print("Something strange happened. Carrying on.") #this shouldn't happen
                        
                d.add_thread(thread)
            except TypeError:
                print("No thread header, ignoring thread") #Some threads don't have a header in messages.htm.

        print("Load done. Pickling...")

        with open(pickled, "wb") as f: pickle.dump(d, f)

        print("Pickle saved. Done.")





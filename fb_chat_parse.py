#!/usr/bin/env python3

from bs4 import BeautifulSoup
from datetime import datetime
import time

class Data:
    """Class to store all imported data. Pickle this class to speed up future use."""
    
    def __init__(self, _me, _threads = []):
        self.me = _me #The name of the person whose messages are being analyzed
        self.threads = _threads

    def __setitem__(self, key, item):
        self.threads[key] = item

    def __getitem__(self, key):
        return self.threads[key]
        
    def add_thread(self, thread):
        """Add thread to data structure"""
        self.threads.append(thread)

    def get_threads(self, people):
        """Returns list of all threads of specified people.

        Note that Facebook sometimes splits up a single chat into multiple threads."""
        return [i for i in self.threads if i.people == people]

    def get_threads_with(self, person):
        """Returns all threads of individual chat with a person"""
        return self.get_threads({self.me, person})
        
    def get_messages(self, people):
        """Return list of all messages in threads of specified people"""
        return sum([thread.messages for thread in self.get_threads(people)], [])

    def get_messages_with(self, person):
        """Return list of all messages in individual chat with a person"""
        return self.get_messages({self.me, person})
        
    def get_total_message_list(self):
        """Return list of all messages sent and received"""
        return sum([thread.messages for thread in self.threads], [])

    def get_my_message_list(self):
        """Return list of all messages sent"""
        return sum([thread.messages for thread in self.threads if thread.sender == self.me], [])
           
    def parse(self, file_location):
        """Parse the downloaded Facebook message file.

        file_location should be the location of the messages.htm file"""
        
        html_doc = open(file_location, "rb")

        print("Beginning parse...")
        
        soup = BeautifulSoup(html_doc)
        print("Parse done.")
        print("Loading into thread...")

        threaditer = soup.find_all("div", class_ = "thread")
        for tel in threaditer:
            try:
                thread = Thread(set(tel.contents[0].split(", ")), []) #set the people in conversation
                message = Message()
                
                for mel in tel.children:
                    if mel.name == None:
                        #should only happen once, for the list of participants
                        pass
                    elif mel.name == "div":
                        try:
                            message.sender = str(mel.find_all("span", class_ = "user")[0].string)
                            timestr = str(mel.find_all("span", class_ = "meta")[0].string[0:-4])
                            message.time = datetime.strptime(timestr, "%A, %B %d, %Y at %I:%M%p")
                        except IndexError:
                            pass
                    elif mel.name == "p":
                        if mel.string == None: #this happens if there's no text in the message, e.g. meep/pusheen/etc
                            message.content = ""
                        else:
                            message.content = str(mel.string)

                        thread.add_message(message)
                        message = Message()
                    else:
                        print("Oh, dear me.") #this shouldn't happen
                self.add_thread(thread)
            except TypeError:
                print("No thread header, ignoring thread")
                #Some threads don't have a header in messages.htm, for some reason I can't explain. This is really rare though, so it's no big deal.

        print("Load done.")
        
class Thread:
    def __init__(self, _people = [], _messages = []):
        self.messages = _messages
        self.people = _people
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
        
class Message:
    def __init__(self, _sender = None, _time = None, _content = ""):
        self.sender = _sender
        self.time = _time
        self.content = _content
    def __len__(self):
        return len(self.content)

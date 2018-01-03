#!/usr/bin/env python3

# First, run:
#
# python parse_messages.py messages_dir dump_file
#
# To generate a pickled fb_chat.Data object. The filename provided to
# this command as `dump_file` is the argument to provide the
# fb_chat.load_data function.

from datetime import datetime
import random

import fb_chat

data = fb_chat.load_data("fb_chat_dump.p")

# Print the number of messages in individual chat with a particular
# person.
num_with_john = len(data.query(indv="John Smith"))
print("Messages with John: {}".format(num_with_john))

# Print a random message in individual chat with a particular person
print(random.choice(data.query(indv="John Smith").messages))

# Print statistics on usage of a particular group chat.
club_thread = data.query(chat_name="Programming Club")
for member in club_thread.members:
    messages = club_thread.query(sender=member,
                                 start=datetime(2017, 1, 1),
                                 end=datetime(2018, 1, 1))
    print("{} sent {} messages in 2017".format(member, len(messages)))

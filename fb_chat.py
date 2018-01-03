from datetime import datetime
import pickle

def load_data(filename):
    """Return a Data object loaded from the given pickle file."""
    with open(filename, "rb") as f:
        return pickle.load(f)

class Data:
    def __init__(self, threads, me=None):
        self.threads = threads

        if me:
            self.me = me
        else:
            counts = {}

            # set 'me' as the most common sender in the threads
            for thread in self.threads:
                for mess in thread.messages:
                    counts[mess.sender] = counts.get(mess.sender, 0) + 1

            self.me = max(counts, key=lambda x: counts[x])

        for thread in self.threads:
            thread.add_me(self.me)

    def query(self, *,
              indv=None,
              chat_name=None,
              members=None,
              first=True):

        """Query the threads in this chat data.

        indv (string) - Return the individual chat thread with this person.
        chat_name (string) - Return the chat thread with this name.
        member (iterable of names) - Return the chat thread with these members.
        first (bool) - If true, return only the longest match.

        Exactly one of indv, chat_name, and members may be specified.
        """
        if [indv, chat_name, members].count(None) < 2:
            raise ValueError("Multiple query types may not be specified.")

        if indv:
            threads = [t for t in self.threads
                       if t.name == indv and
                       t.members == set((self.me, indv))]
        elif chat_name:
            threads = [t for t in self.threads if t.name == chat_name]
        elif members:
            members = set(members)
            members.add(self.me)

            threads = [t for t in self.threads if t.members == members]

        if first:
            return max(threads, key=len, default=None)
        else:
            return threads

    def __getitem__(self, key):
        return self.threads[key]

    def __iter__(self):
        return iter(self.threads)

    def __len__(self):
        return len(self.threads)


class Thread:
    def __init__(self, name, messages, raw_members, filename):
        self.name = name
        self.filename = filename
        self.messages = messages
        self.me = None

        # We take the raw members and add everyone who spoke in the
        # chat to get the final members list.
        self.members = set(raw_members)
        for message in messages:
            self.members.add(message.sender)

    def add_me(self, me):
        """Add the given person as a member of this thread and as the self.me
        for this thread.

        This function is called automatically by the Data constructor,
        so that each individual thread has both you and the other
        people as members.

        """
        self.me = me
        self.members.add(me)

    def query(self, *,
              sender=None,
              senders=None,
              start=datetime.min,
              end=datetime.max):
        """Query this thread's messages.

        start (datetime) - return only messages after this time (inclusive)
        end (datetime) - return only messages before this time (exclusive)
        sender (string) - return only messages by the given sender
        senders (iterable of strings) - return only messages by one of the given senders
        """
        if sender and senders:
            raise ValueError("`sender` and `senders` cannot be simultaneously specified")

        if sender:
            senders = set([sender])

        def condition(m):
            return (start <= m.time < end) and (not senders or m.sender in senders)

        return [m for m in self.messages if condition(m)]

    def get_my_messages(self):
        return self.query(sender=self.me)

    def __repr__(self):
        return "<Thread of {} named {}>".format(
            ", ".join(self.members), self.name)

    def __getitem__(self, key):
        return self.messages[key]

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)


class Message:
    def __init__(self, sender, text, time):
        self.sender = sender
        self.text = text
        self.time = time

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return "(" + str(self.time) + ") " + self.sender + ": " + self.text

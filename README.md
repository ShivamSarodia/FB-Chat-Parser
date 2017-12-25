FB-Chat-Parse
======

**NOTE: The Facebook data download format has changed, so this tool no longer works. I'll update this repository shortly.**

Parses Facebook messages into a format convenient for analysis. Based on Python 3; requires BeautifulSoup.

To use, download your Facebook user data as described [here](https://www.facebook.com/help/131112897028467/), and unzip the provided file. To parse the messages into a pickled binary, call fb_chat_parse with arguments as below:

```fb_chat_parse.py [location of messages.htm file] [name to save parsed pickle file]```

The first argument should be the location of the /html/messages.htm file contained within the downloaded zip.

A few notes:
* Intuitively, you'd expect each thread to correspond to exactly one chat--however, this isn't the case. Facebook caps each thread length at 10,000 messages, so long chats can carry over to multiple threads.
* The parsing can take a while; be patient.

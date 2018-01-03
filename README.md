Facebook chat parser and query API
======

Parses Facebook messages into Python objects to enable convenient analysis. Requires Python 3 and BeautifulSoup.

To use, download your Facebook user data as described [here](https://www.facebook.com/help/131112897028467/) and unzip the resulting file. Note the `messages/` directory in this data dump; it contains the raw HTML files containing your chat messages.

To parse the messages into a pickled binary, call parse_messages.py with arguments as below:

```python parse_messages.py [location of messages/ directory] [name to save parsed pickle file]```

Then, see `example.py` for usage examples, and `fb_chat.py` for details on the querying API.

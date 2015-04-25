FB-Chat-Parse
======

Parses Facebook messages into a format convenient for analysis. Based on Python 3; requires BeautifulSoup.

To use, download your Facebook user data as described [here](https://www.facebook.com/help/131112897028467/), and unzip the provided file. The argument for parse should be the location of the /html/messages.htm file contained within.

A few notes:
* Intuitively, you'd expect each thread to correspond to exactly one chat--however, this isn't the case. Facebook caps each thread length at 10,000 messages, so long chats can carry over to multiple threads.
* `Data.parse` can take a while to run. To speed up processing in the future, I recommend pickling the `Data` object after first parsing it, then unpickling for later use. Use `pickle.dump(d, open("parsed.p", "wb"))` to pickle, and `d = pickle.load(open("parsed.p", "rb"))` to unpickle.
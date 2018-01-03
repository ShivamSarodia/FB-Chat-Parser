from bs4 import BeautifulSoup
from datetime import datetime
import os
import pickle
import re
import sys
import time

import fb_chat

def _get_message_files(messages_dir):
    files = {}
    for dir_entry in os.scandir(messages_dir):
        # Skip non-files or non-HTML-files
        if not dir_entry.is_file() or dir_entry.path[-5:] != ".html":
            continue

        files[dir_entry.path] = dir_entry.stat().st_size

    return files


def _parse_file(filename):
    with open(filename) as f:
        body = f.read()

    soup = BeautifulSoup(body, "lxml")
    base_filename = os.path.basename(filename)
    return _parse_thread(soup, base_filename)


def _parse_thread(soup, base_filename):
    # Extract thread name from the bold h3 heading
    h3 = soup.find("h3")
    header = h3.text
    match = re.search(r"^Conversation with (.+)$", header)
    if not match:
        raise ValueError("could not parse thread header '{}' in file {}"
                         .format(header, filename))
    name = match.group(1)

    # Extract raw participants list from the heading. This list includes
    # everyone who was in the chat at donwload time, except the user themselves.
    parts_el = h3.next_sibling
    parts_text = parts_el.string
    match = re.search(r"^Participants: (.*)$", parts_text)
    if not match:
        raise ValueError("could not parse participants list '{}' in file {}"
                         .format(parts_text, filename))

    # If user is the only member in the conversation, the participants list is
    # empty, so we deal with that case separately.
    if not match.group(1).strip():
        raw_parts = []
    else:
        raw_parts = [part.strip() for part in match.group(1).split(",")]

    messages = []

    # Extract all the message contents
    el = parts_el.next_sibling
    while el:
        messages.append(_parse_message(el, el.next_sibling))
        el = el.next_sibling.next_sibling

    messages.reverse()
    return fb_chat.Thread(name, messages, raw_parts, base_filename)


def _parse_message(header_el, content_el):
    sender = header_el.find("span", "user").text
    time_str = header_el.find("span", "meta").text
    time = datetime.strptime(time_str, "%A, %B %d, %Y at %I:%M%p %Z")
    text = content_el.text

    return fb_chat.Message(sender, text, time)


def parse(message_file_dir, silent=True):
    def log(s):
        if not silent: print(s)

    log("Beginning parsing messages...")

    message_files = _get_message_files(message_file_dir)

    # Size in bytes that has been parsed
    processed_size = 0

    # Size in bytes that is left to parse
    total_size = sum(message_files.values())

    # Next % progress to log
    next_print = 5

    # Start time (in seconds)
    start_time = time.time()

    threads = []
    for i, message_file in enumerate(message_files):
        progress = int(round(100 * processed_size / total_size))
        if progress > next_print:
            # Compute time left
            time_so_far = time.time() - start_time
            time_left = int(time_so_far * (total_size / processed_size - 1))
            min_left, sec_left = divmod(time_left, 60)

            log("{}% complete ({} files out of {}) - ETA: {}:{:02d}"
                  .format(progress, i, len(message_files),
                          int(min_left), int(sec_left)))

            next_print = progress + 5

        threads.append(_parse_file(message_file))
        processed_size += message_files[message_file]

    log("Finished parsing messages.")

    data = fb_chat.Data(threads)
    return data


def save_data(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)


if __name__=="__main__":
    if len(sys.argv) != 3:
        print("""usage: python parse_messages.py messages_dir dump_file
  messages_dir  Path to the 'messages/' directory within the Facebook data dump.
  dump_file     File path at which to save the pickled data dump file.""")
        exit(1)

    messages_dir = sys.argv[1]
    dump_file = sys.argv[2]

    data = parse(messages_dir, silent=False)
    print("Saving data...")
    save_data(data, dump_file)

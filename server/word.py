# -*- coding: utf-8 -*-

import sys
import re
import sqlite3
import datetime
import re
import random
from flask import current_app as app
from server.db import query_db
from server.db import exists_unused_word_in_db
from server.db import exists_used_word_in_db
from server.db import select_unused_word_in_db
from server.db import select_used_word_in_db
from server.db import choose_last_unused_word_in_db
from server.db import choose_last_modified_used_word_in_db
from server.db import get_last_modified_in_db
from server.db import get_url_in_db

# normally we want to use a memcached server.
from werkzeug.contrib.cache import SimpleCache

split_words = lambda url: \
                  filter(str.isalnum, re.findall('[^\W]+', url))

class Word(object):
    def __init__(self):
        self.cache = SimpleCache(threshold=1000, 
                                 default_timeout=60*60)

    def find_word(self, url):
        """ if any of words in unused, then select one.
        """
        def generator(url):
            for l in [self.cache.get, 
                      self.find_unused_word, 
                      self.find_used_word]:
                yield l(url)
        for selected_word in generator(url):
            if bool(selected_word):
                self.cache.set(url, selected_word)
                return selected_word 

    def find_url(self, word):
        if exists_used_word_in_db(word):
            return get_url_in_db(word)
        return None

    def find_unused_word(self, url):
        # find one from unused
        for word in split_words(url):
            if exists_unused_word_in_db(word):
                return select_unused_word_in_db(word, url)

        # one random
        last_word = choose_last_unused_word_in_db()
        return select_unused_word_in_db(last_word, url)

    def find_used_word(self, url):
        words = {}
        for word in split_words(url):
            if exists_used_word_in_db(word):
                words.setdefault(word, 
                         get_last_modified_in_db(word))

        oldest_word = ""
        if bool(words):
            oldest_word = min(words) 
        else:
            oldest_word = choose_last_modified_used_word_in_db()
        return select_used_word_in_db(oldest_word, url)

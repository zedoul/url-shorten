#!/usr/bin/env Python

import re
import sqlite3
import datetime
import logging
import random
from config import *

def load_words_from_datafiles(datafiles=DATAFILES_PATH):
    for datafile in datafiles:
        with open(datafile, 'r') as wordsfile:
            for word in wordsfile.readlines():
                yield filter(re.compile('[a-z0-9]').match,
                             word.strip('\n').lower())
        wordsfile.close()

def initialize_db(reset = False):
    conn = sqlite3.connect(DATABASE_PATH, 
                           check_same_thread = False)
    cursor = conn.cursor()
    if reset:
        cursor.executescript('DROP TABLE IF EXISTS %s;' % 
                             UNUSED_WORD_TABLE_NAME)
        cursor.executescript('DROP TABLE IF EXISTS %s;' % 
                             USED_WORD_TABLE_NAME)
        cursor.execute("CREATE TABLE %s (" \
                 "word TEXT PRIMARY KEY," \
                 "created DATETIME DEFAULT CURRENT_TIMESTAMP)" %
                            UNUSED_WORD_TABLE_NAME)
        cursor.execute("CREATE TABLE %s (" \
                 "word TEXT PRIMARY KEY," \
                 "url TEXT," \
                 "last_modified DATETIME DEFAULT CURRENT_TIMESTAMP)" %
                            USED_WORD_TABLE_NAME)

    wordset = set()
    wordlist = [word for word in load_words_from_datafiles() \
                if not (word in wordset or wordset.add(word))] 
    random.shuffle(wordlist)

    for word in wordlist:
        query = "SELECT word FROM %s WHERE word = '%s'" % \
                    (UNUSED_WORD_TABLE_NAME, word)
        if not cursor.execute(query).fetchone():
            query = "INSERT INTO %s('word') VALUES (?)" % \
                        (UNUSED_WORD_TABLE_NAME)
            cursor.execute(query, (word,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db(reset = True)
    print "complete"

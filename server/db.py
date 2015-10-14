import sqlite3
from flask import current_app as app
from flask import g

def connect_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(app.config['DATABASE_PATH'])
    return db

def close_db():
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    conn = connect_db()
    cursor = conn.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    conn.commit()
    return (rv[0] if rv else None) if one else rv

def exists_unused_word_in_db(word):
    query = "SELECT EXISTS(SELECT 1 FROM %s " \
            "WHERE word = '%s' LIMIT 1)" % \
            (app.config.get("UNUSED_WORD_TABLE_NAME"), word)
    return query_db(query, one = True)[0]

def exists_used_word_in_db(word):
    query = "SELECT EXISTS(SELECT 1 FROM %s " \
            "WHERE word = '%s' LIMIT 1)" % \
            (app.config.get("USED_WORD_TABLE_NAME"), word)
    return query_db(query, one = True)[0]

def choose_last_unused_word_in_db():
    # last_rowid
    query = 'SELECT max(rowid) FROM %s' % \
            app.config.get("UNUSED_WORD_TABLE_NAME")
    last_rowid = query_db(query, one = True)[0]

    # choose last unused word
    query = "SELECT word FROM %s WHERE rowid = %d LIMIT 1" % \
            (app.config.get("UNUSED_WORD_TABLE_NAME"), last_rowid)
    return query_db(query, one = True)[0]

def select_unused_word_in_db(word, url):
    delete_query = "DELETE FROM '%s' WHERE word = '%s'" % \
        (app.config.get("UNUSED_WORD_TABLE_NAME"), word)
    insert_query = "INSERT INTO %s('word', 'url') VALUES (?, ?)" % \
        app.config.get("USED_WORD_TABLE_NAME")
    query_db(delete_query)
    query_db(insert_query, (word, url))
    return word

def select_used_word_in_db(word, url):
    query = "UPDATE '%s' SET url = (?) WHERE word = '%s'" % \
            (app.config.get("USED_WORD_TABLE_NAME"), word)
    query_db(query, (url,))
    return word

def get_last_modified_in_db(word):
    query = "SELECT last_modified FROM '%s' " \
            "WHERE word = '%s' " \
            "ORDER BY last_modified ASC " \
            "LIMIT 1" % \
            (app.config.get("USED_WORD_TABLE_NAME"), word)
    return query_db(query, one = True)[0]

def get_url_in_db(word):
    query = "SELECT url FROM '%s' " \
            "WHERE word = '%s' " \
            "ORDER BY last_modified ASC " \
            "LIMIT 1" % \
            (app.config.get("USED_WORD_TABLE_NAME"), word)
    return query_db(query, one = True)[0]

def choose_last_modified_used_word_in_db():
    query = "SELECT word FROM '%s' " \
            "ORDER BY last_modified ASC " \
            "LIMIT 1" % \
            app.config.get("USED_WORD_TABLE_NAME")
    return query_db(query, one = True)[0]

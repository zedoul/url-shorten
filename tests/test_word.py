# -*- coding: utf-8 -*-
"""
    tests.word
    ~~~~~~~~~~~~~~~~~~~~~

    The word functionality.
"""

import pytest
import unittest
import os

from server.word import Word

class TestWord(unittest.TestCase):
    def test_database(self):
        os.system("./wordloader.py")
        word = Word()
        r = word.find_word("www.forrest.com") # unused word
        assert "forrest" in r 
        r = word.find_word("www.forrest.com") # cached / stored word
        assert "forrest" in r 
        r = word.find_word("www.asdfsd.forrest.com") # random
        assert "forrest" not in r 

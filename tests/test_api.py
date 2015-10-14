# -*- coding: utf-8 -*-
"""
    tests.api
    ~~~~~~~~~~~~~~~~~~~~~

    The api functionality.
"""

import pytest

def test_api_speed_performance(client):
    import time
    start = time.time()
    rv = client.get('/search?link="www.google.com"')
    elapsed = time.time() - start
    assert elapsed < 0.1, "elapsed %f" % elapsed

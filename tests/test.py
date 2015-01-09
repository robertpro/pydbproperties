#!/usr/bin/env python

from pydbproperties import pydbproperties


if __name__ == "__main__":
    a = pydbproperties()
    # a.set_table_name('my_table')
    for b in range(5):
        a.set_property('key' + str(b), 'value' + str(b))

    config = {
        "host": 'localhost',
        "user": 'root',
        "passwd": '',
        "db": 'test_pydbproperties',
    }
    a.conn(**config)
    a.list()
    a.set_auto_load(True)
    a.list()
    a.set_auto_store(True)
    a.set_property('w', 'w')
    a.list()
    a.remove_property('w')
    a.list()

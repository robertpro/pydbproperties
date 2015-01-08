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
    print('\nLoading from table')
    a.load()
    a.list()
    a.set_property('key_test', 'value_test')
    a.store()
    a.list()
    print('\nRemoving property "key2"')
    a.remove_property('key2')
    a.list()
    print('\nOverriding value of property "key_test"')
    a.set_property('key_test', 'value_test2')
    a.list()
    a.remove_property_db('key1')
    a.list()

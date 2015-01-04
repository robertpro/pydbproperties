pydbproperties
==============

    a = pydbproperties()
    a.set_table_name('my_table')
    for b in range(5):
        a.set_property('key' + str(b), 'value' + str(b))

    config = {
        "host": 'localhost',
        "user": 'root',
        "passwd": '',
        "db": 'test_pydbproperties',
    }
    a.conn(**config)
    # a.load()
    a.list()
    a.set_property('key_test', 'value_test')
    a.store()
    a.list()

======================    
Output:
-- listing properties --
key3=value3
key2=value2
key1=value1
key0=value0
key4=value4
-- listing properties --
key3=value3
key2=value2
key1=value1
key0=value0
key4=value4
key_test=value_test

=====================
Table in MySQL:

MariaDB [test_pydbproperties]> use test_pydbproperties
Database changed
MariaDB [test_pydbproperties]> show tables;
+-------------------------------+
| Tables_in_test_pydbproperties |
+-------------------------------+
| my_table                      |
+-------------------------------+
1 row in set (0.00 sec)

MariaDB [test_pydbproperties]> select * from my_table;
+----------+------------+
| key      | value      |
+----------+------------+
| key0     | value0     |
| key1     | value1     |
| key2     | value2     |
| key3     | value3     |
| key4     | value4     |
| key_test | value_test |
+----------+------------+
6 rows in set (0.00 sec)

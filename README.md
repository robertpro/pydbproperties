pydbproperties 0.3
==============
With this script, you can use store properties into a 
MySQL table, you can change the name of the table, and 
list the properties into a output stream or file 
stream, etc.

Right now it only works with MySQL Database, I will be
working in other databases.

Dependencies:
=============
MySQL-python (1.2.3)
MysqlSimpleQueryBuilder (0.2.8)

Installation:
=============
MySQL-python has issues when installing by pip
you can install it with your package manage of
your distribution

ubuntu: sudo apt-get install python2.7-mysqldb
Centos/RHEL/Fedora: yum install MySQL-python

Once MySQL-python is installed, you can install
MysqlSimpleQueryBuilder:

    pip install MysqlSimpleQueryBuilder

And now you are ready to install pydbproperties:

    pip install pydbproperties

Example:
========
    from pydbproperties import pydbproperties
    prop = pydbproperties()
    prop.set_table_name('my_table')
    for b in range(5):
        prop.set_property('key' + str(b), 'value' + str(b))

    config = {
        "host": 'localhost',
        "user": 'root',
        "passwd": '',
        "db": 'test_pydbproperties',
    }
    prop.conn(**config)
    # prop.load()
    prop.list()
    prop.set_property('key_test', 'value_test')
    prop.store()
    prop.list()
    
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

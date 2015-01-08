%define name pydbproperties
%define version 0.1
%define unmangled_version 0.1
%define unmangled_version 0.1
%define release 1

Summary: Store property in database, like pyjavaproperties(Property JAVA)
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL v3
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Jose Roberto Meza Cabrera <robertpro01@gmail.com>
Url: https://github.com/robertpro

%description
pydbproperties 0.1
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


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

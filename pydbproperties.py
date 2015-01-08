#!/usr/bin/env python2
# coding=utf8

from __future__ import print_function
import re
import sys

__doc__ = """
author: José Roberto Meza Cabrera
mail: robertpro01@gmail.com

With this script, you can use key and values as property
it save the properties into a table, you can change the
name of the table, and list the properties into a output
stream or file stream, etc.
"""

try:
    import myquerybuilder
except:
    print('MySql Simple Query Builder module not found')
    print('pip install MysqlSimpleQueryBuilder')
    sys.exit(1)
    pass

NULL = ('', None, (), [], {})


class pydbproperties():
    """
    A Python implements of pyjavaproperties for database
    """
    def __init__(self):
        # Dictionary of properties.
        self._props = {}
        self.bspacere = re.compile(r'\\(?!\s$)')
        self.othercharre = re.compile(r'(?<!\\)(\s*\=)|(?<!\\)(\s*\:)')

        # Dictionary mapping keys from property
        # Dictionary to pristine dictionary
        self._keymap = {}
        # This is used for dumping the properties to a file
        # using the 'store' method
        self._origprops = {}
        self._keyorder = []
        # Connection to DB
        self._conn = None
        # Table name for properties
        self._table_name = 'pydbproperties'
        pass

    def get_property(self, key):
        """ Return a property for the given key """

        return self._props.get(key, '')

    def set_property(self, key, value):
        """ Set the property for the given key """
        if type(key) is str and type(value) is str:
            if len(key) != 0:
                self.process_pair(key, value)
            else:
                raise ValueError("key can't be null!")
        else:
            raise TypeError('both key and value should be strings!')
        pass

    def process_pair(self, key, value):
        """ Process a (key, value) pair """

        oldkey = key
        oldvalue = value

        # Create key intelligently
        keyparts = self.bspacere.split(key)
        # print keyparts

        strippable = False
        lastpart = keyparts[-1]

        if lastpart.find('\\ ') != -1:
            keyparts[-1] = lastpart.replace('\\', '')

        # If no backspace is found at the end, but empty
        # space is found, strip it
        elif lastpart and lastpart[-1] == ' ':
            strippable = True

        key = ''.join(keyparts)
        if strippable:
            key = key.strip()
            oldkey = oldkey.strip()

        # oldvalue = self.unescape(oldvalue)
        # value = self.unescape(value)

        # Patch from N B @ ActiveState
        curlies = re.compile("{.+?}")
        found = curlies.findall(value)

        for f in found:
            srcKey = f[1:-1]
            if srcKey in self._props:
                value = value.replace(f, self._props[srcKey], 1)

        self._props[key] = value.strip()

        # Check if an entry exists in pristine keys
        if key in self._keymap:
            oldkey = self._keymap.get(key)
            self._origprops[oldkey] = oldvalue.strip()
        else:
            self._origprops[oldkey] = oldvalue.strip()
            # Store entry in keymap
            self._keymap[key] = oldkey

        if key not in self._keyorder:
            self._keyorder.append(key)
        pass

    def escape(self, value):
        # Java escapes the '=' and ':' in the value
        # string with backslashes in the store method.
        # So let us do the same.

        newvalue = value.replace(':', '\:')
        newvalue = newvalue.replace('=', '\=')

        return newvalue

    def unescape(self, value):
        # Reverse of escape

        newvalue = value.replace('\:', ':')
        newvalue = newvalue.replace('\=', '=')

        return newvalue

    def list(self, out=sys.stdout):
        """ Prints a listing of the properties to the
        stream 'out' which defaults to the standard output """

        if out == sys.stdout or type(out) is file:
            out.write('-- listing properties --\n')
            for key, value in self._props.items():
                out.write(''.join((key, '=', value, '\n')))
                pass
            pass
        else:
            raise TypeError('Argument should be a file or sys.stdout object!')
        pass

    def get_property_dict(self):
        """
        Returns property dict
        """
        return self._props

    def store(self):
        """
        Stores the dict to a database
        """

        try:
            # Create the table, and be happy without errors
            self.create_table()
            for prop in self._keyorder:
                if prop in self._origprops:
                    val = self._origprops[prop]
                    if prop == self._conn.one(('key',), self.get_table_name(),
                                              {'key': prop}):
                        # if prop == self._conn.query('update `my_table` set
                        # `key`='key5' where `key`='key0')
                        # Update
                        self._conn.update(self.get_table_name(),
                                          {'value': val}, {'key': prop})
                    else:
                        # Insert
                        self._conn.insert(self.get_table_name(),
                                          {'key': prop,
                                           # 'value': self.escape(val)})
                                           'value': val})
        except:
            raise
            pass

    def load(self):
        """
        Load properties from database
        """
        try:
            # Create the table, and be happy without errors
            self.create_table()
        except:
            pass
        # self._props = {}
        # self._keyorder = []
        # self._origprops = {}
        if self._conn is None:
            raise ValueError('Connection not initialized')
        attr = ('key', 'value')
        if self._table_name in NULL:
            raise ValueError('Table name can\'t be null')
        properties_dict = self._conn.select(attr, self._table_name)
        properties_list = [b.get('key') + '=' + b.get('value') +
                           '\n' for b in properties_dict]
        self.__parse(properties_list)
        pass

    def __parse(self, lines):
        """ Parse a list of lines and create
        an internal property dictionary """

        # Every line in the file must consist of either a comment
        # or a key-value pair. A key-value pair is a line consisting
        # of a key which is a combination of non-white space characters
        # The separator character between key-value pairs is a '=',
        # ':' or a whitespace character not including the newline.
        # If the '=' or ':' characters are found, in the line, even
        # keys containing whitespace chars are allowed.

        # A line with only a key according to the rules above is also
        # fine. In such case, the value is considered as the empty string.
        # In order to include characters '=' or ':' in a key or value,
        # they have to be properly escaped using the backslash character.

        # Some examples of valid key-value pairs:
        #
        # key     value
        # key=value
        # key:value
        # key     value1,value2,value3
        # key     value1,value2,value3 \
        #         value4, value5
        # key
        # This key= this value
        # key = value1 value2 value3

        # Any line that starts with a '#' or '!' is considerered a comment
        # and skipped. Also any trailing or preceding whitespaces
        # are removed from the key/value.

        # This is a line parser. It parses the
        # contents like by line.

        lineno = 0
        i = iter(lines)

        for line in i:
            lineno += 1
            line = line.strip()
            # Skip null lines
            if not line:
                continue
            # Skip lines which are comments
            if line[0] in ('#', '!'):
                continue
            # Some flags
            # escaped = False
            # Position of first separation char
            sepidx = -1
            # A flag for performing wspace re check
            # flag = 0
            # Check for valid space separation
            # First obtain the max index to which we
            # can search.
            m = self.othercharre.search(line)
            if m:
                first, last = m.span()
                start, end = 0, first
                # flag = 1
                wspacere = re.compile(r'(?<![\\\=\:])(\s)')
            else:
                if self.othercharre2.search(line):
                    # Check if either '=' or ':' is present
                    # in the line. If they are then it means
                    # they are preceded by a backslash.

                    # This means, we need to modify the
                    # wspacere a bit, not to look for
                    # : or = characters.
                    wspacere = re.compile(r'(?<![\\])(\s)')
                start, end = 0, len(line)

            m2 = wspacere.search(line, start, end)
            if m2:
                # print 'Space match=>',line
                # Means we need to split by space.
                first, last = m2.span()
                sepidx = first
            elif m:
                # print 'Other match=>',line
                # No matching wspace char found, need
                # to split by either '=' or ':'
                first, last = m.span()
                sepidx = last - 1
                # print line[sepidx]
                pass

            # If the last character is a backslash
            # it has to be preceded by a space in which
            # case the next line is read as part of the
            # same property
            while line[-1] == '\\':
                # Read next line
                nextline = i.next()
                nextline = nextline.strip()
                lineno += 1
                # This line will become part of the value
                line = line[:-1] + nextline
                pass

            # Now split to key,value according to separation char
            if sepidx != -1:
                key, value = line[:sepidx], line[sepidx+1:]
            else:
                key, value = line, ''
            self._keyorder.append(key)
            self.process_pair(key, value)
            pass
        pass

    def set_table_name(self, table_name):
        """
        Sets table name
        """
        if table_name not in NULL:
            self._table_name = table_name
            return
        raise ValueError('Table name can\'t be null')

    def get_table_name(self):
        """
        Returns table name
        """
        return self._table_name

    def get_property_names(self):
        """ Return an iterator over all the keys of the property
        dictionary, i.e the names of the properties """

        return self._props.keys()

    def remove_property(self, property):
        """
        Remove a property
        if property is None: remove all properties
        """
        if property is None:
            self._props = {}
            self._keyorder = []
            self._keymap = {}
            pass
        else:
            try:
                self._props.pop(property)
                self._keyorder.remove(property)
                self._keymap.pop(property)
            except:
                pass
        pass

    def remove_property_db(self, prop):
        """
        Remove a property directly from a database
        if property is None: remove all properties directly from a database
        """
        if prop is None:
            value = None
        else:
            value = {'key': prop}
            pass
        self._conn.delete(self.get_table_name(), value)
        pass

    def __getitem__(self, name):
        """ To support direct dictionary like access """

        return self.get_property(name)

    def __setitem__(self, name, value):
        """ To support direct dictionary like access """

        self.set_property(name, value)
        pass

    def conn(self, **kwargs):
        """
        Instance a connection with the database
        """
        try:
            self._conn = myquerybuilder.QueryBuilder(**kwargs)
        except:
            print('An error has occurred\n')
            raise
        pass

    def create_table(self):
        """
        Create a table, if you don't use set_table_name() method, the
        name of the table will be default( pydbproperties )
        """

        def validate_table():
            """
            This method is auxiliar to create_table() method, it will
            return True if table definition is correct
            """
            try:
                aux = self._conn.query("describe " +
                                       self._table_name).fetchall()
                key = aux[0]
                value = aux[1]
                if len(aux) != 2 or\
                        key['Field'] != 'key' or \
                        value['Field'] != 'value' or\
                        not key['Type'].lower().startswith('varchar') or\
                        not value['Type'].lower().startswith('longtext') or\
                        not key['Null'].upper() == 'NO' or\
                        not value['Null'].upper() == 'YES':
                    return False
                return True
            except:
                return False

        query = """
        create table {0} ( `key` varchar(30) not null,
        `value` longtext null, primary key (`key`));
        """.format(self.get_table_name())
        try:
            self._conn.query(query)
        except:
            pass
        return validate_table()
    pass

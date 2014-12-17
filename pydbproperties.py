#!/usr/bin/env python2

import re


class pydbproperties():
    """
    A Python implements of pyjavaproperties for database
    """
    def __init__(self, database=None, table_name=None):
        # Dictionary of properties.
        self._props = {}
        self._database = database
        self._table_name = table_name
        self.bspacere = re.compile(r'\\(?!\s$)')
        # Dictionary mapping keys from property
        # Dictionary to pristine dictionary
        self._keymap = {}
        # This is used for dumping the properties to a file
        # using the 'store' method
        self._origprops = {}
        self._keyorder = []
        pass

    def getProperty(self, key):
        """ Return a property for the given key """

        return self._props.get(key, '')

    def setProperty(self, key, value):
        """ Set the property for the given key """
        if type(key) is str and type(value) is str:
            if len(key) != 0 and len(value) != 0:
                self.processPair(key, value)
            else:
                raise ValueError, "'both key and value can't be null!"
        else:
            raise TypeError, 'both key and value should be strings!'
        pass

    def processPair(self, key, value):
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

    def list(self):
        """ Prints a listing of the properties to the
        stream 'out' which defaults to the standard output """

        pass

    def getPropertyDict(self):
        return self._props

    def store(self, database=None, table_name=None):
        if database is None and self._database is None:
            raise ValueError, "Database can't be None"
        if table_name is None and self._table_name is None:
            raise ValueError, "TableName can't be None"
        pass

    def load(self, database, table_name):
        pass

    def propertyNames(self):
        """ Return an iterator over all the keys of the property
        dictionary, i.e the names of the properties """

        return self._props.keys()
    pass


if __name__ == "__main__":
    a = pydbproperties()
    for b in range(10):
        a.setProperty('key' + str(b), 'value' + str(b))
    print a.getPropertyDict()
    print a.getProperty('key11')

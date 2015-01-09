#!/usr/bin/env python
# coding=utf8

from setuptools import setup

LONG_DESCRIPTION = open('README.md').read()

setup(name="pydbproperties",
      version=0.2,
      description="Store property in database, like pyjavaproperties"
      "(Property JAVA)",
      long_description=LONG_DESCRIPTION,
      author="Jose Roberto Meza Cabrera",
      author_email="robertpro01@gmail.com",
      url="https://github.com/robertpro",
      license="GPL v3",
      packages=["."],
      install_requires=["MysqlSimpleQueryBuilder"])
